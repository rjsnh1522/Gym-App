from enum import Enum


class GenderEnum(Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"


class GoalEnum(Enum):
    GAIN_WEIGHT = "Gain Weight"
    LOSE_WEIGHT = "Lose Weight"
    GET_FITTER = "Get Fitter"
    GAIN_FLEXIBILITY = "Gain More flexibility"
    LEARN_BASICS = "Lean Basics"


class PhysicalLevelEnum(Enum):
    ROOKIE = "Rookie"
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    ADVANCE = "Advance"
    BEAST = "Beast"


class ExerciseCategoryEnum(Enum):
    ABS = "Abs"
    BACK = "Back"
    BICEPS = "Biceps"
    CARDIO = "Cardio"
    CHEST = "Chest"
    LEGS = "Legs"
    SHOULDERS = "Shoulders"
    TRICEPS = "Triceps"


class ExerciseTypeEnum(Enum):
    WEIGHT_AND_REPS = "Weight & Reps"
    DISTANCE_AND_TIME = "Distance & Time"
    WEIGHT_AND_DISTANCE = "Weight & Distance"
    WEIGHT_AND_TIME = "Weight & Time"
    REPS_AND_DISTANCE = "Reps & Distance"
    REPS_AND_TIME = "Reps & Time"
    WEIGHT = "Weight"
    REPS = "Reps"
    DISTANCE = "Distance"
    TIME = "Time"

