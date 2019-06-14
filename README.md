# esri2gpd

A lightweight Python tool to scrape features from the ArcGIS Server REST API and return a geopandas GeoDataFrame
python.

Inspired by the R package [esri2sf](https://github.com/yonghah/esri2sf/).

# Example

```python
import esri2gpd

url = "https://services.arcgis.com/fLeGjb7u4uXqeF9q/ArcGIS/rest/services/Philly_Neighborhoods/FeatureServer/0"
gdf = esri2gpd.get(url, fields=['MAPNAME'], where="MAPNAME='Chestnut Hill'")

gdf.head()
```
