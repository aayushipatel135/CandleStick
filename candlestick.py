import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly
import random
import plotly.graph_objs as go
from collections import deque
import pandas as pd
import dash_daq as daq
from flask import request


df = pd.read_csv('working.csv')
x = []
x.append(df.iloc[0,0])
open = []
open.append(df.iloc[0,4])
high = []
high.append(df.iloc[0,2])
low = []
low.append(df.iloc[0,3])
close = []
close.append(df.iloc[0,1])
last = 0


# Initialising variables
X, y = [], []
X.append(0); y.append(1)

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    daq.ToggleSwitch(
        id='my-toggle-switch',
        value=True
    ),
    html.Div(id='toggle-switch-output'),

    dcc.Graph(id='live-graph', animate=False),
            dcc.Interval(
                id='graph-update',
                interval=2000
            ),

])

@app.callback(
    [Output('toggle-switch-output', 'children'),
     Output('live-graph', 'figure')],
    [Input('my-toggle-switch', 'value'),
     Input('graph-update', 'n_intervals')])

def update_output(value,data):
    global last
    global time_interval


    string1 = 'The switch is off'
    string2 = 'This is working'

    if value==False:
        time_interval = 9999999999999900000
        time.sleep(60)
        if last < 15 : 
            candle = plotly.graph_objs.Candlestick(
                    x = list(x),
                    low = list(low),
                    high = list(high),
                    close = list(close),
                    open = list(open),
                    increasing_line_color = 'green',
                    decreasing_line_color = 'red'
            )
            scatter = plotly.graph_objs.Scatter(
                x=list(x),
                y=list(open),
                name='Scatter',
                mode= 'lines+markers'
            )
            print(x[-1],x[-1])
            fig = go.Figure(
                data =  [candle,scatter]
            )
            fig.update_layout(showlegend=False)
            fig.update_xaxes(visible=False)
            fig.update_yaxes(visible=False)
            return (string1,
                    {'data': [candle,scatter],
                    'layout' : go.Layout(xaxis_rangeslider_visible=True,
                                        xaxis = dict(
                                        autorange=False,
                                        range = [x[0] , x[-1] ],
                                        type='date'),
                                        yaxis = dict(range = [min(low),max(high)]),
                    )}
                   )
        else : 
            candle = plotly.graph_objs.Candlestick(
                    x = list(x),
                    low = list(low),
                    high = list(high),
                    close = list(close),
                    open = list(open),
                    increasing_line_color = 'green',
                    decreasing_line_color = 'red'
            )
            scatter = plotly.graph_objs.Scatter(
                x=list(x),
                y=list(open),
                name='Scatter',
                mode= 'lines+markers'
            )
            print(x[-1],x[-1])
            fig = go.Figure(
                data =  [candle,candle1,scatter]
            )
            fig.update_layout(showlegend=False)
            fig.update_xaxes(visible=False)
            fig.update_yaxes(visible=False)
            return (string1,
                    {'data': [candle,scatter],
                    'layout' : go.Layout(xaxis_rangeslider_visible=True,
                                        xaxis = dict(
                                        autorange=False,
                                        range = [x[-15] , x[-1] ],
                                        type='date'),
                                        yaxis = dict(range = [min(low),max(high)]),
                    )}
                   )
    else:
        time_interval = 1500
        if last < len(df) : 
                if last < 15 : 
                    x.append(df.iloc[last,0])
                    open.append(df.iloc[last,4])
                    high.append(df.iloc[last,2])
                    low.append(df.iloc[last,3])
                    close.append(df.iloc[last,1])
            
                    candle = plotly.graph_objs.Candlestick(x = list(x),
                            low = list(low),
                            high = list(high),
                            close = list(close),
                            open = list(open),
                            increasing_line_color = 'green',
                            decreasing_line_color = 'red'
                    )
                    scatter = plotly.graph_objs.Scatter(
                        x=list(x),
                        y=list(open),
                        name='Scatter',
                        mode= 'lines+markers'
                    )
                    last = last + 1
                    print(x[0] ,x[-1])
                    fig = go.Figure(
                        data =  [candle,scatter]
                    )
                    fig.update_layout(showlegend=False)
                    fig.update_xaxes(visible=False)
                    fig.update_yaxes(visible=False)
                    return (string2, 
                            {'data': [candle,scatter],
                            'layout' : go.Layout(xaxis_rangeslider_visible=True,
                                                xaxis = dict(
                                                    autorange=False,
                                                    range = [x[0] , x[-1] ],
                                                    type='date'),
                                                yaxis = dict(range = [min(low),max(high)]),
                                                )},
                            
                            )
                else : 
                    x.append(df.iloc[last,0])
                    open.append(df.iloc[last,4])
                    high.append(df.iloc[last,2])
                    low.append(df.iloc[last,3])
                    close.append(df.iloc[last,1])
            
                    candle = plotly.graph_objs.Candlestick(
                            x = list(x),
                            low = list(low),
                            high = list(high),
                            close = list(close),
                            open = list(open),
                            increasing_line_color = 'green',
                            decreasing_line_color = 'red'
                    )
                    candle1 = plotly.graph_objs.Candlestick(
                    x = [x[5]],
                    low = [low[5]],
                    high = [high[5]],
                    close = [close[5]],
                    open = [open[5]],
                    increasing_line_color = 'blue',
                    decreasing_line_color = 'blue'
            )
                    scatter = plotly.graph_objs.Scatter(
                        x=list(x),
                        y=list(open),
                        name='Scatter',
                        mode= 'lines+markers'
                    )
                    last = last + 1
                    print(x[-15],x[-1])
                    fig = go.Figure(
                        data =  [candle,scatter]
                    )
                    fig.update_layout(showlegend=False)
                    fig.update_xaxes(visible=False)
                    fig.update_yaxes(visible=False)
                    return (string2,
                            {'data': [candle,candle1,scatter],
                            'layout' : go.Layout(xaxis_rangeslider_visible=True,
                                                xaxis = dict(
                                                    autorange=False,
                                                    range = [x[-15] , x[-1] ],
                                                    type='date'),
                                                yaxis = dict(range = [min(low),max(high)]),
                                                ) },
                            
                           )
        else : 
            candle = plotly.graph_objs.Candlestick(
                            x = list(x),
                            low = list(low),
                            high = list(high),
                            close = list(close),
                            open = list(open),
                            increasing_line_color = 'green',
                            decreasing_line_color = 'red'
            )
            scatter = plotly.graph_objs.Scatter(
                    x=list(x),
                    y=list(open),
                    name='Scatter',
                    mode= 'lines+markers'
            )
            print(x[-15],x[-1])
            fig = go.Figure(
                data =  [candle,scatter]
            )
            fig.update_layout(showlegend=False)
            fig.update_xaxes(visible=False)
            fig.update_yaxes(visible=False)
            time.sleep(60)
            return (string2,
                    {'data': [candle,scatter],
                    'layout' : go.Layout(xaxis_rangeslider_visible=True,
                                xaxis = dict(autorange=False,
                                            range = [x[-15] , x[-1] ],
                                            type='date'),
                                            yaxis = dict(range = [min(low),max(high)]),
                    )}
            )
        #return (string2,fig2)


if __name__ == '__main__':
    app.run_server(debug=True)
