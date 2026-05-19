import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os

# this file sets up database when no database is initialized yet
# this part is for the constants (db name is lto-go, user uses postgres, useruser as password, and localhost settings)
DB_NAME = "lto-go"
USER = "postgres"
PASSWORD = "useruser"
HOST = "localhost"
PORT = "5432"

# function to create the database if not exists
def create_database():
    print(f"Connecting to default 'postgres' database to check for '{DB_NAME}'...")
    conn = psycopg2.connect(host=HOST, port=PORT, dbname="postgres", user=USER, password=PASSWORD) # connect to default postgres database
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor() # create a cursor
    
    cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (DB_NAME,))
    exists = cur.fetchone() # checks to see if there is existing database named lto-go
    
    if not exists: # if no database named lto-go exists, create it
        print(f"Database '{DB_NAME}' does not exist. Creating it now...")
        cur.execute(f'CREATE DATABASE "{DB_NAME}"') # !! EXECUTES SQL STATEMENT !!
        print("Database created successfully.")
    else: # if database exists then no need to create new database
        print(f"Database '{DB_NAME}' already exists.")
        
    cur.close()
    conn.close()

def setup_schema_and_data():
    # this function is to set up the example database (50 minimum required)
    print(f"Connecting to '{DB_NAME}' database to set up tables...")
    conn = psycopg2.connect(host=HOST, port=PORT, dbname=DB_NAME, user=USER, password=PASSWORD)
    cur = conn.cursor() # similar logic to previous, just connects to postgres and uses cursor

    # create tables (but first delete tables if existing to make sure everything is fresh)
    print("Creating tables...")
    cur.execute("""
        DROP TABLE IF EXISTS traffic_vio CASCADE;
        DROP TABLE IF EXISTS registration CASCADE;
        DROP TABLE IF EXISTS vehicle CASCADE;
        DROP TABLE IF EXISTS driver CASCADE;
        DROP TABLE IF EXISTS driver_address CASCADE;
        DROP TABLE IF EXISTS app_users CASCADE;

        CREATE TABLE app_users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        );

        CREATE TABLE driver (
            license_no VARCHAR(13) PRIMARY KEY,
            last_name VARCHAR NOT NULL,
            first_name VARCHAR NOT NULL,
            middle_name VARCHAR,
            suffix VARCHAR(10),
            dob DATE NOT NULL,
            sex CHAR(1) NOT NULL CHECK (sex in ('M', 'F')),
            license_type VARCHAR NOT NULL,
            license_status VARCHAR NOT NULL,
            license_issued DATE NOT NULL,
            license_expire DATE NOT NULL,
            CONSTRAINT chk_dob CHECK (dob < CURRENT_DATE),
            CONSTRAINT chk_license_expire CHECK (license_expire > license_issued)
        );
        
        CREATE TABLE driver_address (
            license_no VARCHAR(13) REFERENCES driver(license_no) ON DELETE CASCADE,
            d_address VARCHAR NOT NULL,
            d_street VARCHAR NOT NULL,
            d_barangay VARCHAR NOT NULL,
            d_city VARCHAR NOT NULL,
            d_region VARCHAR NOT NULL,
            PRIMARY KEY (license_no, d_address)
        );

        CREATE TABLE vehicle (
            plate_no VARCHAR PRIMARY KEY,
            engine_no VARCHAR NOT NULL,
            chassis_no VARCHAR NOT NULL,
            vehicle_type VARCHAR NOT NULL,
            make VARCHAR NOT NULL,
            model VARCHAR NOT NULL,
            year INTEGER NOT NULL,
            color VARCHAR NOT NULL,
            owner_id VARCHAR(13) REFERENCES driver(license_no) ON DELETE SET NULL
        );

        CREATE TABLE registration (
            reg_no VARCHAR PRIMARY KEY,
            plate_no VARCHAR REFERENCES vehicle(plate_no) ON DELETE CASCADE,
            reg_date DATE NOT NULL,
            expiry_date DATE NOT NULL,
            status VARCHAR NOT NULL,
            CONSTRAINT chk_expiry_date CHECK (expiry_date > reg_date)
        );

        CREATE TABLE traffic_vio(
            tv_id VARCHAR PRIMARY KEY,
            tv_type VARCHAR NOT NULL,
            tv_status VARCHAR NOT NULL,
            tv_date DATE NOT NULL,
            tv_fine INT NOT NULL,
            app_officer VARCHAR,
            tv_street VARCHAR NOT NULL,
            tv_barangay VARCHAR NOT NULL,
            tv_city VARCHAR NOT NULL,
            tv_region VARCHAR NOT NULL,
            plate_no VARCHAR REFERENCES vehicle(plate_no) ON DELETE SET NULL,
            license_no VARCHAR(13) REFERENCES driver(license_no) ON DELETE SET NULL
        )
    """)
    conn.commit()

    # load and execute mock data from SQL files if they exist
    sql_files = {
        "user_sql.sql": "app_users",
        "driver_insert.sql": "driver",
        "vehicle_insert.sql": "vehicle",
        "registration_insert.sql": "registration",
        "violation_insert.sql": "traffic_vio"
    }

    for file_name, table_name in sql_files.items():
        if os.path.exists(file_name):
            print(f"Loading data from {file_name} into {table_name} table...")
            with open(file_name, 'r', encoding='utf-8') as f:
                sql_content = f.read()
                try:
                    cur.execute(sql_content)
                    conn.commit()
                    print(f"Successfully loaded {file_name}.")
                except Exception as e:
                    print(f"Error loading {file_name}: {e}")
                    conn.rollback()
        else:
            print(f"Warning: {file_name} not found. Skipping data insertion for {table_name}.")

    cur.close()
    conn.close()
    print("Setup complete! Your database is ready.")

if __name__ == "__main__":
    try:
        create_database()
        setup_schema_and_data()
    except Exception as e:
        print(f"An error occurred: {e}")
