from minio import Minio
from pathlib import Path
import pandas as pd
from io import BytesIO
from datetime import datetime
import os


def extract_accident():
    encodings = ["utf-8", "cp874", "tis-620", "utf-8-sig", "latin1"]
    
    minio_url = os.getenv("MINIO_URL")
    minio_user = os.getenv("MINIO_USER")
    minio_password = os.getenv("MINIO_PASSWORD")
    
    client = Minio(minio_url,
                   access_key=minio_user,
                   secret_key=minio_password,
                   secure=False)
    
    path =  str(datetime.now().date()) + '/accident/'
    
    
    
    for obj in client.list_objects(bucket_name="raw-data",prefix="dataset_acc/" , recursive=True):
        if obj.object_name.endswith(".csv"):
            response = client.get_object("raw-data", obj.object_name)
            df = pd.DataFrame()
            for enc in encodings:
                try:
                    df = pd.read_csv(response, encoding=enc)
                    break
                except Exception:
                    continue
            response.close()
            response.release_conn()
            buffer = BytesIO()
            df.to_parquet(buffer, index=False)
            
            buffer.seek(0)
            
            parquet_name = str(Path(obj.object_name).with_suffix(".parquet"))
            parquet_name = parquet_name.removeprefix("dataset_acc/")
            
            client.put_object(
                bucket_name="extracted-data",
                object_name= path + parquet_name,
                data=buffer,
                length=buffer.getbuffer().nbytes,
                content_type="application/octet-stream",
            )