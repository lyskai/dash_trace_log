import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import json
import pandas as pd
import numpy as np
import plotly

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
    #print "===> start"
    dff = pd.DataFrame(rows)
    #print rows
    #print dff
    #print "=== "
    fig = plotly.tools.make_subplots(
        rows=1, cols=1
        )
    marker = {'color':['#0074D9']*len(dff)}
    for i in (selected_row_indices or []):
        marker['color'][i] = '#FF851B'
    #for item in rows
        #print "======>"
        #print item
        #print item['process']
    #    if item
    #        if item['process'].find('AR6K-8139') != -1
    #            index = rows.index(item)
    #            marker['color'][index] = '#FF851B'
    #        elif item['process'].find('iperf-8259') != -1
    #            index = rows.index(item)
    #            marker['color'][index] = '#33851B'
    fig.append_trace({
        'x' : dff['time'],
        'y' : dff['process'],
        'type' : 'histogram',
        'marker': marker
    }, 1, 1)
#    fig.append_trace({
#        'x' dff['time'],
#        'y' dff['process'],
#        'type' 'bar',
#        'marker' marker
#    }, 2, 1)
#    fig.append_trace({
#        'x' dff['process'],
#        'y' dff['cpu'],
#        'type' 'bar',
#        'marker' marker
#    }, 3, 1)
#    fig['layout']['showlegend'] = False
#    fig['layout']['height'] = 800
#    fig['layout']['margin'] = {
#        'l' 40,
#        'r' 10,
#        't' 60,
#        'b' 200
#    }
#    fig['layout']['yaxis3']['type'] = 'log'
    fig['layout'].update(height=300, width=1600, title='ele')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, host="10.231.194.176")
