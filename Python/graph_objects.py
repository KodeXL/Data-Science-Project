import pandas as pd
import plotly.express as px
import numpy as np

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("https://raw.githubusercontent.com/KodeXL/Data-Science-Project/main/Data%20Sets/spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

color_discrete_map = {
    'v1.0': '#636EFA',
    'v1.1': '#EF553B',
    'FT': '#00CC96',
    'B4': '#AB63FA',
    'B5': '#FFA15A'
}

# Function to return pie chart for success rate data
def get_pie_chart(entered_site):    
    category_colors = {'Failure':'#EF553B', 'Success':'#636EFA'}
    if entered_site == 'ALL':
        ovr_success = spacex_df.loc[spacex_df['class'] == 1].copy() 
        ovr_success = ovr_success.groupby(['Launch Site'])['class'].count()
        ovr_success = ovr_success.to_frame().reset_index()
        ovr_success['Success Rate']= np.round((ovr_success['class']/ovr_success['class'].sum())*100 , 1)
        fig = px.pie(ovr_success, values='Success Rate',
            template = 'plotly_dark',                     
            names='Launch Site', 
            title='Total Successful Booster Landings by Site',
            custom_data=[ovr_success['class']]
        )
        fig.update_layout(
            margin=dict(t=120),
            font=dict(size=18), 
            title= {'x': 0.47, 'xanchor': 'center'})
        fig.update_traces(
           hovertemplate=
                "Launch Site: %{label}<br>" +
                "Success Landings: %{customdata[0]}<br>" +
                "Percentage: %{percent}<extra></extra>"
        )
        return fig
    else:
        filtered_df = spacex_df.loc[spacex_df['Launch Site'] == entered_site].copy()
        filtered_df_class = filtered_df.groupby(['class'])['class'].count()
        filtered_df_class.index.name = "Outcome"
        filtered_df_class = filtered_df_class.rename(index={0: "Failure", 1: "Success"})
        filtered_df_class = filtered_df_class.to_frame().reset_index()
        fig = px.pie(filtered_df_class, values='class',
            template = 'plotly_dark', 
            names='Outcome', 
            color = 'Outcome',
            color_discrete_map=category_colors,
            category_orders={"Outcome": ["Success", "Failure"]},   
            title=f'Total Successful Booster Landings <br> {entered_site}',
            custom_data=[filtered_df_class['class']]
        )
        fig.update_layout(
            margin=dict(t=120),
            font=dict(size=18), 
            title= {'x': 0.47, 'xanchor': 'center'})
        fig.update_traces(
            hovertemplate=
                "Outcome: %{customdata[0]}<extra></extra>"
        )
        return fig
        # return the outcomes piechart for a selected site


def get_scatter_chart(entered_site, payload_range):
    if entered_site == 'ALL':
        filtered_df = spacex_df.loc[(spacex_df['Payload Mass (kg)']>= payload_range[0]) &
                                (spacex_df['Payload Mass (kg)']<= payload_range[1])].copy()
        filtered_df['Booster Version Category'] = [x.split()[1] for x in filtered_df['Booster Version']]
        filtered_df["Outcome"] = filtered_df["class"].replace({1: "Success", 0: "Failure"})    
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y = 'Outcome', color='Booster Version Category',
                template = 'plotly_dark', 
                category_orders={"Outcome": ["Success", "Failure"]},
                color_discrete_map=color_discrete_map,
                labels={'Booster Version Category': 'Version'},
                title='Booster Version Evolution<br>Payload vs Landing Success for All Sites ')
        fig.update_layout(
            legend_title_text='',
            height=600,
            margin=dict(t=150, r=80, l = 20),
            font=dict(size=18), 
            title= {'x': 0.47, 
                'xanchor': 'center',
                #'pad': {'b': 500}, 
                'y': 0.9
            }
        )
        fig.update_traces(hovertemplate=
                            "Booster Version Category: %{fullData.name}<br>" +
                            "Payload Mass (kg): %{x}<br>" +
                            "Outcome: %{y}<extra></extra>"
        )
        return fig
    else:
        filtered_df = spacex_df.loc[(spacex_df['Launch Site'] == entered_site) & 
                      (spacex_df['Payload Mass (kg)']>= payload_range[0]) &
                      (spacex_df['Payload Mass (kg)']<= payload_range[1])].copy()
        filtered_df["Outcome"] = filtered_df["class"].replace({1: "Success", 0: "Failure"})
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y = 'Outcome', color='Booster Version Category',
                template = 'plotly_dark', 
                category_orders={"Outcome": ["Success", "Failure"]},
                color_discrete_map=color_discrete_map,
                labels={'Booster Version Category': 'Version'},
                title= f'Booster Version Evolution<br>Payload vs Landing Success - {entered_site}')
        fig.update_layout(
            legend_title_text='',
            height=600,
            margin=dict(t=150, r=80, l = 20 ),
            font=dict(size=18), 
            title= {'x': 0.47, 
                'xanchor': 'center', 
                'y': 0.9
            }
        )
        fig.update_traces(hovertemplate=
                            "Booster Version: %{fullData.name}<br>" +
                            "Payload Mass (kg): %{x}<br>" +
                            "Outcome: %{y}<extra></extra>"
        )
        return fig
