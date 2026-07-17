import psycopg2
from psycopg2.extras import RealDictCursor
import os

def get_conn():
    
    return psycopg2.connect(
        host=os.getenv("WAREHOUSE_HOST"),
        port=os.getenv("WAREHOUSE_PORT"),
        dbname=os.getenv("WAREHOUSE_DATABASE"),
        user=os.getenv("WAREHOUSE_USER"),
        password=os.getenv("WAREHOUSE_PASSWORD")
    )
    
def close_conn (conn):
    conn.close()

def get_file_meta(id,conn):
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    cur.execute("""
                SELECT file_id, last_modified, status
                FROM metadata.file_status
                WHERE file_id = %s
                """,(id,))
    
    row = cur.fetchone()
    cur.close()
    return row
    
def import_new_file(conn,status:str,file,file_location):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT 1
            FROM metadata.file_status
            WHERE file_id = %s
        """, (file["id"],))

        if cur.fetchone() is None:
            cur.execute("""
                INSERT INTO metadata.file_status(file_id, filename, file_location, status, last_modified)
                VALUES (%s, %s,%s,%s,%s)
            """, (file["id"], file["name"],file_location,status,file["last_modified"]))
        else:
            cur.execute("""
                UPDATE metadata.file_status
                SET status = %s,
                    last_modified = %s,
                    file_location = %s,
                    filename = %s
                WHERE file_id = %s
            """, (status, file["last_modified"], file_location, file["name"],file["id"]))

    conn.commit()
    
def get_imported_file(conn):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
                SELECT file_id, filename, file_location
                FROM metadata.file_status
                WHERE status = 'extracted';
            """)
        
        result = cur.fetchall()
    return result

def update_file_status(conn, id, status):
    with conn.cursor() as cur:
        cur.execute("""
                    UPDATE metadata.file_status
                    SET status = %s
                    WHERE file_id = %s
                """, (status,id)
            )
        
    conn.commit()