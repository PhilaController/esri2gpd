#!/bin/bash

set -e

for packageName in "arcgis2geojson" "esri2gpd";
do
    echo "Building conda recipe..."
    conda build --variants "{python: [3.6, 3.7, 3.8]}" conda-recipe/$packageName

    echo "Converting conda package..."
    conda convert --platform all $HOME/miniconda/conda-bld/linux-64/$packageName-*.tar.bz2 --output-dir conda-bld/

    echo "Deploying to Anaconda.org..."
    anaconda -t $ANACONDA_TOKEN upload --skip-existing conda-bld/**/$packageName-*.tar.bz2
done

echo "Successfully deployed to Anaconda.org."
exit 0