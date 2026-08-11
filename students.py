from database import get_connection

def insert_student(adm, first, last, roll, mobile):

    mydb = get_connection()
    mycursor = mydb.cursor()

    # Check Admission Number
    query = "SELECT admno FROM student WHERE admno = %s"
    mycursor.execute(query, (adm,))
    if mycursor.fetchone():
        mycursor.close()
        mydb.close()
        return False, "Admission Number already exists"

    # Check Roll Number
    query = "SELECT roll FROM student WHERE roll = %s"
    mycursor.execute(query, (roll,))
    if mycursor.fetchone():
        mycursor.close()
        mydb.close()
        return False, "Roll Number already exists"

    # Validate Mobile Number
    if not str(mobile).isdigit() or len(str(mobile)) != 10:
        mycursor.close()
        mydb.close()
        return False, "Mobile Number should be exactly 10 digits"

    # Insert Student
    query = """
    INSERT INTO student(ADMNO, FNAME, LNAME, ROLL, MOBNO)
    VALUES(%s,%s,%s,%s,%s)
    """

    mycursor.execute(query, (adm, first, last, roll, mobile))
    mydb.commit()

    mycursor.close()
    mydb.close()

    return True, "Student Added Successfully"


def delete_student(adm):
    mydb = get_connection()
    mycursor = mydb.cursor()

    query = '''SELECT admno FROM student WHERE admno = %s'''
    mycursor.execute(query, (adm,))
    student = mycursor.fetchone()

    if not student:
        mycursor.close()
        mydb.close()
        return False, "Student Not Found"

    query = '''DELETE FROM student WHERE admno = %s'''
    mycursor.execute(query, (adm,))
    mydb.commit()

    mycursor.close()
    mydb.close()

    return True, "Student Deleted Successfully"


def update_student(adm, fname, lname, roll, mobno):

    mydb = get_connection()
    mycursor = mydb.cursor()

    # Check if student exists
    query = """
    SELECT ADMNO
    FROM student
    WHERE ADMNO=%s
    """

    mycursor.execute(query, (adm,))

    if not mycursor.fetchone():
        mycursor.close()
        mydb.close()
        return False, "Student not found"

    # Check duplicate roll number
    query = """
    SELECT ADMNO
    FROM student
    WHERE ROLL=%s
    AND ADMNO!=%s
    """

    mycursor.execute(query, (roll, adm))

    if mycursor.fetchone():
        mycursor.close()
        mydb.close()
        return False, "Roll Number already exists"

    # Validate mobile number
    if not str(mobno).isdigit() or len(str(mobno)) != 10:
        mycursor.close()
        mydb.close()
        return False, "Mobile Number must contain exactly 10 digits"

    # Update
    query = """
    UPDATE student

    SET
        FNAME=%s,
        LNAME=%s,
        ROLL=%s,
        MOBNO=%s

    WHERE ADMNO=%s
    """

    mycursor.execute(
        query,
        (fname, lname, roll, mobno, adm)
    )

    mydb.commit()

    mycursor.close()
    mydb.close()

    return True, "Student Updated Successfully"

    


def view_students():
    mydb = get_connection()
    mycursor = mydb.cursor(dictionary=True)

    query = """
    SELECT 
    ADMNO as admno,
    FNAME as fname,
    LNAME as lname,
    ROLL as roll,
    MOBNO as mobno
    FROM student
    """

    mycursor.execute(query)

    students = mycursor.fetchall()

    mycursor.close()
    mydb.close()

    return students

def search_student(keyword):

    mydb = get_connection()
    mycursor = mydb.cursor(dictionary=True)

    query = """
    SELECT
        ADMNO AS admno,
        FNAME AS fname,
        LNAME AS lname,
        ROLL AS roll,
        MOBNO AS mobno
    FROM student
    WHERE
        ADMNO=%s
        OR ROLL=%s
    """

    mycursor.execute(query, (keyword, keyword))

    student = mycursor.fetchall()

    mycursor.close()
    mydb.close()

    return student

def get_student(adm):

    mydb = get_connection()
    mycursor = mydb.cursor(dictionary=True)

    query = """
    SELECT
        ADMNO AS admno,
        FNAME AS fname,
        LNAME AS lname,
        ROLL AS roll,
        MOBNO AS mobno
    FROM student
    WHERE ADMNO=%s
    """

    mycursor.execute(query,(adm,))

    student=mycursor.fetchone()

    mycursor.close()
    mydb.close()

    return student

def get_dashboard_stats():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM student")
    student_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM user_details")
    user_count = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return student_count, user_count

def get_recent_students():

    mydb = get_connection()
    mycursor = mydb.cursor(dictionary=True)

    query = """
    SELECT
        ADMNO AS admno,
        FNAME AS fname,
        LNAME AS lname,
        ROLL AS roll,
        MOBNO AS mobno
    FROM student
    ORDER BY ADMNO DESC
    LIMIT 5
    """

    mycursor.execute(query)

    students = mycursor.fetchall()

    mycursor.close()
    mydb.close()

    return students