#!/usr/bin/env python3
"""Build a SPAN campaign landing page from site.json. Standard library only, one inline HTML file.

Usage: python3 build.py examples/span-peo-eor --out /abs/path/artifact.html
"""
import argparse
import base64
import html
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent
E = html.escape
DASH = re.compile('[\u2013\u2014]')
GLOBE = ('<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/>'
         '<path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/></svg>')


def script_json(value):
    """JSON in an inline script must not be able to close its script element."""
    return (json.dumps(value).replace('&', '\\u0026').replace('<', '\\u003c')
            .replace('>', '\\u003e').replace('\u2028', '\\u2028').replace('\u2029', '\\u2029'))


def safe_url(value, allow_tel=False):
    if not isinstance(value, str) or re.search(r'[\s<>"\x00-\x1f]', value):
        raise ValueError('URL contains whitespace, control characters or markup: %r' % value)
    if allow_tel and value.startswith('tel:'):
        return value
    p = urlsplit(value)
    if p.scheme != 'https' or not p.hostname or p.username or p.password:
        raise ValueError('Only absolute HTTPS URLs without credentials: %r' % value)
    return value


def walk_strings(obj, path='site'):
    """Every string in the contract: no dashes, nothing empty."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            walk_strings(v, path + '.' + k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            walk_strings(v, '%s[%d]' % (path, i))
    elif isinstance(obj, str):
        if DASH.search(obj):
            raise ValueError('Forbidden dash in ' + path)
        if not obj.strip() and not path.endswith('.href'):
            raise ValueError('Empty text in ' + path)


def validate(site, source):
    walk_strings(site)
    for key in ['brand', 'meta', 'headlines', 'hero', 'form', 'account', 'dossier', 'faq', 'closer', 'footer', 'tracking']:
        if key not in site:
            raise ValueError('Missing section ' + key)
    # band, clients and compare are optional: a {{#key}}...{{/key}} block in the template drops out when the key is absent
    if not isinstance(site['form'].get('phoneRequired', True), bool):
        raise ValueError('form.phoneRequired must be a boolean')
    safe_url(site['brand']['domain'])
    safe_url(site['brand']['privacyUrl'])
    safe_url(site['meta']['canonical'])
    logo = (source / site['brand']['logo']).resolve()
    if not logo.is_relative_to(source.resolve()) or not logo.is_file() or \
            not logo.read_bytes().startswith(b'\x89PNG\r\n\x1a\n'):
        raise ValueError('Logo must be a PNG inside the source directory')
    for side in ('left', 'right') if 'compare' in site else ():
        s = site['compare'][side]
        if not s['items'] or any(int(i['count']) <= 0 for i in s['items']):
            raise ValueError('compare.%s needs positive counts' % side)
        if sum(int(i['count']) for i in s['items']) > int(s['total']):
            raise ValueError('compare.%s items exceed the stated total' % side)
    if 'band' in site and len(site['band']) != 4:
        raise ValueError('band needs exactly four counters')
    for src in site['hero'].get('sources', []) + site['account'].get('sources', []):
        safe_url(src['url'])
    for col in site['footer']['columns']:
        for item in col['items']:
            if item.get('href'):
                safe_url(item['href'], allow_tel=True)
    if len(site['faq']['items']) != 5:
        raise ValueError('faq.items needs exactly five entries (the sixth tile is the ask)')
    for item in site['faq']['items']:
        if item.get('visual') not in VISUALS:
            raise ValueError('faq item needs a visual in ' + ', '.join(sorted(VISUALS)))
    for key in ('idle', 'idleName', 'hint', 'share', 'rank', 'all', 'vs', 'of', 'rest', 'preview', 'pinned', 'contacts', 'cta') if 'compare' in site else ():
        if key not in site['compare']['strip']:
            raise ValueError('compare.strip.' + key + ' missing')


def fav(domain):
    return ('<span class="fav">%s<img src="https://www.google.com/s2/favicons?domain=%s&amp;sz=64" '
            'width="22" height="22" alt="" loading="lazy" onerror="this.remove()"></span>') % (GLOBE, E(domain))


def sources(id_, items, label):
    if not items:
        return ''
    stack = ''.join(fav(i['domain']) for i in items)
    rows = ''.join(
        '<li><a href="%s" target="_blank" rel="noopener">%s<span><b>%s</b><small>%s</small></span></a></li>'
        % (E(i['url']), fav(i['domain']), E(i['title']), E(i['snippet'])) for i in items)
    return ('<div class="srcs" id="%s"><button type="button" class="srcs__btn" aria-expanded="false" aria-controls="%s-list">'
            '<span class="srcs__stack">%s</span><span>%s</span>'
            '<svg class="srcs__chev" viewBox="0 0 24 24" aria-hidden="true"><path d="M9 6l6 6-6 6"/></svg></button>'
            '<div class="srcs__list" id="%s-list"><ul>%s</ul></div></div>') % (id_, id_, stack, E(label), id_, rows)


def tiles(site):
    """One entry per provider across both books, with share and rank precomputed for the strip."""
    grand = sum(int(site['compare'][k]['total']) for k in ('left', 'right'))
    bento = site['compare'].get('bento', {})
    lg_at, wide_at = int(bento.get('lgAt', 20)), int(bento.get('wideAt', 10))
    out = []
    for key, side_id in (('left', 'peo'), ('right', 'eor')):
        side = site['compare'][key]
        total = int(side['total'])
        items = sorted(((i['name'], int(i['count']), False) for i in side['items']), key=lambda t: -t[1])
        other = total - sum(c for _, c, _ in items)
        if other > 0:
            items.append((side['otherLabel'], other, True))
        for rank, (name, count, is_all) in enumerate(items, 1):
            share = count / total * 100
            size = 'wide' if is_all else 'lg' if share >= lg_at else 'wide' if share >= wide_at else 'sm'
            out.append({'name': name, 'count': count, 'all': is_all, 'side': side_id, 'sideName': side['name'],
                        'sideShort': side.get('short', side['name']), 'seg': side['segment'], 'rank': rank,
                        'n': len([i for i in items if not i[2]]), 'share': round(share),
                        'shareAll': round(count / grand * 100), 'size': size})
    return out


VISUALS = {
    'calls': '<div class="calls"><div class="call"><em>{a}</em>{at}</div><div class="call call--on"><em>{b}</em>{bt}</div></div>',
    'sources': '<div class="trail"><ul>{chips}</ul><svg viewBox="0 0 110 230" aria-hidden="true">{paths}</svg>'
               '<div class="rec"><b>{rec}</b><i></i><i></i><i></i><div class="law">{law}</div></div></div>',
    'renewal': '<div class="ren"><div class="ren__bar">{bar}</div><div class="ren__lab">{lab}</div>'
               '<div class="ren__keys"><span><i></i>{k1}</span><span><i class="win"></i>{k2}</span><span><i class="end"></i>{k3}</span></div>'
               '<span class="ren__pin">{pin}</span></div>',
    'sample': '<div class="samp"><div class="samp__card"><b>{card}</b><i></i><i></i><i></i><i></i><span class="stamp">{stamp}</span></div><ul>{ticks}</ul></div>',
    'roles': '<div class="roles"><div class="roles__r">{roles}</div><div class="roles__at">{at}</div><div class="roles__c">{cos}</div></div>',
}


def visual(item):
    kind, d = item['visual'], item.get('visualData', {})
    if kind == 'calls':
        return VISUALS[kind].format(a=E(d['beforeLabel']), at=E(d['before']), b=E(d['afterLabel']),
                                    bt=re.sub(r'\*(.+?)\*', r'<mark>\1</mark>', E(d['after'])))
    if kind == 'sources':
        n = len(d['sources'])
        paths = ''.join('<path d="M0 %d C 55 %d, 55 115, 110 115"/>' % (y, y) for y in
                        (round(18 + k * (194 / max(n - 1, 1))) for k in range(n)))
        return VISUALS[kind].format(chips=''.join('<li>%s</li>' % E(x) for x in d['sources']), paths=paths,
                                    rec=E(d['record']), law=''.join('<span>%s</span>' % E(x) for x in d['laws']))
    if kind == 'renewal':
        bar = ''.join('<i class="%s"></i>' % ('end' if m == 12 else 'win' if m in d['window'] else '') for m in range(1, 13))
        lab = ''.join('<span>%d</span>' % m for m in range(1, 13))
        return VISUALS[kind].format(bar=bar, lab=lab, k1=E(d['keys'][0]), k2=E(d['keys'][1]), k3=E(d['keys'][2]), pin=E(d['pin']))
    if kind == 'sample':
        return VISUALS[kind].format(card=E(d['card']), stamp=E(d['stamp']), ticks=''.join('<li>%s</li>' % E(x) for x in d['ticks']))
    if kind == 'roles':
        return VISUALS[kind].format(roles=''.join('<span>%s</span>' % E(x) for x in d['roles']), at=E(d['at']),
                                    cos=''.join('<span>%s</span>' % E(x) for x in d['companies']))
    raise ValueError('Unknown faq visual ' + repr(kind))


def render(site, source):
    tick = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12.5l5 5L20 6.5"/></svg>'
    logo = 'data:image/png;base64,' + base64.b64encode((source / site['brand']['logo']).read_bytes()).decode()
    headlines = dict(site['headlines'].get('variants', {}))
    d = site['dossier']
    cols = ''
    for col in d['columns']:
        rows = ''.join('            <div class="srow"><span>%s</span><b>%s</b>%s</div>\n' % (
            E(r['label']), E(r['value']),
            '<span class="ok">%s</span>' % E(d['verifiedLabel']) if r.get('verified') else '') for r in col['rows'])
        cols += '          <div class="dcol">\n            <h3>%s</h3>\n%s          </div>\n' % (E(col['title']), rows)
    tabs = panes = ''
    for n, item in enumerate(site['faq']['items'], 1):
        tabs += ('          <button type="button" role="tab" id="tab%d" aria-controls="pane%d" aria-selected="false">'
                 '<i>%02d</i><span>%s</span></button>\n') % (n, n, n, E(item['q']))
        panes += ('          <div class="pane2" id="pane%d" role="tabpanel" aria-labelledby="tab%d" hidden>\n'
                  '            <div class="vis">%s</div>\n            <div class="ans"><h3>%s</h3>\n'
                  '            <p class="faq__lead">%s</p>\n            <p>%s</p></div>\n          </div>\n') % (
            n, n, visual(item), E(item['q']), E(item['lead']), E(item['detail']))
    fcols = ''
    for col in site['footer']['columns']:
        lis = ''.join('<li>%s</li>' % (
            '<a href="%s">%s</a>' % (E(i['href']), E(i['label'])) if i.get('href') else E(i['label'])) for i in col['items'])
        fcols += '    <nav class="hwf__col" aria-label="%s">\n      <h3>%s</h3>\n      <ul>%s</ul>\n    </nav>\n' % (
            E(col['title']), E(col['title']), lis)
    v = {
        'logo': logo,
        'brand.name': E(site['brand']['name']), 'brand.domain': E(site['brand']['domain']),
        'brand.phone': E(site['brand']['phone']), 'brand.phoneHref': E(site['brand']['phoneHref']),
        'brand.privacyUrl': E(site['brand']['privacyUrl']),
        'meta.title': E(site['meta']['title']), 'meta.description': E(site['meta']['description']),
        'meta.canonical': E(site['meta']['canonical']),
        'headlines.default': E(site['headlines']['default']), 'headlines.json': script_json(headlines),
        'hero.eyebrow': E(site['hero']['eyebrow']), 'hero.lede': E(site['hero']['lede']),
        'hero.ledeEmphasis': E(site['hero']['ledeEmphasis']),
        'hero.ticks': ''.join('        <li>%s%s</li>\n' % (tick, E(t)) for t in site['hero']['ticks']),
        'hero.callout.lead': E(site['hero']['callout']['lead']), 'hero.callout.text': E(site['hero']['callout']['text']),
        'hero.callout.link': E(site['hero']['callout']['link']),
        'hero.sources': sources('sources', site['hero'].get('sources', []), site['hero'].get('sourcesLabel', '')),
        'form.title': E(site['form']['title']), 'form.sub': E(site['form']['sub']),
        'form.subChosenJson': script_json(site['form']['subChosen']),
        'form.segments': ''.join('                <option>%s</option>\n' % E(x) for x in site['form']['segments'])
                         + '                <option>%s</option>\n' % E(site['form']['specific']),
        'form.specificJson': script_json(site['form']['specific']),
        'form.providerPlaceholder': E(site['form']['providerPlaceholder']),
        'form.segmentLabel': E(site['form'].get('segmentLabel', 'Which install base')),
        'form.providerLabel': E(site['form'].get('providerLabel', 'Which provider')),
        'form.providerError': E(site['form'].get('providerError', 'Please name the provider')),
        'form.phoneRequiredJson': script_json(site['form'].get('phoneRequired', True)),
        'form.consent': E(site['form']['consent']), 'form.submit': E(site['form']['submit']),
        'form.sticky': E(site['form']['sticky']), 'form.foot': E(site['form']['foot']),
        'form.thanksTitle': E(site['form']['thanksTitle']), 'form.thanksText': E(site['form']['thanksText']),
        'account.title': E(site['account']['title']), 'account.lede': E(site['account']['lede']),
        'account.groups': ''.join('          <li>%s</li>\n' % E(g) for g in site['account']['groups']),
        'account.fit': E(site['account']['fit']),
        'account.sources': sources('sources2', site['account'].get('sources', []), site['account'].get('sourcesLabel', '')),
        'dossier.title': E(d['title']), 'dossier.tag': E(d['tag']), 'dossier.providerLabel': E(d['providerLabel']),
        'dossier.provider': E(d['provider']), 'dossier.columns': cols, 'dossier.footer': E(d['footer']),
        'faq.title': E(site['faq']['title']), 'faq.sub': E(site['faq']['sub']), 'faq.tabs': tabs, 'faq.panes': panes,
        'faq.ask.title': E(site['faq']['ask']['title']), 'faq.ask.text': E(site['faq']['ask']['text']),
        'faq.ask.button': E(site['faq']['ask']['button']),
        'closer.title': E(site['closer']['title']), 'closer.text': E(site['closer']['text']),
        'closer.button': E(site['closer']['button']), 'closer.small': E(site['closer']['small']),
        'footer.wordmark': E(site['footer']['wordmark']), 'footer.wordmarkJson': script_json(site['footer']['wordmark']),
        'footer.meta': E(site['footer']['meta']), 'footer.columns': fcols,
        'tracking.offerJson': script_json(site['tracking']['offer']), 'tracking.campaignJson': script_json(site['tracking']['campaign']),
        'tracking.formJson': script_json(site['tracking']['form']), 'tracking.conversionJson': script_json(site['tracking']['conversionLabel']),
    }
    if 'band' in site:
        v['band'] = ''.join('    <div class="band__n"><b>%s</b><span>%s</span></div>\n' % (E(b['value']), E(b['label'])) for b in site['band'])
    if 'clients' in site:
        v['clients.label'] = E(site['clients']['label'])
        v['clients.names'] = '    ' + ''.join('<span>%s</span>' % E(n) for n in site['clients']['names']) + '\n'
    if 'compare' in site:
        c = site['compare']
        v.update({'compare.title': E(c['title']), 'compare.sub': E(c['sub']), 'compare.note': E(c['note']),
                  'compare.tilesJson': script_json(tiles(site)), 'compare.stripJson': script_json(c['strip']),
                  'compare.bentoJson': script_json(c['bento'])})
        v.update({'compare.bento.' + k: E(str(x)) for k, x in c['bento'].items()})
        v.update({'compare.strip.' + k: E(x) for k, x in c['strip'].items()})
        for side in ('left', 'right'):
            v['compare.%s.name' % side] = E(c[side]['name'])
            v['compare.%s.total' % side] = str(int(c[side]['total']))
            v['compare.%s.totalText' % side] = format(int(c[side]['total']), ',')
    template = (ROOT / 'template.html').read_text(encoding='utf-8')
    for key in ('band', 'clients', 'compare'):
        template = re.sub(r'\{\{#%s\}\}(.*?)\{\{/%s\}\}' % (key, key), (lambda m: m.group(1)) if key in site else '', template, flags=re.S)
    out = re.sub(r'\{\{([a-zA-Z.]+)\}\}', lambda m: v[m.group(1)], template)
    if DASH.search(out):
        raise ValueError('Dash in built output')
    return out


def build(source, out):
    source = Path(source)
    site = json.loads((source / 'site.json').read_text(encoding='utf-8'))
    validate(site, source)
    text = render(site, source)
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding='utf-8')
    return text


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('source', type=Path, help='Directory holding site.json and the PNG logo')
    p.add_argument('--out', type=Path, required=True, help='Path of the HTML file to write')
    a = p.parse_args()
    build(a.source, a.out)
    print('built', a.out)
