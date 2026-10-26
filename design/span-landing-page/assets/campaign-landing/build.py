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
        visual(item, interactive=True)
    if 'visual' in site['hero']:
        visual(site['hero']['visual'])
    if 'diagram' in site['account']:
        diagram = site['account']['diagram']
        require_data(diagram, 'market', ('label', 'hint'), {'regions': 4})
        options = site['form']['segments'] + [site['form']['specific']]
        for region in diagram['regions']:
            require_data(region, 'market region', ('label', 'option', 'description'))
            if region['option'] not in options:
                raise ValueError('Market region option must match a form requirement')
    if 'sheet' in site['dossier']:
        sheet(site['dossier'], site.get('sampleRecords'))
    if 'sampleRecords' in site:
        records = site['sampleRecords']
        if not isinstance(records, list) or len(records) != 6:
            raise ValueError('sampleRecords needs six fictional records')
        if not isinstance(site.get('jobTitles'), list) or not site['jobTitles']:
            raise ValueError('jobTitles needs the allowed titles')
        for record in records:
            require_data(record, 'sample record', ('name', 'email', 'jobTitle', 'company', 'location', 'state', 'segment'))
            for field in ('name', 'email', 'company'):
                if '•••' not in record[field] or re.search(r'[\w.]{4,}•', record[field]):
                    raise ValueError('Sample identifiers need three bullets and at most three leading characters')
            if record['jobTitle'] not in site['jobTitles']:
                raise ValueError('Sample job title must appear in jobTitles')
    if 'orbit' in site:
        items = site['orbit'].get('items')
        if not isinstance(items, list) or not items:
            raise ValueError('orbit.items needs a nonempty list')
        ids = set()
        for item in items:
            require_data(item, 'orbit item', ('id', 'title', 'text', 'icon', 'formValue'))
            if not re.fullmatch(r'[a-z][a-z0-9-]*', item['id']) or item['id'] in ids:
                raise ValueError('orbit item ids must be unique lowercase identifiers')
            ids.add(item['id'])
            if item['icon'] not in ORBIT_ICONS:
                raise ValueError('orbit icon must be server, shield, cloud or sliders')
            if item['formValue'] not in site['form']['segments'] + [site['form']['specific']]:
                raise ValueError('orbit formValue must match a form requirement')
    if 'picker' in site:
        p = site['picker']
        require_data(p, 'picker', ('title', 'hint'))
        if not isinstance(p.get('items'), list) or not p['items']:
            raise ValueError('picker.items needs a nonempty list')
        ids = set()
        for item in p['items']:
            require_data(item, 'picker item', ('id', 'title', 'text', 'size', 'formValue'))
            if not re.fullmatch(r'[a-z][a-z0-9-]*', item['id']) or item['id'] in ids:
                raise ValueError('picker item ids must be unique lowercase identifiers')
            ids.add(item['id'])
            if item['size'] not in ('sm', 'wide', 'lg'):
                raise ValueError('picker item size must be sm, wide or lg')
            if item['formValue'] not in site['form']['segments'] + [site['form']['specific']]:
                raise ValueError('picker formValue must match a form requirement')
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


def diagram_icon(index=0):
    paths = (
        '<circle cx="12" cy="8" r="3"/><path d="M5 21v-3a7 7 0 0 1 14 0v3"/>',
        '<rect x="3" y="5" width="18" height="14" rx="3"/><path d="m3 7 9 6 9-6"/>',
        '<rect x="3" y="7" width="18" height="14" rx="3"/><path d="M8 7V3h8v4M3 12h18M10 12v3h4v-3"/>',
        '<path d="M4 21V5l8-2v18M12 9h8v12M2 21h20M8 8v1m0 4v1m0 4v1m8-6v1m0 4v1"/>',
        '<path d="m12 3 8 3v6c0 5-8 9-8 9s-8-4-8-9V6l8-3Z"/><path d="m8 12 3 3 5-6"/>',
        '<ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v14c0 4 16 4 16 0V5M4 12c0 4 16 4 16 0"/>',
        '<path d="M2 12h5l3-8 4 16 3-8h5"/>',
        '<rect x="3" y="4" width="18" height="16" rx="3"/><path d="M3 9h18M7 15h4"/>',
        '<path d="M6 18a5 5 0 0 1-1-10 7 7 0 0 1 13-1 5.5 5.5 0 0 1 0 11H6Z"/>',
    )
    return '<svg class="diagram__icon" viewBox="0 0 24 24" aria-hidden="true">%s</svg>' % paths[index % len(paths)]


VISUALS = {
    'fanout-widget': '<div class="diagram widget widget--fanout" role="group" aria-label="{label}" data-widget="fanout"><div class="widget__eyebrow">Explore the route</div><div class="fanout__tools">{tools}</div><svg class="widget__wires" viewBox="0 0 600 80" preserveAspectRatio="none" aria-hidden="true">{wires}</svg><div class="widget__hub">{icon}{hub}</div><svg class="widget__wires widget__downstream" viewBox="0 0 600 60" preserveAspectRatio="none" aria-hidden="true"><path d="M300 0C300 30 100 20 100 60M300 0V60M300 0C300 30 500 20 500 60"/></svg><div class="fanout__clients">{clients}</div><p class="widget__hint">Choose a tool to follow its path to MSPs.</p></div>',
    'loop-widget': '<div class="diagram widget widget--loop" role="group" aria-label="{label}" data-widget="loop"><div class="widget__eyebrow">Partner possibilities</div><div class="orbit"><div class="orbit__track" aria-hidden="true"></div><div class="orbit__arc" aria-hidden="true"></div><b class="orbit__center">{center}</b>{steps}</div><p class="widget__hint">Explore a route. Each is a possibility, not a promise.</p></div>',
    'narrow-widget': '<div class="diagram widget widget--narrow" role="group" aria-label="{label}" data-widget="narrow"><div class="widget__eyebrow">Build a focused audience</div><div class="funnel">{stages}</div><p class="widget__hint">Explore each band. Widths do not represent volume.</p></div>',
    'anatomy-widget': '<div class="diagram widget widget--anatomy" role="group" aria-label="{label}" data-widget="anatomy"><div class="widget__eyebrow">Inside the sample</div><div class="record"><div class="record__chrome">{icon}<b>{title}</b><span aria-hidden="true">•••</span></div>{fields}<div class="record__tags">{pills}<span>{custom}</span></div></div><p class="widget__hint">{note}</p></div>',
    'path-widget': '<div class="diagram widget widget--path" role="group" aria-label="{label}" data-widget="path" data-step="0"><div class="widget__eyebrow">Preview the request journey</div><div class="steps"><div class="steps__track" aria-hidden="true"><i></i></div>{steps}</div><div class="steps__footer"><span class="widget__hint" aria-live="polite">Choose a step to begin. This preview sends nothing.</span><button type="button" class="widget__reset" hidden>Reset</button></div></div>',
    'fanout': '<div class="diagram fanout" role="img" aria-label="{label}"><div class="fanout__tools">{tools}</div><svg class="diagram__links fanout__links" viewBox="0 0 600 70" preserveAspectRatio="none" aria-hidden="true"><path d="M75 3C75 40 300 20 300 67M225 3C225 35 300 35 300 67M375 3C375 35 300 35 300 67M525 3C525 40 300 20 300 67"/><path class="diagram__dots" d="M75 3h0M225 3h0M375 3h0M525 3h0M300 67h0"/></svg><div class="fanout__trunk"><b class="diagram__node diagram__node--emphasis">{icon}{hub}</b></div><svg class="diagram__links" viewBox="0 0 600 70" preserveAspectRatio="none" aria-hidden="true"><path d="M300 3C300 40 100 30 100 67M300 3C300 30 300 40 300 67M300 3C300 40 500 30 500 67"/><path class="diagram__dots" d="M300 3h0M100 67h0M300 67h0M500 67h0"/></svg><div class="fanout__clients">{clients}</div></div>',
    'loop': '<div class="diagram cycle" role="img" aria-label="{label}"><svg class="diagram__links cycle__links" viewBox="0 0 360 330" aria-hidden="true"><path d="M224 56C290 72 325 128 306 206m-7-13 7 13 12-8M270 270C220 313 140 313 90 270m14 0-14 0 2 14M54 206C35 128 70 72 136 56m-10-7 10 7-6 12"/><path class="diagram__dots" d="M224 56h0M270 270h0M54 206h0"/></svg><b class="cycle__center">{center}</b>{steps}</div>',
    'narrow': '<div class="diagram narrow" role="img" aria-label="{label}">{stages}</div>',
    'anatomy': '<div class="diagram anatomy" role="img" aria-label="{label}"><div class="anatomy__drawing"><b class="anatomy__title">{title}</b>{fields}</div><div class="anatomy__pills">{pills}<span class="anatomy__custom">{custom}</span></div><small>{note}</small></div>',
    'path': '<div class="diagram journey" role="img" aria-label="{label}">{steps}</div>',
    'calls': '<div class="calls"><div class="call"><em>{a}</em>{at}</div><div class="call call--on"><em>{b}</em>{bt}</div></div>',
    'sources': '<div class="trail"><ul>{chips}</ul><svg viewBox="0 0 110 230" aria-hidden="true">{paths}</svg>'
               '<div class="rec"><b>{rec}</b><i></i><i></i><i></i><div class="law">{law}</div></div></div>',
    'renewal': '<div class="ren"><div class="ren__bar">{bar}</div><div class="ren__lab">{lab}</div>'
               '<div class="ren__keys"><span><i></i>{k1}</span><span><i class="win"></i>{k2}</span><span><i class="end"></i>{k3}</span></div>'
               '<span class="ren__pin">{pin}</span></div>',
    'sample': '<div class="samp"><div class="samp__card"><b>{card}</b><i></i><i></i><i></i><i></i><span class="stamp">{stamp}</span></div><ul>{ticks}</ul></div>',
    'roles': '<div class="roles"><div class="roles__r">{roles}</div><div class="roles__at">{at}</div><div class="roles__c">{cos}</div></div>',
}


def require_data(data, kind, strings=(), lists=None):
    if not isinstance(data, dict):
        raise ValueError(kind + ' needs an object')
    for key in strings:
        if not isinstance(data.get(key), str) or not data[key].strip():
            raise ValueError(kind + '.' + key + ' needs nonempty text')
    for key, count in (lists or {}).items():
        values = data.get(key)
        if not isinstance(values, list) or len(values) != count:
            raise ValueError('%s.%s needs exactly %d entries' % (kind, key, count))
        if key != 'regions' and any(not isinstance(x, str) or not x.strip() for x in values):
            raise ValueError(kind + '.' + key + ' needs nonempty text entries')


def visual(item, interactive=False):
    kind, d = item['visual'], item.get('visualData', {})
    if kind in ('fanout', 'loop', 'narrow', 'anatomy', 'path'):
        strings, lists = {
            'fanout': (('label', 'hub'), {'tools': 4, 'clients': 3}),
            'loop': (('label', 'center'), {'steps': 3}),
            'narrow': (('label',), {'stages': 4}),
            'anatomy': (('label', 'title', 'custom', 'note'), {'fields': 4, 'pills': 3}),
            'path': (('label',), {'steps': 3}),
        }[kind]
        require_data(d, kind, strings, lists)
        if interactive:
            return widget(kind, d)
        values = {key: E(d[key]) for key in strings}
        values['icon'] = diagram_icon(3)
        for key in lists:
            values[key] = ''.join('<span class="diagram__node">%s%s</span>' % (diagram_icon(i + 4 if key == 'tools' else 3 if key == 'clients' else i), E(x)) for i, x in enumerate(d[key]))
        if kind == 'fanout':
            values['tools'] = ('<svg class="diagram__links fanout__mobile-links" viewBox="0 0 300 230" preserveAspectRatio="none" aria-hidden="true">'
                               '<path d="M132 37C150 37 150 60 150 80V227M168 37C150 37 150 60 150 80M132 126C150 126 150 150 150 170M168 126C150 126 150 150 150 170"/>'
                               '<path class="diagram__dots" d="M132 37h0M168 37h0M132 126h0M168 126h0M150 227h0"/></svg>') + values['tools']
        if kind == 'anatomy':
            values['fields'] = ''.join('<div class="anatomy__row"><span>%s%s</span><svg class="diagram__links anatomy__leader" viewBox="0 0 80 30" preserveAspectRatio="none" aria-hidden="true"><path d="M3 20C30 20 35 15 77 15"/><path class="diagram__dots" d="M3 20h0M77 15h0"/></svg><b aria-hidden="true"></b></div>' % (diagram_icon(i), E(x)) for i, x in enumerate(d['fields']))
        if kind == 'path':
            values['steps'] = '<svg class="diagram__links journey__link" viewBox="0 0 60 60" aria-hidden="true"><path d="M3 20C25 20 30 40 53 40m-7-7 7 7-7 7"/><path class="diagram__dots" d="M3 20h0M53 40h0"/></svg>'.join('<span class="diagram__node">%s%s</span>' % (diagram_icon(i), E(x)) for i, x in enumerate(d['steps']))
        return VISUALS[kind].format(**values)
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


def widget(kind, d):
    values = {k: E(v) for k, v in d.items() if isinstance(v, str)}
    values['icon'] = diagram_icon(3)
    def node(text, i, extra=''):
        return ('<button type="button" class="widget__node" data-node="%d" aria-pressed="false" style="--i:%d" %s>%s<span>%s</span></button>'
                % (i, i, extra, diagram_icon(i + 4 if kind == 'fanout' else i), E(text)))
    if kind == 'fanout':
        values['tools'] = ''.join(node(x, i) for i, x in enumerate(d['tools']))
        values['wires'] = ''.join('<path data-wire="%d" d="M%d 0C%d 45 300 25 300 80"/>' % (i, 75 + i * 150, 75 + i * 150) for i in range(4))
        values['clients'] = ''.join('<span class="diagram__node">%s%s</span>' % (diagram_icon(3), E(x)) for x in d['clients'])
    elif kind == 'loop':
        values['steps'] = ''.join(node(x, i) for i, x in enumerate(d['steps']))
    elif kind == 'narrow':
        require_data(d, 'narrow', lists={'captions': 4})
        values['stages'] = ''.join('<button type="button" class="funnel__band" data-node="%d" aria-expanded="false" style="--i:%d"><b>%s</b><span>%s</span></button>' % (i, i, E(x), E(d['captions'][i])) for i, x in enumerate(d['stages']))
    elif kind == 'anatomy':
        values['fields'] = ''.join('<div class="record__row"><button type="button" data-node="%d" aria-pressed="false">%s%s</button><svg class="record__leader" viewBox="0 0 80 24" aria-hidden="true"><path d="M0 18C35 18 40 6 80 6"/></svg><i aria-hidden="true"></i></div>' % (i, diagram_icon(i), E(x)) for i, x in enumerate(d['fields']))
        values['pills'] = ''.join('<span>%s</span>' % E(x) for x in d['pills'])
    elif kind == 'path':
        values['steps'] = ''.join(node(x, i) for i, x in enumerate(d['steps']))
    return VISUALS[kind + '-widget'].format(**values)


ORBIT_ICONS = {
    'server': '<rect x="3" y="3" width="18" height="7" rx="2"/><rect x="3" y="14" width="18" height="7" rx="2"/><path d="M7 6.5h.01M7 17.5h.01M11 6.5h6M11 17.5h6"/>',
    'shield': '<path d="m12 3 8 3v6c0 5-8 9-8 9s-8-4-8-9V6l8-3Z"/><path d="m8 12 3 3 5-6"/>',
    'cloud': '<path d="M6 18a5 5 0 0 1-1-10 7 7 0 0 1 13-1 5.5 5.5 0 0 1 0 11H6Z"/>',
    'sliders': '<path d="M4 7h5m4 0h7M4 17h9m4 0h3"/><circle cx="11" cy="7" r="2"/><circle cx="15" cy="17" r="2"/>',
}


def orbit_markup(items):
    rings = ''.join('<div class="ot-orbit ot-hidden"><i class="ot-ln"></i><i class="ot-ac"></i></div>' for _ in items)
    labels = ''.join('<button type="button" class="ot-year ot-hidden" data-index="%d">%s</button>' % (i, E(item['title'])) for i, item in enumerate(items))
    nodes = ''.join('<button type="button" class="ot-node ot-hidden" data-index="%d" aria-label="%s" aria-pressed="false" aria-controls="orbitCard"><svg viewBox="0 0 24 24" aria-hidden="true">%s</svg></button>' % (i, E(item['title']), ORBIT_ICONS[item['icon']]) for i, item in enumerate(items))
    return rings + labels + '<i class="ot-emit"></i><i class="ot-emit ot-emit-2"></i><i class="ot-emit ot-emit-3"></i><div class="ot-core" aria-hidden="true"><div class="ot-core-fill"><div class="ot-blob ot-b1"></div><div class="ot-blob ot-b2"></div><div class="ot-blob ot-b3"></div><div class="ot-blob ot-b4"></div></div><div class="ot-core-gloss"></div><div class="ot-core-shine"></div></div>' + nodes


def sample_hero(records):
    panels = []
    for index, record in enumerate(records[:4]):
        rows = ''.join('<div class="sample-record__row"><span>%s%s</span><b class="%s">%s</b></div>' % (diagram_icon(i), label, 'masked' if key in ('name', 'email', 'company') else '', E(record[key])) for i, (key, label) in enumerate((('name', 'Name'), ('email', 'Business email'), ('jobTitle', 'Job title'), ('company', 'Company'), ('location', 'Location'))))
        panels.append('<div class="sample-record__panel%s" aria-hidden="%s">%s</div>' % (' is-current' if index == 0 else '', 'false' if index == 0 else 'true', rows))
    return ('<div class="hero__object hero__object--sample"><div class="sample-record" role="group" aria-label="Fictional masked sample record"><div class="sample-record__heading"><b>Sample record, masked</b><button type="button" class="sample-record__pause" aria-label="Pause sample rotation" aria-pressed="false">Pause</button></div><div class="sample-record__panels">%s</div><div class="sample-record__footer"><span>Illustrative, not real data</span><span>Available fields and coverage vary by segment</span></div></div><div class="sample-record__pills"><span>MSP</span><span>MSSP</span><span>Cloud MSP</span><span>Custom</span></div></div>') % ''.join(panels)


def sheet(d, records=None):
    s = d.get('sheet', {})
    require_data(s, 'sheet', ('label', 'hint'), {'fields': 4, 'chips': 2})
    heads = ''.join('<th scope="col" data-column="%d" aria-sort="none"><button type="button" class="sheet__label" data-column="%d" aria-label="Sort illustrative %s column">%s<svg class="sheet__sort" viewBox="0 0 16 16" aria-hidden="true"><path d="m4 6 4-4 4 4M4 10l4 4 4-4"/></svg></button></th>' % (i, i, E(x), E(x)) for i, x in enumerate(s['fields']))
    rows = ''.join('<tr data-row="%d">%s</tr>' % (r, ''.join('<td data-column="%d">%s<i aria-hidden="true" style="width:%d%%"></i><span class="sr">Illustrative placeholder</span></td>' % (i, '<b class="sheet__monogram" aria-hidden="true">XX</b>' if i == 0 else '', 40 + (r * 17 + i * 13) % 54) for i in range(4))) for r in range(6))
    if records:
        for i, label in enumerate(('Segment', 'State'), 4):
            heads += '<th scope="col" data-column="%d" aria-sort="none"><button type="button" class="sheet__label" data-column="%d">%s<svg class="sheet__sort" viewBox="0 0 16 16" aria-hidden="true"><path d="m4 6 4-4 4 4M4 10l4 4 4-4"/></svg></button></th>' % (i, i, label)
        rows = ''
        for r, record in enumerate(records):
            cells = ''
            for i, key in enumerate(('name', 'email', 'jobTitle', 'company', 'segment', 'state')):
                monogram = '<b class="sheet__monogram" aria-hidden="true">%s</b>' % E(record['name'][0]) if i == 0 else ''
                cls = 'masked' if key in ('name', 'email', 'company') else 'sheet__segment' if key == 'segment' else 'sheet__title' if key == 'jobTitle' else ''
                cells += '<td data-column="%d">%s<span class="%s">%s</span></td>' % (i, monogram, cls, E(record[key]))
            rows += '<tr data-row="%d">%s</tr>' % (r, cells)
    chips = ''.join('<span>%s</span>' % E(x) for x in s['chips'])
    return ('<div class="sheet sheet--playable%s" id="dossier" role="group" aria-label="Interactive illustrative sample sheet"><div class="sheet__chrome"><span aria-hidden="true">•••</span><b>%s</b></div>'
            '<div class="sheet__toolbar"><span class="sheet__tab">Sample</span><span class="sheet__search">%s<span>Search sample layout</span></span><span class="sheet__filter">Layout preview</span></div>'
            '<div class="sheet__body"><p class="sheet__hint">%s</p>'
            '<div class="sheet__scroll" role="region" aria-label="Sample records, scroll horizontally for all fields" tabindex="0"><table aria-label="%s"><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>'
            '<div class="sheet__chips">%s</div><p class="sheet__stamp">%s</p></div>%s</div>') % (
                ' sheet--records' if records else '', E(d['title']), '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="10" cy="10" r="6"/><path d="m15 15 5 5"/></svg>', E(s['hint']), E(s['label']), heads, rows, chips, E(d['tag']), '<div class="sheet__unlock"><span>Full sample unlocks on request</span><a href="#form">Request a sample <span aria-hidden="true">→</span></a></div>' if records else '')


def market(d):
    regions = d['regions']
    buttons = ''
    for i, r in enumerate(regions):
        content = diagram_icon((3, 4, 8, 0)[i]) + E(r['label']) + '<span aria-hidden="true">↗</span>'
        if i == 3:
            content = ('<svg class="market__arc" viewBox="0 0 360 110" aria-hidden="true">'
                       '<path class="market__cut" d="M8 18C70 110 290 110 352 18"/>'
                       '<path id="custom-arc" d="M22 14C80 96 280 96 338 14" fill="none" stroke="none"/>'
                       '<text><textPath href="#custom-arc" startOffset="50%%" text-anchor="middle">%s</textPath></text></svg>') % E(r['label'])
        buttons += ('<button type="button" class="market__region market__region--%d" data-requirement="%s" '
                    'aria-describedby="market-legend-%d" aria-label="%s">%s</button>') % (i, E(r['option']), i, E(r['label']), content)
    legend = ''.join('<div id="market-legend-%d"><dt><i aria-hidden="true">%02d</i>%s</dt><dd>%s</dd></div>' % (i, i + 1, E(r['label']), E(r['description'])) for i, r in enumerate(regions))
    return '<div class="market__layout"><div class="market__map" role="group" aria-label="%s">%s</div><dl class="market__legend">%s</dl></div><p class="market__hint">%s</p>' % (E(d['label']), buttons, legend, E(d['hint']))


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
            n, n, visual(item, interactive=True), E(item['q']), E(item['lead']), E(item['detail']))
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
        'hero.object': sample_hero(site['sampleRecords']) if 'sampleRecords' in site else ('<div class="hero__object">%s</div>' % visual(site['hero']['visual'])) if 'visual' in site['hero'] else '<ul class="ticks">' + ''.join('<li>%s%s</li>\n' % (tick, E(t)) for t in site['hero']['ticks']) + '</ul>',
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
    diagram = 'diagram' in site['account']
    orbit = site.get('orbit')
    if orbit:
        v.update({'orbit.markup': orbit_markup(orbit['items']), 'orbit.json': script_json(orbit['items'])})
    picker = site.get('picker')
    if picker:
        v.update({'picker.title': E(picker['title']), 'picker.hint': E(picker['hint'])})
    if 'compare' in site or picker:
        board_tiles = tiles(site) if 'compare' in site else []
        board_tiles += [dict(item, side='picker', icon=diagram_icon((3, 4, 8, 0)[i % 4])) for i, item in enumerate(picker['items'])] if picker else []
        v['bento.tilesJson'] = script_json(board_tiles)
    if 'sheet' in d:
        v['dossier.sheet'] = sheet(d, site.get('sampleRecords'))
    if diagram:
        v['dossier.sheet'] = sheet(d)
        v['account.diagram'] = market(site['account']['diagram'])
    template = (ROOT / 'template.html').read_text(encoding='utf-8')
    sections = {key: key in site for key in ('band', 'clients', 'compare')}
    sections.update(market=diagram and not picker and not orbit, orbit=bool(orbit), sheet='sheet' in d, picker=bool(picker), bento='compare' in site or bool(picker), legacy='sheet' not in d)
    for key, enabled in sections.items():
        template = re.sub(r'\{\{#%s\}\}(.*?)\{\{/%s\}\}' % (key, key), (lambda m: m.group(1)) if enabled else '', template, flags=re.S)
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
