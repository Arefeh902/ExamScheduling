## Introduction

The problem of some universities in exam scheduling is they can not find a good (or probably best) schedule solution for exams. It is so important for both students and teachers to be satisfied with the schedule. In this project, with the help of `Genetic Algorithm`, we are going to find a good solution to fit courses in the best way.

## Live Demo

[exam-scheduling.vercel.app](https://exam-scheduling.vercel.app/)

## Installation

Backend Repo: https://github.com/Arefeh902/ExamScheduling

Python is used for the algorithm, so you must have [python](https://www.python.org/) installed in your system.

Install the requirements:

```
pip install -r requirements.txt
```

Then:

```
python main.py
```

To execute the program, you should also run frontend project.

Frontend Repo: https://github.com/AmirHosein-Gharaati/ExamScheduling

## Description

### Logic

The algorithm as said before is `Genetic Algorithm`. We are trying to solve the problem with randomly create and making solutions better and better. Multiple parameters are required and are important which we tried to make the best ones for our problem. There are some constraints that need to be checked and ranked to determine the penalty. Constraints have different ranks and some are more important.

After many generations, the algorithm tries to make a solution that satisfies our needs, or it will try again and randomly creates and fits times, courses and... to solve in another way.

### Assumptions

- User can set number of time slots per day.

- The program can try as many times as user wants.

- The higher the fitness score, the better the solution.

- Data should be read from specific format in xlsx.

### Hyper parameters

- Population size

- Maximum of Generation

- Mutation Probability

### Constraints

- Hard Constraints:

  1. No student should have more than one exam in a day

  2. No teacher should have more than one exam in a day

- Soft Constraints:

  1. Two consecutive exams has a penalty of

  2. Three consecutive exams has a penalty of

  3. Having an exam on a holiday has a penalty of

  4. Single day rest between exams has a penalty of

  5. Two day rest between exams has a penalty of

### User-Defined classes

- Course: stores `title`, `professor` and list of `student ids`.

- Student: stores list of `courses`

- TimeSlot: stores `is_available` and `is_holiday`

- Schedule: stores `time_to_course` and `course_to_time`

### Steps

#### Reading input data

The input are read from two separate files with data regarding:

1. which courses each student is enrolled in
2. which courses does each professor teach

#### Run the Genetic Algorithm

For this problem we are using `Genetic Algorithm` to find a good solution.
The algorithm is as follows:

1. Generate a set of N random solutions. This set is called a population
2. Repeat:
   1. calculate how good each solution in the population. This value is called fitness.
   2. pick two solutions at random with weights proportional to each schedule's fitness.
   3. crossover the two chosen solutions and create a new solution
   4. mutate the chosen the new solution (this is to accumulate for lack of verity in out initial population)
   5. repeat this process N times to get a new population
3. Report best found solution

## References

https://github.com/HxnDev/Exam-Scheduler-Generator-Using-Genetic-Algorithm

https://youtu.be/4XZoVQOt-0I

https://youtu.be/9zfeTw-uFCw

## About Us

Arefeh Ahmadi

Github:https://github.com/Arefeh902

Amirhosein Gharaati

Github: https://github.com/AmirHosein-Gharaati
