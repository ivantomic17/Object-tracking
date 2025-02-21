import base64
import io
import sqlite3
import matplotlib.pyplot as plt
import matplotlib
from django.http import JsonResponse
from django.shortcuts import render

def index(request):
    video_id = 1
    object_id = 1
    db_file = "C:/work/database/object_tracking_sql.db"

    if request.method == 'POST':
        video_id = int(request.POST.get('video_id', video_id))
        object_id = int(request.POST.get('object_id', object_id))

    img_base64, table_data = generate_object_curve_image(db_file, video_id, object_id)

    available_video_runs = get_available_videos(db_file)
    available_objects = get_available_objects_for_video(video_id, db_file)

    # Render the updated page
    return render(request, 'index.html', {
        'img_base64': img_base64,
        'table_data': table_data,
        'video_id': video_id,
        'object_id': object_id,
        'available_video_runs': available_video_runs,
        'available_objects': available_objects,
    })


def generate_object_curve_image(db_file, video_id, object_id):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    query = """
        SELECT ft.location_x, ft.location_y, ft.probability, f.frame_number
        FROM frame_tracks ft
        JOIN frames f ON ft.frame_id = f.id
        JOIN object_tracking_runs otr ON f.object_tracking_runs_id = otr.id
        JOIN tracks t ON ft.track_id = t.id
        WHERE otr.id = ? AND t.object_id = ?
        ORDER BY f.frame_number;
    """

    cursor.execute(query, (video_id, object_id))
    db_data = cursor.fetchall()

    if db_data:
        x_coords = [loc[0] for loc in db_data]
        y_coords = [loc[1] for loc in db_data]

        table_data = [{'x': loc[0], 'y': loc[1], 'probability': loc[2]} for loc in db_data]

        matplotlib.use('agg')
        plt.figure(figsize=(10, 6))
        plt.xlim(0, 1920)
        plt.ylim(0, 1080)
        plt.plot(x_coords, y_coords, marker='o', linestyle='-', color='b', label="Object Movement Path")
        plt.gca().invert_yaxis()
        plt.title(f"Object Movement Path (Video {video_id}, Object {object_id})")
        plt.xlabel("X Coordinate")
        plt.ylabel("Y Coordinate")
        plt.legend()

        # Save plot to a BytesIO object
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        img_base64 = base64.b64encode(img.read()).decode('utf-8')
        plt.close()
        conn.close()
        return img_base64, table_data
    else:
        conn.close()
        return None


def get_available_videos(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT id, path_source FROM object_tracking_runs")
    videos = cursor.fetchall()
    conn.close()
    return videos


def get_available_objects_for_video(video_id, db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t.object_id
        FROM frame_tracks ft
        JOIN frames f ON ft.frame_id = f.id
        JOIN tracks t ON ft.track_id = t.id
        JOIN object_tracking_runs otr ON f.object_tracking_runs_id = otr.id
        WHERE otr.id = ?
        GROUP BY t.object_id
    """, (video_id,))
    objects = cursor.fetchall()
    conn.close()
    return objects


def fetch_objects(request, video_id):
    db_file = "C:/work/database/object_tracking_sql.db"
    objects = get_available_objects_for_video(video_id, db_file)
    return JsonResponse({'objects': [{'id': obj[0], 'object_id': obj[0]} for obj in objects]})
