## Introduction

The problem of some universities in exam scheduling is they can not find a good (or probably best) schedule solution for exams. It is so important for both students and teachers to be satisfied with the schedule. In this project, with the help of `Genetic Algorithm`, we are going to find a good solution to fit courses in the best way.

## Installation

[Github Repo](https://github.com/Arefeh902/ExamScheduling)

Python is used for the algorithm, so you must have [python](https://www.python.org/) installed in your system.

Install the requirements:

```
pip install -r requirements.txt
```

For dataset, put the BLOB.txt and BLOB2.txt near the program.

Then run:

```
python main.py
```

Execution takes some time, so just wait for the results.

## Description

### Logic

The algorithm as said before is `Genetic Algorithm`. We are trying to solve the problem with randomly create and making solutions better and better. Multiple parameters are required and are important which we tried to make the best ones for our problem. There are some constraints that need to be checked and ranked to determine the penalty. Constraints have different ranks and some are more important.

After many generations, the algorithm tries to make a solution that satisfies our needs, or it will try again and randomly creates and fits times, courses and... to solve in another way.

### Assumptions

- There are 3 time slots in a day

- Each exam will be ? hours

- The higher the fitness score, the better solution

### Hyper parameters

There are 3 main parameters: `Population size`, `Maximum of Generation`, `Mutation Probability`.

In `test_params.py` a range defined for every parameter and the program runs 10 times for every set of values. The ranges are:

- Population size: [100, 600] with step 100

- Maximum of Generation: [100, 300] with step 100

- Mutation Probability: [0.4, 0.9] with step 0.1

To calculate which sets are the best, there are 2 scenarios:

1. Evaluate average of fitnesses including values equal to 1

2. Evaluate average of fitnesses excluding values equal to 1

If we want to be more accurate we should use the first one, because genetic algorithm is a random based algorithm and we should consider all possible situations.

The data is important to use the best possible values. We consider the data format and size is sames as we use in example data.

### Constraints

- Hard Constraints:

  1. No student should have more than one exam in a day

  2. No teacher should have more than one exam in a day

- Soft Constraints:

  1. No two or three consecutive exams are allowed

  2. In two consecutive exams, there should be a single day rest

  3. There should not be exams in holidays

### User-Defined classes

- Course: stores `teacher`, `title` and list of `student ids`.

- Student: stores list of `courses`

- TimeSlot: stores `is_available` and `is_holiday`

- Schedule: stores `time_to_course` and `course_to_time`

### Steps

## Example

### Sample Dataset

### Output

## References

## About Us

Arefeh Ahmadi

Amirhosein Gharaati
