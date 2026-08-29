from flask import Flask, make_response, request, jsonify
from flask_migrate import Migrate
from marshmallow import ValidationError

from models import db, Exercise, Workout, WorkoutExercise
from schemas import(
    exercise_schema, exercises_schema, workout_exercise_schema,
    workout_schema,workouts_schema
)


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app,db)
db.init_app(app)

#~~~~~~~~~~~~~ WORKOUTS ~~~~~~~~~~~~~
@app.route('/workouts', methods=['GET','POST'])
def workouts():
    if request.method == 'GET':
        return jsonify(workouts_schema.dump(Workout.query.all())), 200 #serializes every workout for a list view

    data = request.get_json()
    try:
        #the load() runs the schema validation and returns a plain dict of clean data
        validated = workout_schema.load(data)
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400

    workout = Workout(**validated)
    db.session.add(workout)
    try:
        db.session.commit() #Triggers the model @validates and db constraints
    except ValueError as e:
        db.session.rollback()
        return jsonify({'error': [str(e)]}), 400

    return jsonify(workout_schema.dump(workout)), 201

@app.route('/workouts/<int:id>', methods=['GET', 'DELETE'])
def workout_by_id(id):
    workout = Workout.query.get(id)
    if not workout:
        return jsonify({'error': 'Workout not Found'}), 404

    if request.method == 'GET':
        #The full schema including the nested workout exercises 
        return jsonify(workout_schema.dump(workout)), 200

    #Deletion process
    db.session.delete(workout)
    db.session.commit()
    return jsonify({}), 204

#~~~~~~~~~~~~~ EXERCISES ~~~~~~~~~~~~~

@app.route('/exercises',methods = ['GET', 'POST'])
def exercises():
    if request.method == 'GET':
        return jsonify(exercises_schema.dump(Exercise.query.all())), 200

    data = request.get_json()
    try:
        validated = exercise_schema.load(data)
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400

    exercise = Exercise(**validated)
    db.session.add(exercise)

    try:
        db.session.commit()
    except ValueError as e:
        db.session.rollback()
        return jsonify({'errors': [str(e)]}), 400
    return jsonify(exercise_schema.dump(exercise)), 201


@app.route('/exercises/<int:id>', methods=['GET', 'DELETE'])
def exercises_by_id(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return jsonify({'error': 'Exercise not found'}), 404

    if request.method == 'GET':
        #Shows the exercise and the workout it is used in 
        result = exercise_schema.dump(exercise)
        result['workouts'] = workouts_schema.dump(exercise.workouts)
        return jsonify(result), 200

    db.session.delete(exercise) #chains with the WorkoutExercises as well
    db.session.commit()
    return jsonify({}), 204


#~~~~~~~~~~~~~ WORKOUT && EXERCISE ~~~~~~~~~~~~~
@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    workout = Workout.query.get(workout_id)
    exercise = Exercise.query.get(exercise_id)

    if not workout or not exercise:
        return jsonify({'error':'Workout or Exercise not found'}), 404

    data= request.get_json() or {}
    try: 
        validated = workout_exercise_schema.load(data, partial=True)
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400

    we = WorkoutExercise(workout=workout, exercise=exercise, **validated)
    db.session.add(we)

    try:
        db.session.commit()
    except ValueError as e:
        db.session.rollback()
        return jsonify({'error': [str(e)]}), 400

    return jsonify(workout_exercise_schema.dump(we)), 201


if __name__ == '__main__':
    app.run(port=5555, debug=True)