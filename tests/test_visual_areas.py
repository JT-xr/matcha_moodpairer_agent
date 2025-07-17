import streamlit as st
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(page_title="Visual Areas Tests", page_icon="🌍")

st.title("🌍 Location Selection Visual Tests")

# Test data
boroughs = ["Brooklyn, NY", "Manhattan, NY", "Queens, NY", "Other"]

st.divider()

# Option 1: Current Style (Dropdown)
st.header("Option 1: Current Style (Dropdown)")
st.markdown("### 📍 Choose a location")
selected_borough_1 = st.selectbox("", boroughs, key="option1")

if selected_borough_1 == "Other":
    custom_location_1 = st.text_input("Enter a location", key="custom1")

st.divider()

# Option 2: Button Grid Layout
st.header("Option 2: Button Grid Layout")
st.markdown("### 📍 Choose a location")

# Create button grid for locations
cols = st.columns(2)
location_buttons = ["Brooklyn, NY", "Manhattan, NY", "Queens, NY", "Other"]

selected_location_2 = None
for i, location in enumerate(location_buttons):
    with cols[i % 2]:
        if st.button(location, key=f"loc_btn_{i}"):
            selected_location_2 = location

if selected_location_2:
    st.success(f"Selected: {selected_location_2}")
    if selected_location_2 == "Other":
        custom_location_2 = st.text_input("Enter custom location", key="custom2")

st.divider()

# Option 3: Radio Buttons
st.header("Option 3: Radio Buttons")
st.markdown("### 📍 Choose a location")
selected_location_3 = st.radio("", boroughs, key="radio_option")

if selected_location_3 == "Other":
    custom_location_3 = st.text_input("Enter a location", key="custom3")

st.divider()

# Option 4: Tabs Layout
st.header("Option 4: Tabs Layout")
st.markdown("### 📍 Choose a location")

tab1, tab2, tab3, tab4 = st.tabs(["Brooklyn", "Manhattan", "Queens", "Custom"])

with tab1:
    st.markdown("🏙️ **Brooklyn, NY**")
    if st.button("Select Brooklyn", key="brooklyn_tab"):
        st.success("Brooklyn selected!")

with tab2:
    st.markdown("🌆 **Manhattan, NY**")
    if st.button("Select Manhattan", key="manhattan_tab"):
        st.success("Manhattan selected!")

with tab3:
    st.markdown("🏘️ **Queens, NY**")
    if st.button("Select Queens", key="queens_tab"):
        st.success("Queens selected!")

with tab4:
    st.markdown("🌍 **Custom Location**")
    custom_location_4 = st.text_input("Enter any location", key="custom4")
    if st.button("Use Custom Location", key="custom_tab"):
        st.success(f"Custom location: {custom_location_4}")

st.divider()

# Option 5: Map-Style Visual
st.header("Option 5: Map-Style Visual")
st.markdown("### 📍 Choose a location")

# Create visual map-like layout
st.markdown("""
<div style="display: flex; justify-content: center; margin: 20px 0;">
    <div style="text-align: center; font-size: 24px;">🗽 NYC Boroughs</div>
</div>
""", unsafe_allow_html=True)

# Create columns for map-like layout
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.markdown("**Brooklyn**")
    if st.button("🏙️ Brooklyn", key="map_brooklyn"):
        st.success("Brooklyn selected!")

with col2:
    st.markdown("**Manhattan**")
    if st.button("🌆 Manhattan", key="map_manhattan"):
        st.success("Manhattan selected!")
    
    st.markdown("**Queens**")
    if st.button("🏘️ Queens", key="map_queens"):
        st.success("Queens selected!")

with col3:
    st.markdown("**Custom**")
    custom_location_5 = st.text_input("Other location", key="custom5")
    if st.button("🌍 Custom", key="map_custom"):
        st.success(f"Custom: {custom_location_5}")

st.divider()

# Option 6: Compact Card Style
st.header("Option 6: Compact Card Style")
st.markdown("### 📍 Choose a location")

# Create compact cards
for i, location in enumerate(boroughs):
    if location != "Other":
        emoji = ["🏙️", "🌆", "🏘️"][i]
        st.markdown(f"""
        <div style="
            background: #f0f8ff; 
            padding: 15px; 
            border-radius: 10px; 
            margin: 10px 0;
            border: 1px solid #ddd;
        ">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <span style="font-size: 20px;">{emoji}</span>
                    <span style="font-size: 16px; margin-left: 10px;">{location}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="
            background: #fff8f0; 
            padding: 15px; 
            border-radius: 10px; 
            margin: 10px 0;
            border: 1px solid #ddd;
        ">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <span style="font-size: 20px;">🌍</span>
                    <span style="font-size: 16px; margin-left: 10px;">Custom Location</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

custom_location_6 = st.text_input("Enter custom location", key="custom6")

st.divider()

# Option 7: Pill-Style Buttons
st.header("Option 7: Pill-Style Buttons")
st.markdown("### 📍 Choose a location")

# Create pill-style buttons
st.markdown("""
<div style="display: flex; gap: 10px; flex-wrap: wrap; margin: 20px 0;">
    <button style="
        background: #4CAF50; 
        color: white; 
        padding: 10px 20px; 
        border: none; 
        border-radius: 25px; 
        cursor: pointer;
        font-size: 14px;
    ">🏙️ Brooklyn</button>
    <button style="
        background: #2196F3; 
        color: white; 
        padding: 10px 20px; 
        border: none; 
        border-radius: 25px; 
        cursor: pointer;
        font-size: 14px;
    ">🌆 Manhattan</button>
    <button style="
        background: #FF9800; 
        color: white; 
        padding: 10px 20px; 
        border: none; 
        border-radius: 25px; 
        cursor: pointer;
        font-size: 14px;
    ">🏘️ Queens</button>
    <button style="
        background: #9C27B0; 
        color: white; 
        padding: 10px 20px; 
        border: none; 
        border-radius: 25px; 
        cursor: pointer;
        font-size: 14px;
    ">🌍 Other</button>
</div>
""", unsafe_allow_html=True)

custom_location_7 = st.text_input("Enter custom location", key="custom7")

st.divider()

# Option 8: Slider Selection
st.header("Option 8: Slider Selection")
st.markdown("### 📍 Choose a location")

location_options = ["Brooklyn, NY", "Manhattan, NY", "Queens, NY", "Other"]
selected_index = st.slider("", 0, len(location_options)-1, 0, key="slider_option")
selected_location_8 = location_options[selected_index]

st.markdown(f"**Selected:** {selected_location_8}")

if selected_location_8 == "Other":
    custom_location_8 = st.text_input("Enter custom location", key="custom8")

st.divider()

# Option 9: Expandable Menu
st.header("Option 9: Expandable Menu")
st.markdown("### 📍 Choose a location")

with st.expander("🌍 Select Location", expanded=True):
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🏙️ Brooklyn, NY", key="exp_brooklyn"):
            st.success("Brooklyn selected!")
        if st.button("🌆 Manhattan, NY", key="exp_manhattan"):
            st.success("Manhattan selected!")
    
    with col2:
        if st.button("🏘️ Queens, NY", key="exp_queens"):
            st.success("Queens selected!")
        custom_location_9 = st.text_input("🌍 Other location", key="custom9")

st.divider()

# Option 10: Search Bar with Suggestions
st.header("Option 10: Search Bar with Suggestions")
st.markdown("### 📍 Choose a location")

# Auto-complete style
location_input = st.text_input("Start typing a location...", key="search_input")

if location_input:
    suggestions = [loc for loc in boroughs if location_input.lower() in loc.lower()]
    if suggestions:
        st.markdown("**Suggestions:**")
        for suggestion in suggestions:
            if st.button(f"📍 {suggestion}", key=f"suggest_{suggestion}"):
                st.success(f"Selected: {suggestion}")

st.divider()

# Option 11: Toggle-Style Selection
st.header("Option 11: Toggle-Style Selection")
st.markdown("### 📍 Choose a location")

# Create toggle buttons
col1, col2, col3, col4 = st.columns(4)

with col1:
    brooklyn_toggle = st.checkbox("🏙️ Brooklyn", key="toggle_brooklyn")
with col2:
    manhattan_toggle = st.checkbox("🌆 Manhattan", key="toggle_manhattan")
with col3:
    queens_toggle = st.checkbox("🏘️ Queens", key="toggle_queens")
with col4:
    other_toggle = st.checkbox("🌍 Other", key="toggle_other")

# Show selected
selected_toggles = []
if brooklyn_toggle: selected_toggles.append("Brooklyn, NY")
if manhattan_toggle: selected_toggles.append("Manhattan, NY")
if queens_toggle: selected_toggles.append("Queens, NY")
if other_toggle: selected_toggles.append("Other")

if selected_toggles:
    st.success(f"Selected: {', '.join(selected_toggles)}")

st.divider()

# Option 12: Nested Dropdown
st.header("Option 12: Nested Dropdown")
st.markdown("### 📍 Choose a location")

# First level selection
region = st.selectbox("Select Region", ["New York City", "Other US City", "International"], key="region_select")

if region == "New York City":
    borough = st.selectbox("Select Borough", ["Brooklyn", "Manhattan", "Queens", "Bronx", "Staten Island"], key="borough_select")
    st.success(f"Selected: {borough}, NY")
elif region == "Other US City":
    us_city = st.text_input("Enter US city", key="us_city")
elif region == "International":
    intl_city = st.text_input("Enter international city", key="intl_city")

st.divider()

# Option 13: Card Grid with Hover Effects
st.header("Option 13: Card Grid with Hover Effects")
st.markdown("### 📍 Choose a location")

# Create hoverable cards
locations_with_info = [
    {"name": "Brooklyn", "emoji": "🏙️", "desc": "Trendy cafes & artisan spots"},
    {"name": "Manhattan", "emoji": "🌆", "desc": "Premium matcha experiences"},
    {"name": "Queens", "emoji": "🏘️", "desc": "Diverse neighborhood gems"},
    {"name": "Custom", "emoji": "🌍", "desc": "Anywhere in the world"}
]

cols = st.columns(2)
for i, loc in enumerate(locations_with_info):
    with cols[i % 2]:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 15px;
            margin: 10px 0;
            text-align: center;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        ">
            <div style="font-size: 30px; margin-bottom: 10px;">{loc['emoji']}</div>
            <div style="font-size: 18px; font-weight: bold; margin-bottom: 5px;">{loc['name']}</div>
            <div style="font-size: 14px; opacity: 0.9;">{loc['desc']}</div>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# Option 14: Minimal Text Input
st.header("Option 14: Minimal Text Input")
st.markdown("### 📍 Choose a location")

# Simple, clean text input
location_minimal = st.text_input("", placeholder="Enter location (e.g., Brooklyn, NY)", key="minimal_input")

if location_minimal:
    st.markdown(f"**Looking for matcha in:** {location_minimal}")