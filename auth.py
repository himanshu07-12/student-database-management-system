import random
import string
from database import get_connection

def signup(username,password):
    mydb = get_connection()
    mycursor = mydb.cursor()
    N = 5
    login_id = ''.join(random.choices(string.digits, k=N))
    query = """
    INSERT INTO user_details(login_id, username, password)
    VALUES(%s, %s, %s)
    """
    mycursor.execute(query, (login_id, username, password))
    mydb.commit()
    mycursor.close()
    mydb.close()
    return login_id

def login(login_id, username, password):

    mydb = get_connection()
    mycursor = mydb.cursor()

    query = """
    SELECT *
    FROM user_details
    WHERE login_id=%s
    AND username=%s
    AND password=%s
    """

    mycursor.execute(query, (login_id, username, password))

    user = mycursor.fetchone()

    if user:

        history_query = """
        INSERT INTO log_details
        VALUES(%s,%s,SYSDATE(),NOW())
        """

        mycursor.execute(history_query, (login_id, username))
        mydb.commit()

        mycursor.close()
        mydb.close()

        return True

    mycursor.close()
    mydb.close()

    return False