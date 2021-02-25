import json
import os
import sys

data_directory = "./data_sets_json/"
data_set_files = os.listdir(data_directory)


def main():
    for i, data_set_file in enumerate(data_set_files):
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
    streets_by_intersection = compose_streets_by_intersection(streets)
    car_weights = compose_car_weights(data)
    return [(intersection, [(street, car_weights[street]) for street in streets if street in car_weights] or [(streets[0], 1)]) for intersection, streets in streets_by_intersection.items()]

def compose_car_weights(data):
    cars = data["cars"]
    result = {}
    for car in cars:
        for street in car["path"]:
            if street not in result:
                result[street] = 0
            result[street] += 1
    return result

################################################################
main()
