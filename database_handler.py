import sqlite3
from sqlite3 import Error


class DatabaseHandler:
    def __init__(self, db_file):
        """Initialize the database handler with a database file."""
        self.db_file = db_file
        self.conn = None

    def connect(self):
        """Create a connection to the SQLite database."""
        try:
            self.conn = sqlite3.connect(self.db_file)
            self.conn.execute('PRAGMA foreign_keys = ON;')  # Enable foreign key support
            print(f"Connected to database {self.db_file}")
        except Error as e:
            print(f"Error connecting to database: {e}")

    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            print("Connection closed.")

    def create_tables(self):
        """Create tables if they don't exist."""
        try:
            cursor = self.conn.cursor()

            # Create object_tracking_runs table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS object_tracking_runs (
                    id INTEGER PRIMARY KEY,                     -- Auto-incrementing primary key
                    path_source TEXT,                           -- Path or source URL to the video
                    path_output TEXT,                           -- Path or output URL to the video
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP   -- Timestamp
                );
            """)

            # Create frames table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS frames (
                    id INTEGER PRIMARY KEY,                     -- Auto-incrementing primary key
                    frame_number INTEGER NOT NULL,              -- Frame number in the video
                    object_tracking_runs_id INTEGER NOT NULL,   -- Foreign key to object_tracking_runs table
                    FOREIGN KEY (object_tracking_runs_id) REFERENCES object_tracking_runs(id) ON DELETE CASCADE
                );
            """)

            # Create tracks table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tracks (
                    id INTEGER PRIMARY KEY,                     -- Auto-incrementing primary key
                    object_id INTEGER NOT NULL                  -- Track ID (track_id)
                );
            """)

            # Create frame_tracks table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS frame_tracks (
                    id INTEGER PRIMARY KEY,                     -- Auto-incrementing primary key
                    frame_id INTEGER NOT NULL,                  -- Foreign key to frames table
                    track_id INTEGER NOT NULL,                  -- Foreign key to tracks table
                    probability REAL NOT NULL,                  -- Confidence of the detection
                    location_x REAL NOT NULL,                   -- coordinate of the object's location
                    location_y REAL NOT NULL,                   -- Y-coordinate of the object's location
                    location_width REAL NOT NULL,               -- Width of the bounding box
                    location_height REAL NOT NULL,              -- Height of the bounding box
                    FOREIGN KEY (frame_id) REFERENCES frames(id) ON DELETE CASCADE,
                    FOREIGN KEY (track_id) REFERENCES tracks(id) ON DELETE CASCADE
                );
            """)

            # Commit changes
            self.conn.commit()
            print("Tables created successfully.")
        except Error as e:
            print(f"Error creating tables: {e}")

    def insert_object_tracking_run(self, path_source, path_output=None):
        """Insert a new object tracking run into the object_tracking_runs table."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO object_tracking_runs (path_source, path_output)
                VALUES (?, ?);
            """, (path_source, path_output))
            self.conn.commit()
            print(f"Object tracking run inserted with source: {path_source}")
            return cursor.lastrowid  # Return the id of the last inserted object_tracking_run
        except Error as e:
            print(f"Error inserting object tracking run: {e}")
            return None

    def insert_frame(self, frame_number, object_tracking_runs_id):
        """Insert a new frame into the frames table."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO frames (frame_number, object_tracking_runs_id)
                VALUES (?, ?);
            """, (frame_number, object_tracking_runs_id))
            self.conn.commit()
            print(f"Frame {frame_number} inserted successfully.")
            return cursor.lastrowid  # Return the id of the last inserted frame
        except Error as e:
            print(f"Error inserting frame: {e}")
            return None

    def insert_track(self, object_id):
        """Insert a new track into the tracks table."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO tracks (object_id)
                VALUES (?);
            """, (object_id,))
            self.conn.commit()
            print(f"Track inserted for object {object_id}.")
            return cursor.lastrowid  # Return the id of the last inserted track
        except Error as e:
            print(f"Error inserting track: {e}")
            return None

    def insert_frame_track(self, frame_id, track_id, probability, location_x, location_y, location_width,
                           location_height):
        """Insert data into the frame_tracks table."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO frame_tracks (frame_id, track_id, probability, location_x, location_y, location_width, location_height)
                VALUES (?, ?, ?, ?, ?, ?, ?);
            """, (frame_id, track_id, probability, location_x, location_y, location_width, location_height))
            self.conn.commit()
            print(f"Frame track inserted for frame {frame_id} and track {track_id}.")
        except Error as e:
            print(f"Error inserting frame track: {e}")
