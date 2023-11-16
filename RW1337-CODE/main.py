import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, callback, Output, Input, State
from dash import dash_table
from Expense import Expense
from ExpenseList import ExpenseList

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])

expense_obj = Expense()
expense_list_obj = ExpenseList()

app.layout = html.Div([
    dbc.Row(dbc.Col(html.H1(children='Money Spend Tracking System', style={'textAlign': 'center', 'margin': '50px'}))),
    dbc.Row(
        [
            dbc.Col(dash_table.DataTable(
                id="my-table",
                editable=True,
                row_deletable=True,
                columns=[{'name': i, 'id': i} for i in expense_list_obj.df.columns],
                data=expense_list_obj.records,
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
                                        {"label": "Transport", "value": "Transport"},
                                        {"label": "Food", "value": "Food"},
                                        {"label": "Cloth", "value": "Cloth"},
                                        {"label": "Others", "value": "Others"},
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
            dbc.Col(dcc.Graph(id='pie-chart', figure=expense_obj.fig1), style={'margin': '50px'}),
        ], width=6),
        dbc.Col([
            dbc.Col(dcc.Graph(id='line-chart', figure=expense_obj.fig2), style={'margin': '50px'})
        ], width=6)
    ])
])

# callback function1
@app.callback(
    Output('pie-chart', 'figure'),
    Output('line-chart', 'figure'),
    Input('my-table', 'data')
)
def update_graph(data):
    global length, records
    length = len(data)
    expense_list_obj.records = data
    return expense_obj.update_pie_chart(data), expense_obj.update_line_chart(data)

# callback function2
@app.callback(
    Output('my-table', 'data'),
    Input('add-btn', 'n_clicks'),
    State('item-name-input', 'value'),
    State('amount-input', 'value'),
    State('category-dropdown', 'value'),
    prevent_initial_call=True
)
def add_new_item(btn, item_name, amount, category):
    global length, records, global_count
    expense_list_obj.add_new_item(item_name, amount, category)
    return expense_list_obj.records

if __name__ == '__main__':
    app.run_server(debug=True)
