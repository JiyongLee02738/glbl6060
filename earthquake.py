
# !pip install streamlit plotly

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Page functions
def home_page(df):
    if df is not None:
        #df = pd.read_csv(file)
        st.title("Earthquake Data Analysis Dashboard")
        st.markdown("## Welcome to the Earthquake Data Analysis Dashboard!")
        st.write("These are the first five rows of your data.")
        st.write(df.head())
        st.write("Choose an option from the side bar if you want to explore more!")

def data_overview(df):
    if df is not None:
        #df = pd.read_csv(file)
        st.title("Data Overview")
        st.write(df)
        st.header("Summary Stats")
        st.write(df.describe())

def interactive_plot(df):
    # if file is not None:
    #df = pd.read_csv(file)
    st.title("Interactive Plot")
    # Filter to reduce data size for visualization (optional, depending on performance)
    filtered_data = df.sample(n=1000, random_state=1)  # Sample 1000 random rows

    st.header("Earthquake Visualization")
    # Create an interactive global map of earthquakes
    fig = px.scatter_geo(filtered_data,
                         lat='Latitude',
                         lon='Longitude',
                         color='Magnitude',  # Color by magnitude
                         size='Magnitude',  # Size by magnitude
                         hover_name='ID',
                         hover_data=['Date', 'Depth', 'Magnitude'],
                         title='Global Distribution of Earthquakes',
                         projection='natural earth',
                         color_continuous_scale='Plasma')

    # Show the plot
    fig.show()

        #fig, ax = plt.subplots(1, 1)
        #ax.scatter(x=df['Depth'], y=df['Magnitude'])
        #ax.set_xlabel("Depth")
        #ax.set_ylabel("Magnitude")

        #st.pyplot(fig)

def interactive_histogram(file, column):
    fig = px.histogram(file, x=column, title=f'Distribution of {column}', template="plotly_dark")
    st.plotly_chart(fig)

    # fig = px.histogram(df, x=selected_column, title=f'Histogram of {selected_column}')
    # st.plotly_chart(fig, use_container_width=True)

# Main app
def main():
    st.sidebar.title("Navigation")
    file = st.sidebar.file_uploader("Upload your file")
    options = ["Home", "Data Overview", "Interactive Plot"]
    selected_option = st.sidebar.radio("Choose an option:", options)

    if file:
        df = pd.read_csv(file)
        if selected_option == "Home":
            home_page(df)
        elif selected_option == "Data Overview":
            st.title("Data Overview")
            data_overview(df)
            # Allow the user to select a column for histogram within the "Data Overview" section
            st.sidebar.subheader("Histogram Settings")
            selected_column = st.sidebar.selectbox('Choose a column for histogram', df.columns)

            # Display data overview and histogram in the main area
            if pd.api.types.is_numeric_dtype(df[selected_column]):
                interactive_histogram(df, selected_column)
            else:
                st.error('Please select a numeric column for the histogram.')

        elif selected_option == "Interactive Plot":
            interactive_plot(df)

if __name__ == "__main__":
    main()
