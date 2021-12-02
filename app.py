import dash
from dash import Input, Output, State, html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from dc import *
from components import *

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
server = app.server

### LAYOUT ###
app.layout = html.Div(
    [
        dbc.Container(
            [
                html.H1('US Food Consumption', className="display-3"),
                html.P(
                    "How much does the average American consume across key food categories? "
                    "Find out using this interactive dashboard.",
                    className="lead",
                ),
                html.Hr(className="my-2"),
                html.P(
                    "The data used here is from the USDA ERS Food Availability (Per Capita) Data System (FADS). "
                    "The data serve as proxies for actual consumption at the national level. " 
                    "To learn more about the dataset, please visit the following link.",
                    className="col-md-9",
                ),
                html.P(
                    dbc.Button("Learn more", color="success", 
                    href="https://www.ers.usda.gov/data-products/food-availability-per-capita-data-system/"),
                    className="lead",
                ),
            ],
            className="py-3 px-4 bg-primary mt-3 rounded-3 text-white",
        ),

        dbc.Container(
            [
                product_categories,
            ],
            className="py-3",
        ),

        dbc.Container(
            dbc.Row(
                [
                    dbc.Col(
                        html.H5('Select the Year Range:'),
                        md=3,
                    ),
                    dbc.Col(
                        year_slider,
                        md=9,
                        class_name='row align-items-center',
                    )
                ],
                class_name='py-3'
            )
        ),

        html.Div(id='tab-content'),

    ],
    className='bg-white',
)


### CALLBACKS ###
@app.callback(
    Output('tab-content','children'),
    Input('product_categories','active_tab')
)
def render_content(tab):
    if tab in tab_dict:
        content = eval(tab_dict[tab])
        return content

# callback for dairy products main line chart
@app.callback(
    Output("trends","figure"),
    Input('yr_slider','value'),
    Input('dairy_prod_dropdown','value')
)
def update_figure(year, products):
    data = dairy_prod_pcc.loc[dairy_prod_pcc['Year'].between(year[0],year[1],inclusive='both')]
    mask = data.Attribute.isin(products)
    figure = px.line(data[mask], x="Year", y="Value", color='Attribute', 
                    title="Dairy Product Consumption", template="simple_white",
                    labels={"Value":"Pounds per Capita", "Attribute":"Product"},
                    )
    return figure

# callback for egg line chart
@app.callback(
    Output("trends-eggs","figure"),
    Input('yr_slider','value'),
    Input('egg_prod_dropdown','value')
)
def update_figure(year, products):
    data = eggs_pcc.loc[eggs_pcc['Year'].between(year[0],year[1],inclusive='both')]
    mask = data.Attribute.isin(products)
    figure = px.line(data[mask], x="Year", y="Value", color='Attribute', 
                    title="Egg Consumption", template="simple_white",
                    labels={"Value":"Number of Eggs per Capita", "Attribute":"Category"},
                    )
    return figure

# callback for produce product options based on view selection
@app.callback(
    Output("produce_prod_dropdown",'options'),
    Output('produce_prod_dropdown','value'),
    Input('produce-view-dropdown','value')
)
def update_prod_dropdown(view):
    if view == 'Total':
        data = produce_pcc.loc[produce_pcc.Aggregation == view]
        produce_prod = data.Product.unique()
        options = [{"label": x, "value": x}
                for x in produce_prod]
        return options, produce_prod
    elif view == 'Fruit' or view == 'Vegetable':
        data = produce_pcc.loc[produce_pcc.Category == view]
        produce_prod = data.Product.unique()
        options = [{"label": x, "value": x}
                for x in produce_prod]
        return options, produce_prod
    elif view == 'Processed' or view == 'Fresh':
        data = produce_pcc.loc[produce_pcc.Type == view]
        produce_prod = data.Product.unique()
        options = [{"label": x, "value": x}
                for x in produce_prod]
        return options, produce_prod

# callback for produce line chart based on view selection and dropdown options
@app.callback(
    Output("trends-produce","figure"),
    Input('yr_slider','value'),
    Input('produce-view-dropdown','value'),
    Input('produce_prod_dropdown','value')
)
def update_figure(year, view, products):
    data = produce_pcc.loc[produce_pcc['Year'].between(year[0],year[1],inclusive='both')]
    if view == 'Total':
        data = data.loc[data.Aggregation == view]
        mask = data.Product.isin(products)
        figure = px.line(data[mask], x="Year", y="Value", color='Product', 
                    title="Produce Consumption", template="simple_white",
                    labels={"Value":"Pounds per Capita"},
                    )
        return figure
    elif view == 'Fruit' or view == 'Vegetable':
        data = data.loc[data.Category == view]
        mask = data.Product.isin(products)
        figure = px.line(data[mask], x="Year", y="Value", color='Product', 
                    title= view+" Consumption", template="simple_white",
                    labels={"Value":"Pounds per Capita"},
                    )
        return figure
    elif view == 'Processed' or view == 'Fresh':
        data = data.loc[data.Type == view]
        mask = data.Product.isin(products)
        figure = px.line(data[mask], x="Year", y="Value", color='Product', 
                    title= view+" Produce Consumption", template="simple_white",
                    labels={"Value":"Pounds per Capita"},
                    )
        return figure

# callback for grain line chart
@app.callback(
    Output("trends-grains","figure"),
    Input('yr_slider','value'),
    Input('grains_prod_dropdown','value')
)
def update_figure(year, products):
    data = grains_pcc.loc[grains_pcc['Year'].between(year[0],year[1],inclusive='both')]
    mask = data.Attribute.isin(products)
    figure = px.line(data[mask], x="Year", y="Value", color='Attribute', 
                    title="Grain Consumption", template="simple_white",
                    labels={"Value":"Pounds per Capita", "Attribute":"Product"},
                    )
    return figure

if __name__ == "__main__":
    app.run_server()