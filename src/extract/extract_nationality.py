from src.utils.fetch_data import fetch_data
import pandas as pd
import os
from minio import Minio
from pathlib import Path
from io import BytesIO
from datetime import datetime

def extract_main_nationality():
    
    df = pd.DataFrame()
    try:
        url='https://en.wikipedia.org/wiki/ISO_3166-1'
        headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/138.0.0.0 Safari/537.36"
                )
            }
        
        data = fetch_data(url,headers=headers)
        df = pd.read_html(data)[0]
    except RuntimeError as e:
        print(f"Error: {e}")
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
    df.to_csv(buffer, index=False)
    
    buffer.seek(0)
    
    path = '/nationality/' + str(datetime.now().date())
    
    client.put_object(
        bucket_name="raw-data",
        object_name= path + "main_nationality.csv",
        data=buffer,
        length=buffer.getbuffer().nbytes,
        content_type="application/octet-stream",
    )
    
def extract_adjectival_nationality():
    
    df = pd.DataFrame()
    try:
        url='https://en.wikipedia.org/wiki/List_of_adjectival_and_demonymic_forms_for_countries_and_nations'
        headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/138.0.0.0 Safari/537.36"
                )
            }
        
        data = fetch_data(url,headers=headers)
        df = pd.read_html(data)[0]
    except RuntimeError as e:
        print(f"Error: {e}")
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
    df.to_csv(buffer, index=False)
    
    buffer.seek(0)
    
    path =  '/nationality/' + str(datetime.now().date())
    
    client.put_object(
        bucket_name="raw-data",
        object_name= path + "adjectival.csv",
        data=buffer,
        length=buffer.getbuffer().nbytes,
        content_type="application/octet-stream",
    )
    
def move_nationality_to_stage():
    minio_url = os.getenv("MINIO_URL")
    minio_user = os.getenv("MINIO_USER")
    minio_password = os.getenv("MINIO_PASSWORD")
    
    client = Minio(minio_url,
                   access_key=minio_user,
                   secret_key=minio_password,
                   secure=False)
    
    path =  '/nationality/' + str(datetime.now().date())
    
    for obj in client.list_objects(bucket_name="raw-data",prefix="nationality/" , recursive=True):
        if obj.object_name.endswith(".csv"):
            response = client.get_object("raw-data", obj.object_name)
            df = pd.read_csv(response)
            response.close()
            response.release_conn()
            buffer = BytesIO()
            df.to_parquet(buffer, index=False)
            
            buffer.seek(0)
            
            parquet_name = str(Path(obj.object_name).with_suffix(".parquet"))
            parquet_name = parquet_name.removeprefix("nationality/")
            
            client.put_object(
                bucket_name="stage-data",
                object_name= path + parquet_name,
                data=buffer,
                length=buffer.getbuffer().nbytes,
                content_type="application/octet-stream",
            )