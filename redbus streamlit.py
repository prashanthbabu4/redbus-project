import streamlit as st
import pandas as pd
from PIL import Image

# Load the data
table = pd.read_csv('3rdproject.csv')
table.columns = table.columns.str.strip()  # Clean column names

# Ensure 'Seats' column is rounded to integers
table["Seats"] = table["Seats"].apply(lambda x: round(x) if isinstance(x, (float, int)) else x)

# Car selection dropdown


# Display title and image
st.markdown("<h1 style='color: black;'>CarDekho Project</h1>", unsafe_allow_html=True)
image = Image.open("C:/Users/dhars/Downloads/3car.jpg")
st.image(image, use_column_width=True)
st.markdown('<h2 style="color:purple; font-size:20px;">WELCOME 🤝</h2>', unsafe_allow_html=True)
st.markdown("<h3 style='color: black;'>Find your right car!</h3>", unsafe_allow_html=True)
carlist = ["Choose your car"] + table["oem"].unique().tolist()
selected_car = st.selectbox("Choose your car", carlist)


# Sidebar filters
if selected_car != "Choose your car":
    selected_model = st.selectbox("Choose your car model", ["Choose your desired model"] + table[table["oem"] == selected_car]["Car model"].unique().tolist())
    
    # Display Filter Title and Input Fields in Sidebar
# Display Filter Title and Input Fields in Sidebar
    st.sidebar.markdown('<h2 style="color:purple; font-size:20px;">Filter Budget ₹</h2>', unsafe_allow_html=True)

# Use numeric values for the slider, without ₹ in the slider arguments
    max_price = st.sidebar.slider("Max Price (INR)", 50000, 1000000, 50000, 50000)

# Display the selected max price with ₹ symbol in the sidebar
    st.sidebar.markdown(f"Selected Max Price: ₹{max_price}")

    st.sidebar.markdown('<h2 style="color:purple; font-size:20px;">Fuel Type⛽ </h2>', unsafe_allow_html=True)
    fuel_type = st.sidebar.selectbox("Choose Fuel Type", ["Choose your fuel type"] + table["Fuel_Type"].unique().tolist())
    
    # Transmission Type section
    st.sidebar.markdown('<h2 style="color:purple; font-size:20px;">Transmission Type </h2>', unsafe_allow_html=True)
    transmission_type = st.sidebar.selectbox("Choose Transmission Type", ["Choose Transmission Type"] + table["Transmission type"].unique().tolist())
    
    # Mileage filter
    st.sidebar.markdown('<h2 style="color:purple; font-size:20px;">Kilometer Driven ⏲</h2>', unsafe_allow_html=True)
    min_mileage, max_mileage = table["Mileage_km"].min(), table["Mileage_km"].max()
    mileage_range = st.sidebar.slider("Mileage (km/l)", min_mileage, max_mileage, (min_mileage, max_mileage))
    
    # Additional filters
    st.sidebar.markdown('<h2 style="color:purple; font-size:20px;">Number Of Owner</h2>', unsafe_allow_html=True)
    owners_list = ["Choose Number of Owners"] + sorted(table["Number of owner"].unique().tolist())
    selected_owners = st.sidebar.selectbox("Choose Number of Owners", owners_list)

    st.sidebar.markdown('<h2 style="color:purple; font-size:20px;">Seat Capacity </h2>', unsafe_allow_html=True)
    seats_list = ["Choose Number of Seats"] + sorted(table["Seats"].dropna().unique().tolist())  # Drop NaN and ensure integer values
    selected_seats = st.sidebar.selectbox("Choose Number of Seats", seats_list)

    st.sidebar.markdown('<h2 style="color:purple; font-size:20px;">Body Type </h2>', unsafe_allow_html=True)
    body_type_list = ["Choose Body Type"] + sorted(table["Body_Type"].dropna().unique().tolist())
    selected_body_type = st.sidebar.selectbox("Choose Body Type", body_type_list)

    # Apply filters
    filtered_table = table[
        (table["oem"] == selected_car) & 
        (table["price"] <= max_price) &
        (table["Fuel_Type"] == fuel_type if fuel_type != "Choose your fuel type" else table["Fuel_Type"]) &
        (table["Transmission type"] == transmission_type if transmission_type != "Choose Transmission Type" else table["Transmission type"]) &
        (table["Mileage_km"] >= mileage_range[0]) &
        (table["Mileage_km"] <= mileage_range[1])
    ]
    
    if selected_owners != "Choose Number of Owners":
        filtered_table = filtered_table[filtered_table["Number of owner"] == selected_owners]
    if selected_seats != "Choose Number of Seats":
        filtered_table = filtered_table[filtered_table["Seats"] == selected_seats]
    if selected_body_type != "Choose Body Type":
        filtered_table = filtered_table[filtered_table["Body_Type"] == selected_body_type]
    if selected_model != "Choose your desired model":
        filtered_table = filtered_table[filtered_table["Car model"] == selected_model]

    # Display filtered results
    if not filtered_table.empty:
        st.write(f"Showing {len(filtered_table)} results.")
        st.dataframe(filtered_table)
    else:
        st.write("No cars found matching your criteria.")
else:
    st.write("Please select a car to filter the results.")
