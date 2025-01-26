import sqlite3
import matplotlib.pyplot as plt

def plot_object_movement_on_canvas(db_file, video_id, object_id):
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

    # If there are any locations, plot them
    if locations:
        # Extract X and Y coordinates (x_coords and y_coords) as a list of points
        x_coords = [loc[0] for loc in locations]
        y_coords = [loc[1] for loc in locations]

        # Create a plot for the object's movement on a canvas with a resolution of 1920x1080
        plt.figure(figsize=(10, 6))  # Set figure size to give it more space

        # Set the limits of the plot to match the canvas size (1920x1080)
        plt.xlim(0, 1920)
        plt.ylim(0, 1080)

        # Plot the points on the canvas
        plt.plot(x_coords, y_coords, marker='o', linestyle='-', color='b', label="Object Movement Path")

        # Invert the y-axis to match the video coordinate system (y increases downward)
        plt.gca().invert_yaxis()

        # Add titles and labels
        plt.title(f"Object Movement Path (Video {video_id}, Object {object_id})")
        plt.xlabel("X Coordinate")
        plt.ylabel("Y Coordinate")
        plt.legend()

        # Show the plot
        plt.show()
    else:
        print(f"No locations found for video ID {video_id}, object ID {object_id}.")

    # Close the connection
    conn.close()

# Example usage
db_file = "object_tracking_sql.db"  # Your database file
video_id = 4                    # Video ID
object_id = 5                    # Object ID (from the tracks table)
plot_object_movement_on_canvas(db_file, video_id, object_id)
plot_object_movement_on_canvas(db_file, video_id, 9)
