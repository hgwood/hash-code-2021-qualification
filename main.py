import json
import os
import sys

from math import gcd
from collections import defaultdict



data_directory = "./data_sets_json/"
data_set_files = os.listdir(data_directory)


def main():
    for i, data_set_file in enumerate(data_set_files):
        # if i != 1:
        #     continue
        filename = os.path.join(data_directory, data_set_file)
        with open(filename) as current_file:
            data = json.load(current_file)
        solution = handle_dataset(data)
        solution_output = compose_output(solution)

        output_basename = os.path.basename(
            filename).replace(".json", ".out.txt")
        output_file = os.path.join(
            data_directory, "..", ".petibrugnon", "solutions", output_basename)
        with open(output_file, "w") as file_output:
            file_output.write(solution_output)

# Forme de l'output
# [
#   (1, [("rue-d-athenes", 2), ("rue-d-amsterdam", 1)]),
#   (0, [("rue-de-londres", 2)]),
#   (2, [("rue-de-moscou", 1)]),
# ]


def compose_output(solution):
    lines = []
    lines.append(str(len(solution)))
    for (id, schedule) in solution:
        lines.append(str(id))
        lines.append(str(len(schedule)))
        for (street, duration) in schedule:
            lines.append(street + " " + str(duration))
    return "\n".join(lines)


def compose_streets_by_intersection(streets):
    result = {}
    for street in streets:
        name = street["name"]
        start = street["start"]
        end = street["end"]
        if end not in result:
            result[end] = []
        result[end].append(name)
    return result


def handle_dataset(data):
    streets = data["streets"]
    streets_by_name = {
        street['name']: street
        for street in data['streets']
    }
    streets_by_intersection = compose_streets_by_intersection(streets)

    car_journeys = {
        i:
            sum(
                streets_by_name[street]['length']
                for street in car['path']
            )
        for i, car in enumerate(data["cars"])
    }
    car_weights = compose_car_weights(data, streets_by_name, car_journeys)
    # print(car_weights)
    return [
        (
            intersection,
            [
                (street_name, min(data["duration"], round(car_weights[intersection][street_name] / min(car_weights[intersection].values()))))
                for street_name in streets if street_name in car_weights[intersection]
            ] or [(streets[0], 1)]
        ) for intersection, streets in streets_by_intersection.items()
    ]

def compose_car_weights(data, streets_by_name, car_journeys):
    cars = data["cars"]
    result = defaultdict(lambda: defaultdict(int))
    out_of_time_cars = compose_out_of_time_cars(data, streets_by_name)
    for i, car in enumerate(cars):
        if i in out_of_time_cars:
            continue
        for street_name in car["path"]:
            journey_length = car_journeys[i]
            weight = journey_length / data["duration"]
            result[streets_by_name[street_name]["end"]][street_name] += weight
    return result

def compose_out_of_time_cars(data, streets_by_name):
    for i, car in enumerate(data['cars']):
        s = sum(
            streets_by_name[street]['length']
            for street in car['path'])
        # print(f"car {i}: {s}")
        if s > data['duration']:
            yield i


################################################################
main()
