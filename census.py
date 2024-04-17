import streamlit as st
import pandas as pd
import altair as alt
from vega_datasets import data
import plotly.express as px

# Page functions
def home_page(df):
    if df is not None:
        st.title("US Census Dashboard")
        st.markdown("## Explore US census data through interactive visualizations!")
        st.write("These are the first five rows of your data.")
        st.write(df.head())
        st.write("Choose an option from the side bar if you want to explore more!")

# Function to load and prepare the data
def load_data():
    df = pd.read_csv('/Users/jiyonglee/Downloads/us-population-2010-2019-states-code.csv')
    df['states'] = df['states'].astype(str)  # Example, adjust according to actual column name
    a = df.iloc[:, 4:14]  # extracted year columns
    df = df.melt(id_vars=['id', 'states', 'states_code'],  # reshaped so that year is one column
                            value_vars=a, var_name='year', value_name='population')
    df['year'] = df['year'].astype(int)
    df['population'] = df['population'].str.replace(',', '').astype(int)
    return df

# Function to plot trends
def plot_population_trends(df): # , selected_states
    # Filter data for the selected states
    #mask = df['states'].isin(selected_states)
    #filtered_data = df[mask]

    # Create the plot
    fig = px.line(
        df,
        x='year',
        y='population',
        color='states',
        title='Population Trends by State',
        labels={'population': 'Population', 'year': 'Year'},
        markers=True
    )

    # Improve layout
    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Population',
        legend_title='States',
        hovermode='x unified'
    )

    # Return the figure object to be used in Streamlit
    st.plotly_chart(fig)

# Function to draw a heatmap
def draw_heatmap(df):
    alt.themes.enable("dark")

    heatmap = alt.Chart(df).mark_rect().encode(
        y=alt.Y('year:O',
                axis=alt.Axis(title="Year", titleFontSize=16, titlePadding=15, titleFontWeight=900, labelAngle=0)),
        x=alt.X('states:O', axis=alt.Axis(title="States", titleFontSize=16, titlePadding=15, titleFontWeight=900)),
        color=alt.Color('max(population):Q',
                        legend=alt.Legend(title=" "),
                        scale=alt.Scale(scheme="blueorange")),
        stroke=alt.value('black'),
        strokeWidth=alt.value(0.25),
        # tooltip=[
        #    alt.Tooltip('year:O', title='Year'),
        #    alt.Tooltip('population:Q', title='Population')
        # ]
    ).properties(width=900
                 # ).configure_legend(orient='bottom', titleFontSize=16, labelFontSize=14, titlePadding=0
                 # ).configure_axisX(labelFontSize=14)
                 ).configure_axis(
        labelFontSize=12,
        titleFontSize=12
    )
    st.altair_chart(heatmap, use_container_width=True)


# Function to draw a choropleth map
def draw_choropleth(df):
    states = alt.topo_feature(data.us_10m.url, 'states')
    choropleth = alt.Chart(states).mark_geoshape().encode(
        color='population:Q'
    ).transform_lookup(
        lookup='id',
        from_=alt.LookupData(df, 'id', ['population'])
    ).properties(
        width=500,
        height=300
    ).project(
        type='albersUsa'
    )
    st.altair_chart(choropleth, use_container_width=True)

# Main function to organize the UI
def main():
    df = load_data()

    st.sidebar.title("Visualization Options")
    page = st.sidebar.radio("Choose a visualization:", ["Home", "Trends", "Heatmap", "Choropleth Map"])

    if page == "Home":
        home_page(df)
    elif page == "Trends":
        plot_population_trends(df)
    elif page == "Heatmap":
        draw_heatmap(df)
    elif page == "Choropleth Map":
        draw_choropleth(df)

if __name__ == "__main__":
    main()
