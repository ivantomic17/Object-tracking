import sqlite3

def get_object_locations_by_object_id(db_file, video_id, object_id):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # SQL query to get the locations for the given video and object_id
    query = """
        SELECT ft.location_x, ft.location_y, f.frame_number
        FROM frame_tracks ft
        JOIN frames f ON ft.frame_id = f.id
        JOIN object_tracking_runs otr ON f.object_tracking_runs_id = otr.id
        JOIN tracks t ON ft.track_id = t.id
        WHERE otr.id = ? AND t.object_id = ?
        ORDER BY f.frame_number;
    """

    # Execute the query with the video_id and object_id as parameters
    cursor.execute(query, (video_id, object_id))

    # Fetch all the rows from the result
    locations = cursor.fetchall()

    # Debugging: Check how many rows are returned
    print(f"Total locations found for object_id {object_id} in video {video_id}: {len(locations)}")

    # Print the locations
    if locations:
        print(f"Locations for video ID {video_id}, object ID {object_id}:")
        for loc in locations:
            print(f"Frame {loc[2]}: Location (X: {loc[0]}, Y: {loc[1]})")
    else:
        print(f"No locations found for video ID {video_id}, object ID {object_id}.")

    # Close the connection
    conn.close()

# Example usage
db_file = "object_tracking_sql.db"  # Your database file
video_id = 4                    # Video ID
object_id = 3                    # Object ID (from the tracks table)
get_object_locations_by_object_id(db_file, video_id, object_id)
