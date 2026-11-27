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
    '1382057': [
        (None, -85.652751, 38.336043),
    ],
    '1592397': [
        ('B-04', -85.33058, 39.31684),
    ],
    '1593232': [
        ('RB-6',  -85.517449, 39.797128),
        ('RB-5A', -85.520239, 39.796073),
        ('RB-5',  -85.520239, 39.796073),
        ('RB-4',  -85.524015, 39.795496),
        ('RB-3',  -85.528790, 39.795158),
    ],
    '1800324': [
        (None, -86.41370217, 39.4167992),   # ← positive lon (probably should be negative)
    ],
    '1800325': [
        (None, -86.41370217, 39.4167992),   # ← positive lon (probably should be negative)
    ],
    '1800329': [
        (None, -86.414208, 39.416767),
    ],
    '1900053': [
        ('TB-2a', -85.137981, 40.655207),
        ('TB-2',  -85.137981, 40.655207),
    ],
    '1902653': [
        (None, -85.78360, 38.71460),
    ],
    '9620750': [
        (None, -87.333283, 39.075410),
    ],
    '96207501': [
        (None, -87.333283, 39.075410),
    ],
    '9803540': [
        (None, -84.912515, 40.658406),
    ],
    '1500657': [
        (None, -87.11145, 39.44986),
    ],
    '1401350': [
        (None, -85.76920, 38.31108),
    ],
    '1800136': [
        (None, -87.072852, 40.025938),
    ],
    # --- new ones ---
    '1901879': [
        (None, -86.046810, 40.059425),
    ],
    '1901880': [
        (None, -86.025610, 40.049135),
    ],
    '2101141': [
        (None, -87.064387, 41.466813),
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