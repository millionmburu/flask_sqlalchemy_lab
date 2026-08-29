from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy import MetaData

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s"
})

db = SQLAlchemy(metadata=metadata)

#Defines the exercise class

class Exercise(db.Model):
    __tablename__ = 'exercises'
    __table_args__ = (
        db.CheckConstraint('length(name) > 0', name='exercise_name_not_empty'),
    )

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable=False,unique = True) #Rejects duplicate names
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, default = False)

    #to delete workout excercises if the Exercise is deleted
    workout_exercises= db.relationship(
        "WorkoutExercise",
        back_populates = "exercise",
        cascade = "all, delete-orphan"
    )

    #An exercise has several workoutExercises
    workouts = association_proxy('workout_exercises', 'workout')

    VALID_CATEGORIES = ["strength", "cardio", "flexibility", "balance"]

    @validates("name")
    def  validate_name(self, key, name):
        #To reject blanks names before reaching the db
        if not name or not name.strip():
            raise ValueError('Exercise name cannot be blank')
        return name

    @validates("category")
    def validate_category(self, key, category):
        #To only allow known categories
        if category not in self.VALID_CATEGORIES:
            raise ValueError(f"Category must be one of {self.VALID_CATEGORIES}")
        return category

    def __repr__(self):
        return f'<Exercise {self.id}: {self.name}>'

#Defines the workout class
class Workout(db.Model):
    __tablename__ = 'workouts'
    __table_args__ = (
        db.CheckConstraint('duration_minutes > 0', name='workout_duration_positive'),
    )

    id = db.Column(db.Integer, primary_key = True)
    date= db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable = False)
    notes = db.Column(db.Text)

    workout_exercises = db.relationship(
        'WorkoutExercise', 
        back_populates="workout",
        cascade ="all, delete-orphan"
    )

    exercises = association_proxy('workout_exercises', 'exercise')

    @validates('duration_minutes')
    def validate_duration(self, key, value):
        #checks if value is none or null or <=0
        if value is None or value <=0:
            raise ValueError('Duration value must be a positive value')
        return value

    def __repr__(self):
        return f'<Workout {self.id}: {self.date}>'

#Defines the workout exercise class
class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'
    __table_args__ = (
        db.CheckConstraint('reps IS NULL OR reps > 0', name='we_reps_positive'),
        db.CheckConstraint('sets IS NULL OR sets > 0', name='we_sets_positive'),
    )

    id = db.Column(db.Integer, primary_key=True)
    #A WorkoutExcersise belongs to both a workout and an Exercise
    workout_id = db.Column(db.Integer,db.ForeignKey('workouts.id'), nullable = False)

    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable = False)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    workout = db.relationship('Workout', back_populates= 'workout_exercises')
    exercise = db.relationship('Exercise', back_populates= 'workout_exercises')

    @validates('reps','sets', 'duration_seconds')
    def validate_positive(self, key, value):
        #Must be a positive number
        if value is not None and value <= 0:
            raise ValueError(f'{key} must be a positive number.')
        return value
    
    def __repr__(self):
        return f'<WorkoutExercise {self.id}>'


