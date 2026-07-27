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
    if len(str(mobile)) != 10:
        mycursor.close()
        mydb.close()
        return False, "Mobile Number should be exactly 10 digits"

    # Insert Student
    query = """
    INSERT INTO student
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


def update_student(adm, field, value):

    mydb = get_connection()
    mycursor = mydb.cursor()

    query = "SELECT admno FROM student WHERE admno=%s"
    mycursor.execute(query, (adm,))
    student = mycursor.fetchone()

    if not student:
        mycursor.close()
        mydb.close()
        return False, "Student not found"

    allowed_fields = [
        "admno",
        "fname",
        "lname",
        "roll",
        "mobno"
    ]

    if field not in allowed_fields:
        mycursor.close()
        mydb.close()
        return False, "Invalid field"

    if field == "mobno":
        if len(str(value)) != 10:
            mycursor.close()
            mydb.close()
            return False, "Invalid Mobile Number"

    if field == "roll":
        query = "SELECT roll FROM student WHERE roll=%s"
        mycursor.execute(query, (value,))
        if mycursor.fetchone():
            mycursor.close()
            mydb.close()
            return False, "Roll Number already exists"

    if field == "admno":
        query = "SELECT admno FROM student WHERE admno=%s"
        mycursor.execute(query, (value,))
        if mycursor.fetchone():
            mycursor.close()
            mydb.close()
            return False, "Admission Number already exists"

    query = f"""
    UPDATE student
    SET {field}=%s
    WHERE admno=%s
    """

    mycursor.execute(query, (value, adm))
    mydb.commit()

    mycursor.close()
    mydb.close()

    return True, "Student Updated Successfully"


def view_students():
    mydb = get_connection()
    mycursor = mydb.cursor(dictionary=True)

    query = """
    SELECT *
    FROM student
    """

    mycursor.execute(query)

    students = mycursor.fetchall()

    mycursor.close()
    mydb.close()

    return students