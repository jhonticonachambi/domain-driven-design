# Simulate a student and courses

from datetime import time
from models import Course, Student, Schedule

# Define sample courses
prog1 = Course("INF101", "Programming I", 4, semester=1, schedules=[
    Schedule("Monday", time(8, 0), time(10, 0))
])
prog2 = Course("INF201", "Programming II", 4, semester=2, prerequisites=[prog1], schedules=[
    Schedule("Tuesday", time(10, 0), time(12, 0))
])
mat1 = Course("MAT101", "Mathematics I", 6, semester=1, schedules=[
    Schedule("Monday", time(9, 30), time(11, 30))
])  # This course overlaps with Programming I

# Create a student instance
student = Student("John Doe")

# Attempt to enroll in courses
student.enroll_in(prog1)  # Should succeed
student.enroll_in(prog2)  # Should succeed (if prog1 passed)
student.enroll_in(mat1)   # Should fail (due to schedule overlap with prog1)

# Mark a course as passed and attempt to enroll again
student.pass_course(prog1)
student.enroll_in(mat1)   # Should succeed now
