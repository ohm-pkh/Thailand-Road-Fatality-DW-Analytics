import psycopg2
import pandas as pd
from minio import Minio
from io import BytesIO
import os

def try_load():
    
    conn = psycopg2.connect(
        dbname=os.getenv("WAREHOUSE_DATABASE"),
        user=os.getenv("WAREHOUSE_USER"),
        password=os.getenv("WAREHOUSE_PASSWORD"),
        host=os.getenv("WAREHOUSE_HOST"),
        port=os.getenv("WAREHOUSE_PORT")
    )
    cursor = conn.cursor()
    
    minio_url = os.getenv("MINIO_URL")
    minio_user = os.getenv("MINIO_USER")
    minio_password = os.getenv("MINIO_PASSWORD")
    client = Minio(minio_url,
        access_key=minio_user,
        secret_key=minio_password,
        secure=False,
    )
    response = client.get_object("test3","transformed_employee.parquet")
    data = response.read()
    buffer1 = BytesIO(data)
    df = pd.read_parquet(buffer1)
    response.close()
    response.release_conn()
    ## as we do full load so clear db first
    cursor.execute("""
                   TRUNCATE TABLE try_dag.employee;
                   """)
    for _,row in df.iterrows():
        cursor.execute("""
        INSERT INTO try_dag.employee (department, avg_salary)
        VALUES (%s, %s)
        """, (row["department"], row["avg_salary"]))
        
    conn.commit()
    cursor.close()
    conn.close()