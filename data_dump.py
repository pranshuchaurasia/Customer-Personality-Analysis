import pymongo
import pandas as pd
import json
from analysis.config import env_var


# Provide the mongodb localhost url to connect python to mongodb.
client = pymongo.MongoClient(env_var.mongo_db_url)

DATA_FILE_PATH="/config/workspace/marketing_campaign.csv"
DATABASE_NAME="customer_data"
COLLECTION_NAME="marketing_campaign"

if __name__=="__main__":
    df=pd.read_csv(DATA_FILE_PATH)
    print(f"Rows and Columns: {df.shape}")
    #Convert dataframe to JSON so that we can dump the record in mongodb
    df.reset_index(drop=True, inplace=True)
    json_record=list(json.loads(df.T.to_json()).values())
    print(json_record[0])

    #insert json record into mongo db
    client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_record)