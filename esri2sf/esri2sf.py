import os
import requests
from arcgis2geojson import arcgis2geojson
import geopandas as gpd


def _get_json_safely(response):
    """
    Check for JSON response errors, and if all clear, 
    return the JSON data
    """
    response.raise_for_status()  # raise exceptions
    json = response.json()  # get the JSON
    if 'error' in json:
        raise ValueError("Error: %s" % json['error']['details'][0])

    return json


def get(url, fields=None, where=None):
    """
    Scrape features from a ArcGIS Server REST API and return a
    geopandas GeoDataFrame.

    Parameters
    ----------
    url : str
        the REST API url for the Feature Service
    fields : list of str
        the list of fields to include; the default behavior ('None') 
        returns all fields
    where : str
        a string specifying the selection clause to select a subset of 
        data; the default behavior ('None') selects all data

    Example
    -------
    >>> url = "https://services.arcgis.com/fLeGjb7u4uXqeF9q/ArcGIS/rest/services/Philly_Neighborhoods/FeatureServer/0"
    >>> gdf = esri2sf.get(url, fields=['MAPNAME'], where="MAPNAME='Chestnut Hill'")
    >>> gdf
    """

    # default behavior matches all features
    if where is None:
        where = "1=1"
    if fields is None:
        fields = "*"
    else:
        fields = ", ".join(fields)

    # extract object IDs of features
    queryURL = os.path.join(url, "query")
    params = dict(where=where, returnIdsOnly="true", f="json")
    response = requests.get(queryURL, params=params)

    # get the object IDs safely
    json = _get_json_safely(response)
    ids = json['objectIds']

    # get raw features
    params = dict(objectIds=", ".join(map(str, ids)),
                  f="json",
                  outSR="4326",
                  outFields=fields)
    response = requests.get(queryURL, params=params)
    json = _get_json_safely(response)

    # convert to GeoJSON and return
    geojson = [arcgis2geojson(f) for f in json['features']]
    return gpd.GeoDataFrame.from_features(geojson, crs={"init": "epsg:4326"})
