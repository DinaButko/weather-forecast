import streamlit as st
import plotly.express as px
from backend import get_data

# Custom CSS to inject a yellow gradient background
yellow_gradient = """
<style>
    .stApp {
        background-image: linear-gradient(to right, #f7f8c4, #ffe585);
    }
</style>
"""

st.markdown(yellow_gradient, unsafe_allow_html=True)

# Command to run streamlit locally: streamlit run main.py
st.title(" 🌤 Weather forecast for the Next Days.")

place = st.text_input("Place: ")
days = st.slider("Forecast Days", min_value=1, max_value=5, help="Select: the number of forecasted days")

option = st.selectbox("Select data to view",
                      ("🌡 Temperature", "🌨 Sky"))

st.subheader(f"{option} for the next {days} days in {place}.")
if place:
    # Get temperature/sky data
    try:
        filtered_data = get_data(place, days)

        if option == "🌡 Temperature":
            temperatures = [dict["main"]["temp"] / 10 for dict in filtered_data]
            dates = [dict["dt_txt"] for dict in filtered_data]
            figure = px.line(x=dates, y=temperatures, labels={"x": "Date", "y": "Temperature (C)"})

            st.plotly_chart(figure)
        if option == "🌨 Sky":
            images = {"Clear": "images/clear.png", "Clouds": "images/cloud.png", "Rain": "images/rain.png",
                      "Snow": "images/snow.png"}
            sky_conditions = [dict["weather"][0]["main"] for dict in filtered_data]
            image_paths = [images[condition] for condition in sky_conditions]
            st.image(image_paths, width=115)
    except KeyError:
        st.write("That place doesn't exist.")




