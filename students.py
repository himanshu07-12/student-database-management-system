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
    pass


def update_student(adm, field, value):
    pass


def view_students():
    pass