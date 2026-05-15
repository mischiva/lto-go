import psycopg2
from psycopg2.extras import RealDictCursor


def connectDatabase():
    return psycopg2.connect(host="localhost", port="5432", dbname="lto-go", user="postgres", password="useruser")


def getRegistrations(search="", status=""):
    query = """
        SELECT
            r.reg_no,
            r.plate_no,
            r.reg_date,
            r.expiry_date,
            r.status,
            v.make || ' ' || v.model AS vehicle_name,
            d.last_name || ', ' || d.first_name || ' ' || LEFT(COALESCE(d.middle_name, ''), 1) || '.' AS owner
        FROM registration r
        JOIN vehicle v ON r.plate_no = v.plate_no
        JOIN driver d ON v.owner_id = d.license_no
        WHERE 0=0
    """
    params = []

    if search:
        query += " AND (r.reg_no ILIKE %s OR r.plate_no ILIKE %s OR v.make ILIKE %s OR v.model ILIKE %s OR d.last_name ILIKE %s OR d.first_name ILIKE %s)"
        params += [f"%{search}%", f"%{search}%", f"%{search}%", f"%{search}%", f"%{search}%", f"%{search}%"]

    if status and status != "All statuses":
        query += " AND r.status = %s"
        params.append(status)

    query += " ORDER BY r.reg_date DESC, r.reg_no"

    with connectDatabase() as server:
        with server.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params)
            return cur.fetchall()


def getRegistration(reg_no):
    with connectDatabase() as server:
        with server.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM registration WHERE reg_no = %s", (reg_no,))
            return cur.fetchone()


def getRegistrationByPlate(plate_no):
    with connectDatabase() as server:
        with server.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM registration WHERE plate_no = %s", (plate_no,))
            return cur.fetchone()


def addRegistration(data: dict):
    with connectDatabase() as server:
        with server.cursor() as cur:
            cur.execute(
                """
                INSERT INTO registration (
                    reg_no, plate_no, reg_date, expiry_date, status
                ) VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    data["reg_no"],
                    data["plate_no"],
                    data["reg_date"],
                    data["expiry_date"],
                    data["status"],
                ),
            )
        server.commit()


def updateRegistration(old_reg_no, data: dict):
    with connectDatabase() as server:
        with server.cursor() as cur:
            cur.execute(
                """
                UPDATE registration SET
                    reg_no=%s,
                    plate_no=%s,
                    reg_date=%s,
                    expiry_date=%s,
                    status=%s
                WHERE reg_no=%s
                """,
                (
                    data["reg_no"],
                    data["plate_no"],
                    data["reg_date"],
                    data["expiry_date"],
                    data["status"],
                    old_reg_no,
                ),
            )
        server.commit()


def deleteRegistration(reg_no):
    with connectDatabase() as server:
        with server.cursor() as cur:
            cur.execute("DELETE FROM registration WHERE reg_no = %s", (reg_no,))
        server.commit()
