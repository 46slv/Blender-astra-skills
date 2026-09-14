"""Host checks for structural retrieval and preserving scoped, versioned knowledge."""
import copy
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'skills/blender/scripts'))
import knowledge


class KnowledgeChecks(unittest.TestCase):
    def test_structural_and_bilingual_retrieval(self):
        for query in ('vertical supports repeated horizontal members count spacing', '支柱横板段数間隔'):
            ids = [e['card']['id'] for e in knowledge.search(query)[:3]]
            self.assertIn('astra.furniture.parametric-shelf', ids)
            self.assertIn('method.supports-and-repeated-members', ids)
        hit = knowledge.search('joint pivot shade exchange telescopic')[0]
        self.assertEqual(hit['card']['id'], 'astra.lighting.articulated-lamp')
        self.assertLess(hit['coverage'], 1)
        self.assertTrue(hit['card']['limits'])
        self.assertEqual(knowledge.search('xyzunknownnonsense'), [])

    def test_identity_and_portability(self):
        for entry in knowledge.cards():
            if entry['card']['kind'] == 'asset':
                self.assertTrue(Path(knowledge.resolve(entry)['file']).is_file())
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / 'moved'
            shutil.copytree(knowledge.LIBRARY, root)
            entry = knowledge.search('desk light', [root])[0]
            self.assertEqual(Path(knowledge.resolve(entry)['file']).parent, root)
            source = root / entry['card']['source']['file']
            with source.open('ab') as stream:
                stream.write(b'changed')
            with self.assertRaisesRegex(ValueError, 'Stale'):
                knowledge.resolve(entry)
            source.unlink()
            with self.assertRaises(FileNotFoundError):
                knowledge.resolve(entry)

    def test_scoped_capture_update_and_failed_overwrite(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            card = {'id': 'private.joint', 'kind': 'method', 'title': 'Private hinge method',
                    'summary': 'secretcomponentxyz', 'unknown_extension': {'keep': True}}
            saved = knowledge.save(card, root)
            with self.assertRaises(ValueError):
                knowledge.save(card, root)
            self.assertFalse(knowledge.search('secretcomponentxyz'))
            self.assertEqual(len(knowledge.search('secretcomponentxyz', [root])), 1)
            saved['terms'] = ['newexperiencexyz']
            revised = knowledge.save(saved, root, expected_revision=1)
            self.assertTrue(revised['unknown_extension']['keep'])
            with self.assertRaises(ValueError):
                knowledge.save(saved, root, expected_revision=1)
            self.assertEqual(knowledge.search('newexperiencexyz', [root])[0]['card']['revision'], 2)
            # Same logical ID in another explicit scope remains two distinct candidates.
            other = root / 'other'
            other.mkdir()
            knowledge.save(card, other)
            self.assertEqual(len(knowledge.search('secretcomponentxyz', [root, other])), 2)
            (root/'knowledge'/'duplicate.json').write_text(json.dumps(revised), encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'duplicate'):
                knowledge.cards([root])

    def test_bad_or_missing_sources_are_visible(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            with self.assertRaises(FileNotFoundError):
                knowledge.search('', [root/'missing'])
            (root/'knowledge').mkdir()
            (root/'knowledge'/'bad.json').write_text('{', encoding='utf-8')
            with self.assertRaises(json.JSONDecodeError):
                knowledge.cards([root])
        hit = copy.deepcopy(next(e for e in knowledge.cards() if e['card']['kind'] == 'asset'))
        hit['card']['source']['file'] = '../escape.blend'
        with self.assertRaisesRegex(ValueError, 'relative'):
            knowledge.resolve(hit)


if __name__ == '__main__':
    unittest.main()
