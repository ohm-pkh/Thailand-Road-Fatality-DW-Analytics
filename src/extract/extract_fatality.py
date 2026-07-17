from minio import Minio
from pathlib import Path
import pandas as pd
from io import BytesIO
from datetime import datetime
import os
from src.utils.db_contact import get_imported_file, get_conn, update_file_status, close_conn


def extract_accident():
    conn = get_conn()
    try:
        require_extract = get_imported_file(conn)
        if len(require_extract) < 1:
            return
        
        print(f"Found {len(require_extract)} files ready to extract.")
        
        encodings = ["utf-8", "cp874", "tis-620", "utf-8-sig", "latin1"]
        
        minio_url = os.getenv("MINIO_URL")
        minio_user = os.getenv("MINIO_USER")    
        minio_password = os.getenv("MINIO_PASSWORD")
        
        client = Minio(minio_url,
                    access_key=minio_user,
                    secret_key=minio_password,
                    secure=False)
        
        print(require_extract)
        print(type(require_extract))
        print(require_extract[0]["file_id"])
        
        for obj in require_extract:
            obj_name = obj["file_location"] + obj["filename"]
            response = client.get_object("raw-data", obj_name)
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
                
            client.put_object(
                bucket_name="stage-data",
                object_name= obj_name+'.parquet',
                data=buffer,
                length=buffer.getbuffer().nbytes,
                content_type="application/octet-stream",
            )
            
            update_file_status(conn,obj["file_id"],"on stage")
    finally:
        close_conn(conn)