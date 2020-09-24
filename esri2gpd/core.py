import warnings

import geopandas as gpd
import numpy as np
import pandas as pd
import requests
from arcgis2geojson import arcgis2geojson


def _get_json_safely(response):
    """
    Check for JSON response errors, and if all clear, 
    return the JSON data
    """
    # bad status code
    if response.status_code != 200:
        response.raise_for_status()

    json = response.json()  # get the JSON
    if "error" in json:
        raise ValueError("Error: %s" % json["error"])

    return json


def get(url, fields=None, where=None, limit=None, **kwargs):
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
    >>> url = "https://services.arcgis.com/fLeGjb7u4uXqeF9q/arcgis/rest/services/Philadelphia_ZCTA_2018/FeatureServer/0"
    >>> gdf = esri2gpd.get(url, fields=['zip_code'], where="zip_code=19123")
    >>> gdf
    """
    # Get the max record count
    metadata = requests.get(url, params=dict(f="pjson")).json()
    max_record_count = metadata["maxRecordCount"]

    # default behavior matches all features
    if where is None:
        where = "1=1"
    if fields is None:
        fields = "*"
    else:
        fields = ", ".join(fields)

    # extract object IDs of features
    queryURL = f"{url}/query"

    # Get the total record count
    params = dict(where=where, returnCountOnly="true", f="json")
    response = requests.get(queryURL, params=params)
    total_size = _get_json_safely(response)["count"]

    # Check the limit
    if limit is not None:
        total_size = limit

    # params for this request
    resultOffset = 0
    params = dict(
        f="json",
        outSR="4326",
        outFields=fields,
        resultOffset=resultOffset,
        where=where,
        **kwargs,
    )

    calls = total_size // max_record_count
    if calls > 10:
        warnings.warn(
            f"Long download time — total download will require {calls} separate requests"
        )

    out = []
    while params["resultOffset"] < total_size:

        remaining = total_size - params["resultOffset"]
        if remaining < max_record_count:
            params["resultRecordCount"] = remaining

        # get raw features
        response = requests.get(queryURL, params=params)
        json = _get_json_safely(response)

        # convert to GeoJSON and save
        geojson = [arcgis2geojson(f) for f in json["features"]]
        if gpd.__version__ >= "0.7":
            gdf = gpd.GeoDataFrame.from_features(geojson, crs="EPSG:4326")
        else:
            gdf = gpd.GeoDataFrame.from_features(geojson, crs={"init": "epsg:4326"})
        out.append(gdf)

        params["resultOffset"] += len(out[-1])

    return pd.concat(out, axis=0).reset_index(drop=True)
