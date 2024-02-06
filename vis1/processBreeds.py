import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objs as go
from plotly.offline import plot
import json
from maps import colourMap, breedMap, agesMap

# scrubbing raw data

# open csv as a pandas dataframe
breedcsv = "static/Hunderassen.csv"
breeds=pd.read_csv(breedcsv)

# remove unnecessary columns
breeds = breeds.iloc[:, [0, 3, 6, 14, 23, 27, 29]]

# rename columns to English
breeds = breeds.rename(columns={'StichtagDatJahr' : 'Year of Registration', 'AlterV10Lang':'Age of Owner', 'SexLang' : 'Sex of Owner', 'Rasse1Text' : 'Breed', 'AlterVHundCd':'Age of Dog', 'SexHundLang':'Sex of Dog', 'HundefarbeText' : 'Primary Colour'})

# remove unknown data
breeds = breeds.loc[~breeds['Breed'].str.contains('Unbekannt')].reset_index(drop=True)
breeds = breeds.loc[~breeds['Age of Owner'].str.contains('Unbekannt')].reset_index(drop=True)

# convert values in numerical columns to int for compatibility
num_cols = breeds.select_dtypes(include=["int64", "float64"]).columns
breeds[num_cols] = breeds[num_cols].astype(int)

# formatting kept data

# format colours to lowercase for mapping
breeds['Primary Colour'] = breeds['Primary Colour'].str.lower()
# map german entries to english
breeds.replace(colourMap, inplace=True)
breeds.replace(breedMap, inplace=True)
breeds.replace(agesMap, inplace=True)
# format colours and breeds to titlecase
breeds['Primary Colour'] = breeds['Primary Colour'].str.title()
breeds['Breed'] = breeds['Breed'].str.title()
breeds.head()


def topDogs():
    females = breeds[breeds['Sex of Dog']=='female']
    males = breeds[breeds['Sex of Dog']=='male']
    female_count = females.groupby('Breed').size().reset_index(name='count')
    male_count = males.groupby('Breed').size().reset_index(name='count')
    female_count = female_count.sort_values('count', ascending=False)
    male_count = male_count.sort_values('count', ascending=False)
    top_female_breeds = female_count.head(30)['Breed'].tolist()
    top_male_breeds = male_count.head(30)['Breed'].tolist()
    top_breeds = top_female_breeds + top_male_breeds
    df = breeds[breeds['Breed'].isin(top_breeds)]
#     df = df[df['Year of Registration'] == y]
    return df
b = topDogs()
top25 = b.groupby([b['Breed'], 'Sex of Dog', 'Primary Colour', 'Year of Registration']).size().reset_index(name='count')
top25 = top25.sort_values(by='count', ascending=False)
top25.head()
# def sepYear(d, year):
#     yearSet = d[d['Year of Registration']==year]
#     return yearSet

# def showFig(b, name):
#     col_counts = b.groupby(['Primary Colour']).size().reset_index(name='count')
#     df_counts = b.groupby([b['Breed'], 'Sex of Dog', 'Primary Colour', 'Year of Registration']).size().reset_index(name='count')
#     df_counts = df_counts.sort_values(by='count', ascending=False)
#     df_counts['percentage'] = df_counts['count'] / len(b) * 100
#     df_counts['percentage'] = df_counts['percentage'].astype(int)

#     df_counts = df_counts.assign(title=name)
#     fig = px.sunburst(
#         data_frame=df_counts,
#         path=['Year of Registration', 'Sex of Dog', 'Breed', 'Primary Colour'],
#         values='count',
#         custom_data=['percentage'],
# #         color_discrete_sequence=px.colors.qualitative.Pastel,
#         color="count",
#         color_continuous_scale=px.colors.sequential.BuGn,
#         range_color=[0,150],
#         branchvalues="total",
#         maxdepth=3,
#     )
#     fig.update_traces(
#         legendwidth=0,
#         insidetextorientation='radial',
#         textinfo='label+percent parent',
# #         hoverinfo='skip',
#         hovertemplate='<b>%{label}</b><br>%{parent}<br>Number of dogs with this criteria: %{value}',
#         hoverlabel=dict(
#         bgcolor='white',
#         font=dict(size=16, color='black', family='Ubuntu'),
#         align='auto',
#         namelength=-1,
#     ))
#     # customize font and legend orientation & position
#     fig.update_layout(
#         coloraxis_showscale=False,
#         showlegend=False,
#         title_text='the 20 most popular dog breeds of Zurich - %s'%name,
#         title_x=0.5,
#         title_y=0.03,
#         font_family="Arial",
#         font_size=28,
#     )
#     fig.show()
#     plot(fig, include_plotlyjs='directory', filename='output/green_fig_%s.html' % (name))

# for y in yearsList:
#     dataToFig = sepYear(top_dogs_df, y)
#     showFig(dataToFig, str(y))
# showFig(top25, 'all')


# dataToFig = sepYear(top_dogs_df, 2023)
# showFig(dataToFig, str(2023))
