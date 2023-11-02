from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
import os

app = Dash(__name__)

cycleList = [i for i in range(10000,20000,1000)]
# pressures = np.concatenate((np.linspace(0.1,0.9,9)*1e6,np.linspace(1,10,10)*1e6),axis=None)
# pressures = np.linspace(5000,65000,13)
pressures = [5000]

app.layout = html.Div([
    html.Div(
        children=[
            html.Div([
                html.H3("Cycle Number",style={"text-align":"center"}),
                dcc.Dropdown(cycleList, min(cycleList), id='cycle-dropdown',clearable=False),
            ],style={"width":"30vw","float": "left"}),
            html.Div([
                html.H3("Projection direction",style={"text-align":"center"}),
                dcc.Dropdown(['X','Y','Z'], 'Z', id='cycle-dropdown-2',clearable=False)
            ],style={"width":"30vw","float": "left"}),
            html.Div([
                html.H3("Choose Pressure",style={"text-align":"center"}),
                dcc.Dropdown(pressures, pressures[0], id='pressure-dropdown',clearable=False)
            ],style={"width":"30vw","float": "left"}),
        ],style={'display': 'block',"align-vertical":'top',"margin":"0px auto"}
    ),
    html.Div(
        children=[
            dcc.Graph(id='graph-with-dropdown',style={"text-align": "center","height":"90vh"})
        ],style={'display': 'inline-block',"width":"48vw"} 
    ),
    html.Div(
        children=[
            dcc.Graph(id='graph-with-dropdown-2',style={"text-align": "center","height":"90vh"})
        ],style={'display': 'inline-block',"width":"48vw"} 
    ),
    html.Div(
        children=[
            dcc.Graph(id='graph-with-dropdown-3',style={"text-align": "center","height":"90vh"})
        ],style={'display': 'inline-block',"width":"48vw"} 
    ),
    
])
# 
@app.callback(
    Output("graph-with-dropdown", "figure"), 
    Input("cycle-dropdown", "value"),
    Input("pressure-dropdown", "value"))
def update_bar_chart(selected_cycle,selected_pressure):
    filePath = os.path.join(os.path.expanduser('~'),'Documents/Phd_Research/Molecular Simulation/GCMCBasicCPP/GrapheneArgonResults/MoleculePositions')
    df = pd.read_csv(os.path.join(filePath,f'position_{selected_cycle}_{selected_pressure:.2f}_87.00.csv')) # replace with your own data source
    df.columns = ['x','y','z']
    fig = px.scatter_3d(df, 
        x='x', y='y', z='z',color='z')
    # fig = px.scatter(df,x='x',y='y')
    return fig

@app.callback(
    Output("graph-with-dropdown-2", "figure"),
    Input("cycle-dropdown", "value"), 
    Input("cycle-dropdown-2", "value"),
    Input("pressure-dropdown", "value"))
def update_bar_chart_2(selected_cycle,projection_dir,selected_pressure):
    filePath = os.path.join(os.path.expanduser('~'),'Documents/Phd_Research/Molecular Simulation/GCMCBasicCPP/GrapheneArgonResults/MoleculePositions')
    df = pd.read_csv(os.path.join(filePath,f'position_{selected_cycle}_{selected_pressure:.2f}_87.00.csv')) # replace with your own data source
    df.columns = ['x','y','z']
    # fig = px.scatter_3d(df, 
    #     x='x', y='y', z='z')
    if projection_dir == 'Z':
        fig = px.scatter(df, x='x',y='y',color='z')
    elif projection_dir == 'Y':
        fig = px.scatter(df, x='x',y='z',color='y')
    else:
        fig = px.scatter(df, x='y',y='z',color='x')
    
    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        # 'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        })
    fig.update_xaxes(ticks="inside", tickwidth=4, tickcolor='black', ticklen=10)
    fig.update_yaxes(ticks="inside", tickwidth=4, tickcolor='black', ticklen=10)

    fig.update_xaxes(minor_ticks="inside",minor=dict(ticklen=6, tickcolor="black"))
    fig.update_yaxes(minor_ticks="inside",minor=dict(ticklen=6, tickcolor="black"))
    
    fig.update_xaxes(showline=True, linewidth=2, linecolor='black', mirror="all")
    fig.update_yaxes(showline=True, linewidth=2, linecolor='black', mirror="all")

    # fig.update_xaxes(range=[0,26])
    # fig.update_yaxes(range=[0,26])

    return fig

### For graphene line plot
@app.callback(
    Output("graph-with-dropdown-3", "figure"),
    Input("pressure-dropdown", "value"))
def update_bar_chart_2(selected_pressure):
    filePath = os.path.join(os.path.expanduser('~'),'Documents/Phd_Research/Molecular Simulation/GCMCBasicCPP/GrapheneArgonResults/NumberDensity')
    df = pd.read_csv(os.path.join(filePath,f'NumberDensity_{selected_pressure:.2f}_87.00.csv')) # replace with your own data source
    df.columns = ['zPositions','avgNumOfMethanesAtZ']
    # fig = px.scatter_3d(df, 
    #     x='x', y='y', z='z')
    
    fig = px.line(df,x='zPositions',y='avgNumOfMethanesAtZ')
    
    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        # 'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        })
    fig.update_xaxes(ticks="inside", tickwidth=4, tickcolor='black', ticklen=10)
    fig.update_yaxes(ticks="inside", tickwidth=4, tickcolor='black', ticklen=10)

    fig.update_xaxes(minor_ticks="inside",minor=dict(ticklen=6, tickcolor="black"))
    fig.update_yaxes(minor_ticks="inside",minor=dict(ticklen=6, tickcolor="black"))
    
    fig.update_xaxes(showline=True, linewidth=2, linecolor='black', mirror="all")
    fig.update_yaxes(showline=True, linewidth=2, linecolor='black', mirror="all")

    # fig.update_xaxes(range=[0,26])
    # fig.update_yaxes(range=[0,26])

    return fig

app.run_server(debug=False)