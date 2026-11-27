import json

with open('legacy_boreholes-fixed.geojson') as f:
    data = json.load(f)

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
        (None, -86.41370217, 39.4167992),
    ],
    '1800325': [
        (None, -86.41370217, 39.4167992),
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

print(f"Updated {changed} points.")