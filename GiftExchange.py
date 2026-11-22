"""Read in history of Santa and Person, output random list for current year"""

import random
import yaml
import math
from datetime import datetime

families = ('Shibata', 'Meinhart')


for family in families:
        
    with open(f"{family}_cousins.yaml", "r") as yaml_input:
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
            history = data["history"][person] if data["history"][person] else {}
    
            history_len = len(history)
            i_year = 1
    
            # Weight assignments based on history (skip when there is only a
            # single year of history, since log base 1 is undefined).
            if history_len > 1:
                for rx in history:
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
    
    family_colors = ["lightgreen", "lightblue", "#FFCC99"]  
    
    html = []
    html.append("<!DOCTYPE html>")
    html.append("<html lang=\"en\">")
    html.append("<head>")
    html.append("<meta charset=\"UTF-8\">")
    html.append(f"<title>Gift Exchange - {family}</title>")
    html.append("<style>")
    html.append("body { font-family: Arial, sans-serif; margin: 2em; }")
    html.append("h2 { font-family: Arial, sans-serif; }")
    html.append("table { border-collapse: collapse; margin-top: 1em; }")
    html.append("th, td { border: 1px solid #999; padding: 6px 12px; text-align: left; }")
    html.append("th { background: #444; color: #fff; }")
    html.append("tr.blank td { height: 14px; border: none; padding: 0; }")
    html.append("</style>")
    html.append("</head>")
    html.append("<body>")
    html.append(f"<h2>Gift Exchange - {family} {str(datetime.now().year)}</h2>")
    html.append("<table>")
    html.append("<tr><th>Family</th><th>Santa</th><th>Person</th></tr>")
    html.append("<tr class=\"blank\"><td colspan=\"3\"></td></tr>")
    
    family_color_map = {}
    color_index = 0
    i_list = 0
    for exclude_group in data["exclude_lists"]:
        i_list += 1
        if i_list not in family_color_map:
            family_color_map[i_list] = family_colors[color_index % len(family_colors)]
            color_index += 1
        color = family_color_map[i_list]
        for person in exclude_group:
            html.append(f"<tr style=\"background-color: {color};\">")
            html.append(f"<td>{i_list}</td><td>{person}</td>"
                        f"<td>{data['history'][person][-1]}</td></tr>")
        html.append("<tr class=\"blank\"><td colspan=\"3\"></td></tr>")
    
    html.append("</table>")
    html.append("</body>")
    html.append("</html>")
    
    with open(f"{family}.html", "w") as output:
        output.write("\n".join(html))
    
    
    with open(f"{family}_cousins.yaml", "w") as yaml_output:
        yaml.dump(data, yaml_output)
    
