import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import json
import pandas as pd
import numpy as np
import plotly
import time

app = dash.Dash()

DF_GAPMINDER = pd.read_csv('sample.csv')

app.layout = html.Div([
    html.H4('Gapminder DataTable'),
    dt.DataTable(
        rows=DF_GAPMINDER.to_dict('records'),

        # optional - sets the order of columns
        # columns=sorted(DF_GAPMINDER.columns),

        row_selectable=True,
        filterable=True,
        sortable=True,
        selected_row_indices=[],
        id='datatable-gapminder'
    ),
    html.Div(id='selected-indexes'),
    dcc.Graph(
        id='graph-gapminder'
    ),
], className="container")


@app.callback(
    Output('datatable-gapminder', 'selected_row_indices'),
    [Input('graph-gapminder', 'clickData')],
    [State('datatable-gapminder', 'selected_row_indices')])
def update_selected_row_indices(clickData, selected_row_indices):
    if clickData:
        for point in clickData['points']:
            if point['pointNumber'] in selected_row_indices:
                selected_row_indices.remove(point['pointNumber'])
            else:
                selected_row_indices.append(point['pointNumber'])
    return selected_row_indices


@app.callback(
    Output('graph-gapminder', 'figure'),
    [Input('datatable-gapminder', 'rows'),
     Input('datatable-gapminder', 'selected_row_indices')])
def update_figure(rows, selected_row_indices):
    print "===> start" , time.time()
    dff = pd.DataFrame(rows)
    #print rows
    #print dff
    #print "=== "
    fig = plotly.tools.make_subplots(
        rows=3, cols=1,
        subplot_titles=('AR6K', 'iperf', 'irq',),
        shared_xaxes=True)
    marker = {'color':['#0074D9']*len(dff)}
    for i in (selected_row_indices or []):
        marker['color'][i] = '#FF851B'
    #for item in rows:
        #print "======>"
        #print item
        #print item['process']
     #   if item:
     #       if item['process'].find('AR6K-8139') != -1:
     #           index = rows.index(item)
     #           marker['color'][index] = '#FF851B'
     #           AR6K.append(item)
     #       elif item['process'].find('iperf-8259') != -1:
     #           index = rows.index(item)
     #           marker['color'][index] = '#33851B'
     #           iperf.append(item)
     #       else:
     #           irq.append(item)

    #print "=== dff start"
    #print dff
    #print "=== AR6K-8139"
    #print dff['process'].values
    # fixme: need use a proper way to find out process
    AR6K2=dff.loc[dff['process'].values == '            AR6K-8139  ']
    iperf2=dff.loc[dff['process'].values == '           iperf-8259  ']
    irq2=dff.loc[dff['process'].values == '     irq/45-mmc0-140   ']
    #print "=== start"
    #print dff['time']
    #print "=== end"
    #print "=== start 1"
    #print dff['time'][1]
    #print "=== end"
    fig.append_trace({
        'x': AR6K2['time'],
        'y': [10]*len(AR6K2),
        'type': 'bar'
#        'marker': marker
    }, 1, 1)
    fig.append_trace({
        'x': iperf2['time'],
        'y': [10]*len(iperf2),
        'type': 'bar'
#        'marker': marker
    }, 2, 1)
    fig.append_trace({
        'x': irq2['time'],
        'y': [10]*len(irq2),
        'type': 'bar'
 #       'marker': marker
    }, 3, 1)
    fig['layout']['showlegend'] = False
    fig['layout']['height'] = 800
    fig['layout']['margin'] = {
            'l':40,
            'r':10,
            't':60,
            'b':200
    }
    #fig['layout']['yaxis3']['type'] = 'log'
#    fig['layout'].update(height=300, width=1600, title='ele')
    print "===> end" , time.time()
    return fig

if __name__ == '__main__':
    app.run_server( host="10.231.194.176")
