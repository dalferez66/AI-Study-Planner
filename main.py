import pandas as pd
from sklearn.linear_model import LinearRegression
from datetime import date, timedelta, datetime

def train_study_model():
    # AI model training off this data to help predict study hours
    data = {
        "difficulty": [8, 3, 5, 9, 2, 7, 4, 6],
        "target_score": [90, 70, 80, 95, 60, 85, 75, 88],
        "past_avg_score": [85, 60, 75, 90, 50, 82, 70, 84],
        "hours_needed": [12, 3, 7, 15, 2, 10, 5, 9]
    }
    df = pd.DataFrame(data)
    model = LinearRegression()
    model.fit(df[["difficulty", "target_score", "past_avg_score"]], df["hours_needed"])
    return model

def get_user_inputs():

    print("[--- AI STUDY PLANNER ---]\n")
    print("Welcome! Let's create your personalized schedule.\n")

    # Validate user average score
    while True:
        try:
            user_avg = float(input("Enter your overall average score from past exams (0-100): "))
            if 0 <= user_avg <= 100: break
            print("Please enter a valid score.")
        except ValueError:
            print("Invalid input.")

    # Validate max hours
    while True:
        try:
            limit = float(input("Enter max study hours allowed per day (1-24): "))
            if 0 < limit <= 24: break
            print("Please enter a number between 1 and 24.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    exams = {}
    print("\nEnter your exams. Type 'done' to finish.")
    
    while True:
        name = input("\nExam Name: ")
        if name.lower() == 'done':
            if not exams:
                print("Enter at least one exam.")
                continue
            break
        
        # Difficulty validation
        while True:
            try:
                diff = int(input(f"Difficulty of {name} (1-10): "))
                if 1 <= diff <= 10: break
                print("Must be 1-10.")
            except ValueError:
                print("Enter a whole number.")

        # Target Score validation
        while True:
            try:
                target = int(input(f"Target Score for {name} (0-100): "))
                if 0 <= target <= 100: break
                print("Must be 0-100.")
            except ValueError:
                print("Enter a whole number.")

        # Date validation
        while True:
            date_str = input(f"Date for {name} (YYYY-MM-DD): ")
            try:
                exam_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                if exam_date > date.today(): break
                print("Date must be in the future.")
            except ValueError:
                print("Use YYYY-MM-DD format.")

        exams[name] = {"diff": diff, "target": target, "exam_date": exam_date}
    
    return limit, exams, user_avg

def generate_schedule(predictions, exam_info, limit):

    start_date = date.today()
    last_exam_date = max(info["exam_date"] for info in exam_info.values())
    total_days = (last_exam_date - start_date).days

    print(f"\n--- YOUR {total_days}-DAY STUDY PLAN ---")
    print(f"Daily Limit: {limit} hours")

    for day_num in range(total_days + 1):
        current_date = start_date + timedelta(days=day_num)
        print(f"\nDay {day_num} ({current_date.strftime('%b %d')}):")
        
        day_total = 0
        for subject, hours in predictions.items():
            exam_date = exam_info[subject]["exam_date"]
            
            if current_date < exam_date:
                days_until_this_exam = (exam_date - start_date).days
                daily_chunk = hours / days_until_this_exam
                print(f"  - {subject}: {daily_chunk:.1f} hours")
                day_total += daily_chunk
            elif current_date == exam_date:
                print(f"  - {subject}: EXAM DAY!")

        if day_total > limit:
            print(f"  WARNING: Total ({day_total:.1f}h) exceeds your {limit}h limit!")

def main():
    
    # 1. Train
    model = train_study_model()
    
    # 2. Input
    max_hours, my_exams, user_avg = get_user_inputs()
    
    # 3. Predict
    exam_predictions = {}
    for name, info in my_exams.items():
        pred = model.predict([[info["diff"], info["target"], user_avg]])
        exam_predictions[name] = max(0.5, round(float(pred[0]), 1))
    
    # 4. Schedule   
    generate_schedule(exam_predictions, my_exams, max_hours)

if __name__ == "__main__":
    main()