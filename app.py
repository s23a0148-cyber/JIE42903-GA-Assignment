
import streamlit as st
import pandas as pd
import random

# Application title
st.title("TV Program Scheduling using Genetic Algorithm")

# Load modified program ratings
df = pd.read_csv('modified_program_ratings.csv')

# Convert CSV data into dictionary
ratings = {}

for index, row in df.iterrows():
    program = row['Type of Program']
    program_ratings = row.iloc[1:].astype(float).tolist()
    ratings[program] = program_ratings

# Define programs and time slots
all_programs = list(ratings.keys())
all_time_slots = list(range(6, 24))

# Display program ratings
st.subheader("Program Ratings")
st.dataframe(df)

# Fitness Function
def fitness_function(schedule):
    total_rating = 0

    for time_slot, program in enumerate(schedule):
        total_rating += ratings[program][time_slot]

    return total_rating

# Initialize Population
def initialize_pop(programs, time_slots, population_size):
    population = []

    for _ in range(population_size):
        schedule = [random.choice(programs) for _ in time_slots]
        population.append(schedule)

    return population

# Finding Best Schedule
def finding_best_schedule(population):
    best_schedule = max(population, key=fitness_function)
    return best_schedule

# Crossover
def crossover(schedule1, schedule2):
    crossover_point = random.randint(1, len(schedule1) - 1)

    child1 = schedule1[:crossover_point] + schedule2[crossover_point:]
    child2 = schedule2[:crossover_point] + schedule1[crossover_point:]

    return child1, child2

# Mutation
def mutate(schedule):
    mutation_point = random.randint(0, len(schedule) - 1)

    new_program = random.choice(all_programs)

    schedule[mutation_point] = new_program

    return schedule


# Genetic Algorithm
def genetic_algorithm(generations=100,
                      population_size=50,
                      crossover_rate=0.8,
                      mutation_rate=0.02,
                      elitism_size=2):

    population = initialize_pop(
        all_programs,
        all_time_slots,
        population_size
    )

    for generation in range(generations):

        population.sort(
            key=fitness_function,
            reverse=True
        )

        new_population = population[:elitism_size]

        while len(new_population) < population_size:

            parent1, parent2 = random.choices(population, k=2)

            if random.random() < crossover_rate:
                child1, child2 = crossover(parent1, parent2)
            else:
                child1 = parent1.copy()
                child2 = parent2.copy()

            if random.random() < mutation_rate:
                child1 = mutate(child1)

            if random.random() < mutation_rate:
                child2 = mutate(child2)

            new_population.extend([child1, child2])

        population = new_population[:population_size]

    best_schedule = finding_best_schedule(population)

    return best_schedule


# Genetic Algorithm Parameters
st.subheader("Genetic Algorithm Parameters")

CO_R = st.slider(
    "Crossover Rate (CO_R)",
    min_value=0.0,
    max_value=0.95,
    value=0.8,
    step=0.05
)

MUT_R = st.slider(
    "Mutation Rate (MUT_R)",
    min_value=0.01,
    max_value=0.05,
    value=0.02,
    step=0.01
)


# Run Genetic Algorithm Button
if st.button("Run Genetic Algorithm"):

    best_schedule = genetic_algorithm(
        crossover_rate=CO_R,
        mutation_rate=MUT_R
    )

    total_rating = fitness_function(best_schedule)

    st.subheader("Optimal TV Program Schedule")

    schedule_data = {
        "Time Slot": [f"{hour}:00" for hour in all_time_slots],
        "Program": best_schedule
    }

    schedule_df = pd.DataFrame(schedule_data)

    st.dataframe(schedule_df)

    st.metric("Total Ratings", round(total_rating, 2))

# Three Experimental Trials
st.subheader("Three Experimental Trials")

st.write("Set different crossover and mutation rates for each trial.")

trial_parameters = []

for i in range(1, 4):

    st.markdown(f"### Trial {i}")

    col1, col2 = st.columns(2)

    with col1:
        co_rate = st.slider(
            f"Crossover Rate - Trial {i}",
            min_value=0.0,
            max_value=0.95,
            value=0.8,
            step=0.05,
            key=f"co_{i}"
        )

    with col2:
        mut_rate = st.slider(
            f"Mutation Rate - Trial {i}",
            min_value=0.01,
            max_value=0.05,
            value=0.02,
            step=0.01,
            key=f"mut_{i}"
        )

    trial_parameters.append((co_rate, mut_rate))

if st.button("Run Three Experiments"):

    for i, (co_rate, mut_rate) in enumerate(trial_parameters, start=1):

        best_schedule = genetic_algorithm(
            crossover_rate=co_rate,
            mutation_rate=mut_rate
        )

        total_rating = fitness_function(best_schedule)

        st.subheader(f"Trial {i} Results")

        st.write(f"Crossover Rate: {co_rate}")
        st.write(f"Mutation Rate: {mut_rate}")

        result_df = pd.DataFrame({
            "Time Slot": [f"{hour}:00" for hour in all_time_slots],
            "Program": best_schedule
        })

        st.dataframe(result_df)

        st.metric(
            f"Trial {i} Total Ratings",
            round(total_rating, 2)
        )
