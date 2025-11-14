def calculate_letter_grade(midterm1, midterm2, final_exam):
    total_score = midterm1 * 0.30 + midterm2 * 0.30 + final_exam * 0.40

    if total_score >= 90:
        return "AA"
    elif total_score >= 85:
        return "BA"
    elif total_score >= 80:
        return "BB"
    elif total_score >= 75:
        return "CB"
    elif total_score >= 70:
        return "CC"
    elif total_score >= 65:
        return "DC"
    elif total_score >= 60:
        return "DD"
    elif total_score >= 55:
        return "FD"
    else:
        return "FF"

def get_input(score_name):
    while True:
        try:
            value = float(input(f"Enter {score_name} score (0‑100): "))
            if 0 <= value <= 100:
                return value
            else:
                print("Error: Score must be between 0 and 100.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def main():
    print("Letter Grade Calculator")
    v1 = get_input("Midterm 1")
    v2 = get_input("Midterm 2")
    final = get_input("Final Exam")

    letter = calculate_letter_grade(v1, v2, final)
    total = v1 * 0.30 + v2 * 0.30 + final * 0.40

    print(f"\nYour total score: {total:.2f}")
    print(f"Your letter grade: {letter}")

if __name__ == "__main__":
    main()
