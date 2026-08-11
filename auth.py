from database import get_connection
from werkzeug.security import check_password_hash


def login(login_id, username, password):

    mydb = get_connection()
    mycursor = mydb.cursor()

    query = """
    SELECT LOGIN_ID, USERNAME, PASSWORD
    FROM user_details
    WHERE LOGIN_ID=%s
    AND USERNAME=%s
    """

    mycursor.execute(
        query,
        (login_id, username)
    )

    user = mycursor.fetchone()

    if user:

        stored_password = user[2]

        if check_password_hash(
            stored_password,
            password
        ):

            history_query = """
            INSERT INTO log_details
            VALUES(%s,%s,SYSDATE(),NOW())
            """

            mycursor.execute(
                history_query,
                (login_id, username)
            )

            mydb.commit()

            mycursor.close()
            mydb.close()

            return True

    mycursor.close()
    mydb.close()

    return False