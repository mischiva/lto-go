import psycopg2
from psycopg2.extras import RealDictCursor


def connectDatabase():
    return psycopg2.connect(host="localhost", port="5432", dbname="lto-go", user="postgres", password="useruser")


def _fetch_all(query, params=()):
    with connectDatabase() as server:
        with server.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params)
            return cur.fetchall()


def _table_exists(table_name):
    with connectDatabase() as server:
        with server.cursor() as cur:
            cur.execute(
                "SELECT 1 FROM information_schema.tables WHERE table_schema = 'public' AND table_name = %s",
                (table_name,),
            )
            return cur.fetchone() is not None


# 1. View all registered drivers filtered by license type, status, age range, and sex.
def get_registered_drivers(search="", license_type="", license_status="", min_age=None, max_age=None, sex=""):
    query = "SELECT license_no, last_name, first_name, middle_name, suffix, dob, DATE_PART('year', AGE(dob))::int AS age, sex, license_type, license_status, license_issued, license_expire FROM driver"
    params = []
    clauses = []

    if search:
        clauses.append("(LOWER(license_no) LIKE LOWER(%s) OR LOWER(CONCAT(last_name, ', ', first_name)) LIKE LOWER(%s) OR LOWER(CONCAT(first_name, ' ', last_name)) LIKE LOWER(%s))")
        params += [f"%{search}%", f"%{search}%", f"%{search}%"]
    if license_type:
        clauses.append("license_type = %s")
        params.append(license_type)
    if license_status:
        clauses.append("license_status = %s")
        params.append(license_status)
    if min_age is not None:
        clauses.append("DATE_PART('year', AGE(dob))::int >= %s")
        params.append(min_age)
    if max_age is not None:
        clauses.append("DATE_PART('year', AGE(dob))::int <= %s")
        params.append(max_age)
    if sex:
        clauses.append("sex = %s")
        params.append(sex)

    if clauses:
        query += " WHERE " + " AND ".join(clauses)
    query += " ORDER BY last_name, first_name"
    return _fetch_all(query, params)


# 2. View all vehicles owned by a given driver.
def get_vehicles_by_driver(search="", license_no=""):
    query = """
        SELECT
            d.license_no,
            d.last_name,
            d.first_name,
            d.middle_name,
            v.plate_no,
            v.vehicle_type AS v_type,
            v.make AS v_make,
            v.model AS v_model,
            v.color AS v_color,
            v.year AS v_year,
            v.engine_no,
            v.chassis_no
        FROM driver d
        JOIN vehicle v ON d.license_no = v.owner_id
    """
    params = []
    clauses = []

    if license_no:
        clauses.append("license_no = %s")
        params.append(license_no)
    elif search:
        clauses.append("(LOWER(d.license_no) LIKE LOWER(%s) OR LOWER(CONCAT(d.last_name, ', ', d.first_name)) LIKE LOWER(%s) OR LOWER(CONCAT(d.first_name, ' ', d.last_name)) LIKE LOWER(%s) OR LOWER(v.plate_no) LIKE LOWER(%s))")
        params += [f"%{search}%", f"%{search}%", f"%{search}%", f"%{search}%"]

    if clauses:
        query += " WHERE " + " AND ".join(clauses)
    query += " ORDER BY v.plate_no"
    return _fetch_all(query, params)


# 3. View all vehicles with expired registrations as of a given date.
def get_vehicles_with_expired_registrations(as_of_date):
    query = """
        SELECT
            v.plate_no,
            v.vehicle_type AS v_type,
            v.make AS v_make,
            v.model AS v_model,
            v.color AS v_color,
            v.year AS v_year,
            v.engine_no,
            v.chassis_no,
            r.reg_no,
            r.expiry_date AS exp_date,
            r.status
        FROM vehicle v
        JOIN registration r ON r.plate_no = v.plate_no
        WHERE r.expiry_date < %s
    """
    params = [as_of_date]

    query += " ORDER BY exp_date, v.plate_no"
    return _fetch_all(query, params)


# 4. View all drivers with expired or suspended licenses.
def get_expired_or_suspended_drivers(search=""):
    query = "SELECT license_no, last_name, first_name, middle_name, suffix, dob, DATE_PART('year', AGE(dob))::int AS age, sex, license_type, license_status, license_issued, license_expire FROM driver WHERE (license_status='Expired' OR license_status='Suspended')"
    params = []
    clauses = []

    if search:
        clauses.append("(LOWER(license_no) LIKE LOWER(%s) OR LOWER(CONCAT(last_name, ', ', first_name)) LIKE LOWER(%s) OR LOWER(CONCAT(first_name, ' ', last_name)) LIKE LOWER(%s))")
        params += [f"%{search}%", f"%{search}%", f"%{search}%"]

    if clauses:
        query += " AND " + " AND ".join(clauses)
    query += " ORDER BY last_name, first_name"
    return _fetch_all(query, params)


# 5. View all traffic violations committed by a given driver within a date range.
def get_violations_by_driver(search="", start_date=None, end_date=None):
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
        WHERE 1=1
    """
    params = []

    if search:
        query += " AND (d.last_name ILIKE %s OR d.first_name ILIKE %s OR tv.plate_no ILIKE %s OR tv.license_no ILIKE %s)"
        params += [f"%{search}%", f"%{search}%", f"%{search}%", f"%{search}%"]

    if start_date is not None and end_date is not None:
        query += " AND tv.tv_date BETWEEN %s AND %s"
        params.append(start_date)
        params.append(end_date)

    query += " ORDER BY tv.tv_date DESC, tv.tv_id DESC"
    return _fetch_all(query, params)


# 6. View the total number of violations per violation type for a given year.
def get_violation_totals_by_year(year, tv_type=""):
    query = """
        SELECT
            tv.license_no,
            tv.tv_type,
            COUNT(*) AS violation_count
        FROM traffic_vio tv
        WHERE EXTRACT(YEAR FROM tv.tv_date) = %s
    """
    params = [year]

    if tv_type:
        query += " AND tv.tv_type = %s"
        params.append(tv_type)

    query += " GROUP BY tv.license_no, tv.tv_type ORDER BY violation_count DESC, tv.license_no"
    return _fetch_all(query, params)


# 7. View all vehicles involved in violations within a given city or region.
def get_vehicles_in_violations(city_or_region="", search="", tv_type=""):
    pass