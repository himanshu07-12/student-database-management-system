from werkzeug.security import generate_password_hash
from database import get_connection

login_id = input("Enter Administrator ID: ")
current_password = input("Enter current password: ")

hashed_password = generate_password_hash(current_password)

mydb = get_connection()
mycursor = mydb.cursor()

query = """
UPDATE user_details
SET PASSWORD = %s
WHERE LOGIN_ID = %s
"""

mycursor.execute(
    query,
    (hashed_password, login_id)
)

mydb.commit()

if mycursor.rowcount == 1:
    print("Password successfully converted to a secure hash.")
else:
    print("Administrator ID not found.")

mycursor.close()
mydb.close()