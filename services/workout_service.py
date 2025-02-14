from db import get_connection
import datetime

def create_workout_entry(user_id, exercise, weight, reps, sets):
    """
    Creates a workout log entry in the workouts table.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        workout_date = datetime.date.today().isoformat()  # e.g., '2024-01-01'
        cursor.execute("""
            INSERT INTO workouts (user_id, exercise, weight, reps, sets, workout_date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, exercise, weight, reps, sets, workout_date))

        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        print(f"Error creating workout entry: {e}")
        return None
    finally:
        conn.close()

def get_workout_history_by_user(user_id):
    """
    Retrieves all workout entries for a given user.
    Returns a list of dictionaries.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, exercise, weight, reps, sets, workout_date
        FROM workouts
        WHERE user_id = ?
        ORDER BY workout_date ASC
    """, (user_id,))

    rows = cursor.fetchall()
    conn.close()

    workout_history = []
    for row in rows:
        workout_history.append({
            'workout_id': row[0],
            'exercise': row[1],
            'weight': row[2],
            'reps': row[3],
            'sets': row[4],
            'date': row[5]
        })
    return workout_history

def update_workout_entry(workout_id, exercise=None, weight=None, reps=None, sets=None):
    """
    Updates the specified fields of a workout entry.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Build the SQL dynamically based on which arguments are not None
    columns = []
    values = []

    if exercise is not None:
        columns.append("exercise = ?")
        values.append(exercise)
    if weight is not None:
        columns.append("weight = ?")
        values.append(weight)
    if reps is not None:
        columns.append("reps = ?")
        values.append(reps)
    if sets is not None:
        columns.append("sets = ?")
        values.append(sets)

    if columns:
        query = f"UPDATE workouts SET {', '.join(columns)} WHERE id = ?"
        values.append(workout_id)

        cursor.execute(query, tuple(values))
        conn.commit()

    conn.close()

def delete_workout_entry(workout_id):
    """
    Deletes a workout entry by ID.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM workouts WHERE id = ?", (workout_id,))
    conn.commit()
    conn.close()
