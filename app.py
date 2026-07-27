#to insert a student into the database
"""from students import insert_student

success, message = insert_student(
    103,
    "Divyanshu",
    "Tripathi",
    12,
    7355525494
)

print(success)
print(message)"""
# to view all students in the database
"""from students import view_students

students = view_students()

for student in students:
    print(student)
"""     
#to delete a student in the database
"""from students import delete_student

success, message = delete_student(101)

print(success)
print(message)"""
#to update a student in the database
"""from students import update_student

success, message = update_student(
    999,
    "fname",
    "ABC"
)

print(success)
print(message)"""