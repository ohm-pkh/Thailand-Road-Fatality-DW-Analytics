import requests
import pandas as pd
import os
from minio import Minio
from io import BytesIO
from datetime import datetime

def extract_main_nationality():
    url='https://en.wikipedia.org/wiki/ISO_3166-1'
    df = pd.DataFrame()
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

        df = pd.read_html(response.text)[1]
        print(df)
        
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
    
    path = str(datetime.now().date()) + '/nationality/'
    
    client.put_object(
        bucket_name="extracted-data",
        object_name= path + "main_nationality.parquet",
        data=buffer,
        length=buffer.getbuffer().nbytes,
        content_type="application/octet-stream",
    )
    
def extract_adjectival_nationality():
    url='https://en.wikipedia.org/wiki/List_of_adjectival_and_demonymic_forms_for_countries_and_nations'
    df = pd.DataFrame()
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
        print(df)
        
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
    
    path =  str(datetime.now().date()) + '/nationality/' 
    
    client.put_object(
        bucket_name="extracted-data",
        object_name= path + "adjectival.parquet",
        data=buffer,
        length=buffer.getbuffer().nbytes,
        content_type="application/octet-stream",
    )