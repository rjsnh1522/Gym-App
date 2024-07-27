


### Requirements to Build a Gym App


#### Onboarding
1. Auth Service
   a. Login
   b. Logout
   c. Forget Password
   d. verify email
2. Profile Service
   a. Todays sessions
   b. Workout Categories
   c. All workout options
   d. Daily insight
   e. Workout histroy
   f. Track workouts
   g. Add, Updated, Delete Profile
3. Workout Plan details
4. Personal Coach Option
   a. Book appointment with a coach
5. Subscription
6. Fitness Instructors
    a. Trainer details
    b. Book Appointment
    c. Trainer Reviews
    d. Write a Review
    e. Payment for appointment
    f. Add card, Edit card, remove card
7. Notification 
   a. Email 
   b. SMS 
   c. PUSH
8. Settings
   a. unit of measure
   b. Notifications
   c. Language
   d. Contact us
9. Workouts
   a. PPL, Bro Split and other kind of excerices
   b. Body parts and available Exercises
   c. CRUD operation on adding Exercises
   d. track workout with, sets reps times etc etc
   


Musthave
- [ ] Middle ware to have protected APIS and non protected APIS


#### ENUMS
##### Goal ENUM
* [gain weight, Lose weight, get Fitter, Gain More flexibility, Lean basics]

##### Workout Categories ENUM
* [Rookie, Beginner, Intermediate, Advance, True Beast]

##### Exercise Category
* [Abs, Back, Biceps, Cardio, Chest, Legs, Shoulders, Triceps]

##### Exercise Types
* [Weight & Reps, Distance & Time, Weight & Distance, Weight & time, Reps & Distance, 
Reps & Time, Weight, Reps, Distance, Time]


#### User Model
* name
* email
* hashed_password
* is_active
* created_at
* updated_at

#### Profile Model
* gender
* age
* weight
* height
* Goal  [Goal ENUM]
* physical_activity_level [Workout Categories ENUM]
* user_id [one to one, each user has a profile]
* ProfileType [Coach, Trainee]


#### Workout Plan:
* workout title
* Workout category 
* Total workouts
* Workouts [list]
* Description
* Calories Burn

#### Workouts
1. Exercises name
2. Target muscle
3. Time
4. workout_plan_id [one to many, workout plan can have many workouts]

#### Exercises
user_id
exercise_category
name
notes
exercise type
weight unit
is_default



