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


df = pd.read_csv('final.csv')
df = df.iloc[88992:,:]
df['date'] = df['Date'] + " " +  df['Time'] + ":00+05:30"
df['Actions'] = df['Actions'].apply(lambda x : int(x[1:-1]))

x_pos = []
open_pos = []
high_pos = []
low_pos = []
close_pos = []
display_pos = []

x_neg = []
open_neg = []
high_neg = []
low_neg = []
close_neg = []
display_neg = []

x_neu = []
open_neu = []
high_neu = []
low_neu = []
close_neu = []
display_neu = []


if df.iloc[0,9] < 0 :
    x_neg.append(df.iloc[0,12])
    open_neg.append(df.iloc[0,4])
    high_neg.append(df.iloc[0,5])
    low_neg.append(df.iloc[0,6])
    close_neg.append(df.iloc[0,7])
    display_neg.append("No. of lots held : " +  str(df.iloc[0,10]) )
elif df.iloc[0,9] > 0 : 
    x_pos.append(df.iloc[0,12])
    open_pos.append(df.iloc[0,4])
    high_pos.append(df.iloc[0,5])
    low_pos.append(df.iloc[0,6])
    close_pos.append(df.iloc[0,7])
    display_pos.append("No. of lots held : " +  str(df.iloc[0,10]) )
else : 
    x_neu.append(df.iloc[0,12])
    open_neu.append(df.iloc[0,4])
    high_neu.append(df.iloc[0,5])
    low_neu.append(df.iloc[0,6])
    close_neu.append(df.iloc[0,7])
    display_neu.append("No. of lots held : " +  str(df.iloc[0,10]) )

x = []
x.append(df.iloc[0,12])
open = []
open.append(df.iloc[0,4])
high = []
high.append(df.iloc[0,5])
low = []
low.append(df.iloc[0,6])
close = []
close.append(df.iloc[0,7])
display = []
display.append( "No. of lots held : " +  str(df.iloc[0,10]) )
last = 0


# Initialising variables
X, y = [], []
X.append(0); y.append(1)

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1(children="Candle Stick Plot Nifty50 2018",
           style = {'textAlign': 'center','color': 'black'}
    ),
    daq.ToggleSwitch(
        id='my-toggle-switch',
        value=True
    ),
    html.Div(id='toggle-switch-output'),

    dcc.Graph(id='live-table', 
              style={'height': '40vh'
                    },
              animate=False),

    dcc.Graph(id='live-graph', 
              style={'height': '85vh'
                    },
              animate=False),
            dcc.Interval(
                id='graph-update',
                interval=700
            ),

])

@app.callback(
    [Output('toggle-switch-output', 'children'),
     Output('live-table', 'figure'),
     Output('live-graph', 'figure')],
    [Input('my-toggle-switch', 'value'),
     Input('graph-update', 'n_intervals')])

def update_output(value,data):
    global last
    global time_interval


    string1 = ''
    string2 = ''

    if value==False:
        fig = go.Figure(data=[go.Table(
                columnwidth = [40,40],
                header=dict(values=['A', 'B'],height=20),
                cells=dict(values=[ df.iloc[last:last+2,0 ] ,  df.iloc[last:last+2,1 ]   ], height=20  ) 
        )])
        time_interval = 9999999999999900000
        time.sleep(60)
        if last < 30 :
            candle = plotly.graph_objs.Candlestick(
                    x = list(x),
                    low = list(low),
                    high = list(high),
                    close = list(close),
                    open = list(open),
                    increasing_line_color = 'green',
                    decreasing_line_color = 'red',
                    name='candles',
                    text=display,
                    # hoverinfo="display"
            )
            candle_pos = plotly.graph_objs.Candlestick(
                    x = list(x_pos),
                    low = list(low_pos),
                    high = list(high_pos),
                    close = list(close_pos),
                    open = list(open_pos),
                    increasing_line_color = 'blue',
                    decreasing_line_color = 'blue',
                    name='selling candle',
                    text=display_pos,
            )
            candle_neg = plotly.graph_objs.Candlestick(
                    x = list(x_neg),
                    low = list(low_neg),
                    high = list(high_neg),
                    close = list(close_neg),
                    open = list(open_neg),
                    increasing_line_color = 'yellow',
                    decreasing_line_color = 'yellow',
                    name='buying candle',
                    text=display_neg,
            )
            candle_neu = plotly.graph_objs.Candlestick(
                    x = list([x[0]]),
                    low = list([low[0]]),
                    high = list([high[0]]),
                    close = list([close[0]]),
                    open = list([open[0]]),
                    increasing_line_color = 'blue',
                    decreasing_line_color = 'blue',
                    name='selling candle',
            )
            scatter = plotly.graph_objs.Scatter(
                x=list(x),
                y=list(open),
                name='Nifty 50',
                mode= 'lines+markers'
            )
            print(x[-1],x[-1])
            return (string1,fig,
                    {'data': [candle_neu,candle,candle_pos,candle_neg,scatter],
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
                    decreasing_line_color = 'red',
                    name='candles',
                    text =display,
                    # hoverinfo="display"
            )
            candle_pos = plotly.graph_objs.Candlestick(
                    x = list(x_pos),
                    low = list(low_pos),
                    high = list(high_pos),
                    close = list(close_pos),
                    open = list(open_pos),
                    increasing_line_color = 'blue',
                    decreasing_line_color = 'blue',
                    name='selling candle',
                    text=display_pos,
            )
            candle_neg = plotly.graph_objs.Candlestick(
                    x = list(x_neg),
                    low = list(low_neg),
                    high = list(high_neg),
                    close = list(close_neg),
                    open = list(open_neg),
                    increasing_line_color = 'yellow',
                    decreasing_line_color = 'yellow',
                    name='buying candle',
                    text=display_neg,
            )
            candle_neu = plotly.graph_objs.Candlestick(
                    x = list([x[0]]),
                    low = list([low[0]]),
                    high = list([high[0]]),
                    close = list([close[0]]),
                    open = list([open[0]]),
                    increasing_line_color = 'blue',
                    decreasing_line_color = 'blue',
                    name='selling candle',
            )
            scatter = plotly.graph_objs.Scatter(
                x=list(x),
                y=list(open),
                name='Nifty 50',
                mode= 'lines+markers'
            )
            print(x[-1],x[-1])
            if last < 52 : 
                return (string1,fig,
                        {'data': [candle_neu,candle,candle_pos,candle_neg,scatter],
                        'layout' : go.Layout(xaxis_rangeslider_visible=True,
                                            xaxis = dict(
                                            autorange=False,
                                            range = [x[-30] , x[-1] ],
                                            type='date'),
                                            yaxis = dict(range = [min(low),max(high)]),
                        )}
                       )
            else : 
                return (string1,fig,
                        {'data': [candle,candle_pos,candle_neg,scatter],
                        'layout' : go.Layout(xaxis_rangeslider_visible=True,
                                            xaxis = dict(
                                            autorange=False,
                                            range = [x[-30] , x[-1] ],
                                            type='date'),
                                            yaxis = dict(range = [min(low),max(high)]),
                        )}
                       )
    else:
        time_interval = 1500
        fig = go.Figure(data=[go.Table(
                columnwidth = [40,40],
                header=dict(values=['A', 'B'],height=20),
                cells=dict(values=[ df.iloc[last:last+2,0 ] ,  df.iloc[last:last+2,1 ]   ]  ,  height=20 )
        )])
        if last < len(df) : 
                if last < 30 : 
                    print(display[last])
                    if df.iloc[last,9] < 0 :
                        x_neg.append(df.iloc[last,12])
                        open_neg.append(df.iloc[last,4])
                        high_neg.append(df.iloc[last,5])
                        low_neg.append(df.iloc[last,6])
                        close_neg.append(df.iloc[last,7])
                        display_neg.append( "No. of lots held : " +  str(df.iloc[last,10]) )
                    elif df.iloc[last,9] > 0 : 
                        x_pos.append(df.iloc[last,12])
                        open_pos.append(df.iloc[last,4])
                        high_pos.append(df.iloc[last,5])
                        low_pos.append(df.iloc[last,6])
                        close_pos.append(df.iloc[last,7])
                        display_pos.append( "No. of lots held : " +  str(df.iloc[last,10] ) )
                    else : 
                        x_neu.append(df.iloc[last,12])
                        open_neu.append(df.iloc[last,4])
                        high_neu.append(df.iloc[last,5])
                        low_neu.append(df.iloc[last,6])
                        close_neu.append(df.iloc[last,7])
                        display_neu.append( "No. of lots held : " +  str(df.iloc[last,10] ) )
                    x.append(df.iloc[last,12])
                    open.append(df.iloc[last,4])
                    high.append(df.iloc[last,5])
                    low.append(df.iloc[last,6])
                    close.append(df.iloc[last,7])
                    display.append( "No. of lots held : " +  str(df.iloc[last,10]) )
            
                    candle = plotly.graph_objs.Candlestick(x = list(x),
                            low = list(low),
                            high = list(high),
                            close = list(close),
                            open = list(open),
                            increasing_line_color = 'green',
                            decreasing_line_color = 'red',
                            name='candles',
                            text=display,
                            # hoverinfo="display"
                    )
                    candle_pos = plotly.graph_objs.Candlestick(
                            x = list(x_pos),
                            low = list(low_pos),
                            high = list(high_pos),
                            close = list(close_pos),
                            open = list(open_pos),
                            increasing_line_color = 'blue',
                            decreasing_line_color = 'blue',
                            name='selling candle',
                            text=display_pos,
                    )
                    candle_neg = plotly.graph_objs.Candlestick(
                            x = list(x_neg),
                            low = list(low_neg),
                            high = list(high_neg),
                            close = list(close_neg),
                            open = list(open_neg),
                            increasing_line_color = 'yellow',
                            decreasing_line_color = 'yellow',
                            name='buying candle',
                            text=display_neg,
                    )
                    candle_neu = plotly.graph_objs.Candlestick(
                            x = list([x[0]]),
                            low = list([low[0]]),
                            high = list([high[0]]),
                            close = list([close[0]]),
                            open = list([open[0]]),
                            increasing_line_color = 'blue',
                            decreasing_line_color = 'blue',
                            name='selling candle',
                    )
                    scatter = plotly.graph_objs.Scatter(
                        x=list(x),
                        y=list(open),
                        name='Nifty 50',
                        mode= 'lines+markers'
                    )
                    last = last + 1
                    print(x[0] ,x[-1])
                    return (string2,fig,
                            {'data': [candle_neu,candle,candle_pos,candle_neg,scatter],
                            'layout' : go.Layout(xaxis_rangeslider_visible=True,
                                                xaxis = dict(
                                                    autorange=False,
                                                    range = [x[0] , x[-1] ],
                                                    type='date'),
                                                yaxis = dict(range = [min(low),max(high)]),
                                                )},
                            
                            )
                else : 
                    print(display[last])
                    if df.iloc[last,9] < 0 :
                        x_neg.append(df.iloc[last,12])
                        open_neg.append(df.iloc[last,4])
                        high_neg.append(df.iloc[last,5])
                        low_neg.append(df.iloc[last,6])
                        close_neg.append(df.iloc[last,7])
                        display_neg.append( "No. of lots held : " +  str(df.iloc[last,10] ) ) 
                    elif df.iloc[last,9] > 0 : 
                        x_pos.append(df.iloc[last,12])
                        open_pos.append(df.iloc[last,4])
                        high_pos.append(df.iloc[last,5])
                        low_pos.append(df.iloc[last,6])
                        close_pos.append(df.iloc[last,7])
                        display_pos.append( "No. of lots held : " +  str(df.iloc[last,10] ) )
                    else : 
                        x_neu.append(df.iloc[last,12])
                        open_neu.append(df.iloc[last,4])
                        high_neu.append(df.iloc[last,5])
                        low_neu.append(df.iloc[last,6])
                        close_neu.append(df.iloc[last,7])
                        display_neu.append( "No. of lots held : " +  str(df.iloc[last,10]) )
                    x.append(df.iloc[last,12])
                    open.append(df.iloc[last,4])
                    high.append(df.iloc[last,5])
                    low.append(df.iloc[last,6])
                    close.append(df.iloc[last,7])
                    display.append( "No. of lots held : " +  str(df.iloc[last,10])  )
                    
                    candle = plotly.graph_objs.Candlestick(
                            x = list(x),
                            low = list(low),
                            high = list(high),
                            close = list(close),
                            open = list(open),
                            increasing_line_color = 'green',
                            decreasing_line_color = 'red',
                            name='candles',
                            text=display,
                            # hoverinfo="display"
                    )
                    candle_pos = plotly.graph_objs.Candlestick(
                            x = list(x_pos),
                            low = list(low_pos),
                            high = list(high_pos),
                            close = list(close_pos),
                            open = list(open_pos),
                            increasing_line_color = 'blue',
                            decreasing_line_color = 'blue',
                            name='selling candle',
                            text=display_pos,
                    )
                    candle_neg = plotly.graph_objs.Candlestick(
                            x = list(x_neg),
                            low = list(low_neg),
                            high = list(high_neg),
                            close = list(close_neg),
                            open = list(open_neg),
                            increasing_line_color = 'yellow',
                            decreasing_line_color = 'yellow',
                            name='buying candle',
                            text=display_neg,
                    )
                    candle_neu = plotly.graph_objs.Candlestick(
                            x = list([x[0]]),
                            low = list([low[0]]),
                            high = list([high[0]]),
                            close = list([close[0]]),
                            open = list([open[0]]),
                            increasing_line_color = 'blue',
                            decreasing_line_color = 'blue',
                            name='selling candle',
                    )
                    scatter = plotly.graph_objs.Scatter(
                        x=list(x),
                        y=list(open),
                        name='Nifty 50',
                        mode= 'lines+markers'
                    )
                    last = last + 1
                    print(x[-15],x[-1])
                    if last < 52 : 
                        return (string2,fig,
                                {'data': [candle_neu,candle,candle_pos,candle_neg,scatter],
                                'layout' : go.Layout(xaxis_rangeslider_visible=True,
                                                    xaxis = dict(
                                                        autorange=False,
                                                        range = [x[-30] , x[-1] ],
                                                        type='date'),
                                                    yaxis = dict(range = [min(low),max(high)]),
                                                    ) },
                                
                               )
                    else :
                        return (string1,fig,
                        {'data': [candle,candle_pos,candle_neg,scatter],
                        'layout' : go.Layout(xaxis_rangeslider_visible=True,
                                            xaxis = dict(
                                            autorange=False,
                                            range = [x[-30] , x[-1] ],
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
                            decreasing_line_color = 'red',
                            name='candles',
                            text=display,
                            # hoverinfo="display"
            )
            candle_pos = plotly.graph_objs.Candlestick(
                    x = list(x_pos),
                    low = list(low_pos),
                    high = list(high_pos),
                    close = list(close_pos),
                    open = list(open_pos),
                    increasing_line_color = 'blue',
                    decreasing_line_color = 'blue',
                    name='selling candle',
                    text=display_pos, 
            )
            candle_neg = plotly.graph_objs.Candlestick(
                    x = list(x_neg),
                    low = list(low_neg),
                    high = list(high_neg),
                    close = list(close_neg),
                    open = list(open_neg),
                    increasing_line_color = 'yellow',
                    decreasing_line_color = 'yellow',
                    name='buying candle',
                    text=display_neg,
            )
            candle_neu = plotly.graph_objs.Candlestick(
                    x = list([x[0]]),
                    low = list([low[0]]),
                    high = list([high[0]]),
                    close = list([close[0]]),
                    open = list([open[0]]),
                    increasing_line_color = 'blue',
                    decreasing_line_color = 'blue',
                    name='selling candle',
            )
            scatter = plotly.graph_objs.Scatter(
                    x=list(x),
                    y=list(open),
                    name='Nifty 50',
                    mode= 'lines+markers'
            )
            print(x[-15],x[-1])
            time.sleep(60)
            return (string2,fig,
                    {'data': [candle,candle_pos,candle_neg,scatter],
                    'layout' : go.Layout(xaxis_rangeslider_visible=True,
                                xaxis = dict(autorange=False,
                                            range = [x[-30] , x[-1] ],
                                            type='date'),
                                            yaxis = dict(range = [min(low),max(high)]),
                    )}
            )
        #return (string2,fig2)


if __name__ == '__main__':
    app.run_server(debug=True)
