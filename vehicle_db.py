import psycopg2
from psycopg2.extras import RealDictCursor

def connectDatabase():
    return psycopg2.connect(host="localhost", port="5432", dbname="lto-go", user="postgres", password="useruser")

def getVehicles(search="", vehicle_type=""):
    query = """
        SELECT 
            v.plate_no, 
            v.make || ' ' || v.model AS make_model, 
            v.year, 
            v.vehicle_type AS type, 
            d.last_name || ', ' || d.first_name || ' ' || LEFT(d.middle_name, 1) || '.' AS owner,
            v.engine_no,
            v.chassis_no,
            v.make,
            v.model,
            v.color,
            v.owner_id
        FROM vehicle v
        JOIN driver d ON v.owner_id = d.license_no
        WHERE 0=0
    """
    params = []

    if search:
        query += " AND (v.plate_no ILIKE %s OR v.engine_no ILIKE %s OR d.last_name ILIKE %s OR d.first_name ILIKE %s)"
        params += [f"%{search}%", f"%{search}%", f"%{search}%", f"%{search}%"]
        
    if vehicle_type and vehicle_type != "All types":
        query += " AND v.vehicle_type = %s"
        params.append(vehicle_type)

    query += " ORDER BY v.plate_no"

    with connectDatabase() as server:
        with server.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params)
            return cur.fetchall()

def getVehicle(plate_no):
    with connectDatabase() as server:
        with server.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM vehicle WHERE plate_no = %s", (plate_no,))
            return cur.fetchone()

def addVehicle(data: dict):
    with connectDatabase() as server:
        with server.cursor() as cur:
            cur.execute("""
                INSERT INTO vehicle (
                    plate_no, engine_no, chassis_no, vehicle_type, 
                    make, model, year, color, owner_id
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                data["plate_no"], data["engine_no"], data["chassis_no"], 
                data["vehicle_type"], data["make"], data["model"], 
                data["year"], data["color"], data["owner_id"]
            ))
        server.commit()

def updateVehicle(old_plate_no, data: dict):
    with connectDatabase() as server:
        with server.cursor() as cur:
            cur.execute("""
                UPDATE vehicle SET
                    plate_no=%s, engine_no=%s, chassis_no=%s, vehicle_type=%s,
                    make=%s, model=%s, year=%s, color=%s, owner_id=%s
                WHERE plate_no=%s
            """, (
                data["plate_no"], data["engine_no"], data["chassis_no"], 
                data["vehicle_type"], data["make"], data["model"], 
                data["year"], data["color"], data["owner_id"], old_plate_no
            ))
        server.commit()

def deleteVehicle(plate_no):
    with connectDatabase() as server:
        with server.cursor() as cur:
            cur.execute("DELETE FROM vehicle WHERE plate_no = %s", (plate_no,))
        server.commit()
