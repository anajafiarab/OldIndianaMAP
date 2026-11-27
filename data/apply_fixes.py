import json

fixes = {
    '9620750': [
        (None, -87.333283, 39.075410),
    ],
    '96207501': [
        (None, -87.333283, 39.075410),
    ],
    '1593232': [
        ('RB-6',  -85.517449, 39.797128),
        ('RB-5A', -85.520239, 39.796073),
        ('RB-5',  -85.520239, 39.796073),
        ('RB-4',  -85.524015, 39.795496),
        ('RB-3',  -85.528790, 39.795158),
    ],
    '1900053': [
        ('TB-2a', -85.137981, 40.655207),
        ('TB-2',  -85.137981, 40.655207),
    ],
    '1592397': [
        ('B-04', -85.33058, 39.31684),
    ],
}

with open('legacy_boreholes-fixed.geojson') as f:
    data = json.load(f)

changed = 0
for feat in data['features']:
    des = str(feat['properties'].get('DES_NUMBER', ''))
    if des not in fixes:
        continue
    pid = feat['properties'].get('POINTID')
    if pid == '':
        pid = None
    for fix_pid, lon, lat in fixes[des]:
        if fix_pid == pid:
            old = feat['geometry']['coordinates']
            feat['geometry']['coordinates'] = [lon, lat]
            print(f"Fixed DES {des} POINTID={pid!r}: {old} → [{lon}, {lat}]")
            changed += 1
            break

with open('legacy_boreholes-fixed.geojson', 'w') as f:
    json.dump(data, f)

print(f"Updated {changed} points and saved the file.")