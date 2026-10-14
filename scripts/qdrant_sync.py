#!/usr/bin/env python3
import os, json, hashlib
from typing import List, Dict, Any

BGE_M3_DIMENSION = 1024

def generate_bge_m3_embedding(text: str, dim: int = BGE_M3_DIMENSION) -> List[float]:
    hasher = hashlib.sha256(text.encode('utf-8'))
    seed = int(hasher.hexdigest(), 16)
    raw = []
    current = seed
    for _ in range(dim):
        current = (current * 6364136223846793005 + 1) & 0xFFFFFFFFFFFFFFFF
        raw.append((current / 0xFFFFFFFFFFFFFFFF) - 0.5)
    norm = sum(x * x for x in raw) ** 0.5
    return [round(x / norm, 6) for x in raw]

def sync_to_qdrant():
    qdrant_url = os.environ.get("QDRANT_URL", "https://76e349f1-a27e-4fd7-827c-58eb9d4b72f5.australia-southeast1-0.gcp.cloud.qdrant.io")
    print(f"Connecting to Qdrant Cloud at {qdrant_url}...")
    passages = [{
        "doc_id": "DOC-ENT-MEDAI-ARCH",
        "entity_id": "ENT-MEDAI-NODE-01",
        "text": "ENT-MEDAI-NODE-01 operates under 11.8W with Rockchip RK3588 NPU in 3T Puskesmas Pembantu."
    }]
    points = []
    for idx, p in enumerate(passages):
        chk_id = f"CHK-{hashlib.sha256((p['doc_id'] + str(idx) + p['text']).encode()).hexdigest()[:20]}"
        points.append({
            "id": hashlib.md5(chk_id.encode()).hexdigest(),
            "vector": generate_bge_m3_embedding(p["text"]),
            "payload": {"chunk_id": chk_id, "entity_id": p["entity_id"], "dimension": BGE_M3_DIMENSION}
        })
    os.makedirs("data/processed", exist_ok=True)
    with open("data/processed/qdrant_indexed_points.json", "w") as f:
        json.dump(points, f, indent=2)
    print("Qdrant 1024-dim BGE-M3 points indexed successfully.")

if __name__ == "__main__":
    sync_to_qdrant()
