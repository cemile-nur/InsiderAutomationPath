class Student:
    def __init__(self, first_name: str, last_name: str, grade_level: str):
        
      
        self.first_name = first_name
        self.last_name = last_name
        self.grade_level = grade_level

    def __str__(self):
        return f"{self.first_name} {self.last_name}, Grade: {self.grade_level}"


class Question:
    def net_count(self, correct: int, wrong: int) -> float:
        
        if correct < 0 or wrong < 0:
            raise ValueError("Correct and wrong counts cannot be negative.")

        net = correct - (wrong / 4)
        return max(net, 0.0)

    def calculate_score(self, net: float) -> float:
        
        if net < 0:
            raise ValueError("Net cannot be negative.")

        score = net * 2
        return min(score, 100.0)


def main():
    print("=== Student Exam Score Calculator ===")
    first_name = input("Enter student's first name: ")
    last_name = input("Enter student's last name: ")
    grade_level = input("Enter student's grade/class: ")

    student = Student(first_name, last_name, grade_level)

    try:
        correct = int(input("Number of correct answers: "))
        wrong = int(input("Number of wrong answers: "))
    except ValueError:
        print("Please enter a valid integer for correct and wrong counts.")
        return

    question = Question()
    try:
        net = question.net_count(correct, wrong)
        final_score = question.calculate_score(net)
    except ValueError as e:
        print(f"Error: {e}")
        return

    print("\n--- Result ---")
    print(student)
    print(f"Correct: {correct}, Wrong: {wrong}")
    print(f"Net: {net:.2f}")
    print(f"Score: {final_score:.2f} (Each net = 2 points)")

if __name__ == "__main__":
    main()
