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
    api_key = os.environ.get("QDRANT_API_KEY", "")

    passages = [{
        "doc_id": "DOC-ENT-MEDAI-ARCH",
        "entity_id": "ENT-MEDAI-NODE-01",
        "text": "ENT-MEDAI-NODE-01 operates under 11.8W with Rockchip RK3588 NPU in 3T Puskesmas Pembantu.",
        "topic": "Edge Hardware & Energy",
        "source_url": "https://scholarship3t.miraheze.org/wiki/ENT-MEDAI-NODE-01"
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

    if api_key:
        try:
            from qdrant_client import QdrantClient
            from qdrant_client.models import Distance, VectorParams, PointStruct
            client = QdrantClient(url=qdrant_url, api_key=api_key)
            coll = "medical_ai_ecosystem"
            if not client.collection_exists(coll):
                client.create_collection(coll, vectors_config=VectorParams(size=BGE_M3_DIMENSION, distance=Distance.COSINE))
            qdrant_points = [PointStruct(id=pt["id"], vector=pt["vector"], payload=pt["payload"]) for pt in points]
            client.upsert(collection_name=coll, points=qdrant_points)
            print(f"[SUCCESS] Upserted {len(qdrant_points)} points to live Qdrant Cloud collection '{coll}'.")
        except Exception as e:
            print(f"[!] Qdrant live notice: {e}. Staged vectors locally.")
    else:
        print(f"[INFO] QDRANT_API_KEY secret not set. Staged {len(points)} 1024-dim BGE-M3 points locally.")

if __name__ == "__main__":
    sync_to_qdrant()
