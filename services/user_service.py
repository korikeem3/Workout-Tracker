from db import get_connection

def create_user(username,password):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (username,password)
            VALUES (?,?)
        """, (username, password))

        conn.commit()
        user_id = cursor.lastrowid
        return user_id
    except Exception as e:
        print(f"Error creating user {e}")
        return None
    finally:
        conn.close()

def get_user_by_username(username):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, username, password FROM users
        WHERE username = ?
    """, (username,))

    row = cursor.fetchone()
    conn.close()

    if row:
        return{
            'id': row[0],
            'username':row[1],
            'password':row[2]
        }
    return None

def delete_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?",(user_id,))
    conn.commit()
    conn.close()

def update_user_password(user_id, new_password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE users
        SET password = ?
        WHERE id = ?
    """, (new_password,user_id))

    conn.commit()
    conn.close()