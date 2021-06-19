# Temperature Analyzer

## Problem Statement

<em> Copied from <a href="https://github.com/magiclabs/email_screening_question/tree/master/Backend">this repository</a> </em>

Thank you for taking the time out of your day to tackle this problems set with us! We expect the solution to be
written in **Python**, if you choose to use libraries to help you accomplish the task at hand,
we ask that you leave plenty room in your work to showcase your **algorithms**, and **design** skillsets.

We expect each candidate to spend no more than 2 hours on the solution (we'll take your
word for it 😇). As there are multiple parts to the question, do not feel the need to complete it
all, instead please feel free to stop once you've crossed the two hour mark. If you were in
the midst of a question, feel free to leave some pseudocode for how you would've completed it.

You'll find the dataset for the questions in `data.csv` after unzipping `data.csv.zip`. The dataset
represents temperatures reported by specific weather stations (`station_id`) at a particular point
in time (`date`). The first 4 digits of the `date` value represents the year that the temperature was
collected, the second 3 digit portion appearing after the `.` represents a unique point during the
year such that no two days within the year has the same 3 digit representation.


**Part 1**:

Create a function that when called returns the `station_id`, and `date` pair that reported the
lowest temperature. If a tie occurs simply return one pair at random.

**Part 2**:

Create a function that returns the `station_id` that experienced the most amount of temperature
fluctuation across all dates that it reported temperatures for. For example with the following dataset:

    station_id,     date, temperature_c
             1, 2000.001,             5
             1, 2000.123,             0
             1, 2000.456,             5

we are expecting the total fluctuation to be 10 degrees, as opposed to 0 which is the net difference
in temperature between the first and last dates.

**Part 3**:

Create a function that will return the `station_id` that experienced the most amount of temperature
fluctuation for any given range of dates. I.E to get the result of 10 degrees from part 2 above, we
would expect the input dates to be `2000.001` and `2000.456`.

## Evaluation Criteria
We will be evaluating your submission based on the following criteria, in no particular order:

* Readability: Consistent styling, aptly named functions, and variables.
* Coherent Design: Where applicable, sensible abstractions are employed, functions are well-intentioned.
* Test coverage: The solution is tested, and proveably functions correctly.
* Correctness

In other words, the end product should be something that you wouldn't hesitate to hit shippit on and
productionize!


## Solution

### How to run.

Make sure you have `make` and `python 3.8` is installed. No 3rd party libraries are installed, so a pipenv/virtualenv is not required.

`make run`

This executes index.py and runs all three functions with valid inputs.

`make test`

This executes all unit tests in the tests directory.

### Motivations/Considerations:

Since this task would be trivial using a library such as pandas, I decided against using external libraries to highlight
my code and algorithms.

The solution implemented is not very scalable - it stores all the temperature data in memory. However, I created an interface
according to the access patterns needed that could be implemented by a real database. I go into detail
about the database solution and schema I'd likely use if I had more time below.

### Part 1:

To find the minimum temperature value, I iterate through all temperature readings and compare the current value with the 
lowest value found thus far. If it's lower, I replace the current minimum.

### Part 2:

To calculate the total temperature fluctuation, I summed the absolute value of the difference between 
subsequent temperature readings for each station, one at a time. Then, if the total fluctuation
for that particular station exceeds the max, replace it with the new max value and continue.

The time complexity would be O(n*k) where n is the number of unique stations and k is the average
number of temperature readings. The storage required is O(k) since we load all temperature readings from a particular
station at a time.
With a real database this would be reduced since we could paginate the results.

### Part 3: 

This solution is similar to part 2. However, the main difference is the additional time range requirement. I made 
the decision to filter the data manually rather than using a library. Since the data is sorted according to date for
each station, I use binary search to find the correct indexes to slice the dataset. In the interest of time,
I used python's built-in bisect library to do this which implements a basic binary search algorithm.

## Evaluation Criteria

**Readability:**

*"There are only two hard things in computer science: cache invalidation and naming things."*

I've named modules, classes and variables as succinctly and precisely as possible. 
See below about module organization.

Type hints are included in all function definitions to make the code easier to read and reason about.

I use Pycharm's built in formatting to format all files.

**Coherent Design:**

I tried my best to follow separation of concerns - business logic, data access logic and data loading logic are all separated
into different modules. The 'components' module includes all business logic classes. The accessors module includes all data access logic.

In cases where a particular system component has state, I use python classes. However, for the data loader,
I decided against it since it is stateless and it primary method is static.

Data models are represented with python dataclasses.

**Test Coverage and Correctness:**

I've striven to test all edge cases where possible and to cover every branch. 

## Roadmap

1. External Database

Rather than indexing the data manually using a python dictionary, using a scalable data store such as DynamoDB
would be preferred. In Dynamo's case, designating the station_id as a hash key and the date as a range key would make
filtering by date range much, much easier. We also would not be bound by the limits of how much of the data fits in 
memory. This would add in an extra network hop when fetching the data, but latency doesn't seem like a very high priority
for this type of problem.

A SQL database would also work great. One benefit of having a SQL database is that all three parts of the problem could be solved
with SQL queries directly - no need for application logic. 
However, it would eventually be a scaling bottleneck given enough data (and a large cost center). 
One way to solve that would be to use something like Hive or Athena although latency would likely suffer.

2. API

If this needed to be accessed by other services, it would be relatively simple to build a small Flask microservice 
to expose these three functions over HTTP with a RESTful API.

3. Up-to-date data

If new data was flowing in continuously, there would be a lot of optimizations that could be made here using memoization.

For part 1, it would be best to store a minimum for each station_id and update as each new reading comes in.

For part 2, we could store a running cumulative sum for each station_id.

For part 3, storing intermediate results over specific periods (such as years) would speed up calculating the cumulative sum over a given range.
