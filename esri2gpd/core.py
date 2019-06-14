import os
import requests
from arcgis2geojson import arcgis2geojson
import geopandas as gpd
import pandas as pd
import numpy as np


def _get_json_safely(response):
    """
    Check for JSON response errors, and if all clear, 
    return the JSON data
    """
    # bad status code
    if response.status_code != 200:
        reponse.raise_for_status()

    json = response.json()  # get the JSON
    if "error" in json:
        raise ValueError("Error: %s" % json["error"])

    return json


def get(url, fields=None, where=None, limit=None):
    """
    Scrape features from a ArcGIS Server REST API and return a
    geopandas GeoDataFrame.

    Parameters
    ----------
    url : str
        the REST API url for the Feature Service
    fields : list of str, optional
        the list of fields to include; the default behavior ('None') 
        returns all fields
    where : str, optional
        a string specifying the selection clause to select a subset of 
        data; the default behavior ('None') selects all data
    limit : int, optional
        limit the returned data to this many features

    Example
    -------
    >>> import esri2gpd
    >>> url = "https://services.arcgis.com/fLeGjb7u4uXqeF9q/ArcGIS/rest/services/Philly_Neighborhoods/FeatureServer/0"
    >>> gdf = esri2gpd.get(url, fields=['MAPNAME'], where="MAPNAME='Chestnut Hill'")
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
    ids = json["objectIds"]

    # impose the limit
    if limit is not None:
        ids = ids[:limit]

    # query in batches
    out = []
    batch_size = 250
    for sub_ids in np.array_split(ids, len(ids) // batch_size + 1):

        # params for this request
        params = dict(
            objectIds=", ".join(map(str, sub_ids)),
            f="json",
            outSR="4326",
            outFields=fields,
        )

        # get raw features
        response = requests.get(queryURL, params=params)
        json = _get_json_safely(response)

        # convert to GeoJSON and save
        geojson = [arcgis2geojson(f) for f in json["features"]]
        out.append(gpd.GeoDataFrame.from_features(geojson, crs={"init": "epsg:4326"}))

    return pd.concat(out, axis=0).reset_index(drop=True)
