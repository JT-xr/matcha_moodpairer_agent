import sys
import os
import streamlit as st
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cafe_search import search_matcha_cafes


st.set_page_config(page_title="Café Layout Tests", page_icon="🍵")

st.title("🍵 Café Display Layout Tests")

# Get test data
cafes = search_matcha_cafes("Brooklyn, NY")[:5]  # Limit to 5 for testing

# Option 1: Enhanced Card Layout
st.header("Option 1: Enhanced Card Layout")
if cafes:
    for i, cafe in enumerate(cafes):
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 10px;
            border-radius: 20px;
            border-left: 5px solid #4CAF50;
            margin: 10px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        ">
            <h4 style="color: #2E7D32; margin: 0 0 10px 0;">
                🍵 {cafe['name']}
            </h4>
            <p style="color: #666; margin: 5px 0;">
                📍 {cafe['address']}
            </p>
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="background: #4CAF50; color: white; padding: 5px 10px; border-radius: 1px; font-size: 14px;">
                    ⭐ {cafe.get('rating', '?')} stars
                </span>
                <a href="{cafe['map_link']}" target="_blank" style="
                    background: #2196F3; 
                    color: white; 
                    padding: 8px 15px; 
                    text-decoration: none; 
                    border-radius: 20px;
                    font-size: 14px;
                ">🗺️ View on Maps</a>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# Option 2: Grid Layout
st.header("Option 2: Grid Layout")
if cafes:
    for i in range(0, len(cafes), 2):
        col1, col2 = st.columns(2)
        
        with col1:
            if i < len(cafes):
                cafe = cafes[i]
                st.markdown(f"""
                <div style="background: #f0f8f0; padding: 15px; border-radius: 10px; height: 150px;">
                    <h5 style="color: #2E7D32;">🍵 {cafe['name']}</h5>
                    <p style="font-size: 12px; color: #666;">📍 {cafe['address'][:50]}{'...' if len(cafe['address']) > 50 else ''}</p>
                    <p style="font-size: 14px;">⭐ {cafe.get('rating', '?')} stars</p>
                    <a href="{cafe['map_link']}" target="_blank">🗺️ View</a>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            if i + 1 < len(cafes):
                cafe = cafes[i + 1]
                st.markdown(f"""
                <div style="background: #f0f8f0; padding: 15px; border-radius: 10px; height: 150px;">
                    <h5 style="color: #2E7D32;">🍵 {cafe['name']}</h5>
                    <p style="font-size: 12px; color: #666;">📍 {cafe['address'][:50]}{'...' if len(cafe['address']) > 50 else ''}</p>
                    <p style="font-size: 14px;">⭐ {cafe.get('rating', '?')} stars</p>
                    <a href="{cafe['map_link']}" target="_blank">🗺️ View</a>
                </div>
                """, unsafe_allow_html=True)

st.divider()

# Option 3: Expandable Cards (Column Control)
st.header("Option 3: Expandable Cards")
if cafes:
    col1, col2, col3 = st.columns([2.5, 1, 1])  # Adjust ratios as needed
    
    with col1:  # Main content in left column
        for i, cafe in enumerate(cafes):
            with st.expander(f"🍵 {cafe['name']} ⭐ {cafe.get('rating', '?')}"):
                st.markdown(f"""
                <div style="line-height: 1.2;">
                    <p style="font-size: 12px; margin: 3px 0;"><strong>📍 Location:</strong> {cafe['address']}</p>
                    <div style="display: flex; gap: 8px; margin-top: 10px; margin-bottom: 10px;">
                        <div style="background: white; color: black; padding: 3px 8px; border-radius: 12px; font-size: 12px;">
                            ⭐ {cafe.get('rating', '?')}
                        </div>
                        <a href="{cafe['map_link']}" target="_blank" style="
                            background: white; 
                            color: black; 
                            padding: 4px 10px; 
                            text-decoration: none; 
                            border-radius: 12px;
                            font-size: 11px;
                        ">🗺️ Maps</a>
                        <a href="https://www.google.com/search?q={cafe['name'].replace(' ', '+')}+website" target="_blank" style="
                            background: white; 
                            color: black; 
                            padding: 4px 10px; 
                            text-decoration: none; 
                            border-radius: 12px;
                            font-size: 11px;
                        ">🌐 Website</a>
                    </div>
                </div>
                """, unsafe_allow_html=True)

st.divider()

# Option 4: Compact Cards (Modified)
st.header("Option 4: Compact Cards (Modified)")
if cafes:
    for i, cafe in enumerate(cafes, 1):
        st.markdown(f"""
        <div style="
            background: linear-gradient(90deg, #e8f5e8 0%, #f0f8f0 100%);
            padding: 10px 15px;
            border-radius: 10px;
            margin: 5px 0;
            border: 1px solid #c8e6c9;
            max-width: 600px;
        ">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="flex-grow: 1;">
                    <h5 style="margin: 0 0 5px 0; color: #2E7D32; font-size: 16px;">
                        🍵 {cafe['name']}
                    </h5>
                    <p style="margin: 0; color: #666; font-size: 12px;">
                        📍 {cafe['address'][:50]}{'...' if len(cafe['address']) > 50 else ''}
                    </p>
                </div>
                <div style="text-align: center; margin-left: 15px;">
                    <div style="background: #4CAF50; color: white; padding: 3px 8px; border-radius: 12px; margin-bottom: 3px; font-size: 12px;">
                        ⭐ {cafe.get('rating', '?')}
                    </div>
                    <a href="{cafe['map_link']}" target="_blank" style="
                        background: #2196F3; 
                        color: white; 
                        padding: 4px 10px; 
                        text-decoration: none; 
                        border-radius: 12px;
                        font-size: 11px;
                    ">🗺️ Maps</a>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# Ultra-compact version with stacked buttons
st.header("Option 5: Ultra-Compact Cards")
if cafes:
    for i, cafe in enumerate(cafes):
        st.markdown(f"""
        <div style="
            background: white;
            padding: 8px 12px;
            border-radius: 8px;
            margin: 3px 0;
            border-left: 3px solid #4CAF50;
            max-width: 400px;
        ">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <strong style="color: #2E7D32; font-size: 14px;">🍵 {cafe['name']}</strong>
                    <br>
                    <small style="color: #666; font-size: 10px;">📍 {cafe['address'][:45]}{'...' if len(cafe['address']) > 45 else ''}</small>
                </div>
                <div style="text-align: center; margin-left: 15px;">
                    <div style="background: #4CAF50; color: white; padding: 2px 6px; border-radius: 10px; margin-bottom: 3px; font-size: 10px;">
                        ⭐ {cafe.get('rating', '?')}
                    </div>
                    <a href="{cafe['map_link']}" target="_blank" style="
                        background: #2196F3; 
                        color: white; 
                        padding: 3px 8px; 
                        text-decoration: none; 
                        border-radius: 10px;
                        font-size: 10px;
                    ">🗺️ Map</a>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)