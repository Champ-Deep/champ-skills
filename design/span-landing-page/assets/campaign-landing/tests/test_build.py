import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('campaign_build', ROOT / 'build.py')
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
SOURCE = ROOT / 'examples/span-peo-eor'


class BuildTests(unittest.TestCase):
    def setUp(self):
        self.site = json.loads((SOURCE / 'site.json').read_text())

    def build(self, site=None):
        with tempfile.TemporaryDirectory() as td:
            src = Path(td) / 'src'
            src.mkdir()
            (src / 'logo.png').write_bytes((SOURCE / 'logo.png').read_bytes())
            (src / 'site.json').write_text(json.dumps(site or self.site))
            return module.build(src, Path(td) / 'out.html')

    def test_example_builds_with_counts_and_no_placeholders(self):
        text = self.build()
        self.assertNotIn('{{', text)
        self.assertNotIn('\u2014', text)
        self.assertNotIn('\u2013', text)
        for side in ('left', 'right'):
            s = self.site['compare'][side]
            self.assertIn(format(s['total'], ','), text)
            other = s['total'] - sum(i['count'] for i in s['items'])
            self.assertIn('"name": "%s", "count": %d, "all": true' % (s['otherLabel'], other), text)
        tiles = module.tiles(self.site)
        self.assertEqual(len(tiles), 16)
        self.assertEqual(sum(t['count'] for t in tiles if t['side'] == 'peo'), self.site['compare']['left']['total'])
        self.assertEqual([t['rank'] for t in tiles if t['side'] == 'eor'], list(range(1, 9)))
        self.assertEqual(text.count('class="board" data-side='), 2)
        self.assertIn('"rank": "#{rank} of {n}"', text)
        self.assertEqual(text.count('role="tab"'), 5)
        self.assertEqual(text.count('class="pane2"'), 5)
        self.assertIn('data:image/png;base64,', text)
        self.assertIn('"deel": "Who Is On Deel? We Can Tell You."', text)

    def test_tile_shares(self):
        by = {t['name']: t for t in module.tiles(self.site)}
        self.assertEqual(by['Insperity']['share'], 26)
        self.assertEqual(by['Deel']['share'], 50)
        self.assertEqual(by['Insperity']['size'], 'lg')
        self.assertEqual(by['Deel']['size'], 'lg')
        self.assertEqual(by['TriNet']['size'], 'wide')
        self.assertEqual(by['CoAdvantage']['size'], 'sm')
        self.assertEqual(by['All other PEOs']['size'], 'wide')
        self.assertEqual(by['Oyster HR']['sideShort'], 'EOR')
        self.assertEqual(by['All other PEOs']['count'], 25846)
        self.assertTrue(by['All other PEOs']['all'])

    def test_optional_sections_drop_out(self):
        site = json.loads(json.dumps(self.site))
        for key in ('band', 'clients', 'compare'):
            del site[key]
        del site['hero']['sources']
        text = self.build(site)
        self.assertNotIn('{{', text)
        for marker in ('class="band"', 'class="clients"', 'id="strip"', 'var TILES', 'class="srcs" id="sources"'):
            self.assertNotIn(marker, text)
        self.assertIn('id="dither"', text)
        self.assertIn('id="sources2"', text)

    def test_optional_sections_independent(self):
        for key in ('band', 'clients', 'compare'):
            with self.subTest(section=key):
                site = json.loads(json.dumps(self.site))
                del site[key]
                text = self.build(site)
                self.assertNotIn('{{', text)
                self.assertNotIn({'band': 'class="band"', 'clients': 'class="clients"',
                                  'compare': 'var TILES'}[key], text)
        site = json.loads(json.dumps(self.site))
        del site['account']['sources']
        self.assertNotIn('id="sources2"', self.build(site))

    def test_inline_json_cannot_close_script(self):
        import re
        site = json.loads(json.dumps(self.site))
        payload = '</script><script>alert("example")</script>&'
        site['headlines']['variants']['test'] = payload
        site['compare']['left']['items'][0]['name'] = payload
        text = self.build(site)
        self.assertNotIn(payload, text)
        match = re.search(r'var HEADLINES = (.*);', text)
        assert match is not None
        self.assertEqual(json.loads(match.group(1))['test'], payload)
        self.assertIn('\\u003c/script\\u003e', text)

    def test_msp_example_builds_without_peo_proof(self):
        source = ROOT / 'examples/span-msp-us'
        with tempfile.TemporaryDirectory() as td:
            text = module.build(source, Path(td) / 'msp.html')
        self.assertNotIn('{{', text)
        for marker in ('331,816', 'class="band"', 'class="clients"', 'var TILES', 'id="sources2"'):
            self.assertNotIn(marker, text)
        self.assertIn('MSP', text)

    def test_escapes_markup(self):
        site = json.loads(json.dumps(self.site))
        site['hero']['eyebrow'] = '<script>alert(1)</script>'
        text = self.build(site)
        self.assertNotIn('<script>alert', text)
        self.assertIn('&lt;script&gt;alert', text)

    def check_new_visual(self, kind):
        site = json.loads((ROOT / 'examples/span-msp-us/site.json').read_text())
        item = next(i for i in site['faq']['items'] if i['visual'] == kind)
        rendered = module.visual(item, interactive=True)
        self.assertIn('class="diagram ', rendered)
        self.assertIn('role="group" aria-label=', rendered)
        payload = '<img src=x onerror="alert(1)">&'
        for key, value in item['visualData'].items():
            with self.subTest(kind=kind, field=key):
                altered = json.loads(json.dumps(item))
                altered['visualData'][key] = [payload] * len(value) if isinstance(value, list) else payload
                output = module.visual(altered, interactive=True)
                self.assertNotIn(payload, output)
                self.assertIn('&lt;img', output)
                del altered['visualData'][key]
                with self.assertRaises(ValueError):
                    module.visual(altered, interactive=True)
                altered['visualData'][key] = [] if isinstance(value, list) else ''
                with self.assertRaises(ValueError):
                    module.visual(altered, interactive=True)

    def test_fanout_contract(self):
        self.check_new_visual('fanout')

    def test_loop_contract(self):
        self.check_new_visual('loop')

    def test_narrow_contract(self):
        self.check_new_visual('narrow')

    def test_anatomy_contract(self):
        self.check_new_visual('anatomy')

    def test_path_contract(self):
        self.check_new_visual('path')

    def test_sheet_and_market_contract(self):
        source = ROOT / 'examples/span-msp-us'
        site = json.loads((source / 'site.json').read_text())
        text = module.render(site, source)
        self.assertEqual(text.count('class="sample-record__panel'), 5)
        self.assertEqual(text.count('class="record__row"'), 4)
        self.assertEqual(text.count('<td data-column='), 36)
        self.assertEqual(text.count('"formValue":'), 4)
        self.assertNotIn('<ul class="ticks">', text)
        self.assertIn('sheet__stamp', text)
        site['dossier']['sheet']['fields'][0] = '<script>bad</script>'
        site['orbit']['items'][0]['title'] = '<script>bad</script>'
        text = module.render(site, source)
        self.assertNotIn('<script>bad', text)
        self.assertIn('&lt;script&gt;bad', text)
        site['orbit']['items'][0]['formValue'] = 'not an option'
        with self.assertRaises(ValueError):
            module.validate(site, source)
        del site['dossier']['sheet']['fields']
        with self.assertRaises(ValueError):
            module.sheet(site['dossier'])

    def test_picker_rendering_omission_and_validation(self):
        site = json.loads((ROOT / 'examples/span-msp-us/site.json').read_text())
        site['picker'] = {'title': 'Pick your list', 'hint': 'Choose a list', 'items': [dict(item, size='wide') for item in site.pop('orbit')['items']]}
        text = self.build(site)
        self.assertIn('id="picker"', text)
        self.assertNotIn('class="market__map"', text)
        self.assertNotIn('class="market__legend"', text)
        self.assertNotIn('id="picker"', self.build())
        without = json.loads(json.dumps(site))
        del without['picker']
        self.assertNotIn('id="picker"', self.build(without))
        self.assertNotIn('{{', self.build(without))
        for field, bad in [('id', 'INVALID'), ('id', 'mssp'), ('size', 'huge'), ('formValue', 'unknown')]:
            altered = json.loads(json.dumps(site))
            altered['picker']['items'][0][field] = bad
            with self.assertRaises(ValueError):
                self.build(altered)

    def test_orbit_rendering_omission_and_icon_boundary(self):
        site = json.loads((ROOT / 'examples/span-msp-us/site.json').read_text())
        text = self.build(site)
        self.assertEqual(text.count('class="ot-node ot-hidden"'), 4)
        self.assertIn('id="orbitCard"', text)
        self.assertNotIn('id="picker"', text)
        self.assertNotIn('class="market__legend"', text)
        self.assertNotIn('ot-root', self.build())
        without = json.loads(json.dumps(site))
        del without['orbit']
        self.assertNotIn('ot-root', self.build(without))
        self.assertNotIn('{{', self.build(without))
        payload = '</script><svg onload="alert(1)">'
        site['orbit']['items'][0]['title'] = payload
        site['orbit']['items'][0]['text'] = payload
        escaped = self.build(site)
        self.assertNotIn(payload, escaped)
        self.assertIn('&lt;/script&gt;', escaped)
        self.assertIn('\\u003c/script\\u003e', escaped)
        for field, value in [('icon', payload), ('icon', 'unknown'), ('id', 'mssp'), ('formValue', 'unknown')]:
            altered = json.loads(json.dumps(site))
            altered['orbit']['items'][0][field] = value
            with self.assertRaises(ValueError):
                self.build(altered)

    def test_fictional_records_masking_titles_and_escaping(self):
        site = json.loads((ROOT / 'examples/span-msp-us/site.json').read_text())
        for record in site['sampleRecords']:
            for key in ('name', 'email', 'company'):
                self.assertIn('•••', record[key])
                self.assertNotRegex(record[key], r'[\w.]{4,}•')
            self.assertIn(record['jobTitle'], site['jobTitles'])
        for key, value in [('name', 'Unmasked'), ('email', 'test@example.com'), ('company', 'Longprefix•••'), ('jobTitle', 'Not allowed')]:
            altered = json.loads(json.dumps(site))
            altered['sampleRecords'][0][key] = value
            with self.assertRaises(ValueError):
                self.build(altered)
        site['sampleRecords'][0]['name'] = '<img src=x onerror=alert(1)>•••'
        self.assertNotIn('<img src=x', self.build(site))
        self.assertIn('&lt;img src=x', self.build(site))

    def test_rejects_dash_bad_url_and_overflowing_counts(self):
        for mutate in [
            lambda s: s['hero'].__setitem__('lede', 'a \u2014 b'),
            lambda s: s['hero']['sources'][0].__setitem__('url', 'http://napeo.org'),
            lambda s: s['compare']['left']['items'][0].__setitem__('count', 10 ** 9),
            lambda s: s['faq']['items'].pop(),
            lambda s: s['faq']['items'][0].__setitem__('visual', 'nope'),
        ]:
            site = json.loads(json.dumps(self.site))
            mutate(site)
            with self.assertRaises(ValueError):
                self.build(site)


if __name__ == '__main__':
    unittest.main()
