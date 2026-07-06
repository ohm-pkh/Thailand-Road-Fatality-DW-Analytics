import os
import pandas as pd
from io import BytesIO
from minio import Minio

def try_transform():
    minio_url = os.getenv("MINIO_URL")
    minio_user = os.getenv("MINIO_USER")
    minio_password = os.getenv("MINIO_PASSWORD")
    client = Minio(minio_url,
        access_key=minio_user,
        secret_key=minio_password,
        secure=False,
    )
    response = client.get_object("test2","employee.parquet")
    data = response.read()
    buffer1 = BytesIO(data)
    df = pd.read_parquet(buffer1)
    response.close()
    response.release_conn()
    df["salary"] = pd.to_numeric(df["salary"], errors="coerce")
    transformed_df = df.groupby("department", as_index=False).agg(
        avg_salary=("salary", "mean")
    )
    
    buffer2 = BytesIO()
    
    transformed_df.to_parquet(buffer2, index=False)
    
    buffer2.seek(0)
    
    client.put_object(
        bucket_name="test3",
        object_name="transformed_employee.parquet",
        data=buffer2,
        length=buffer2.getbuffer().nbytes,
        content_type="application/octet-stream",
    )