import esri2gpd
import pytest


def test_limit():
    url = "https://services.arcgis.com/fLeGjb7u4uXqeF9q/arcgis/rest/services/Philadelphia_ZCTA_2018/FeatureServer/0"
    gdf = esri2gpd.get(url, fields=["zip_code"], limit=1)
    assert len(gdf) == 1


def test_fields():
    url = "https://services.arcgis.com/fLeGjb7u4uXqeF9q/arcgis/rest/services/Philadelphia_ZCTA_2018/FeatureServer/0"
    gdf = esri2gpd.get(url, fields=["zip_code"])
    assert all(col in gdf.columns for col in ["zip_code", "geometry"])


def test_where():
    url = "https://services.arcgis.com/fLeGjb7u4uXqeF9q/arcgis/rest/services/Philadelphia_ZCTA_2018/FeatureServer/0"
    gdf = esri2gpd.get(url, fields=["zip_code"], where="zip_code=19123")
    assert (gdf["zip_code"] == 19123).all()

