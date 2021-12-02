from dash import html, dcc
import dash_bootstrap_components as dbc
from dc import *

### COMPONENTS ###
# Year Range Slider
year_slider = dcc.RangeSlider(
    min=years.min(),
    max=years.max(),
    value=[1999, 2019],
    tooltip={"placement": "bottom", "always_visible": True},
    id = 'yr_slider',
)

# Dairy Product Multi Dropdown
dairy_prod_dropdown = dcc.Dropdown(
    id='dairy_prod_dropdown',
    options = [{"label": x, "value": x}
                for x in dairy_prod],
    value= dairy_prod,
    multi=True,
)

egg_prod_dropdown = dcc.Dropdown(
    id='egg_prod_dropdown',
    options = [{"label": x, "value": x}
                for x in egg_prod],
    value= egg_prod,
    multi=True,
)

produce_view_dropdown = dcc.Dropdown(
    id='produce-view-dropdown',
    options= [
        {"label":'Total', 'value':'Total'},
        {"label":'Fruit', 'value':'Fruit'},
        {"label":'Vegetable', 'value':'Vegetable'},
        {"label":'Fresh', 'value':'Fresh'},
        {"label":'Processed', 'value':'Processed'},
    ],
    value='Total',
)

grains_prod_dropdown = dcc.Dropdown(
    id='grains_prod_dropdown',
    options = [{"label": x, "value": x}
                for x in grains_prod],
    value= grains_prod,
    multi=True,
)


# Tabs for the Product Categories
product_categories = dbc.Tabs(
    [
        dbc.Tab(label='Dairy',tab_id='tab-1',),
        dbc.Tab(label='Eggs',tab_id='tab-2'),
        dbc.Tab(label='Produce',tab_id='tab-3'),
        dbc.Tab(label='Grains',tab_id='tab-4'),
        dbc.Tab(label='Nuts',tab_id='tab-5'),
        dbc.Tab(label='Meat & Poultry',tab_id='tab-6'),
        dbc.Tab(label='Seafood',tab_id='tab-7'),
        dbc.Tab(label='Sugars & Sweeteners',tab_id='tab-8'),
        dbc.Tab(label='Fats & Oils',tab_id='tab-9'),
    ],
    id='product_categories',
    active_tab="tab-1",
)

tab_dict = {"tab-1":'dairy',
            "tab-2":'eggs',
            "tab-3":'produce',
            "tab-4":'grains',
            "tab-5":'nuts',
            "tab-6":"meat_poultry",
            "tab-7":"seafood",
            "tab-8":"sugars",
            "tab-9":'fats_oils',}


### COMING SOON / UNDER CONSTRUCTION CONTENT ###
under_construct = dbc.Col(
    [
        dbc.Row(
            [
                html.H1('UNDER CONSTRUCTION', className='text-bold'),
                html.P('The charts here are still being developed. Please check back soon!')
            ],
        )
    ],
    class_name='bg-primary shadow rounded-3 text-white text-center d-flex justify-content-center align-items-center',
    style={'height':'75vh'},
)


### Layout components that will be rendered as part of the callback for each tab ###
dairy = dbc.Container(
    dbc.Row(
        [
            dbc.Col(
                dcc.Graph(id='trends', className='shadow'),
                md=9,
            ),
            dbc.Col(
                dairy_prod_dropdown,
                md=3,
            )
        ],
        className='py-3'
    ),
)

eggs = dbc.Container(
    dbc.Row(
        [
            dbc.Col(
                dcc.Graph(id='trends-eggs', className='shadow'),
                md=9,
            ),
            dbc.Col(
                egg_prod_dropdown,
                md=3,
            )
        ],
        className='py-3'
    ),
)

produce = dbc.Container(
    dbc.Row(
        [
            dbc.Col(
                dcc.Graph(id='trends-produce', className='shadow'),
                md=9,
            ),
            dbc.Col(
                [
                    produce_view_dropdown,
                    dcc.Dropdown(id='produce_prod_dropdown', multi=True),
                ],
                md=3,
            )
        ],
        className='py-3'
    ),
)

grains = dbc.Container(
    dbc.Row(
        [
            dbc.Col(
                dcc.Graph(id='trends-grains', className='shadow'),
                md=9,
            ),
            dbc.Col(
                grains_prod_dropdown,
                md=3,
            )
        ],
        className='py-3'
    ),
)

nuts = dbc.Container(
    dbc.Row(
        [
            under_construct,
            # dbc.Col(
            #     dcc.Graph(id='trends-nuts', className='shadow'),
            #     md=9,
            # ),
            # dbc.Col(
            #     html.P('Placeholder for dropdown'),
            #     md=3,
            # )
        ],
        className='py-3'
    ),
)

meat_poultry = dbc.Container(
    dbc.Row(
        [
            under_construct,
            # dbc.Col(
            #     dcc.Graph(id='trends-meat-poultry', className='shadow'),
            #     md=9,
            # ),
            # dbc.Col(
            #     html.P('Placeholder for dropdown'),
            #     md=3,
            # )
        ],
        className='py-3'
    ),
)

seafood = dbc.Container(
    dbc.Row(
        [
            under_construct,
            # dbc.Col(
            #     dcc.Graph(id='trends-seafood', className='shadow'),
            #     md=9,
            # ),
            # dbc.Col(
            #     html.P('Placeholder for dropdown'),
            #     md=3,
            # )
        ],
        className='py-3'
    ),
)

sugars = dbc.Container(
    dbc.Row(
        [
            under_construct,
            # dbc.Col(
            #     dcc.Graph(id='trends-sugars', className='shadow'),
            #     md=9,
            # ),
            # dbc.Col(
            #     html.P('Placeholder for dropdown'),
            #     md=3,
            # )
        ],
        className='py-3'
    ),
)

fats_oils = dbc.Container(
    dbc.Row(
        [
            under_construct,
            # dbc.Col(
            #     dcc.Graph(id='trends-fats_oils', className='shadow'),
            #     md=9,
            # ),
            # dbc.Col(
            #     html.P('Placeholder for dropdown'),
            #     md=3,
            # )
        ],
        className='py-3'
    ),
)