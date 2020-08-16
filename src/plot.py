import os

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

MAPBOX_TOKEN = os.environ['MAPBOX_TOKEN']


def plot_cost():
    lamp_type = ['mercury-vapour lamp', 'compact fluorescent lamp',
                 'light-emitting diode', 'high pressure sodium']
    total_cost = [424.5, 360, 210, 200]

    fig = go.Figure(
        data=[go.Bar(x=lamp_type, y=total_cost, marker_color=[
            'rgb(217, 139, 13)',
            'rgb(204, 148, 57)',
            'rgb(163, 129, 73)',
            'rgb(128, 114, 91)'])],
        layout_title_text="""Operational cost of different types of lights over 25,000 hours
        <br>Standardised to 1700 Lumen""",
        
    )
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor="rgb(50,50,50)",
        xaxis_title="Type of light",
        yaxis_title="Operational Cost",
        title_font_size=20,
        margin=dict(l=0, r=0, t=100, b=20)
    )
    fig.update_xaxes(title_font_size=17)
    fig.update_yaxes(title_font_size=17)
    fig.update_yaxes(tickprefix="$")
    return fig


def plot_lighting_map(light_og):
    light = light_og.copy()
    light['lamp_type'] = np.where((light['lamp_type'] == 'MV') & (
        light['wattage'] == 400), 'To 250 W LED', light['lamp_type'])
    light['lamp_type'] = np.where((light['lamp_type'] == 'MV') & (
        light['wattage'] == 125), 'To 18 W LED', light['lamp_type'])
    light['lamp_type'] = np.where((light['lamp_type'] == 'MV') & (
        light['wattage'] == 150), 'To 18 W LED', light['lamp_type'])

    fig = px.scatter_mapbox(light,
                            lat='latitude',
                            lon='longitude',
                            color='lamp_type',
                            size='wattage',
                            size_max=10,
                            title='Lighting in Hobart',
                            zoom=16,
                            template='plotly_dark',
                            )

    poi_small = light[light['lamp_type'] == 'To 250 W LED']
    fig.add_trace(go.Scattermapbox(
        lat=poi_small.latitude,
        lon=poi_small.longitude,
        mode='markers',
        marker=dict(symbol='square-stroked', size=10),
        showlegend=False
    ))

    poi_large = light[light['lamp_type'] == 'To 18 W LED']
    fig.add_trace(go.Scattermapbox(
        lat=poi_large.latitude,
        lon=poi_large.longitude,
        mode='markers',
        marker=dict(symbol='circle-stroked', size=10),
        showlegend=False
    ))

    fig.update_layout(
        paper_bgcolor="rgb(50,50,50)",
        title_font_size=20,
        height=600,
        mapbox=dict(
            accesstoken=MAPBOX_TOKEN,
            zoom=14,
            center=dict(lat=-42.88, lon=147.329),
            style='dark'
        ),
        margin=dict(l=0, r=0, t=80, b=20))

    return fig


def plot_lamp_hist(light, lamp_type):
    lamp_dict = {'MV': 'Mercury-vapour lamp', 'CFL': 'Compact fluorescent lamp',
                 'LED': 'Light-emitting diode', 'HPS': 'High Pressure Sodium'}
    full_type = lamp_dict[lamp_type]

    foo = light.loc[light['lamp_type'] == lamp_type,
                    'wattage'].value_counts().reset_index().sort_values('index')

    fig = go.Figure(
        data=[go.Bar(x=foo['index'], y=foo['wattage'])],
        layout_title_text=f"Distribution of {full_type} in Hobart",
        layout={'xaxis': {'type': 'category'}}
    )

    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor="rgb(50,50,50)",
        xaxis_title="Wattage",
        yaxis_title="Number of Lamps",
        title_font_size=20,
        margin=dict(l=0, r=0, t=100, b=20))
    fig.update_xaxes(title_font_size=17)
    fig.update_yaxes(title_font_size=17)
    return fig


def plot_solar(solar_df,year_select):
    year_dict = {'Year 1':[1],
    'Year 2':[2],
    'Year 3':[3],
    'Year 4':[4],
    'All Years':[1,2,3,4],
    }
        
    fig = px.scatter_mapbox(solar_df[solar_df['Implementation year'].isin(year_dict[year_select])],
                        lat='Latitude', 
                        lon='Longitude', 
                        color= 'Lamp type', 
                        size = 'Annual savings',
                        zoom=14)

    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor="rgb(50,50,50)",
        title_font_size=20,
        height=400,
        mapbox=dict(
            accesstoken=MAPBOX_TOKEN,
            zoom=12.5,
            center=dict(lat=-42.88, lon=147.329),
            style='dark'
        ),
        margin=dict(l=0, r=0, t=80, b=20))
    return fig