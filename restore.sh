#!/bin/bash

# Script to restore data using mongoimport

# Source common.sh
. ./common.sh

for collection in "${RouteCollections[@]}"; do
    echo "Restoring $collection"
    "/mnt/c/Users/amyho/OneDrive/Desktop/school/Senior_Year/SWE/mongodb-database-tools-windows-x86_64-100.9.4/bin/mongoimport.exe" --db="$DB" --collection="$collection" --drop --file="$BKUP_DIR/$collection.json"
done
