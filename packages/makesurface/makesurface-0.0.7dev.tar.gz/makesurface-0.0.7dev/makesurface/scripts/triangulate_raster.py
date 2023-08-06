import rasterio, mercantile, json, click, sys
import numpy as np

def quadtree(x, y, zoom):
    xA = (2 ** np.arange(zoom))[::-1]
    xA = (x / xA) % 2
    yA = (2 ** np.arange(zoom))[::-1]
    yA = (y / yA) % 2
    out = np.zeros(zoom, dtype=np.str)
    out[np.where((xA == 0) & (yA == 0))] = '0'
    out[np.where((xA == 1) & (yA == 0))] = '1'
    out[np.where((xA == 0) & (yA == 1))] = '2'
    out[np.where((xA == 1) & (yA == 1))] = '3'
    return ''.join(out)

def getCorners(bounds, boolKey):
    coordOrd = {
        False: [
                   [0, 2, 3, 0],
                   [0, 2, 1, 0]
                ],
        True: [
                   [3, 1, 2, 3],
                   [3, 1, 0, 3]
                ]
        }

    corners = np.array([
        [bounds.west, bounds.south],
        [bounds.east, bounds.south],
        [bounds.east, bounds.north],
        [bounds.west, bounds.north]
        ])

    return [
        corners[coordOrd[boolKey][0]],
        corners[coordOrd[boolKey][1]]
    ]

def triangulate(zoom, output, bounds, tile):
    if bounds:
        bounds = np.array(bounds.split(' ')).astype(np.float64)
    elif tile:
        tile = np.array(tile.split(' ')).astype(np.uint16)
        tBounds = mercantile.bounds(tile[0], tile[1], tile[2])
        bounds = np.array([tBounds.west, tBounds.south, tBounds.east , tBounds.north])
    else:
        sys.exit('Error: A bounds or tile must be specified')

    gJSON = {
        "type": "FeatureCollection",
        "features": []
    }
    tileMin = mercantile.tile(bounds[0], bounds[3], zoom)
    tileMax = mercantile.tile(bounds[2], bounds[1], zoom)


    for r in range(tileMin.y, tileMax.y):
        for c in range(tileMin.x, tileMax.x):
            quad = quadtree(c, r, zoom)
            boolKey = (r+c) % 2 == 0

            coords = getCorners(mercantile.bounds(c, r, zoom), boolKey)
            gJSON['features'].append({
                "type": "Feature",
                "properties": {
                    "quadtree": quad,
                    "dir": 'n'
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [coords[0].tolist()]
                }
                })
            gJSON['features'].append({
                "type": "Feature",
                "properties": {
                    "quadtree": quad,
                    "dir": 's'
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [coords[1].tolist()]
                }
                })

    if output:
        with open(output, 'w') as oFile:
            oFile.write(json.dumps(gJSON, indent=2))
    else:
        stdout = click.get_text_stream('stdout')
        stdout.write(json.dumps(gJSON, indent=2))