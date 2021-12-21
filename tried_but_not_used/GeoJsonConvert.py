import pandas as pd
import geojson
import sys

def data2geojson(df):
    features = []
    insert_features = lambda X: features.append(
            geojson.Feature(geometry=geojson.Point((X["long"],
                                                    X["lat"],)),))
    df.apply(insert_features, axis=1)
    with open('map1.geojson', 'w', encoding='utf8') as fp:
        geojson.dump(geojson.FeatureCollection(features), fp, sort_keys=True, ensure_ascii=False)

col = ['lat','long']
data = sys.argv[1]
print("I Got IN here")
print(data)
df = pd.DataFrame(data, columns=col)
data2geojson(df)