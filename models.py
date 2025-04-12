# models.py

from datetime import time

class Schedule:
    def __init__(self, day, start: time, end: time):
        self.day = day  # e.g., "Monday"
        self.start = start
        self.end = end

    def overlaps_with(self, other):
        # Checks if two schedules overlap on the same day
        if self.day != other.day:
            return False
        return not (self.end <= other.start or self.start >= other.end)

    def __str__(self):
        return f"{self.day} from {self.start.strftime('%H:%M')} to {self.end.strftime('%H:%M')}"


class Course:
    def __init__(self, code, name, credits, semester, prerequisites=None, schedules=None):
        self.code = code
        self.name = name
        self.credits = credits
        self.semester = semester
        self.prerequisites = prerequisites or []
        self.schedules = schedules or []

    def __str__(self):
        return f"{self.code} - {self.name} ({self.credits} credits)"


class Enrollment:
    def __init__(self, course: Course):
        self.course = course

    def overlaps_with(self, other_enrollment):
        for s1 in self.course.schedules:
            for s2 in other_enrollment.course.schedules:
                if s1.overlaps_with(s2):
                    return True
        return False


class Student:
    def __init__(self, name):
        self.name = name
        self.approved_courses = []  # Courses the student has passed
        self.enrollments = []  # Active course enrollments

    def total_credits(self):
        return sum(enrollment.course.credits for enrollment in self.enrollments)

    def can_enroll_in(self, course: Course):
        # Check if the student is already enrolled
        if any(enrollment.course == course for enrollment in self.enrollments):
            return False, "You are already enrolled in this course."

        # Check prerequisites
        for prereq in course.prerequisites:
            if prereq not in self.approved_courses:
                return False, f"Missing prerequisite: {prereq.code}"

        # Check credit limit
        if self.total_credits() + course.credits > 24:
            return False, "Exceeds credit limit."

        # Check for schedule overlaps
        new_enrollment = Enrollment(course)
        for enrollment in self.enrollments:
            if new_enrollment.overlaps_with(enrollment):
                return False, "Schedule conflict with another course."

        return True, "Enrollment valid."

    def enroll_in(self, course: Course):
        can_enroll, message = self.can_enroll_in(course)
        if can_enroll:
            self.enrollments.append(Enrollment(course))
            print(f"✅ {self.name} enrolled in: {course}")
        else:
            print(f"❌ Could not enroll in {course}: {message}")

    def pass_course(self, course: Course):
        if course not in self.approved_courses:
            self.approved_courses.append(course)
