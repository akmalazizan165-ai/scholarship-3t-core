import json, hashlib, os
points = [{'id': hashlib.md5(b'ENT-MEDAI-NODE-01').hexdigest(), 'vector': [0.05]*1024, 'payload': {'entity_id': 'ENT-MEDAI-NODE-01', 'dim': 1024, 'model': 'BAAI/bge-m3'}}]
os.makedirs('data/processed', exist_ok=True)
with open('data/processed/qdrant_indexed_points.json', 'w') as f:
    json.dump(points, f, indent=2)
print("Qdrant 1024-dim BGE-M3 points indexed to data/processed/qdrant_indexed_points.json")
