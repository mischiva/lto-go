import psycopg2
from psycopg2.extras import RealDictCursor

def connectDatabase():
    return psycopg2.connect(host="localhost", port="5432", dbname="lto-go", user="postgres", password="useruser")

def getViolations(search="", tv_type="", tv_status=""):
    query = """
        SELECT 
            tv.tv_id,
            tv.tv_type,
            tv.tv_status,
            tv.tv_date,
            tv.tv_fine,
            tv.app_officer,
            tv.tv_street,
            tv.tv_barangay,
            tv.tv_city,
            tv.tv_region,
            tv.plate_no,
            tv.license_no,
            d.last_name || ', ' || d.first_name || ' ' || LEFT(COALESCE(d.middle_name, ''), 1) || '.' AS driver
        FROM traffic_vio tv
        LEFT JOIN driver d ON tv.license_no = d.license_no
        WHERE 0=0
    """
    params = []

    if search:
        query += " AND (d.last_name ILIKE %s OR d.first_name ILIKE %s OR tv.plate_no ILIKE %s OR tv.license_no ILIKE %s)"
        params += [f"%{search}%", f"%{search}%", f"%{search}%", f"%{search}%"]

    if tv_type and tv_type != "All types":
        query += " AND tv.tv_type = %s"
        params.append(tv_type)

    if tv_status and tv_status != "All statuses":
        query += " AND tv.tv_status = %s"
        params.append(tv_status)

    query += " ORDER BY tv.tv_date DESC, tv.tv_id DESC"

    with connectDatabase() as server:
        with server.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params)
            return cur.fetchall()

def getViolation(tv_id):
    with connectDatabase() as server:
        with server.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM traffic_vio WHERE tv_id = %s", (tv_id,))
            return cur.fetchone()

def addViolation(data: dict):
    with connectDatabase() as server:
        with server.cursor() as cur:
            cur.execute("""
                INSERT INTO traffic_vio (
                    tv_id, tv_type, tv_status, tv_date, tv_fine, app_officer, 
                    tv_street, tv_barangay, tv_city, tv_region, plate_no, license_no
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                data["tv_id"], data["tv_type"], data["tv_status"], 
                data["tv_date"], data["tv_fine"], data["app_officer"], 
                data["tv_street"], data["tv_barangay"], data["tv_city"], 
                data["tv_region"], data["plate_no"], data["license_no"]
            ))
        server.commit()

def updateViolation(old_tv_id, data: dict):
    with connectDatabase() as server:
        with server.cursor() as cur:
            cur.execute("""
                UPDATE traffic_vio SET
                    tv_id=%s, tv_type=%s, tv_status=%s, tv_date=%s, tv_fine=%s, app_officer=%s, 
                    tv_street=%s, tv_barangay=%s, tv_city=%s, tv_region=%s, plate_no=%s, license_no=%s
                WHERE tv_id=%s
            """, (
                data["tv_id"], data["tv_type"], data["tv_status"], 
                data["tv_date"], data["tv_fine"], data["app_officer"], 
                data["tv_street"], data["tv_barangay"], data["tv_city"], 
                data["tv_region"], data["plate_no"], data["license_no"], 
                old_tv_id
            ))
        server.commit()

def deleteViolation(tv_id):
    with connectDatabase() as server:
        with server.cursor() as cur:
            cur.execute("DELETE FROM traffic_vio WHERE tv_id = %s", (tv_id,))
        server.commit()
