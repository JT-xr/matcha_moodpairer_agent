import streamlit as st

def display_expandable_cafe_cards(cafes):
    """Display cafes using expandable cards with buttons"""
    if cafes:
        st.markdown(f"📍 **Nearby Cafés ({len(cafes)} found):**")
        
        # Option 3: Expandable Cards (Column Control)
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
    else:
        st.warning("No matcha cafés found near that location.")