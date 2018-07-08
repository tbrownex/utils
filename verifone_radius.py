# Experian will send us demographics on all households within a certain radius of our test stores.
# They charge for each HH they send. So if we already have the demo, then tell them not to send (via the "suppress" file)

import winsound
import sys
import time
import sqlalchemy
from   sqlalchemy.types import TEXT, BIGINT, INTEGER, FLOAT, DATE
from get_chain import chain

# Input Directory
OUTPUT_DIR = "D:\\Loyalty Vision\\data\\"
# Database
LOCAL_PG_USER  = "postgres"
LOCAL_PG_PASS  = "Wftcww1l"
LOCAL_PG_HOST  = "localhost"
LOCAL_DB_NAME  = "LV Test"

engine = sqlalchemy.create_engine('postgres://{username}:{password}@{host}/{db}'.format(
        username=LOCAL_PG_USER,
        password=LOCAL_PG_PASS,
        host=LOCAL_PG_HOST,
        db=LOCAL_DB_NAME))

connection = engine.connect()

chain = chain(connection)           # Get the chain

tab = '\t'

verifone = open(OUTPUT_DIR + 'verifone.csv','w')    # Stores within a radius of HH with a given income
rec = "Store #" +tab+ "CBG ID" +tab+ "\n"
verifone.write(rec)

rad = raw_input("Enter distance in meters: ")

start_time = time.time()
tab = "\t"

#   "store_loc" is a View over store and store_batch with chain, store and geo
sql = "SELECT cbg_id, geo FROM cbg_stats"

try:
    result_set = connection.execute(sql, (chain,))
    cbgs = result_set.fetchall()
except (sqlalchemy.exc.SQLAlchemyError, sqlalchemy.exc.DBAPIError) as e:
        print(sql)
        print("SELECT from store_loc failed")
        e = sys.exc_info()[0]
        print(e)
        sys.exit()

if result_set.rowcount < 1:
    print("no CBGs found")
    sys.exit()

sql = ("SELECT store_num FROM store "
       "WHERE chain = 33 "
       "AND ST_DWithin(geo, %s, %s)")

for cbg in cbgs:
    try:
        result_set = connection.execute(sql, (cbg[1], rad))
        stores = result_set.fetchall()
    except (sqlalchemy.exc.SQLAlchemyError, sqlalchemy.exc.DBAPIError) as e:
        print(sql)
        print("ST_DWithin SELECT failed")
        e = sys.exc_info()[0]
        print(e)
        sys.exit()
# For each household within the radius: if we have the demographics, no need for Experian to send us (and charge for it)
    for store in stores:
        rec = store[0] +tab+ str(cbg[0]) + "\n"
        verifone.write(rec)

print("Processing time:  %s  minutes" % ((time.time() - start_time)/60))
winsound.Beep(300,2000)