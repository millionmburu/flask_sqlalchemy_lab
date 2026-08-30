# Flask SQLAlchemy Workout Application Backend

## Description
A REST API for personal trainers to track workouts and exercises. Exercises are
reusable across multiple workouts, with reps, sets, and duration tracked per
workout-exercise pairing. Built with Flask, SQLAlchemy, and Marshmallow.

## Installation
~Inside bash run the following commands in order:

```bash
git clone https://github.com/<millionmureithimburu>/flask_sqlalchemy_lab.git

cd flask_sqlalchemy_lab

pipenv install

pipenv shell

cd server

export FLASK_APP=app.py

flask db upgrade head

python seed.py
```

## Running the App

```bash
flask run -p 5555
```

The API will be available at `http://127.0.0.1:5555`.

## Endpoints

**GET /workouts**
Returns a list of all workouts.

**GET /workouts/<id>**
Returns a single workout, along with its associated exercises (includes reps, sets, and duration for each).

**POST /workouts**
Creates a new workout. Expects `date`, `duration_minutes`, and `notes` in the request body.

**DELETE /workouts/<id>**
Deletes a workout and removes its associated workout_exercises.

**GET /exercises**
Returns a list of all exercises.

**GET /exercises/<id>**
Returns a single exercise, along with the workouts it's used in.

**POST /exercises**
Creates a new exercise. Expects `name`, `category`, and `equipment_needed` in the request body.

**DELETE /exercises/<id>**
Deletes an exercise and removes its associated workout_exercises.

**POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises**
Adds an exercise to a workout. Expects `reps`, `sets`, and/or `duration_seconds` in the request body.

## Validations
- **Table constraints:** positive `duration_minutes`, `reps`, `sets`; non-empty exercise `name`

- **Model validations:** blank-name rejection, category whitelist, positive-number checks on reps/sets/duration

- **Schema validations:** required fields, allowed category values, positive-number ranges
