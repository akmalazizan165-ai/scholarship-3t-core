import unittest, os, json, hashlib, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.qdrant_sync import generate_bge_m3_embedding, BGE_M3_DIMENSION

class TestEvidenceSync(unittest.TestCase):
    def test_source_id_format(self):
        sample_doi = "doi:10.1016/j.clinmed.2023.10045"
        digest = hashlib.sha256(sample_doi.strip().lower().encode('utf-8')).hexdigest()[:20]
        self.assertEqual(len(f"SRC-{digest}"), 24)

    def test_qdrant_vector_dimension(self):
        self.assertEqual(len(generate_bge_m3_embedding("ENT-MEDAI-NODE-01 test")), 1024)
        self.assertEqual(BGE_M3_DIMENSION, 1024)

    def test_schemas_exist(self):
        self.assertTrue(os.path.exists("schemas/a3p-ref-schema.json"))
        self.assertTrue(os.path.exists("schemas/sch-3t-ref-schema.json"))

if __name__ == "__main__":
    unittest.main()
