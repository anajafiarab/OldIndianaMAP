import json

# Read the current fixed file
with open('legacy_boreholes-fixed.geojson') as f:
    data = json.load(f)

# ===== NEW POINTS TO ADD =====
additions = [
    {
        'DES_NUMBER': '1592448',
        'POINTID': 'End',              # blank is fine
        'lon': -85.845623,
        'lat': 39.927707
    },
    {
        'DES_NUMBER': '1592448',
        'POINTID': 'Begin',
        'lon': -85.843134,
        'lat': 39.900914,
    },
    # add more dicts here
]
# =============================

# Skip only if the DES_NUMBER is already present
existing_des = {str(f['properties'].get('DES_NUMBER', '')) for f in data['features']}

added = 0
for a in additions:
    des = a['DES_NUMBER']
    if des in existing_des:
        print(f"Skipping DES {des} — already exists")
        continue

    new_feat = {
        "type": "Feature",
        "properties": {
            "DES_NUMBER": des,
            "POINTID": a.get('POINTID', ''),   # defaults to empty string
        },
        "geometry": {
            "type": "Point",
            "coordinates": [a['lon'], a['lat']]
        }
    }
    data['features'].append(new_feat)
    print(f"Added DES {des}")
    added += 1

# Write back to the same file
with open('legacy_boreholes-fixed.geojson', 'w') as f:
    json.dump(data, f)

print(f"Done. Added {added} new point(s).")