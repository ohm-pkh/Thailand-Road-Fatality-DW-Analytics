import requests
import pandas as pd
from minio import Minio
import os
from io import BytesIO
from datetime import datetime

def extract_province_shortname():
    url = "https://th.wikipedia.org/wiki/%E0%B8%A3%E0%B8%B2%E0%B8%A2%E0%B8%8A%E0%B8%B7%E0%B9%88%E0%B8%AD%E0%B8%AD%E0%B8%B1%E0%B8%81%E0%B8%A9%E0%B8%A3%E0%B8%A2%E0%B9%88%E0%B8%AD%E0%B8%82%E0%B8%AD%E0%B8%87%E0%B8%88%E0%B8%B1%E0%B8%87%E0%B8%AB%E0%B8%A7%E0%B8%B1%E0%B8%94%E0%B9%83%E0%B8%99%E0%B8%9B%E0%B8%A3%E0%B8%B0%E0%B9%80%E0%B8%97%E0%B8%A8%E0%B9%84%E0%B8%97%E0%B8%A2"
    df= pd.DataFrame()
    try:
        response = requests.get(
            url,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/138.0.0.0 Safari/537.36"
                )
            },
            timeout=30,
        )
        response.raise_for_status() 

        df = pd.read_html(response.text)[0]
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        raise

    except ValueError as e:
        print(f"Unable to parse HTML table: {e}")
        raise
    
    minio_url = os.getenv("MINIO_URL")
    minio_user = os.getenv("MINIO_USER")
    minio_password = os.getenv("MINIO_PASSWORD")
    
    client = Minio(minio_url,
                   access_key=minio_user,
                   secret_key=minio_password,
                   secure=False)
    
    buffer = BytesIO()
    df.to_parquet(buffer, index=False)
    
    buffer.seek(0)
    
    path = str(datetime.now().date()) + '/location/'
    
    client.put_object(
        bucket_name="extracted-data",
        object_name= path + "province_shortname.parquet",
        data=buffer,
        length=buffer.getbuffer().nbytes,
        content_type="application/octet-stream",
    )