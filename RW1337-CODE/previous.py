import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, callback, Output, Input, State, ctx
from dash import dash_table
import plotly.graph_objs as go
import pandas as pd
import json
import datetime

# record table
f = open(r'test_case.json')
content = f.read()
a = json.loads(content)
print(a)
df = pd.DataFrame(a)
records = df.to_dict('records')
length = len(records)
global_count = length

# pie chart
labels = ['fruit', 'vegetable', 'meat', 'staple']
pie_values = [0, 0, 0, 0]
fig1 = go.Figure(data=go.Pie(labels=labels, values=pie_values))

# line chart
fig2 = go.Figure(data=[go.Scatter(x=[1990, 2000, 2010], y=[4, 1, 2])])

# run on application
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])
app.layout = html.Div([
    dbc.Row(dbc.Col(html.H1(children='Personal Meal Record', style={'textAlign': 'center', 'margin': '50px'}))),
    dbc.Row(
        [
            dbc.Col(dash_table.DataTable(
                id="my-table",
                editable=True,
                row_deletable=True,
                columns=[{'name': i, 'id': i} for i in df.columns],
                data=records,
                style_header={'fontWeight': 'bold', 'fontSize': 'larger'},
                style_data={},
            ), style={'overflow': 'scroll', 'height': '300px'}, width=8),
            dbc.Col(
                [
                    dbc.Row(
                        [
                            dbc.Label("Item Name:", html_for="item-name-label", width=3),
                            dbc.Col(
                                dbc.Input(
                                    id="item-name-input", placeholder="Enter Item Name"
                                ),
                                width=9,
                            ),
                        ],
                        className="mb-3",
                    ),
                    dbc.Row(
                        [
                            dbc.Label("Amount:", html_for="amount-label", width=3),
                            dbc.Col(
                                dbc.Input(
                                    id="amount-input", placeholder="Enter Amount($)"
                                ),
                                width=9,
                            ),
                        ],
                        className="mb-3",
                    ),
                    dbc.Row(
                        [
                            dbc.Label("Category:", html_for="category-label", width=3),
                            dbc.Col(
                                dcc.Dropdown(
                                    id="category-dropdown",
                                    options=[
                                        {"label": "fruit", "value": "fruit"},
                                        {"label": "vegetable", "value": "vegetable"},
                                        {"label": "meat", "value": "meat"},
                                        {"label": "staple", "value": "staple"},
                                    ],
                                ),
                                width=9,
                            )
                        ],
                        className="mb-3",
                    ),
                    dbc.Row(
                        dbc.Button(
                            id='add-btn',
                            n_clicks=0,
                            children=[html.I(className="bi bi-plus"), 'Add New Item'],
                            style={'width': '80%', 'margin': 'auto', 'borderRadius': '10px'})
                    ),
                ],
                width=4
            )
        ],
        style={'marginLeft': '200px', 'marginRight': '200px', 'height': '300px'}
    ),
    dbc.Row(html.Div(id='test')),
    dbc.Row([
        dbc.Col([
            dbc.Col(dcc.Graph(id='pie-chart', figure=fig1), style={'margin': '50px'}),
        ], width=6),
        dbc.Col([
            dbc.Col(dcc.Graph(id='line-chart', figure=fig2), style={'margin': '50px'})
        ], width=6)
    ])
])


# function on listener
def updatePieChart():
    global pie_values, records
    pie_values = [0, 0, 0, 0]
    for record in records:
        if record['Category'] == 'fruit':
            pie_values[0] += 1
        elif record['Category'] == 'vegetable':
            pie_values[1] += 1
        elif record['Category'] == 'meat':
            pie_values[2] += 1
        else:
            pie_values[3] += 1
    return go.Figure(data=go.Pie(labels=labels, values=pie_values))

# update the line chart
def updateLineChart():
    x = []
    for record in records:
        year = record['Timestamp'].split('-')[0]
        month = record['Timestamp'].split('-')[1]
        period = year+'-'+month
        if period not in x:
            x.append(period)
    x.sort()
    y = [0] * len(x)
    for record in records:
        year = record['Timestamp'].split('-')[0]
        month = record['Timestamp'].split('-')[1]
        period = year + '-' + month
        index = x.index(period)
        y[index] += float(record['Amount'].split('$ ')[1])
    return go.Figure(data=[go.Scatter(x=x, y=y)])

# callback function1
@callback(
    Output('pie-chart', 'figure'),
    Output('line-chart', 'figure'),
    Input('my-table', 'data')
)
def updateGraph(data):
    global length, records
    length = len(data)
    records = data
    return updatePieChart(), updateLineChart()

# callback function2
@callback(
    Output('my-table', 'data'),
    Input('add-btn', 'n_clicks'),
    State('item-name-input', 'value'),
    State('amount-input', 'value'),
    State('category-dropdown', 'value'),
    prevent_initial_call=True
)

# Add a new record
def addNewItem(btn, item_name, amount, category):
    global length, records, global_count
    records.append({
        'Index': str(global_count),
        'Item Name': item_name,
        'Amount': '$ ' + amount,
        'Category': category,
        'Timestamp': datetime.datetime.now().strftime('%Y-%m-%d')
    })
    length = length + 1
    global_count = global_count + 1
    return records


if __name__ == '__main__':
    app.run(debug=True)
