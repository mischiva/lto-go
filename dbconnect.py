import psycopg2
conn_params = {
    "host": "127.0.0.1",
    "port": "5432",
    "user": "postgres",
    "password": "030302",
    "database": "driver",
    "sslmode": "require"
}

# READ TABLE
def read_table(table_name):
    try:
        conn = psycopg2.connect(**conn_params)
        cur = conn.cursor()
        cur.execute("SELECT * FROM {tblname}")
        rows = cur.fetchall()
        colnames = [desc[0] for desc in cur.description]

        results = []
        for row in rows:
            # Convert each line to a dictionary
            row_dict = {colnames[i]: row[i] for i in range(len(row))}
            results.append(row_dict)

        cur.close()
        conn.close()
        return results
    except psycopg2.Error as e:
        print("Error running query:", e)

# ADD
def insert_into_table(table_name, data):
    try:
        conn = psycopg2.connect(**conn_params)
        cur = conn.cursor()
        
        value_string = ', '.join(['%s' for _ in range(len(data[0]))])
        sql = "INSERT INTO {tblname} VALUES ({value_string})"
        cur.executemany(sql, data)
        conn.commit()

        cur.close()
        conn.close()

    except psycopg2.Error as e:
        print("Error query:", e)
