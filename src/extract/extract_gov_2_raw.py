from src.utils.fetch_data import fetch_data
from src.utils import db_contact
from minio import Minio
import io
import os
import pandas as pd
import json
from datetime import datetime

def get_data_list():
    URL = os.getenv("DATASET_URL")
    
    try:
        res = fetch_data(URL)
        data = json.loads(res)
        resources = data["result"]["results"][0]["resources"]
        resources_csv = list()
        for r in resources:
            
            if r["format"] == "CSV":
                resources_csv.append(r)
                
        return resources_csv

    except RuntimeError as e:
        print(f"Error: {e}")
        raise

    except (json.JSONDecodeError, KeyError) as e:
        print(f"Invalid response: {e}")
        raise

    except Exception as e:
        print(f"Unexpected error: {e}")
        raise
    
def check_file(data:list,conn):
    
    new_upload = list()
    for d in data:
        row = db_contact.get_file_meta(d["id"],conn)
        if row == None:
            print(f"New Data found: {d["id"]}")
            new_upload.append(d)
            continue
        
        print("already have this id in history")  
        
        print(f"row: {row}")
        if row["last_modified"] < datetime.fromisoformat(d["last_modified"]):
            print(f"Print {d["id"]} need to be update")
            new_upload.append(d)
    
    return new_upload
    
    
def import_data(data_list,conn):
    
    try:
        minio_url = os.getenv("MINIO_URL")
        minio_user = os.getenv("MINIO_USER")
        minio_password = os.getenv("MINIO_PASSWORD")
    
        client = Minio(minio_url,
                    access_key=minio_user,
                    secret_key=minio_password,
                    secure=False)
        
        now = datetime.now()
        folder_name = "dataset_acc/" + now.strftime("%Y-%m-%d") + "/"
        
        for data in data_list:
            res = fetch_data(data["url"],binary=True)
            buffer = io.BytesIO(res)

            client.put_object(
                bucket_name="raw-data",
                object_name=folder_name + data["name"],
                data=buffer,
                length=len(res),
                content_type="text/csv",
            )
            
            db_contact.import_new_file(conn,"extracted",data,folder_name)
            
    except RuntimeError as e:
        print(f"Error: {e}")
        raise

    except (json.JSONDecodeError, KeyError) as e:
        print(f"Invalid response: {e}")
        raise
            
            

def extract_data_set_from_gov():
    try:
        conn = db_contact.get_conn()
        current_data_on_web = get_data_list()
        require_import = check_file(current_data_on_web,conn)
        import_data(require_import,conn)
    
    finally:
        db_contact.close_conn(conn)
    
    
if __name__ == "__main__":
    extract_data_set_from_gov()