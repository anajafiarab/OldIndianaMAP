import json
import urllib.request
import time

base = "https://gis.indot.in.gov/ro/rest/services/DOT/BoreRecords/MapServer/0/query"
page_size = 2000
offset = 0
all_features = []

print("Downloading BoreRecords...")

while True:
    url = (
        f"{base}?where=1%3D1"
        f"&outFields=*"
        f"&f=geojson"
        f"&resultOffset={offset}"
        f"&resultRecordCount={page_size}"
        f"&returnGeometry=true"
        f"&outSR=4326"
    )
    print(f"  offset {offset} ...", end=" ", flush=True)
    try:
        with urllib.request.urlopen(url, timeout=60) as r:
            data = json.load(r)
    except Exception as e:
        print(f"Error: {e}")
        break

    features = data.get("features", [])
    print(f"got {len(features)}")
    if not features:
        break

    all_features.extend(features)
    if len(features) < page_size:
        break

    offset += page_size
    time.sleep(0.3)

geojson = {
    "type": "FeatureCollection",
    "features": all_features
}

out_path = "borerecords_backup.geojson"
with open(out_path, "w") as f:
    json.dump(geojson, f)

print(f"\nDone. Wrote {len(all_features)} features to {out_path}")