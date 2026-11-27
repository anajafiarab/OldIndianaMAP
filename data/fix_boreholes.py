#!/usr/bin/env python3
import json
from collections import defaultdict

with open('legacy_boreholes.geojson') as f:
    data = json.load(f)

print(f"Loaded {len(data['features'])} features\n")

outliers = []
for feat in data['features']:
    lon, lat = feat['geometry']['coordinates']
    if lat > 41.9 or lat < 37.7 or lon < -88.1 or lon > -84.7:
        des = feat['properties'].get('DES_NUMBER', '')
        pid = feat['properties'].get('POINTID', '')
        outliers.append((des, pid, lon, lat))

by_des = defaultdict(list)
for des, pid, lon, lat in outliers:
    by_des[des].append((pid, lon, lat))

print("Bad DES numbers (points outside Indiana):")
print("-" * 60)
for des, points in sorted(by_des.items()):
    print(f"\nDES {des}  ({len(points)} points)")
    for pid, lon, lat in points[:5]:
        print(f"  {pid or '(no id)':12}  lon={lon:.6f}  lat={lat:.6f}")
    if len(points) > 5:
        print(f"  ... and {len(points)-5} more")

# ===== EDIT THIS DICTIONARY =====
# Put the correct lon, lat for each DES you want to fix.
# Example:  '1593232': (-85.51, 41.00),
# ===== EDIT THIS DICTIONARY =====
# Each entry is DES_NUMBER -> list of (POINTID or None, lon, lat)
# Fill in the real lon, lat for each boring. Leave the placeholders as-is until you have numbers.
fixes = {
   
    '1901879': [
    ('1', -86.046810, 40.059425),   # first boring
],
    '1901880': [
    ('2', -86.025610, 40.049135),   # first boring
],
    '2101141': [
    ('1', -87.064387, 41.466813),   # first boring
],

}

# ================================
# ================================

fixed_count = 0
for feat in data['features']:
    des = feat['properties'].get('DES_NUMBER', '')
    pid = feat['properties'].get('POINTID', '') or None
    if des in fixes:
        for entry in fixes[des]:
            target_pid, lon, lat = entry
            if target_pid is None or target_pid == pid:
                feat['geometry']['coordinates'] = [lon, lat]
                fixed_count += 1
                break

print(f"\nApplied fixes to {fixed_count} features")

out_name = 'legacy_boreholes-fixed.geojson'
with open(out_name, 'w') as f:
    json.dump(data, f)
print(f"Wrote {out_name}")