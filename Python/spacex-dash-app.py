import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from dash.dependencies import Input, Output
from Python.graph_objects import get_pie_chart, get_scatter_chart

load_figure_template('CYBORG')

footer  = dbc.Container(
            dbc.Row(
                [
                    dbc.Col(html.A("Olamide Olayinka | Github", href = 'https://github.com/kodexl'))
                ],
            ),
        className = 'footer',
        fluid = True
        )

# Create a dash application
app = dash.Dash(__name__, external_stylesheets= [dbc.themes.CYBORG])
server = app.server

# Create an app layout
app.layout = html.Div(
    children=[
        html.H1('SpaceX Launch Records Dashboard', className = 'dropdown-label',
        ),
        # Add a dropdown list to enable Launch Site selection
        # The default select value is for ALL sites
        dcc.Dropdown(id='site-dropdown',            
                    options=[
                        {'label': 'All Sites', 'value': 'ALL'},
                        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                        {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                        {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                    ],
                    value='ALL',
                    placeholder="Select a Launch Site here",
                    searchable=True,
                    style={'color': 'black'},
                    className = 'pad'
        ),
        # Add pie chart to show the total successful launches count for all sites
        # If a specific launch site was selected, show the Success vs. Failed counts for the site
        html.Div(dcc.Graph(id='success-pie-chart', className = 'charts')),

        html.P("Payload range (Kg):", className = 'pad'),
        # Add a slider to select payload range
        dcc.RangeSlider(id='payload-slider',
                        min = 0,
                        max = 10000,
                        step = 1000,
                        #marks={i: str(i) for i in range(0, 10001, 1000)},
                        value = [0, 10000],
                        className = 'pad'
        ),

        # Adding scatter chart to show the correlation between payload and launch success
        html.Div(dcc.Graph(id='success-payload-scatter-chart', className = 'charts')),

        footer
    ]
)

# Callback function for `site-dropdown` and `payload-slider` as input, `success-pie-chart` as output
@app.callback(
    [Output(component_id = 'success-pie-chart', component_property = 'figure'),
     Output(component_id = 'success-payload-scatter-chart', component_property = 'figure')],
    [Input(component_id = 'site-dropdown', component_property = 'value'),
     Input(component_id = 'payload-slider', component_property = 'value')]
)
def update_charts(entered_site, payload_range):
    pie_fig = get_pie_chart(entered_site)
    scatter_fig = get_scatter_chart(entered_site, payload_range)
    return pie_fig, scatter_fig

# Run the app
if __name__ == '__main__':
    app.run()
