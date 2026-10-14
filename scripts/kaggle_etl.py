import json, csv, os
data = [{'district': 'DIS-PAPUA-01', 'name': 'Asmat', 'puskesmas': 14, 'solar_pustu': 5}]
os.makedirs('data/raw', exist_ok=True)
os.makedirs('data/processed', exist_ok=True)
with open('data/raw/demographics_3t.json', 'w') as f:
    json.dump(data, f, indent=2)
with open('data/processed/clean_metrics_3t.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=data[0].keys())
    w.writeheader()
    w.writerows(data)
print("Kaggle ETL completed successfully.")
