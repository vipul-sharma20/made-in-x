import os
import csv
from typing import Dict, Tuple
from collections import Counter

import plotly.graph_objects as go
import plotly.express as px
import chart_studio
import chart_studio.plotly as py


def prepare_country_data(purchase_dict) -> Tuple[Dict, Dict]:
    country_map: Dict = {}

    with open("made-in-x.csv", newline="") as csvfile:
        next(csvfile)
        csv_reader = csv.reader(csvfile, delimiter=",", quotechar="|")
        for row in csv_reader:
            *meta, category, country, purchased_from, quantity = row
            country_map.setdefault(
                country,
                {
                    "category": [],
                    "purchased_from": [],
                    "quantity": [],
                },
            )

            if category != "electronics":
                for i in range(int(quantity)):
                    country_map[country]["category"].append(category)
            else:
                country_map[country]["category"].append(category)
            country_map[country]["purchased_from"].append(purchased_from)
            country_map[country]["quantity"].append(quantity)

            if not purchase_dict[purchased_from].get(category):
                purchase_dict[purchased_from][category] = (
                    1 if category == "electronics" else int(quantity)
                )
            else:
                purchase_dict[purchased_from][category] += (
                    1 if category == "electronics" else int(quantity)
                )

    return country_map


def plot_countries(country_map: Dict, categories: set) -> None:
    countries = country_map.keys()

    categories_count: Dict = {}
    bars: List = []

    for country in countries:
        categories_count[country] = Counter(country_map[country]["category"])

    for category in categories:

        category_count = []
        for k in categories_count:
            category_count.append(categories_count[k].get(category, 0))

        bars.append(go.Bar(name=category, x=list(country_map.keys()), y=category_count))

    fig = go.Figure(data=bars)

    fig.update_layout(
        barmode="stack",
        xaxis={"categoryorder": "total descending", 'fixedrange':True},
        yaxis={'fixedrange':True},
        title_text='Country of Origin<br><i style="font-size:75%;">(Click legends to toggle/isolate categories)</i>',
        title_x=0.7,
        title_y=0.75,
        title_font_size=20,
        legend=dict(yanchor="top", y=0.95, xanchor="right", x=0.95),
    )
    fig.show()
    py.plot(fig, filename='made_in_x', auto_open=True)


def plot_purchase(country_map: Dict, purchase_dict: Dict, categories: set) -> None:
    bars: List = []
    purchase_count_list: Dict = {}

    for country in country_map.keys():
        purchase_count_list[country] = Counter(country_map[country]["purchased_from"])

    for category in categories:

        category_count: List = []
        for k in purchase_dict:
            category_count.append(purchase_dict[k].get(category))

        bars.append(
            go.Bar(name=category, x=list(purchase_dict.keys()), y=category_count)
        )

    fig = go.Figure(data=bars)

    fig.update_layout(
        barmode="stack",
        xaxis={"categoryorder": "total descending", 'fixedrange':True},
        yaxis={'fixedrange':True},
        title_text='Purchased From<br><i style="font-size:75%;">(Click legends to toggle/isolate categories)</i>',
        title_x=0.7,
        title_y=0.75,
        title_font_size=20,
        legend=dict(yanchor="top", y=0.95, xanchor="right", x=0.95),
    )
    fig.show()
    py.plot(fig, filename='purchase_from', auto_open=True)


if __name__ == "__main__":
    username = 'vipul'
    api_key = os.environ.get("PLOTLY_API_KEY")
    chart_studio.tools.set_credentials_file(username=username, api_key=api_key)

    with open("made-in-x.csv", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        data = {}
        for row in reader:
          for header, value in row.items():
            try:
              data[header].append(value)
            except KeyError:
              data[header] = [value]

    purchase_options = data["source"]
    categories = set(data["category"])
    purchase_dict = {option: {} for option in purchase_options}
    print(purchase_dict)

    country_map = prepare_country_data(purchase_dict)

    plot_countries(country_map, categories)
    plot_purchase(country_map, purchase_dict, categories)
