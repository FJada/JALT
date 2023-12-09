#!/bin/bash

# Script to restore data using mongoimport

# Source common.sh
. ./common.sh

for collection in "${RouteCollections[@]}"; do
    echo "Restoring $collection"
    "$IMP" --db="$DB" --collection="$collection" --drop --file="$BKUP_DIR/$collection.json"
done
