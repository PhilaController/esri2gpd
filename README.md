# esri2gpd

[![Build Status](https://travis-ci.org/PhiladelphiaController/esri2gpd.svg?branch=master)](https://travis-ci.org/PhiladelphiaController/esri2gpd)
[![Coverage Status](https://coveralls.io/repos/github/PhiladelphiaController/esri2gpd/badge.svg?branch=master)](https://coveralls.io/github/PhiladelphiaController/esri2gpd?branch=master)
[![](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/download/releases/3.6.0/) 
![t](https://img.shields.io/badge/status-stable-green.svg) 
[![](https://img.shields.io/github/license/PhiladelphiaController/esri2gpd.svg)](https://github.com/PhiladelphiaController/esri2gpd/blob/master/LICENSE)
[![PyPi version](https://img.shields.io/pypi/v/esri2gpd.svg)](https://pypi.python.org/pypi/esri2gpd/) 
[![Anaconda-Server Badge](https://anaconda.org/controllerphl/esri2gpd/badges/version.svg)](https://anaconda.org/controllerphl/esri2gpd)

A lightweight Python tool to scrape features from the ArcGIS Server REST API and return a geopandas GeoDataFrame
python.

Inspired by the R package [esri2sf](https://github.com/yonghah/esri2sf/).

## Installation

Via conda: 

```
conda install -c controllerphl esri2gpd
```

Via PyPi:

```
pip install esri2gpd
```

## Example

```python
import esri2gpd

url = "https://services.arcgis.com/fLeGjb7u4uXqeF9q/ArcGIS/rest/services/Philly_Neighborhoods/FeatureServer/0"
gdf = esri2gpd.get(url, fields=['MAPNAME'], where="MAPNAME='Chestnut Hill'")

gdf.head()
```
