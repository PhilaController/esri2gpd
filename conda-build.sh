#!/bin/bash

set -e

packageName=esri2gpd

echo "Building conda recipe..."
conda build --variants "{python: $PYTHON_VERSIONS}" conda-recipe/$packageName

echo "Converting conda package..."
conda convert --platform all /usr/share/miniconda/conda-bld/linux-64/$packageName-*.tar.bz2 --output-dir conda-bld/

exit 0