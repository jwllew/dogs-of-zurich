import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objs as go
from plotly.offline import plot
import json
import dash
from dash import Dash, html, dash_table, dcc, callback, Output, Input
from processBreeds import breeds


app = Dash(__name__)
app.title = 'Dogs of Zurich' 


def yearPicker(year, num):
    breeds['Sex of Dog'] = breeds['Sex of Dog'].replace('male', 'male dog')
    breeds['Sex of Dog'] = breeds['Sex of Dog'].replace('female', 'female dog')
    b = breeds[breeds['Year of Registration'] == int(year)]
    females = b[b['Sex of Dog']=='female dog']
    males = b[b['Sex of Dog']=='male dog']
    female_count = females.groupby('Breed').size().reset_index(name='count')
    male_count = males.groupby('Breed').size().reset_index(name='count')
    female_count = female_count.sort_values('count', ascending=False)
    male_count = male_count.sort_values('count', ascending=False)
    top_female_breeds = female_count.head(num)['Breed'].tolist()
    top_male_breeds = male_count.head(num)['Breed'].tolist()
    top_breeds = top_female_breeds + top_male_breeds
    df = breeds[breeds['Breed'].isin(top_breeds)]
    df = df.groupby([b['Breed'], 'Sex of Dog', 'Primary Colour', 'Year of Registration', 'Age of Owner']).size().reset_index(name='count')
    df['Breed Count'] = df.groupby('Breed')['count'].transform('sum')
    return df
default = yearPicker(2023,20)

def makeFig():
    fig = px.sunburst(
        data_frame=default,
        path=['Sex of Dog', 'Breed', 'Primary Colour'],
        values='count',
        color="Breed Count",
        color_continuous_scale=px.colors.sequential.Mint,
        range_color=[3,700],
        branchvalues="total",
        maxdepth=2,
    )
    fig.update_traces(
        legendwidth=0,
        insidetextorientation='radial',
        textinfo='label+percent parent',
        hovertemplate='%{root} %{parent} - <b>%{label}</b> - %{value}<br>total number (F&M) of this breed: %{customdata}',
        hoverlabel=dict(
        bgcolor='white',
        font=dict(size=16, color='black', family='Ubuntu, Arial, sans-serif'),
        align='auto',
        namelength=-1,
    ))
    fig.update_layout(
        coloraxis_showscale=True,
        showlegend=False,
        title_text='The dogs of Zürich<br>2023',
        title_x=0,
        title_y=0.85,
        font_family='Ubuntu, Arial, sans-serif',
        font_size=20,
    )
    fig.update_coloraxes(
        colorbar_len=0.4,
        colorbar_orientation="h",
        colorbar_thicknessmode="pixels",
        colorbar_thickness=10,
        colorbar_tickfont=dict(
            family='Ubuntu, Arial, sans-serif',
            size=12,
            ),
        colorbar_y=1,
        colorbar_x=0.8,

    )

    fig.add_annotation(
        x=0.05,
        y=0.0001,
        text='20 top breeds displayed<br>(male or female)',
        showarrow=False,
        font={
            'size': 16
        }
    )
    return fig

fig = makeFig()



numSteps = [2, 10, 20, 30, 50, 75, 100, 150, 200]
app.layout = html.Div([
    html.Div(children=[
        html.Br(),
        dcc.Slider(
            id='yearslider',
            min=breeds['Year of Registration'].min(),
            max=breeds['Year of Registration'].max(),
            value=breeds['Year of Registration'].max(),
            marks={str(year): {
                "label": f"{year}",
                "style": {"white-space": "nowrap", "font-family": 'Ubuntu, Arial, sans-serif', "font-size" : "20px"},
            } for year in breeds['Year of Registration'].unique()},
            step=None,
        ),
        html.Br(),
        dcc.RadioItems(['Default', 'Fully expanded'], 'Default', style={'color': '#44615D', "font-family": 'Ubuntu, Arial, sans-serif', "font-size" : "18px", 'justify':"center", 'align':"center"}, inline=True, id='radio'),
        dcc.Graph(figure=fig, id='graph',style={'width': '100%', 'height': '75vh', 'margin': 'auto'}),
        dcc.RadioItems(['Just dogs', 'Owner mode'], 'Just dogs', style={'color': '#44615D', "font-family": 'Ubuntu, Arial, sans-serif', "font-size" : "16px"}, inline=True, id='ownerradio'),
        html.Br(),
        html.H3("choose the number of breeds to display:",  style={'color': '#44615D', "font-family": 'Ubuntu, Arial, sans-serif', "font-size" : "16px", 'justify':"center", 'align':"center", 'margin':'auto'}),
        dcc.Slider(
            id='numslider', 
            min=min(numSteps), 
            max=max(numSteps), 
            value=20, 
            marks={int(n): {
                "label": f"{n}",
                "style": {"white-space": "nowrap", "font-family": 'Ubuntu, Arial, sans-serif', "font-size" : "20px"},
            } for n in numSteps},
        ),
    ]),
],  style={'width': '70%', 'margin':'auto'})

@callback(
    Output(component_id='graph', component_property='figure'),
    [Input(component_id='yearslider', component_property='value'),
    Input(component_id='numslider', component_property='value'),
    Input(component_id='radio', component_property='value'),
    Input(component_id='ownerradio', component_property='value')]
)


def update_graph(yearslider, numslider, radio, ownerradio):
    if ownerradio == 'Owner mode':
        if radio == 'Fully expanded':
            depthnum = 4
        else: 
            depthnum = 2
        df = yearPicker(int(yearslider), int(numslider)),
        fig = px.sunburst(
            data_frame=yearPicker(int(yearslider), int(numslider)),
            path=['Age of Owner', 'Breed', 'Primary Colour', 'Sex of Dog'],
            values='count',
            custom_data=['Breed Count'],
            color="Breed Count",
            color_continuous_scale=px.colors.sequential.Purp,
            range_color=[-30,700],
            branchvalues="total",
            maxdepth=depthnum,
            )
        fig.update_traces(
            legendwidth=0,
            insidetextorientation='radial',
            textinfo='label+percent parent',
            hovertemplate='%{root} %{parent} - <b>%{label}</b> - %{value} counts<br>total number (F&M) of dog breed: %{customdata}',
            hoverlabel=dict(
            bgcolor='white',
            font=dict(size=16, color='black', family='Ubuntu, Arial, sans-serif'),
            align='auto',
            namelength=-1,
        ))
        fig.update_layout(
            coloraxis_showscale=True,
            showlegend=False,
            title_text="Top dogs of Zürich<br>%s"%(yearslider),
            title_x=0.15,
            title_y=0.85,
            font_family='Ubuntu, Arial, sans-serif',
            font_size=20,
        )
        fig.update_coloraxes(
            colorbar_len=0.4,
            colorbar_orientation="h",
            colorbar_thicknessmode="pixels",
            colorbar_thickness=10,
            colorbar_tickfont=dict(
                family='Ubuntu, Arial, sans-serif',
                size=12,
                ),
            colorbar_y=1,
            colorbar_x=0.8,

        )
        fig.add_annotation(
            x=0.05,
            y=0.0001,
            text="%s top breeds displayed<br>(male or female)<br>grouped by owner's age"%(numslider),
            showarrow=False,
            font={
                'size': 16
            }
        )
        return fig
    else:
        if radio == 'Fully expanded':
            depthnum = 3
        else: 
            depthnum = 2
        df = yearPicker(int(yearslider), int(numslider)),
        fig = px.sunburst(
            data_frame=yearPicker(int(yearslider), int(numslider)),
            path=[ 'Sex of Dog', 'Breed', 'Primary Colour'],
            values='count',
            custom_data=['Breed Count'],
            color="Breed Count",
            color_continuous_scale=px.colors.sequential.Mint,
            range_color=[3,700],
            branchvalues="total",
            maxdepth=depthnum,
            )
        fig.update_traces(
            legendwidth=0,
            insidetextorientation='radial',
            textinfo='label+percent parent',
            hovertemplate='%{root} %{parent} - <b>%{label}</b> - %{value}<br>total number (F&M) of this breed: %{customdata}',
            hoverlabel=dict(
            bgcolor='white',
            font=dict(size=16, color='black', family='Ubuntu, Arial, sans-serif'),
            align='auto',
            namelength=-1,
        ))
        fig.update_layout(
            coloraxis_showscale=True,
            showlegend=False,
            title_text='Top dogs of Zürich<br>%s'%(yearslider),
            title_x=0.15,
            title_y=0.85,
            font_family='Ubuntu, Arial, sans-serif',
            font_size=20,
        )
        fig.update_coloraxes(
            colorbar_len=0.4,
            colorbar_orientation="h",
            colorbar_thicknessmode="pixels",
            colorbar_thickness=10,
            colorbar_tickfont=dict(
                family='Ubuntu, Arial, sans-serif',
                size=12,
                ),
            colorbar_y=1,
            colorbar_x=0.8,

        )
        fig.add_annotation(
            x=0.05,
            y=0.0001,
            text='%s top breeds displayed<br>(male or female)'%(numslider),
            showarrow=False,
            font={
                'size': 16
            }
        )
        return fig


if __name__ == '__main__':
    app.run_server(debug=True)
