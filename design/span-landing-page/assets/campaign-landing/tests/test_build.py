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
