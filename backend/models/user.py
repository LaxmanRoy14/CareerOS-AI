from database.db import get_connection


class User:

    @staticmethod
    def get_user_by_email(email):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        return user

    @staticmethod
    def create_user(full_name, email, password):
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            INSERT INTO users (full_name, email, password)
            VALUES (%s, %s, %s)
        """

        cursor.execute(query, (full_name, email, password))
        conn.commit()

        cursor.close()
        conn.close()