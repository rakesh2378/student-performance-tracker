"""
Student Performance Tracker - CLI
Run: python cli.py
"""
from tracker import StudentTracker

def menu():
    print("\n==== Student Performance Tracker (CLI) ====")
    print("1. Add student")
    print("2. Add/Update grades")
    print("3. View student details")
    print("4. Calculate student's average")
    print("5. Subject-wise topper (bonus)")
    print("6. Class average for subject (bonus)")
    print("7. List all students")
    print("8. Save local backup (bonus)")
    print("9. Exit")

def main():
    tracker = StudentTracker()
    while True:
        menu()
        choice = input("Choose an option (1-9): ").strip()
        if choice == "1":
            name = input("Name: ")
            roll = input("Roll number: ")
            ok = tracker.add_student(name, roll)
            print("Added." if ok else "Roll number already exists.")
        elif choice == "2":
            roll = input("Roll number: ")
            print("Enter grades as Subject:Score (e.g., Math:85), comma-separated.")
            raw = input("Grades: ")
            grades = {}
            for pair in raw.split(","):
                if ":" in pair:
                    sub, sc = pair.split(":", 1)
                    grades[sub.strip()] = float(sc.strip())
            ok, msg = tracker.add_grades(roll, grades)
            print(msg)
        elif choice == "3":
            roll = input("Roll number: ")
            st = tracker.view_student_details(roll)
            if not st:
                print("Student not found.")
            else:
                print(f"{st.roll_number} - {st.name}")
                if not st.grades:
                    print("No grades yet.")
                else:
                    for sub, sc in st.grades.items():
                        print(f"  {sub}: {sc}")
        elif choice == "4":
            roll = input("Roll number: ")
            avg = tracker.calculate_average(roll)
            print(f"Average: {avg}" if avg is not None else "No grades or student not found.")
        elif choice == "5":
            subject = input("Subject: ")
            top = tracker.subject_topper(subject)
            if top:
                name, roll, score = top
                print(f"Topper in {subject}: {name} ({roll}) - {score}")
            else:
                print("No scores for that subject yet.")
        elif choice == "6":
            subject = input("Subject: ")
            avg = tracker.class_average(subject)
            print(f"Class average in {subject}: {avg}" if avg is not None else "No scores yet.")
        elif choice == "7":
            students = tracker.list_students()
            for s in students:
                print(f"{s.roll_number} - {s.name} ({len(s.grades)} subjects)")
        elif choice == "8":
            path = tracker.save_backup()
            print(f"Backup saved to {path}")
        elif choice == "9":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
