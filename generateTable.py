import mysql.connector

def dump_schema(host, user, password, database, output_file='schema.sql'):
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = conn.cursor()

        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()

        with open(output_file, 'w') as f:
            for (table_name,) in tables:
                cursor.execute(f"SHOW CREATE TABLE `{table_name}`")
                create_stmt = cursor.fetchone()[1]
                f.write(f"{create_stmt};\n\n")
                print(f"Exported schema for table `{table_name}`")

        print(f"\n Schema exported to {output_file}")

    except mysql.connector.Error as err:
        print(f" Error: {err}")

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


dump_schema(
    host='localhost',
    user='root',
    password='Root123!',
    database='workbenchdb'
)
