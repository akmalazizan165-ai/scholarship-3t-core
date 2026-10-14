import unittest, os, json, hashlib, sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from scripts.qdrant_sync import generate_bge_m3_embedding, BGE_M3_DIMENSION

class TestEvidenceSync(unittest.TestCase):

    def test_source_id_format(self):
        sample_doi = "doi:10.1016/j.clinmed.2023.10045"
        digest = hashlib.sha256(sample_doi.strip().lower().encode('utf-8')).hexdigest()[:20]
        src_id = f"SRC-{digest}"
        self.assertTrue(src_id.startswith("SRC-"))
        self.assertEqual(len(src_id), 24)

    def test_qdrant_vector_dimension(self):
        vec = generate_bge_m3_embedding("ENT-MEDAI-NODE-01 test")
        self.assertEqual(len(vec), 1024)
        self.assertEqual(BGE_M3_DIMENSION, 1024)

    def test_schemas_exist(self):
        a3p_path = os.path.join(REPO_ROOT, "schemas", "a3p-ref-schema.json")
        sch_path = os.path.join(REPO_ROOT, "schemas", "sch-3t-ref-schema.json")
        self.assertTrue(os.path.exists(a3p_path), f"Missing {a3p_path}")
        self.assertTrue(os.path.exists(sch_path), f"Missing {sch_path}")
        with open(a3p_path) as f:
            data = json.load(f)
            self.assertEqual(data.get("type"), "object")

if __name__ == "__main__":
    unittest.main()
