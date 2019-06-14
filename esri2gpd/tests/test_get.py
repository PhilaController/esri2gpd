import esri2gpd
import pytest


def test_limit():
    url = "https://services.arcgis.com/fLeGjb7u4uXqeF9q/ArcGIS/rest/services/Philly_Neighborhoods/FeatureServer/0"
    gdf = esri2gpd.get(url, fields=["MAPNAME"], limit=1)
    assert len(gdf) == 1


def test_fields():
    url = "https://services.arcgis.com/fLeGjb7u4uXqeF9q/ArcGIS/rest/services/Philly_Neighborhoods/FeatureServer/0"
    gdf = esri2gpd.get(url, fields=["MAPNAME"])
    assert all(col in gdf.columns for col in ["MAPNAME", "geometry"])


def test_where():
    url = "https://services.arcgis.com/fLeGjb7u4uXqeF9q/ArcGIS/rest/services/Philly_Neighborhoods/FeatureServer/0"
    gdf = esri2gpd.get(url, fields=["MAPNAME"], where="MAPNAME='Chestnut Hill'")
    assert (gdf["MAPNAME"] == "Chestnut Hill").all()

