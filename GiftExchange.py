"""Read in history of Santa and Person, output random list for current year"""


import random
import yaml
import math


data = {
    "exclude_lists": [["Marie", "Joey", "Stevie", "Sam", "Tim", "Annie"],
                      ["JJ", "Grace", "Joy", "Mark"],
                      ["TJ", "Abby", "Eli", "Hope"]],
    "history": {
        "Marie": ["TJ", "Abby", "JJ", "Grace", "Eli", "TJ", "Mark", "Joy", "Hope"],
        "JJ": ["Sam", "Marie", "Stevie", "TJ", "Tim", "Joey", "Abby", "Sam", "Stevie"],
        "Joey": ["Joy", "Grace", "Mark", "Eli", "Abby", "Mark", "Joy", "JJ", "TJ"],
        "Grace": ["Stevie", "Sam", "Marie", "Joey", "Sam", "Tim", "Stevie", "Annie", "Joey"],
        "TJ": ["Marie", "Stevie", "Joey", "JJ", "Joy", "Grace", "Marie", "Stevie", "JJ"],
        "Stevie": ["Abby", "JJ", "Grace", "Joy", "Mark", "Eli", "TJ", "Abby", "Grace"],
        "Joy": ["Joey", "TJ", "Abby", "Stevie", "Marie", "Sam", "Tim", "Joey", "Abby"],
        "Abby": ["Grace", "Mark", "Joy", "Sam", "Stevie", "JJ", "Joey", "Tim", "Marie"],
        "Sam": ["JJ", "Joy", "TJ", "Mark", "Grace", "Abby", "Eli", "TJ", "Mark"],
        "Mark": ["NA", "Joey", "Sam", "Abby", "TJ", "Stevie", "Annie", "Marie", "Sam"],
        "Eli": ["NA", "NA", "NA", "Marie", "Joey", "Marie", "Sam", "Grace", "Annie"],
        "Tim": ["NA", "NA", "NA", "NA", "JJ", "Joy", "Grace", "Mark", "Eli"],
        "Annie": ["NA", "NA", "NA", "NA", "NA", "NA", "JJ", "Eli", "Joy"],
        "Hope": ["NA", "NA", "NA", "NA", "NA", "NA", "NA", "NA", "Tim"]
    }
}


# with open("GiftExchange_Shibata_Cousins.yaml", "r") as yaml_input:
#     data = yaml.safe_load(yaml_input)

exclude_lists = data["exclude_lists"]
history = data["history"]


def create_rx_dict(santa):
    person_list = []
    for exclude_list in exclude_lists:
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

    for person in history:
        rx_dict = create_rx_dict(person)

        # Adjust for previous years
        history_len = len(history[person])
        i_year = 1
        for rx in history[person]:
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

with open("GiftExchange_Shibata_Cousins.yaml", "w") as yaml_output:
    yaml.dump(data, yaml_output)
