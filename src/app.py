# -*- coding: utf-8 -*-
# Import libraries
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import calplot
from plotly_calplot import calplot
import plotly.figure_factory as ff
import plotly.offline as py 
from plotly.subplots import make_subplots
import dash
from dash import html
from dash import Dash, Input, Output, callback
from dash.dash_table.Format import Group
import dash_bootstrap_components as dbc
from dash import dcc
from dash.dependencies import Input, Output



# Create app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SANDSTONE])
server = app.server


#Read of the data
df = pd.read_csv('df.csv') # Cork weather forecast for 2022
df_1 = pd.read_csv('df_1.csv') # Historical weather data
df_sarimax = pd.read_csv('sarimax_pred.csv') # Sarimax Prediction
historical_gdd = pd.read_csv('historical_gdd.csv')

# Transform date to datetime type
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# Transform date to datetime type
df_1['Date'] = pd.to_datetime(df_1['Date'], errors='coerce')

# Transform date to datetime type
df_sarimax['date_2'] = pd.to_datetime(df_sarimax['date_2'], errors='coerce')

# Transform date to datetime type
historical_gdd['date_2'] = pd.to_datetime(historical_gdd['date_2'], errors='coerce')

def sarimax():
    
    predictions = go.Figure()

    predictions.add_trace(go.Scatter(x=df_sarimax.date_2, y=df_sarimax.avg_temp_rev.round(2),
                        mode='lines+markers',
                        line=dict(color='#12AD2B', width=1),
                        name='Observed')),
    
    predictions.add_trace(go.Scatter(x=df_sarimax.date_2, y=df_sarimax.predicted.round(2),
                        mode='lines+markers',
                        line=dict(color='rgba(0,102,51)', width=1),
                        name='Forecasted')),

    # Add the Confidence Interval for the Lower Bounds on the test test
    predictions.add_trace(go.Scatter(x=df_sarimax.date_2, y=df_sarimax.lower_pred.round(2),
                        marker=dict(color="#444"),
                        line=dict(width=0, dash='dot'),
                        mode='lines',
                        fillcolor='rgba(102,102,0, 0.1)',
                        fill='tonexty',
                        name='Lower Bound Forecasted'))

    # Add the Confidence Interval for the Upper Bounds on the test test
    predictions.add_trace(go.Scatter(x=df_sarimax.date_2, y=df_sarimax.upper_pred.round(2),
                        marker=dict(color="#444"),
                        line=dict(width=0, dash='dot'),
                        mode='lines',
                        fillcolor='rgba(102,102,0, 0.1)',
                        fill='tonexty',
                        name='Upper Bound Forecasted'))






    # Add widgets and slider range
    predictions.update_xaxes(
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=2, label="2m", step="month", stepmode="backward"),
                dict(count=3, label="3m", step="month", stepmode="backward"),
                dict(count=4, label="4m", step="month", stepmode="backward"),  
                dict(count=5, label="5m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=6, label="7m", step="month", stepmode="backward"),
                dict(count=7, label="8m", step="month", stepmode="backward"),
                dict(count=8, label="9m", step="month", stepmode="backward"),
                dict(count=9, label="10m", step="month", stepmode="backward"),
                dict(count=10, label="11m", step="month", stepmode="backward"),
                dict(count=11, label="12m", step="month", stepmode="backward"),
                dict(step="all")
            ])
        )
    )



    # Use update_layout in order to define few configuration such as figure height and width, title, etc
    predictions.update_layout(
        height=700, # Figure height
        width=1500, # Figure width
        title={
            'text': '', # Subplot main title
            'y':0.91, # Set main title y-axis position
            'x':0.5, # Set main title x-axis position
            'xanchor': 'center', # xachor position
            'yanchor': 'top'}, # yachor position 
        showlegend=True,
        font_color='rgba(0,102,51)',
        font_family="Verdana", # Set Font style
        font_size=14, # Set Font size) # legend false 
        margin=dict(l=60, r=60, t=20, b=20))

    # Update Styling
    predictions.update_layout(hovermode="x", template = 'none')
    
    predictions.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="left",
    x=0.01))

    # Add Spikes
    predictions.update_xaxes(showspikes=True,rangeslider_visible=True)
    predictions.update_yaxes(title_text="Temperature (C°)",showspikes=True)


    # Show Figure
    return predictions




def pred_line():
    
    pred_line = go.Figure()

    pred_line.add_trace(go.Scatter(x=df.Date, y=df.Forecast.round(2),
                        mode='lines+markers',
                        line=dict(color='rgba(0,102,51)', width=1),
                        name='Forecasted')),

    # Add the Confidence Interval for the Lower Bounds on the test test
    pred_line.add_trace(go.Scatter(x=df.Date, y=df["Lower Bound"].round(2),
                        marker=dict(color="#444"),
                        line=dict(width=0, dash='dot'),
                        mode='lines',
                        fillcolor='rgba(102,102,0, 0.1)',
                        fill='tonexty',
                        name='Lower Bound'))

    # Add the Confidence Interval for the Upper Bounds on the test test
    pred_line.add_trace(go.Scatter(x=df.Date, y=df['Upper Bound'].round(2),
                        marker=dict(color="#444"),
                        line=dict(width=0, dash='dot'),
                        mode='lines',
                        fillcolor='rgba(102,102,0, 0.1)',
                        fill='tonexty',
                        name='Upper Bound'))






    # Add widgets and slider range
    pred_line.update_xaxes(
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=2, label="2m", step="month", stepmode="backward"),
                dict(count=3, label="3m", step="month", stepmode="backward"),
                dict(count=4, label="4m", step="month", stepmode="backward"),  
                dict(count=5, label="5m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=6, label="7m", step="month", stepmode="backward"),
                dict(count=7, label="8m", step="month", stepmode="backward"),
                dict(count=8, label="9m", step="month", stepmode="backward"),
                dict(count=9, label="10m", step="month", stepmode="backward"),
                dict(count=10, label="11m", step="month", stepmode="backward"),
                dict(count=11, label="12m", step="month", stepmode="backward"),
                dict(step="all")
            ])
        )
    )



    # Use update_layout in order to define few configuration such as figure height and width, title, etc
    pred_line.update_layout(
        height=700, # Figure height
        width=1500, # Figure width
        title={
            'text': '', # Subplot main title
            'y':0.91, # Set main title y-axis position
            'x':0.5, # Set main title x-axis position
            'xanchor': 'center', # xachor position
            'yanchor': 'top'}, # yachor position 
        showlegend=True,
        font_color='rgba(0,102,51)',
        font_family="Verdana", # Set Font style
        font_size=14, # Set Font size) # legend false 
        margin=dict(l=60, r=60, t=20, b=20))

    # Update Styling
    pred_line.update_layout(hovermode="x", template = 'none')
    
    pred_line.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="left",
    x=0.01))

    # Add Spikes
    pred_line.update_xaxes(showspikes=True,rangeslider_visible=True)
    pred_line.update_yaxes(title_text="Temperature (C°)",showspikes=True)


    # Show Figure
    return pred_line


def calendar():
    
    # Filter out data to start in 2022
    df_gdd_forecasted = df.query("Year==2022")
    df_gdd_forecasted = df_gdd_forecasted.set_index('Date').resample('3M')['DD'].cumsum().round(2)

    # Reset Index
    df_gdd_forecasted = df_gdd_forecasted.reset_index().rename(columns={'DD': 'GDD'})

    # Display series
    df_gdd_forecasted['month'] = df_gdd_forecasted['Date'].dt.month

    df_gdd_forecasted  = df_gdd_forecasted[(df_gdd_forecasted['month']>1)&(df_gdd_forecasted['month']<11)]


    # creating the plot
    calplot_fig = calplot(
        df_gdd_forecasted,
        x="Date",
        y="GDD",
        gap=1,
        month_lines_width=3, 
        month_lines_color="#fff",
        colorscale = 'greens')

    # Use update_layout in order to define few configuration such as figure height and width, title, etc
    calplot_fig.update_layout(
        height=630, # Figure height
        width=1450, # Figure width
        showlegend=False,
        xaxis_nticks=24,
        font_family="Verdana", # Set Font style
        font_color='rgba(0,102,51)',
        font_size=14, # Set Font size) # legend false 
        margin=dict(l=20, r=20, t=20, b=20))
    # Show figure
    return calplot_fig


def seasons():
    
    data = df.query("Year>2021")
    
    data = data.set_index('Date')
    
    data_3 = data['2022-03-20':'2022-06-20']['DD'].cumsum()

    data_3_1 = data['2022-06-20':'2022-09-23']['DD'].cumsum()

    data_3_1_1 = data['2022-09-23':'2022-12-01']['DD'].cumsum()


    # Create Figure
    fig = go.Figure()


    # Figures ---------------------------------------------------------------------------------------------------------

    # Create traces
    fig.add_trace(go.Scatter(
        x=data_3.index, y=data_3,
        name='Spring',
        mode='lines',
        line=dict(width=0.5, color='#00FA9A'),
        fill='tozeroy'

    ))

    fig.add_trace(go.Scatter(
        x=data_3_1.index, y=data_3_1,
        name='Summer',
        mode='lines',
        line=dict(width=0.5,  color="#4CC417"),
        fill='tozeroy',
        #stackgroup='one'
    ))

    fig.add_trace(go.Scatter(
        x=data_3_1_1.index, y=data_3_1_1,
        name='Autumn',
        mode='lines',
        line=dict(width=0.5, color='#34A56F'),
        fill='tozeroy',
        stackgroup='one'
    ))


    # Annotations ----------------------------------------------------------------------------------------------------

    fig.add_annotation(
            x='2022-05-30',
            y=1400,
            text="Spring",
            showarrow=False,
            font=dict(
                family="Verdana",
                size=24,
                color = 'rgba(0,102,51)'
                ),
            align="center",
            ax=-0,
            ay=-50,
            )

    fig.add_annotation(
            x='2022-08-30',
            y=2200,
            text="Summer",
            showarrow=False,
            font=dict(
                family="Verdana",
                size=24,
                color='rgba(0,102,51)'
                ),
            align="center",
            ax=-0,
            ay=-50,
            )


    fig.add_annotation(
            x='2022-11-15',
            y=1300,
            text="Autumn",
            showarrow=False,
            font=dict(
                family="Verdana",
                size=24,
                color='rgba(0,102,51)'
                ),
            align="center",
            ax=-0,
            ay=-50,
            )


    # Layout ------------------------------------------------------------------------------------------------------------

    fig.update_layout(
        height=630, # Figure height
        width=1500, # Figure width
        showlegend=False,
        xaxis_nticks=24,
        font_family="Verdana", # Set Font style
        font_size=14, # Set Font size) # legend false 
        font_color='rgba(0,102,51)',
        template='none',
        hovermode="closest",
        margin=dict(l=60, r=60, t=20, b=20))
        

    # Update axes
    fig.update_yaxes(title_text='GDD', showspikes=True, dtick=250)
    fig.update_xaxes(showspikes=True,automargin=True)
    
    # Return plot
    return fig



def historical_calendars():
    
    df_gdd_cumsum = historical_gdd.set_index('date_2').resample('3M')['dd'].cumsum().round(2)

    # Reset Index
    df_gdd_cumsum = df_gdd_cumsum.reset_index().rename(columns={'dd': 'gdd'})

    # Display series
    df_gdd_cumsum['month'] = df_gdd_cumsum['date_2'].dt.month

    df_gdd_cumsum = df_gdd_cumsum[(df_gdd_cumsum['month']>1)&(df_gdd_cumsum['month']<11)]

    # creating the plot
    hist_cal = calplot(
        df_gdd_cumsum,
        x="date_2",
        y="gdd",
        colorscale="greens",
        gap=5,
        years_title=True,
        month_lines_width=0, 
        month_lines_color="#fff"
    )

    # Use update_layout in order to define few configuration such as figure height and width, title, etc
    hist_cal.update_layout(
        height=630, # Figure height
        width=1500, # Figure width
        title={
            'text': '', # Subplot main title
            'y':0.98, # Set main title y-axis position
            'x':0.5, # Set main title x-axis position
            'xanchor': 'center', # xachor position
            'yanchor': 'top'}, # yachor position 
        showlegend=False,
        font_color='rgba(0,102,51)',
        font_family="Verdana", # Set Font style
        font_size=12) # Set Font size) # legend false 
    
    # Display figure
    return hist_cal




SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": "12rem",
    "width": "16rem",
    "padding": "2rem 1rem",
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    'fontFamily': 'verdana',
    'fontColor': 'white',
               
}





sidebar = html.Div(
    [
        html.H6("Menu", className="display-4", style={'fontFamily': 'verdana',
                                                      'textAlign':'center',
                                                      'color': 'rgba(0,102,51)',
                                                      'fontSize': 40,
                                                      'header_height':'6rem',
                                                      'footer_height':"12rem"}),
        html.Hr(),
        html.P(
            "", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Model Validation", href="/", active="exact",style={'fontFamily': 'verdana',
                                                                                'textAlign':'center',
                                                                                'color': 'rgba(0,102,51)',}),
                
                dbc.NavLink("Weather Forecast", href="/page-1", active="exact",style={'fontFamily': 'verdana',
                                                                                'textAlign':'center',
                                                                                'color': 'rgba(0,102,51)',}),
               
                dbc.NavLink("Crop Stages", href="/page-2", active="exact",style={'fontFamily': 'verdana',
                                                                                 'textAlign':'center',
                                                                                 'color': 'rgba(0,102,51)',}),
                dbc.NavLink("Calendar 2022", href="/page-3", active="exact",style={'fontFamily': 'verdana',
                                                                              'textAlign':'center',
                                                                              'color': 'rgba(0,102,51)',}),
                
                dbc.NavLink("Historical Calendars", href="/page-4", active="exact",style={'fontFamily': 'verdana',
                                                                              'textAlign':'center',
                                                                              'color': 'rgba(0,102,51)',}),
            ],
            vertical=True,
            pills=True,
            
        ),
        html.Hr(),
        html.Div([html.H6("Summary", className="display-4", style={'fontFamily': 'verdana',
                                                      'textAlign':'center',
                                                      'color': 'rgba(0,102,51)',
                                                      'fontSize': 20,
                                                      'header_height':'6rem',
                                                      'footer_height':"12rem"}),
                  html.P('The data was gathered from Roches Point station (Cork) and 5 years of weather historical data from that station was used to build the model. The variables used to predict the temperature were: Wet Bulb Air Temperature, Dew Point Air Temperature, Relativity Humidity, Mean Sea Level Pressure, Mean Hourly Wind Speed, Predominant Hourly wind Direction. One step ahead was forecasted in order to calculate and predict the Growing Degrees Days for Perennial Ryegrass for 2022. The model used was Seasonal Auto-Regressive Integrated Moving Average with eXogenous factors.', 
                         style={'fontSize': 12,
                                'fontFamily': 'verdana',
                                'color': 'rgba(0,102,51)',
                                'textAlign': 'left'}),
                              html.Br(),
                              html.Br(),
                              html.Hr(),
                  html.Label(['Data Source: ',
                              html.A('Met Éireann', 
                                     href='https://www.met.ie/climate/available-data/historical-data',
                                     target="_blank",
                                     style={'fontSize': 14})]),
                  
])

    ],
    style=SIDEBAR_STYLE,
)


content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content
])


@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname == "/":
        return [
                html.H1('Model Validation',
                        style={'textAlign':'center',
                               'fontFamily': 'verdana',
                               'color': 'rgba(0,102,51)'}),
                html.Hr(),
                dcc.Graph(id='predictions',
                          figure=sarimax()), # Specify width for different screen size
        ]
    
    
    elif pathname == "/page-1":
        return [
                html.H1('Cork Weather Forecast',
                        style={'textAlign':'center',
                               'fontFamily': 'verdana',
                               'color': 'rgba(0,102,51)'}),
                html.Hr(),
                dcc.Graph(id='pred_line',
                          figure=pred_line()), # Specify width for different screen size
        ]

   
    
    elif pathname == "/page-2":
        return [
                html.H1('Crop Stages Predictions',
                        style={'textAlign':'center',
                               'fontFamily': 'verdana',
                               'color': 'rgba(0,102,51)'}),
                html.Hr(),
                dcc.Graph(id='count_table',
                         figure=seasons()), # Specify width for different screen sizes
            html.Br(),            
            html.Hr(),
            html.Div([
                html.P('Temperature base at 0° C', style={'fontSize': 14,
                                                          'fontFamily': 'verdana',
                                                          'color': 'rgba(0,102,51)'}),])
        ]



    elif pathname == "/page-3":
        return [
                html.H1('Perennial Ryegrass Degrees Days Calendar 2022',
                        style={'textAlign':'center',
                               'fontFamily': 'verdana',
                               'color': 'rgba(0,102,51)'}),
            html.Hr(),
                dcc.Graph(id='calendar',
                         figure=calendar()),
            html.Br(),           
            html.Hr(),
            html.Div([
                html.P('Temperature base at 0° C', style={'fontSize': 14,
                                                          'fontFamily': 'verdana',
                                                          'color': 'rgba(0,102,51)'}),])
        ]
    
    elif pathname == "/page-4":
        return [
                html.H1('Historical Perennial Ryegrass Degrees Days Calendars',
                        style={'textAlign':'center',
                               'fontFamily': 'verdana',
                               'color': 'rgba(0,102,51)'}),
            html.Hr(),
                dcc.Graph(id='calendar',
                         figure=historical_calendars()),
            html.Br(),
            html.Hr(),
            html.Div([
                html.P('Temperature base at 0° C', style={'fontSize': 14,
                                                          'fontFamily': 'verdana',
                                                          'color': 'rgba(0,102,51)'}),])
        ]



if __name__ == '__main__':
    app.run_server(debug=False,host = '127.0.0.1')
