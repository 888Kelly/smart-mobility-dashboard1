import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import folium
from streamlit_folium import st_folium
import numpy as np
import random
from datetime import datetime, timedelta
import math

# Set page config
st.set_page_config(
    page_title="SmartMobility Dashboard",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .fun-fact {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Load and prepare data
@st.cache_data
def load_parking_data():
    # Sample data based on the CSV structure
    data = {
        'Berlin': [
            {'name': 'Tiefgarage Plaza', 'address': 'Mildred-Harnack-Straße 11-13, 10243 Berlin', 'postal_code': '10243', 'lat': 52.5170, 'lon': 13.4015, 'fee_per_hour': 2.5, 'ev_charging': True, 'total_spots': 400, 'available_spots': 45},
            {'name': 'Parkhaus Spandau Altstädter Ring', 'address': 'Altstädter Ring 20, 13597 Berlin', 'postal_code': '13597', 'lat': 52.5350, 'lon': 13.2050, 'fee_per_hour': 1.5, 'ev_charging': False, 'total_spots': 300, 'available_spots': 78},
            {'name': 'Tiefgarage Hauptbahnhof P1', 'address': 'Clara-Jaschke-Straße 88, 10557 Berlin', 'postal_code': '10557', 'lat': 52.5250, 'lon': 13.3693, 'fee_per_hour': 3.0, 'ev_charging': True, 'total_spots': 814, 'available_spots': 120},
            {'name': 'Parkhaus Europa-Center', 'address': 'Nürnberger Straße 5-7, 10787 Berlin', 'postal_code': '10787', 'lat': 52.5044, 'lon': 13.3347, 'fee_per_hour': 2.8, 'ev_charging': True, 'total_spots': 954, 'available_spots': 230}
        ],
        'Munich': [
            {'name': 'Tiefgarage Hauptbahnhof Süd P4', 'address': 'Senefelderstraße, 80336 München', 'postal_code': '80336', 'lat': 48.1374, 'lon': 11.5588, 'fee_per_hour': 3.0, 'ev_charging': False, 'total_spots': 242, 'available_spots': 34},
            {'name': 'Tiefgarage Stachus', 'address': 'Herzog-Wilhelm-Straße 11, 80331 München', 'postal_code': '80331', 'lat': 48.1395, 'lon': 11.5661, 'fee_per_hour': 2.8, 'ev_charging': False, 'total_spots': 700, 'available_spots': 89},
            {'name': 'Tiefgarage Marienplatz', 'address': 'Rindermarkt 16, 80331 München', 'postal_code': '80331', 'lat': 48.1374, 'lon': 11.5755, 'fee_per_hour': 3.2, 'ev_charging': True, 'total_spots': 265, 'available_spots': 12}
        ],
        'Hamburg': [
            {'name': 'Tiefgarage Am Sandtorkai', 'address': 'Singapurstraße Haus 2, 20457 Hamburg', 'postal_code': '20457', 'lat': 53.5438, 'lon': 9.9955, 'fee_per_hour': 2.2, 'ev_charging': True, 'total_spots': 277, 'available_spots': 56},
            {'name': 'Parkhaus Speicherstadt', 'address': 'Am Sandtorkai 6, 20457 Hamburg', 'postal_code': '20457', 'lat': 53.5441, 'lon': 9.9899, 'fee_per_hour': 2.5, 'ev_charging': False, 'total_spots': 814, 'available_spots': 145},
            {'name': 'Tiefgarage Europa Passage', 'address': 'Hermannstraße 11, 20095 Hamburg', 'postal_code': '20095', 'lat': 53.5511, 'lon': 10.0006, 'fee_per_hour': 2.8, 'ev_charging': False, 'total_spots': 720, 'available_spots': 98}
        ],
        'Frankfurt': [
            {'name': 'Tiefgarage Alte Oper', 'address': 'Opernplatz 1, 60313 Frankfurt am Main', 'postal_code': '60313', 'lat': 50.1188, 'lon': 8.6719, 'fee_per_hour': 2.5, 'ev_charging': True, 'total_spots': 402, 'available_spots': 67},
            {'name': 'Parkhaus Börse', 'address': 'Meisengasse, 60313 Frankfurt am Main', 'postal_code': '60313', 'lat': 50.1136, 'lon': 8.6797, 'fee_per_hour': 2.5, 'ev_charging': True, 'total_spots': 891, 'available_spots': 134},
            {'name': 'Tiefgarage Hauptbahnhof Nord P1', 'address': 'Poststraße 3, 60329 Frankfurt am Main', 'postal_code': '60329', 'lat': 50.1072, 'lon': 8.6647, 'fee_per_hour': 4.0, 'ev_charging': True, 'total_spots': 365, 'available_spots': 89}
        ],
        'Cologne': [
            {'name': 'Parkhaus Dom/Römisch-Germanisches Museum', 'address': 'Burgmauer 40, 50667 Köln', 'postal_code': '50667', 'lat': 50.9413, 'lon': 6.9581, 'fee_per_hour': 2.8, 'ev_charging': True, 'total_spots': 620, 'available_spots': 95},
            {'name': 'Tiefgarage Schildergasse', 'address': 'Schildergasse 57, 50667 Köln', 'postal_code': '50667', 'lat': 50.9356, 'lon': 6.9477, 'fee_per_hour': 3.2, 'ev_charging': False, 'total_spots': 450, 'available_spots': 23},
            {'name': 'Parkhaus Hauptbahnhof', 'address': 'Breslauer Platz 1, 50668 Köln', 'postal_code': '50668', 'lat': 50.9429, 'lon': 6.9591, 'fee_per_hour': 3.5, 'ev_charging': True, 'total_spots': 800, 'available_spots': 156}
        ]
    }
    
    # Convert to DataFrame
    all_data = []
    for city, spots in data.items():
        for spot in spots:
            spot['city'] = city
            all_data.append(spot)
    
    return pd.DataFrame(all_data)

# Calculate distance between two points
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Earth's radius in kilometers
    
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    
    a = math.sin(delta_lat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    return R * c

# Generate CO2 emission data
def generate_co2_data():
    transport_modes = {
        'Car (Gasoline)': 120,  # g CO2/km
        'Car (Diesel)': 110,
        'Electric Car': 30,
        'Hybrid Car': 80,
        'Public Transport': 25,
        'Bicycle': 0,
        'Walking': 0,
        'E-Scooter': 15
    }
    return transport_modes

# Fun facts
def get_fun_fact():
    facts = [
        "🚗 The average car spends 95% of its time parked!",
        "🌱 One electric car can save 1.5 tons of CO2 per year compared to gasoline cars.",
        "🚴‍♀️ Cycling just 10km per week can save 1,600kg of CO2 annually.",
        "🏙️ Smart parking systems can reduce urban traffic by up to 30%.",
        "⚡ Germany has over 60,000 public EV charging points.",
        "🚊 Public transport in German cities is 5x more efficient than private cars.",
        "🌍 Transportation accounts for 24% of global CO2 emissions.",
        "🅿️ Dynamic parking pricing can reduce search time by 43%."
    ]
    return random.choice(facts)

# Main application
def main():
    st.markdown('<h1 class="main-header">🚗 SmartMobility Dashboard</h1>', unsafe_allow_html=True)
    
    # Load data
    df = load_parking_data()
    
    # Sidebar filters
    st.sidebar.title("📍 Location & Preferences")
    
    # City selection
    selected_city = st.sidebar.selectbox("Select City", ["Berlin", "Munich", "Hamburg", "Frankfurt", "Cologne"])
    
    # Location input
    st.sidebar.subheader("Current Location")
    location_method = st.sidebar.radio("Input method:", ["City Center", "Postal Code", "Coordinates"])
    
    if location_method == "Postal Code":
        postal_code = st.sidebar.text_input("Enter Postal Code", "10117")
        user_lat, user_lon = 52.5200, 13.4050  # Default Berlin center
    elif location_method == "Coordinates":
        user_lat = st.sidebar.number_input("Latitude", value=52.5200, step=0.0001, format="%.4f")
        user_lon = st.sidebar.number_input("Longitude", value=13.4050, step=0.0001, format="%.4f")
    else:
        # City center coordinates
        city_coords = {
            "Berlin": (52.5200, 13.4050),
            "Munich": (48.1351, 11.5820),
            "Hamburg": (53.5511, 9.9937),
            "Frankfurt": (50.1109, 8.6821),
            "Cologne": (50.9375, 6.9603)
        }
        user_lat, user_lon = city_coords[selected_city]
    
    # Filters
    st.sidebar.subheader("Filters")
    
    # Fee range
    max_fee = st.sidebar.slider("Maximum Fee per Hour (€)", 0.0, 5.0, 3.0, 0.1)
    
    # Transportation type
    transport_types = st.sidebar.multiselect(
        "Transportation Types",
        ["Car (Gasoline)", "Car (Diesel)", "Electric Car", "Hybrid Car", "Public Transport", "Bicycle", "E-Scooter"],
        default=["Car (Gasoline)", "Electric Car"]
    )
    
    # EV charging requirement
    ev_charging_required = st.sidebar.checkbox("Require EV Charging", value=False)
    
    # Distance filter
    max_distance = st.sidebar.slider("Maximum Distance (km)", 0.5, 10.0, 5.0, 0.5)
    
    # User profile
    st.sidebar.subheader("Commuter Profile")
    user_profile = st.sidebar.selectbox(
        "Select User Type",
        ["Commuter", "Tourist", "Delivery Driver", "Business Traveler"]
    )
    
    # Filter data based on selections
    city_df = df[df['city'] == selected_city].copy()
    
    # Apply filters
    filtered_df = city_df[
        (city_df['fee_per_hour'] <= max_fee) &
        (city_df['ev_charging'] >= ev_charging_required)
    ].copy()
    
    # Calculate distances
    filtered_df['distance'] = filtered_df.apply(
        lambda row: calculate_distance(user_lat, user_lon, row['lat'], row['lon']), axis=1
    )
    
    # Filter by distance
    filtered_df = filtered_df[filtered_df['distance'] <= max_distance].sort_values('distance')
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader(f"🗺️ Parking Locations in {selected_city}")
        
        # Create map
        if not filtered_df.empty:
            center_lat = filtered_df['lat'].mean()
            center_lon = filtered_df['lon'].mean()
        else:
            center_lat, center_lon = user_lat, user_lon
        
        m = folium.Map(location=[center_lat, center_lon], zoom_start=12)
        
        # Add user location
        folium.Marker(
            [user_lat, user_lon],
            popup="Your Location",
            icon=folium.Icon(color='red', icon='user')
        ).add_to(m)
        
        # Add parking spots
        for idx, row in filtered_df.iterrows():
            # Color based on availability
            if row['available_spots'] > 50:
                color = 'green'
            elif row['available_spots'] > 20:
                color = 'orange'
            else:
                color = 'red'
            
            popup_text = f"""
            <b>{row['name']}</b><br>
            Address: {row['address']}<br>
            Fee: €{row['fee_per_hour']}/hour<br>
            Available: {row['available_spots']}/{row['total_spots']}<br>
            Distance: {row['distance']:.1f} km<br>
            EV Charging: {'Yes' if row['ev_charging'] else 'No'}<br>
            <a href="https://maps.google.com/maps?q={row['lat']},{row['lon']}" target="_blank">📍 Open in Google Maps</a>
            """
            
            folium.Marker(
                [row['lat'], row['lon']],
                popup=folium.Popup(popup_text, max_width=300),
                icon=folium.Icon(color=color, icon='car')
            ).add_to(m)
        
        # Display map
        map_data = st_folium(m, width=700, height=400)
    
    with col2:
        st.subheader("📊 Quick Stats")
        
        if not filtered_df.empty:
            # Metrics
            avg_fee = filtered_df['fee_per_hour'].mean()
            total_spots = filtered_df['total_spots'].sum()
            available_spots = filtered_df['available_spots'].sum()
            availability_rate = (available_spots / total_spots * 100) if total_spots > 0 else 0
            
            st.metric("Average Fee", f"€{avg_fee:.2f}/hour")
            st.metric("Total Spots", f"{total_spots:,}")
            st.metric("Available Now", f"{available_spots:,}")
            st.metric("Availability Rate", f"{availability_rate:.1f}%")
        else:
            st.warning("No parking spots match your criteria.")
        
        # Fun fact
        st.markdown('<div class="fun-fact">', unsafe_allow_html=True)
        st.markdown(f"**💡 Fun Fact**\n\n{get_fun_fact()}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Charts section
    st.subheader("📈 Analytics & Insights")
    
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        if not filtered_df.empty:
            # Fee comparison chart
            fig_fee = px.bar(
                filtered_df.head(10),
                x='name',
                y='fee_per_hour',
                color='available_spots',
                title='Parking Fees Comparison',
                labels={'fee_per_hour': 'Fee (€/hour)', 'name': 'Parking Location'},
                color_continuous_scale='RdYlGn'
            )
            fig_fee.update_layout(xaxis_tickangle=-45, height=400)
            st.plotly_chart(fig_fee, use_container_width=True)
    
    with chart_col2:
        # CO2 emissions comparison
        co2_data = generate_co2_data()
        co2_df = pd.DataFrame(list(co2_data.items()), columns=['Transport', 'CO2_grams_per_km'])
        
        fig_co2 = px.bar(
            co2_df,
            x='Transport',
            y='CO2_grams_per_km',
            title='CO2 Emissions by Transport Mode',
            labels={'CO2_grams_per_km': 'CO2 (g/km)'},
            color='CO2_grams_per_km',
            color_continuous_scale='Reds'
        )
        fig_co2.update_layout(xaxis_tickangle=-45, height=400)
        st.plotly_chart(fig_co2, use_container_width=True)
    
    # Trip cost calculator
    st.subheader("💰 Trip Cost Calculator")
    
    calc_col1, calc_col2, calc_col3 = st.columns(3)
    
    with calc_col1:
        trip_distance = st.number_input("Trip Distance (km)", min_value=0.1, value=5.0, step=0.1)
        parking_duration = st.number_input("Parking Duration (hours)", min_value=0.5, value=2.0, step=0.5)
        
    with calc_col2:
        fuel_price = st.number_input("Fuel Price (€/L)", min_value=0.5, value=1.65, step=0.01)
        consumption = st.number_input("Fuel Consumption (L/100km)", min_value=3.0, value=7.5, step=0.1)
        
    with calc_col3:
        time_value = st.number_input("Time Value (€/hour)", min_value=5.0, value=15.0, step=1.0)
        
    if st.button("Calculate Trip Cost"):
        if not filtered_df.empty:
            selected_parking = filtered_df.iloc[0]  # Use closest parking
            
            # Calculations
            fuel_cost = (trip_distance * 2 * consumption / 100) * fuel_price  # Round trip
            parking_cost = selected_parking['fee_per_hour'] * parking_duration
            time_cost = (trip_distance * 2 / 30) * time_value  # Assuming 30 km/h average speed
            
            total_cost = fuel_cost + parking_cost + time_cost
            
            # CO2 calculation
            co2_emission = trip_distance * 2 * 120 / 1000  # kg CO2 for gasoline car
            
            st.success(f"""
            **Trip Cost Breakdown:**
            - Fuel Cost: €{fuel_cost:.2f}
            - Parking Cost: €{parking_cost:.2f}
            - Time Cost: €{time_cost:.2f}
            - **Total Cost: €{total_cost:.2f}**
            
            **Environmental Impact:**
            - CO2 Emissions: {co2_emission:.2f} kg
            - Trees needed to offset: {co2_emission/22:.1f} trees/year
            """)
    
    # Availability heatmap
    st.subheader("🔥 Parking Availability Heatmap")
    
    if not filtered_df.empty:
        # Create availability percentage
        filtered_df['availability_pct'] = (filtered_df['available_spots'] / filtered_df['total_spots'] * 100).round(1)
        
        fig_heatmap = px.scatter(
            filtered_df,
            x='lon',
            y='lat',
            size='total_spots',
            color='availability_pct',
            hover_name='name',
            hover_data=['fee_per_hour', 'available_spots', 'total_spots'],
            title='Parking Availability by Location',
            labels={'availability_pct': 'Availability %', 'lat': 'Latitude', 'lon': 'Longitude'},
            color_continuous_scale='RdYlGn',
            size_max=20
        )
        fig_heatmap.update_layout(height=400)
        st.plotly_chart(fig_heatmap, use_container_width=True)
    
    # Profile-based recommendations
    st.subheader("🎯 Personalized Recommendations")
    
    if not filtered_df.empty:
        if user_profile == "Commuter":
            recommendation = filtered_df.nsmallest(1, 'fee_per_hour')
            st.info(f"💼 **For Commuters**: We recommend {recommendation.iloc[0]['name']} - lowest cost at €{recommendation.iloc[0]['fee_per_hour']}/hour")
        elif user_profile == "Tourist":
            recommendation = filtered_df.nsmallest(1, 'distance')
            st.info(f"🏛️ **For Tourists**: We recommend {recommendation.iloc[0]['name']} - closest to city center ({recommendation.iloc[0]['distance']:.1f}km)")
        elif user_profile == "Delivery Driver":
            recommendation = filtered_df.nlargest(1, 'available_spots')
            st.info(f"📦 **For Delivery Drivers**: We recommend {recommendation.iloc[0]['name']} - most available spots ({recommendation.iloc[0]['available_spots']})")
        else:  # Business Traveler
            recommendation = filtered_df[filtered_df['ev_charging'] == True].nsmallest(1, 'distance') if any(filtered_df['ev_charging']) else filtered_df.nsmallest(1, 'distance')
            st.info(f"💼 **For Business Travelers**: We recommend {recommendation.iloc[0]['name']} - convenient location with premium amenities")

if __name__ == "__main__":
    main()