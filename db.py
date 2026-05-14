import psycopg2
from psycopg2.extras import RealDictCursor
# this python file serves as the database for our lto-go app. uses psycopg2, a python library that connects postgresql and python files


# setup changes depending on user's db configuration, for our case host is localhost, default port, dbname, user, and password

# function to get connection from postgres server, with these parameters
# returns a psycopg2 connection object
def connectDatabase(): # gets a connection from postgres server
    return psycopg2.connect(host="localhost", port="5432", dbname="lto-go", user="postgres", password="useruser")

# function to get drivers data where default are blank strings
def getDrivers(search="", license_type="", license_status="", sex=""):
    # this is the default sql query to get all drivers data without any search parameters
    # || is concat in postgresql, and LEFT(middle_name, 1) gets the first letter of middle name
    query = """
        SELECT
            license_no,
            last_name || ', ' || first_name || ' ' || LEFT(middle_name, 1) || '.' AS full_name,
            dob,
            DATE_PART('year', AGE(dob))::int AS age,
            sex,
            license_type,
            license_status,
            license_expire
        FROM driver
        WHERE 0=0
    """
    params = []

    if search: # if search is not empty
        # PostgreSQL can't use SELECT aliases in WHERE, so we repeat the full_name expression
        query += " AND (license_no ILIKE %s OR (last_name || ', ' || first_name || ' ' || LEFT(middle_name, 1) || '.') ILIKE %s)"
        params += [f"%{search}%", f"%{search}%"] # adds a layer of security to avoid sql injection
    if license_type: # if license_type is not empty
        query += " AND license_type = %s"
        params.append(license_type)
    if license_status: # if license_status is not empty
        query += " AND license_status = %s"
        params.append(license_status)
    if sex:
        query += " AND sex = %s"
        params.append(sex)

    query += " ORDER BY full_name"

    with connectDatabase() as server: # connects to postgres server
        with server.cursor(cursor_factory=RealDictCursor) as cur: #RealDictCursor returns objects, not lists
            cur.execute(query, params) # execute the sql query
            return cur.fetchall() # return all the data from the query (as a list of key-value pairs)

def getDriver(license_no): # only gets one driver (using license_no)
    with connectDatabase() as server: # connects to postgres server
        with server.cursor(cursor_factory=RealDictCursor) as cur: #RealDictCursor returns objects, not lists
            cur.execute("SELECT * FROM driver WHERE license_no = %s", (license_no,)) # execute the sql query
            return cur.fetchone() # return the data from the query

def addDriver(data: dict): # add driver takes a parameter of dictionary with key value pairs 
    with connectDatabase() as server:
        with server.cursor() as cur: #RealDictCursor returns objects, not lists
            cur.execute("""
                INSERT INTO driver (
                    license_no, last_name, first_name, middle_name, suffix,
                    dob, sex, license_type, license_status, license_issued, license_expire
                ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (
                data["license_no"], data["last_name"], data["first_name"],
                data["middle_name"], data["suffix"], data["dob"], data["sex"],
                data["license_type"], data["license_status"],
                data["license_issued"], data["license_expire"]
            ))
        server.commit() # saves the recently executed sql command

def updateDriver(license_no, data: dict): # updates a driver's data using license_no
    with connectDatabase() as server: # connects to postgres server
        with server.cursor() as cur: #RealDictCursor returns objects, not lists
            cur.execute("""
                UPDATE driver SET
                    last_name=%s, first_name=%s, middle_name=%s, suffix=%s,
                    dob=%s, sex=%s, license_type=%s, license_status=%s,
                    license_issued=%s, license_expire=%s
                WHERE license_no=%s
            """, (
                data["last_name"], data["first_name"], data["middle_name"],
                data["suffix"], data["dob"], data["sex"], data["license_type"],
                data["license_status"], data["license_issued"],
                data["license_expire"], license_no
            ))
        server.commit()

def deleteDriver(license_no): # deletes a driver from the database using license_no
    with connectDatabase() as server: # connects to postgres server
        with server.cursor() as cur: #RealDictCursor returns objects, not lists
            cur.execute("DELETE FROM driver WHERE license_no = %s", (license_no,)) # execute the sql query
        server.commit() # saves the recently executed sql command

# References:
# https://www.postgresql.org/docs/9.1/functions-string.html
# https://www.postgresql.org/docs/current/functions-datetime.html
# https://www.geeksforgeeks.org/python/postgresql-ilike-operator/
# https://www.psycopg.org/docs/usage.html