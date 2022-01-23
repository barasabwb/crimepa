
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd


# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})
df2 = pd.read_csv("dataset/kenya_crime2.csv")

#No. of crimes per year
yc = pd.DataFrame([df2['YEAR'], df2['TYPE']]).T
ycTotal = yc.groupby(['YEAR']).count().reset_index()
ycTotal.columns = ['Year','Total']

#Average No. of crimes per Neighbourhood
nc = pd.DataFrame([df2['YEAR'], df2['NEIGHBOURHOOD'], df2['TYPE']]).T 
ncavg = nc.groupby(['YEAR','NEIGHBOURHOOD']).count().reset_index()
ncavg = ncavg.drop('YEAR', axis = 1)
ncavg.columns = ["Neighborhood", "Avg"]
ncavg = ncavg.groupby(['Neighborhood'])['Avg'].mean()

#interactive Crime by location
cbl = pd.DataFrame([df2['YEAR'], df2['NEIGHBOURHOOD'], df2['TYPE']]).T 
subdata = df2.groupby(['YEAR','NEIGHBOURHOOD']).count().reset_index(drop=False)
subdata = subdata[['YEAR','NEIGHBOURHOOD','TYPE']]
subdata.columns = ['YEAR','NEIGHBOURHOOD','Counts']


def create_dash_application(flask_app):
 dash_app = dash.Dash(server = flask_app,name= "Dashboard", url_base_pathname="/dash/")
 
 
 dash_app.layout = html.Div(children=[
    html.Div([
    html.H1(children='Dash Visualizations'),

    html.Div(children='''
        Number of Crimes each Year
    '''),

    dcc.Graph(
        id='example-graph',
        figure=px.bar(ycTotal, x="Year", y="Total", color="Year")
    )]),
    html.Div([
    # html.H1(children='Hello Dash'),

    html.Div(children='''
        Average Number of Crimes Per Neighbourhood per year
    '''),

    dcc.Graph(
        id='example-graph2',
        figure=px.bar(ncavg)
    )]),   
    html.Div([
    # html.H1(children='Hello Dash'),

    html.Div(children='''
        Number of Crimes Per Neighbourhood each year
    '''),


    dcc.Graph(
        id='example-graph3',
        figure=px.bar(subdata ,x='NEIGHBOURHOOD',y='Counts',color='YEAR',title='Total Crimes by Neighbourhood',color_discrete_sequence=['blue','red'])
    )
 
    ])
    
    
   ]
   )



 return dash_app


