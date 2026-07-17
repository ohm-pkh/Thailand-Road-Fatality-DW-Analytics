from minio import Minio
from datetime import datetime
from pathlib import Path
from io import BytesIO
import os
import pandas as pd

def extract_location():
    minio_url = os.getenv("MINIO_URL")
    minio_user = os.getenv("MINIO_USER")
    minio_password = os.getenv("MINIO_PASSWORD")
    
    client = Minio(minio_url,
                   access_key=minio_user,
                   secret_key=minio_password,
                   secure=False)
    
    path = '/location/' + str(datetime.now().date())
    
    for obj in client.list_objects(bucket_name="raw-data",prefix="location/" , recursive=True):
        if obj.object_name.endswith(".csv"):
            response = client.get_object("raw-data", obj.object_name)
            df = pd.read_csv(response)
            response.close()
            response.release_conn()
            buffer = BytesIO()
            df.to_parquet(buffer, index=False)
            
            buffer.seek(0)
            
            parquet_name = str(Path(obj.object_name).with_suffix(".parquet"))
            parquet_name = parquet_name.removeprefix("location/")
            
            client.put_object(
                bucket_name="stage-data",
                object_name= path + parquet_name,
                data=buffer,
                length=buffer.getbuffer().nbytes,
                content_type="application/octet-stream",
            )