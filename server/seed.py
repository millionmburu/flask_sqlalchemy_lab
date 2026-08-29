

from app import app
from models import db, Exercise, Workout, WorkoutExercise
from datetime import date

with app.app_context():
    print("Tables Clearing....")
    #Removes the children before the parent due to the foreign keys
    WorkoutExercise.query.delete()
    Exercise.query.delete()
    Workout.query.delete()

    print("Seeding exercises....")
    push_up = Exercise(name = "Push_up", category="strength", equipment_needed = False)
    squat = Exercise(name = "Squat", category="strength",equipment_needed=False)
    running = Exercise(name="Running", category="cardio", equipment_needed=False)
    plank = Exercise(name="Plank", category="strength", equipment_needed=False)
    db.session.add_all([push_up, squat, running, plank])

    print("Seeding workouts.....")
    workout_1 = Workout(date=date(2024,6,11), duration_minutes=45, notes= "Upper or lower body")
    workout_2 = Workout(date=date(2024,6,12),duration_minutes=30, notes="cardio focus" )

    db.session.commit() #In order for ids to exist and join the records below

    print("Seeding Workour_exercises.....")
    we1 = WorkoutExercise(workout=workout_1, exercise=push_up, reps=25, sets=3)
    we2 = WorkoutExercise(workout=workout_1, exercise=squat, reps=30, sets=3)
    we3 = WorkoutExercise(workout=workout_2, exercise=running, duration_seconds=1200)
    we4 = WorkoutExercise(workout=workout_2, exercise=plank, duration_seconds=60, sets=3)
    db.session.add_all([we1, we2, we3, we4])

    db.session.commit()
    print("Seeding is complete!")