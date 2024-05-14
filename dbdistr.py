import mysql.connector


def get_account_by_gl_contra_code(gl_contra_code):
    """
    Retrieves the account based on the GL Contra Code from the 'codes' table.
    """
    try:
        # Establish a database connection (replace with your actual credentials)
        db = mysql.connector.connect(
            host='',
            user='',
            password='',
            database='contracode'
        )
        cursor = db.cursor()

        # Execute the SQL query
        query = f"SELECT Account  FROM codes WHERE GL_Contra_Code = '{
            gl_contra_code}'"
        cursor.execute(query)
        account = cursor.fetchone()  # Retrieve the first result

        # Clean up
        cursor.close()
        db.close()

        # Return the account or None if not found
        return account[0] if account else None
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return None


# print(get_account_by_gl_contra_code("150004>15006"))
