import sqlite3

#Print sql database to console
def print_all_data(db_file):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Query all data from all relevant tables (you can modify the table name as needed)
    tables = ["object_tracking_runs", "frames", "tracks", "frame_tracks"]  # List of table names
    for table in tables:
        print(f"Data from {table}:")

        # Query all columns from the current table
        cursor.execute(f"SELECT * FROM {table}")

        # Fetch all rows from the result
        rows = cursor.fetchall()

        # Print column names
        column_names = [description[0] for description in cursor.description]
        print("Columns:", column_names)

        # Print all rows
        for row in rows:
            print(row)
        print("-" * 50)  # Print separator between tables

    # Close the connection
    conn.close()

#print columns
db_file = "object_tracking_sql.db"  # Your database file
con = sqlite3.connect(db_file)
cursor = con.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())

print_all_data(db_file)