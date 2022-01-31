import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd 

app = dash.Dash(__name__)
app.title = 'Military Pay'
app._favicon = ("bills.png")
server = app.server  # expose server variable for Procfile

# _________________ Read local data _________________
zip_mha_data = pd.read_csv('./data/sorted_zipmha22.txt', sep = ' ', header=None, names = ['zip','MHA'], dtype = str)

heads = ['MHA', 'E-1', 'E-2', 'E-3', 'E-4', 'E-5', 'E-6', 'E-7', 'E-8', 'E-9', 'W-1', 'W-2', 'W-3', 'W-4', 'W-5', 'O-1E', 'O-2E', 'O-3E', 'O-1', 'O-2', 'O-3', 'O-4', 'O-5', 'O-6', 'O-7', 'O-8', 'O-9', 'O-10']

#Data from https://www.defensetravel.dod.mil/site/pdcFiles.cfm?dir=/Allowances/BAH/PDF/
with_dependents_bah = pd.read_csv('./data/bahw22.txt', sep = ',', header=None, names = heads, dtype = str)
without_dependents_bah = pd.read_csv('./data/bahwo22.txt', sep = ',', header=None, names = heads, dtype = str)
#Data from https://militarybenefits.info/2022-military-pay-charts/
base_pay_tables = pd.read_csv('./data/2022_MIL_PAY_TABLE.csv')

# _________________ APP _______________________
app.layout = html.Div([
   
    html.Div(className="two-thirds column", children=[ 
        html.Header([
            html.Img(src=app.get_asset_url('logo.png')),
            html.Title('Visualize Military Pay'),
        ]),
        
        html.Div(children=[dcc.Markdown('''
            2022 Military Pay Data
            
            How much do I really make?  Where is it all coming from and where is it all going?!

            Should I get married for that sweet dependant pay?  Can I actually afford my **18% APR** Mustang?

            This app is a playground for Sankey diagrams and hopes to answer some of these questions.  Enjoy!
            ''')
        ]),

        # SANKEY
        html.Div(children=[
            html.Div(children=[
                dcc.Graph(id='update-graph', style={'height':400}),
            ]),
        ]),
    ]),
      

    # USER INPUTS
     html.Div(className="one-third column app__right__section", children=[
        html.Div(children=[
            html.Div(children=[
                html.Label('Rank'),
                dcc.Dropdown(
                    id='rank',
                    options=[
                        {'label': 'E-1', 'value': 'E-1'},
                        {'label': 'E-2', 'value': 'E-2'},
                        {'label': 'E-3', 'value': 'E-3'},
                        {'label': 'E-4', 'value': 'E-4'},
                        {'label': 'E-5', 'value': 'E-5'},
                        {'label': 'E-6', 'value': 'E-6'},
                        {'label': 'E-7', 'value': 'E-7'},
                        {'label': 'E-8', 'value': 'E-8'},
                        {'label': 'E-9', 'value': 'E-9'},
                        {'label': 'O-1', 'value': 'O-1'},
                        {'label': 'O-2', 'value': 'O-2'},
                        {'label': 'O-3', 'value': 'O-3'},
                        {'label': 'O-4', 'value': 'O-4'},
                        {'label': 'O-5', 'value': 'O-5'},
                        {'label': 'O-6', 'value': 'O-6'},
                        {'label': 'O-7', 'value': 'O-7'},
                        {'label': 'O-8', 'value': 'O-8'},
                    ],
                    value='E-1'
                ),
                html.Br(),

                html.Label('Years of Service'),
                dcc.Dropdown(
                    id='yrs_of_service',
                    options=[
                        {'label': '1', 'value': 1},
                        {'label': '2', 'value': 2},
                        {'label': '3', 'value': 3},
                        {'label': '4', 'value': 4},
                        {'label': '5', 'value': 5},
                        {'label': '6', 'value': 6},
                        {'label': '7', 'value': 7},
                        {'label': '8', 'value': 8},
                        {'label': '9', 'value': 9},
                        {'label': '10', 'value': 10},
                        {'label': '11', 'value': 11},
                        {'label': '12', 'value': 12},
                        {'label': '13', 'value': 13},
                        {'label': '14', 'value': 14},
                        {'label': '15', 'value': 15},
                        {'label': '16', 'value': 16},
                        {'label': '17', 'value': 17},
                        {'label': '18', 'value': 18},
                        {'label': '19', 'value': 19},
                        {'label': '20', 'value': 20},
                    ],
                    value='1'
                ),
                html.Br(),

                html.Label('Dependants?'),
                dcc.RadioItems(
                    id='dependants',
                    options=[
                        {'label': 'Yes', 'value': 'True'},
                        {'label': 'No', 'value': 'False'},
                    ],
                    value='True',
                ),
                html.Br(),

                html.Label('Zip Code'),
                dcc.Input(
                    id='zip_code',
                    type='number',
                    max=99999,
                    value='32544',
                    debounce = True,
                ),
                html.Br(),

                #html.Button('Update', id='update-data', value='clicked'),
            ]),
        ]),
        
        # TSP SLIDER
        html.Div(children=[
            html.Div(children=[
                html.Label('TSP Contribution %'),
                dcc.Slider(
                id='tsp_savings_rate',
                min=0,
                max=50,
                step=1,
                marks={
                    0: '0%',
                    50: '50%',
                },
                tooltip={"placement": "bottom", "always_visible": True},
                value=15,
            )
            ]),
        ]),

        
        # EXPENSES
        html.Div(children=[
            html.Div(children=[
                html.Label('Monthly Expenses:'),
                html.Button('Add Expense', id='add_expense', n_clicks=0),
                html.Br(),
                dcc.Input(
                    id='expense_name_1',
                    type='text',
                    placeholder='Rent',
                    debounce = True,
                ),
                html.Div([
                    dcc.Input(
                        id='expense_price_1',
                        type='number',
                        placeholder='800',
                        debounce = True,
                    ),
                ]),
                
                html.Br(),
                dcc.Input(
                    id='expense_name_2',
                    type='text',
                    placeholder='Food',
                    debounce = True,
                ),
                html.Div([
                    dcc.Input(
                        id='expense_price_2',
                        type='number',
                        placeholder='200',
                        debounce = True,
                    ),
                ]),

                html.Br(),
                dcc.Input(
                    id='expense_name_3',
                    type='text',
                    placeholder='',
                    debounce = True,
                ),
                html.Div([
                    dcc.Input(
                        id='expense_price_3',
                        type='number',
                        placeholder='',
                        debounce = True,
                    ),
                ]),

                html.Br(),
                dcc.Input(
                    id='expense_name_4',
                    type='text',
                    placeholder='',
                    debounce = True,
                ),
                html.Div([
                    dcc.Input(
                        id='expense_price_4',
                        type='number',
                        placeholder='',
                        debounce = True,
                    ),
                ]),

                html.Br(),
                dcc.Input(
                    id='expense_name_5',
                    type='text',
                    placeholder='',
                    debounce = True,
                ),
                html.Div([
                    dcc.Input(
                        id='expense_price_5',
                        type='number',
                        placeholder='',
                        debounce = True,
                    ),
                ]),
            ]),
        ]),

        # INCOMES
        html.Div(children=[
            html.Div(children=[
                html.Label('Additional Income:'),
                html.Button('Add Income', id='add_income', n_clicks=0),
                html.Br(),
                dcc.Input(
                    id='income_name_1',
                    type='text',
                    placeholder='Hustle 1',
                    debounce = True,
                ),
                html.Div([
                    dcc.Input(
                        id='income_price_1',
                        type='number',
                        placeholder='800',
                        debounce = True,
                    ),
                ]),
                
                html.Br(),
                dcc.Input(
                    id='income_name_2',
                    type='text',
                    placeholder='Landlord',
                    debounce = True,
                ),
                html.Div([
                    dcc.Input(
                        id='income_price_2',
                        type='number',
                        placeholder='200',
                        debounce = True,
                    ),
                ]),

                html.Br(),
                dcc.Input(
                    id='income_name_3',
                    type='text',
                    placeholder='Uber',
                    debounce = True,
                ),
                html.Div([
                    dcc.Input(
                        id='income_price_3',
                        type='number',
                        placeholder='100',
                        debounce = True,
                    ),
                ]),
            ]),
        ]),
        
     # End SideBar 
     ]),    
#End of App
])

# _____________________ CALLBACKS _______________________________

# EXPENSES
@app.callback([Output(component_id='expense_name_1', component_property='style'),
               Output(component_id='expense_price_1', component_property='style'),     
                ],
              [Input(component_id='add_expense', component_property='n_clicks'),         
              ],
              )
def show_expense_elements(n_clicks):
    if int(n_clicks) == 0:
        return [{'display': 'none'}, {'display': 'none'}]
    elif int(n_clicks) >= 1:
        return [{'display': 'block'}, {'display': 'block'}]

@app.callback([Output(component_id='expense_name_2', component_property='style'),
               Output(component_id='expense_price_2', component_property='style'),     
                ],
              [Input(component_id='add_expense', component_property='n_clicks'),         
              ],
              )
def show_expense_elements(n_clicks):
    if int(n_clicks) <= 1:
        return [{'display': 'none'}, {'display': 'none'}]
    elif int(n_clicks) >= 2:
        return [{'display': 'block'}, {'display': 'block'}]

@app.callback([Output(component_id='expense_name_3', component_property='style'),
               Output(component_id='expense_price_3', component_property='style'),     
                ],
              [Input(component_id='add_expense', component_property='n_clicks'),         
              ],
              )
def show_expense_elements(n_clicks):
    if int(n_clicks) <= 2:
        return [{'display': 'none'}, {'display': 'none'}]
    elif int(n_clicks) >= 3:
        return [{'display': 'block'}, {'display': 'block'}]

@app.callback([Output(component_id='expense_name_4', component_property='style'),
               Output(component_id='expense_price_4', component_property='style'),     
                ],
              [Input(component_id='add_expense', component_property='n_clicks'),         
              ],
              )
def show_expense_elements(n_clicks):
    if int(n_clicks) <= 3:
        return [{'display': 'none'}, {'display': 'none'}]
    elif int(n_clicks) >= 4:
        return [{'display': 'block'}, {'display': 'block'}]

@app.callback([Output(component_id='expense_name_5', component_property='style'),
               Output(component_id='expense_price_5', component_property='style'),     
                ],
              [Input(component_id='add_expense', component_property='n_clicks'),         
              ],
              )
def show_expense_elements(n_clicks):
    if int(n_clicks) <= 4:
        return [{'display': 'none'}, {'display': 'none'}]
    elif int(n_clicks) >= 5:
        return [{'display': 'block'}, {'display': 'block'}]

# Incomes
@app.callback([Output(component_id='income_name_1', component_property='style'),
               Output(component_id='income_price_1', component_property='style'),     
                ],
              [Input(component_id='add_income', component_property='n_clicks'),         
              ],
              )
def show_expense_elements(n_clicks):
    if int(n_clicks) == 0:
        return [{'display': 'none'}, {'display': 'none'}]
    elif int(n_clicks) >= 1:
        return [{'display': 'block'}, {'display': 'block'}]

@app.callback([Output(component_id='income_name_2', component_property='style'),
               Output(component_id='income_price_2', component_property='style'),     
                ],
              [Input(component_id='add_income', component_property='n_clicks'),         
              ],
              )
def show_expense_elements(n_clicks):
    if int(n_clicks) <= 1:
        return [{'display': 'none'}, {'display': 'none'}]
    elif int(n_clicks) >= 2:
        return [{'display': 'block'}, {'display': 'block'}]

@app.callback([Output(component_id='income_name_3', component_property='style'),
               Output(component_id='income_price_3', component_property='style'),     
                ],
              [Input(component_id='add_income', component_property='n_clicks'),         
              ],
              )
def show_expense_elements(n_clicks):
    if int(n_clicks) <= 2:
        return [{'display': 'none'}, {'display': 'none'}]
    elif int(n_clicks) >= 3:
        return [{'display': 'block'}, {'display': 'block'}]

# __________________________ UPDATE SANKEY __________________________
@app.callback(Output('update-graph', 'figure'),
               [Input('rank', 'value'),
                Input('yrs_of_service', 'value'),   
                Input('dependants', 'value'), 
                Input('zip_code', 'value'),    
                Input('tsp_savings_rate', 'value'),
                Input('expense_name_1', 'value'),
                Input('expense_price_1', 'value'),
                Input('expense_name_2', 'value'),
                Input('expense_price_2', 'value'),
                Input('expense_name_3', 'value'),
                Input('expense_price_3', 'value'), 
                Input('expense_name_4', 'value'),
                Input('expense_price_4', 'value'),
                Input('expense_name_5', 'value'),
                Input('expense_price_5', 'value'),
                Input('income_name_1', 'value'),
                Input('income_price_1', 'value'),
                Input('income_name_2', 'value'),
                Input('income_price_2', 'value'),
                Input('income_name_3', 'value'),
                Input('income_price_3', 'value'),                
              ],
              #State('update-data', 'value'),
              )
def update_graph(rank, yrs_of_service, dependants, zip_code, tsp_savings_rate, \
                expense_name_1, expense_price_1, expense_name_2, expense_price_2, expense_name_3, expense_price_3, expense_name_4, expense_price_4, expense_name_5, expense_price_5,\
                income_name_1, income_price_1, income_name_2, income_price_2, income_name_3, income_price_3):
    # USER INPUTS
    yrs_of_service = int(yrs_of_service)
    tsp_savings_rate = int(tsp_savings_rate)
    
    # Get Military Housing Area from Data
    try:
        mha = zip_mha_data[zip_mha_data['zip'] == str(zip_code)]['MHA'].values[0]
    except: 
        return 

    if dependants == 'True':
        bah = with_dependents_bah[with_dependents_bah['MHA'] == mha][rank]
    else:
        bah = without_dependents_bah[without_dependents_bah['MHA'] == mha][rank]

    base_pay = base_pay_tables[base_pay_tables['PAY GRADE'] == rank].iloc[0, yrs_of_service]
    tsp_savings = base_pay * tsp_savings_rate / 100

    # New TSP Matching
    if tsp_savings_rate >= 5:
        agency_match = .05 * base_pay
    else:
        agency_match = tsp_savings_rate * base_pay / 100

    if rank in ['O-1E', 'O-2E', 'O-3E', 'O-1', 'O-2', 'O-3', 'O-4', 'O-5', 'O-6', 'O-7', 'O-8', 'O-9', 'O-10']:
        bas = 266.18 #2021 officer bas
    else:
        bas = 386.5 #2021 enlisted bas
    
    #2021 Federal Income Tax
    annual_pay = (base_pay * 12) - (tsp_savings * 12) #deduct 401k contributions
    if annual_pay <= 9950:
        federal_tax = (.1 * annual_pay) / 12
    elif annual_pay <= 40525:
        federal_tax = ((.1 * 9950) + (annual_pay - 9950) * .12) / 12
    elif annual_pay <= 86375:
        federal_tax = ((.1 * 9950) + (30575 * .12) + (annual_pay-40525) * .22) / 12
    else:
        federal_tax = ((.1 * 9950) + (30575 * .12) + (45850*.22) + (annual_pay-86375) * .24) / 12
        #don't think anyone is raking more than this


    label = ["Base Pay", \
            "BAH", \
            "BAS", \
            income_name_1, \
            income_name_2, \
            income_name_3, \
            "Total Monthly Income", \
            "Agency Match",\
            "TSP", \
            expense_name_1, \
            expense_name_2, \
            expense_name_3, \
            expense_name_4, \
            expense_name_5, \
            "Federal Income Tax (Est)", \
            ]

    source = [0, 1, 2, 3, 4, 5, 6, 7, 6, 6, 6, 6, 6, 0]
    target = [6, 6, 6, 6, 6, 6, 8, 8, 9, 10, 11, 12, 13, 14]

    value =  [base_pay, bah, bas, income_price_1, income_price_2, income_price_3,
             tsp_savings, agency_match, expense_price_1, expense_price_2, expense_price_3, expense_price_4, expense_price_5,
             federal_tax]

    link = dict(source = source, target = target, value = value)
    node = dict(label = label, pad=100, thickness=5)
    data = go.Sankey(link = link, node=node)
    
    return go.Figure(data)

if __name__ == '__main__':
    app.run_server(debug=True)
