import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from sheet import initialise_sheets
from misc import load_config
from data import load_data_from_sheet
import flask

external_stylesheets = [dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Malaysia - Covid-19 Dashboard"
server = app.server

# Config
config = load_config()

# Dataframes to be initialised
CASES_DATA = None
VACCINATION_NATIONAL_DATA = None
VACCINATION_STATE_DATA = None

# Google sheets service object
sheets = initialise_sheets()

# Navbar
COVID_LOGO = "covid.png"
home_button = dbc.NavItem(
    dbc.NavLink(
        'Home',
        href="#home",
        external_link=True,
        className='navlinks'))
navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                dbc.Row(
                    [
                        dbc.Col(
                            html.Img(
                                src=app.get_asset_url(COVID_LOGO),
                                className='logo',
                                height="50px")),
                    ],
                    align="center",
                    no_gutters=True,
                ),
                href="#home",
            ),
            dbc.NavbarToggler(
                id="navbar-toggler"),
            dbc.Collapse(
                dbc.Nav(
                    [home_button],
                    className='ml-auto work-sans',
                    navbar=True),
                id="navbar-collapse",
                navbar=True),
        ],
    ),
    color="rgb(42,62,66)",
    dark=True,
    style={
        'background-color': '#191919'},
    className='navbar-change',
    expand='lg')

# Jumbotron
jumbotron = dbc.Container(
    dbc.Jumbotron(
        [
            html.H2("Malaysia COVID-19 Dashboard", className="display-3"),
            html.P(
                "Important statistics to keep track of how we are doing against the virus.",
                className="lead blue",
            ),
        ]
    )
)

app.layout = html.Div([
    navbar,
    jumbotron,
    dbc.Container([
        dcc.Dropdown(
            id="new_cases_plot_dropdown",
            options=[{"label": "Last 30 days", "value": 30},
                     {"label": "Last 7 days", "value": 7}],
            value=30,
            clearable=False,
        ),
        dcc.Graph(id='new_cases_plot')]),
    dcc.Interval(
        id='interval-component',
        interval=60 * 1000,  # in milliseconds
        n_intervals=0
    ),
    html.Div(id='hidden-div', style={'display': 'none'})
])


@app.callback(Output('new_cases_plot',
                     'figure'),
              [Input('interval-component',
                     'n_intervals'),
               Input('new_cases_plot_dropdown',
                     'value')])
def new_cases_plot(n, daterange):
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Bar chart of new cases
    fig.add_trace(go.Bar(
        x=CASES_DATA.date[-daterange:],
        y=CASES_DATA.newCase[-daterange:].apply(float),
        name="New cases"
    ))

    # Line chart of test positivity rate
    fig.add_trace(go.Scatter(
        x=CASES_DATA.date[-daterange:],
        y=CASES_DATA['Positivity rate'][-daterange:].apply(float),
        name="Test positivity rate"
    ), secondary_y=True)

    fig.update_layout(
        title="Covid-19 cases",
        yaxis_title="# new cases",
        font=dict(
            family="Roboto",
            size=18,
            color="Black"
        )
    )
    return fig


@app.callback(Output('hidden-div',
                     'children'),
              [Input('interval-component',
                     'n_intervals'),
               ])
def load_data(n):
    _load_data()
    # We need to do this since we are abusing dash's timer to refresh the data
    if n is not None:
        raise dash.exceptions.PreventUpdate


@app.server.before_first_request
def _load_data():
    global CASES_DATA
    global VACCINATION_NATIONAL_DATA
    global VACCINATION_STATE_DATA

    CASES_DATA = load_data_from_sheet(
        sheets,
        config.get('spreadsheet_id'),
        config['sheets']['cases']['sheet_name'],
        config['sheets']['cases']['start_col'],
        config['sheets']['cases']['end_col'])

    VACCINATION_NATIONAL_DATA = load_data_from_sheet(
        sheets,
        config.get('spreadsheet_id'),
        config['sheets']['vaccination_national']['sheet_name'],
        config['sheets']['vaccination_national']['start_col'],
        config['sheets']['vaccination_national']['end_col'])

    VACCINATION_STATE_DATA = load_data_from_sheet(
        sheets,
        config.get('spreadsheet_id'),
        config['sheets']['vaccination_state']['sheet_name'],
        config['sheets']['vaccination_state']['start_col'],
        config['sheets']['vaccination_state']['end_col'])


if __name__ == '__main__':
    app.run_server(debug=False)
