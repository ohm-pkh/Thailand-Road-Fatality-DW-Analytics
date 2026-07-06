import pandas as pd
import os
from io import BytesIO
from minio import Minio


def try_extract():
    minio_url = os.getenv("MINIO_URL")
    minio_user = os.getenv("MINIO_USER")
    minio_password = os.getenv("MINIO_PASSWORD")
    client = Minio(minio_url,
        access_key=minio_user,
        secret_key=minio_password,
        secure=False,
    )
    
    df_list = []
    
    for obj in client.list_objects("test", recursive=True):
        
        if obj.object_name.endswith(".csv"):
            response = client.get_object("test", obj.object_name)
            df = pd.read_csv(response)
            response.close()
            response.release_conn()
            df_list.append(df)
    
    full_df = pd.concat(df_list, ignore_index=True)
    buffer = BytesIO()
    full_df.to_parquet(buffer, index=False)
    
    buffer.seek(0)
    
    client.put_object(
        bucket_name="test2",
        object_name="employee.parquet",
        data=buffer,
        length=buffer.getbuffer().nbytes,
        content_type="application/octet-stream",
    )
