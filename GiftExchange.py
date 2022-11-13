"""Read in history of Santa and Person, output random list for current year"""


import random
import yaml
import math


with open("GiftExchange_Shibata_Cousins.yaml", "r") as yaml_input:
    data = yaml.safe_load(yaml_input)


def create_rx_dict(santa):
    person_list = []
    for exclude_list in data["exclude_lists"]:
        if santa not in exclude_list:
            person_list += exclude_list

    rx_dict = {}
    for person in person_list:
        rx_dict[person] = 1.0
    return rx_dict


find_list = True
find_loops = 1

while find_list:
    find_list = False
    picked_list = []

    for person in data["history"]:
        rx_dict = create_rx_dict(person)

        # Adjust for previous years
        history_len = len(data["history"][person])
        i_year = 1
        for rx in data["history"][person]:
            if rx in rx_dict:
                rx_dict[rx] *= math.log(history_len + 1 - i_year, history_len)
            i_year += 1

        # Apply random adjustment
        for rx in rx_dict:
            if rx in picked_list:
                adjustment_fact = 0.0
            else:
                adjustment_fact = random.random()

            rx_dict[rx] *= adjustment_fact

        rx = max(rx_dict, key=lambda x: rx_dict[x])

        # check for no solution
        if rx_dict[rx] <= 0.0:
            find_loops += 1
            find_list = True
            break

        picked_list.append(rx)

print(picked_list)
print(find_loops)


for i_list, person in enumerate(data["history"]):
    data["history"][person].append(picked_list[i_list])

i_list = 0
with open("output.csv", "w") as output:
    output.write("Family,Santa,Person\n")
    for list in data["exclude_lists"]:
        output.write("\n")
        i_list += 1
        for person in list:
            output.write("{},{},{}\n".format(i_list, person, data["history"][person][-1]))


with open("GiftExchange_Shibata_Cousins.yaml", "w") as yaml_output:
    yaml.dump(data, yaml_output)
