# common shell for data

echo "Importing from common.sh"

DB=Metro
USER=cluster_user 
CONNECT_STR="mongodb+srv://cluster_user:cluster_pass@cluster0.9laqhsg.mongodb.net/?retryWrites=true&w=majority"
if [ -z $DATA_DIR ]
then
    # DATA_DIR=/home/amyf/SWE/JALT/data
    DATA_DIR=/Users/lalitm/JALT/data
fi
BKUP_DIR=$DATA_DIR/bkup
EXP=C:\Users\amyho\OneDrive\Desktop\school\Senior Year\SWE\mongodb-database-tools-windows-x86_64-100.9.4\bin/mongoexport.exe
# EXP=/Users/lalitm/Downloads/mongodb-database-tools-macos-arm64-100.9.4/bin/mongoexport
IMP=C:\Users\amyho\OneDrive\Desktop\school\Senior Year\SWE\mongodb-database-tools-windows-x86_64-100.9.4\bin/mongoimport.exe
# IMP=/Users/lalitm/Downloads/mongodb-database-tools-macos-arm64-100.9.4/bin/mongoimport

if [ -z $MONGO_PASSWD ]
then
    echo "You must set MONGO_PASSWD in your env before running this script."
    exit 1
fi

declare -a RouteCollections=("buses" "trains" "addresses" "users")
