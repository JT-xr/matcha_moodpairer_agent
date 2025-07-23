import streamlit as st
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(page_title="Recommendation Output Tests", page_icon="🧠")

st.title("🧠 Whiski's Recommendation Output Tests")

# Sample data
sample_drink = "Iced Matcha Latte 🧊"
sample_vibe = "smooth, creamy, and subtly sweet, perfect for unwinding on a warm day. It's like a cool hug in a cup! 😊 Vibe: Imagine yourself in a sun-drenched, airy café in Williamsburg, Brooklyn. Think exposed brick, lush green plants, and comfortable, mismatched seating. Soft indie music plays while you relax in a cozy armchair, watching the world go by. It's a perfect spot to cool down and just be. 🌿🌞"
sample_image = "matcha_cafe.png"

st.divider()

# Option 1: Current Style (Plain)
st.header("Option 1: Current Style (Plain)")
st.markdown("🧠 **Whiski's Recommendation:**")
st.write(sample_vibe)
st.markdown("Mood Image:")
st.image(sample_image, caption="Matcha Vibe")

st.divider()

# Option 2: Card-Style Layout
st.header("Option 2: Card-Style Layout")
st.markdown(f"""
<div style="
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 25px;
    border-radius: 15px;
    margin: 20px 0;
    box-shadow: 0 8px 16px rgba(0,0,0,0.2);
">
    <h3 style="margin: 0 0 15px 0;">🧠 Whiski's Recommendation</h3>
    <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; margin: 10px 0;">
        <h4>🍵 Drink: {sample_drink}</h4>
    </div>
    <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; margin: 10px 0;">
        <p style="margin: 0; line-height: 1.6;">{sample_vibe}</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Image below card
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image(sample_image, caption="✨ Your Matcha Vibe", use_container_width=True)

st.divider()

# Option 3: Split Layout (Text + Image Side by Side)
st.header("Option 3: Split Layout")
col1, col2 = st.columns([3, 2])

with col1:
    st.markdown(f"""
    <div style="
        background: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
        height: 100%;
    ">
        <h3 style="color: #2c3e50; margin-top: 0;">🧠 Whiski's Recommendation</h3>
        <div style="background: #e8f5e8; padding: 10px; border-radius: 8px; margin: 10px 0;">
            <strong>🍵 Drink:</strong> {sample_drink}
        </div>
        <div style="background: #fff; padding: 15px; border-radius: 8px; margin: 10px 0;">
            <strong>✨ Vibe:</strong><br>
            {sample_vibe}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.image(sample_image, caption="Matcha Vibe", width=520)

st.divider()

# Option 4: Tabbed Interface
st.header("Option 4: Tabbed Interface")
st.markdown("### 🧠 Whiski's Recommendation")

tab1, tab2, tab3 = st.tabs(["🍵 Drink", "✨ Vibe", "📸 Mood"])

with tab1:
    st.markdown(f"""
    <div style="text-align: center; padding: 30px;">
        <div style="font-size: 60px; margin-bottom: 20px;">🍵</div>
        <h2 style="color: #4CAF50; margin-bottom: 10px;">Your Perfect Drink</h2>
        <div style="
            background: #e8f5e8;
            padding: 20px;
            border-radius: 15px;
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
        ">
            {sample_drink}
        </div>
    </div>
    """, unsafe_allow_html=True)

with tab2:
    st.markdown(f"""
    <div style="
        background: linear-gradient(45deg, #ffeaa7, #fab1a0);
        padding: 25px;
        border-radius: 15px;
        margin: 20px 0;
    ">
        <h3 style="margin-top: 0; color: #2d3436;">✨ The Perfect Vibe</h3>
        <p style="font-size: 16px; line-height: 1.8; color: #2d3436; margin: 0;">
            {sample_vibe}
        </p>
    </div>
    """, unsafe_allow_html=True)

with tab3:
    st.image(sample_image, caption="Your Matcha Mood", use_container_width=True)

st.divider()

# Option 5: Expandable Sections
st.header("Option 5: Expandable Sections")
st.markdown("### 🧠 Whiski's Recommendation")

with st.expander("🍵 Your Perfect Drink", expanded=True):
    st.markdown(f"""
    <div style="text-align: center; padding: 20px;">
        <div style="
            background: #4CAF50;
            color: white;
            padding: 15px;
            border-radius: 20px;
            font-size: 20px;
            font-weight: bold;
            margin: 10px 0;
        ">
            {sample_drink}
        </div>
    </div>
    """, unsafe_allow_html=True)

with st.expander("✨ The Vibe Description", expanded=False):
    st.markdown(f"""
    <div style="
        background: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #e9ecef;
    ">
        <p style="font-size: 16px; line-height: 1.7; margin: 0;">
            {sample_vibe}
        </p>
    </div>
    """, unsafe_allow_html=True)

with st.expander("📸 Mood Visualization", expanded=False):
    st.image(sample_image, caption="Matcha Vibe", use_container_width=True)

st.divider()

# Option 6: Interactive Cards with Hover Effects
st.header("Option 6: Interactive Cards")
st.markdown("### 🧠 Whiski's Recommendation")

# Create three interactive cards
cards = [
    {"title": "🍵 Your Drink", "content": sample_drink, "bg": "#4CAF50"},
    {"title": "✨ The Vibe", "content": sample_vibe[:100] + "...", "bg": "#2196F3"},
    {"title": "📸 Mood Image", "content": "Click to view", "bg": "#FF9800"}
]

cols = st.columns(3)
for i, card in enumerate(cards):
    with cols[i]:
        st.markdown(f"""
        <div style="
            background: {card['bg']};
            color: white;
            padding: 20px;
            border-radius: 15px;
            margin: 10px 0;
            text-align: center;
            min-height: 200px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        ">
            <h4 style="margin: 0 0 15px 0;">{card['title']}</h4>
            <p style="margin: 0; font-size: 14px; line-height: 1.5;">
                {card['content']}
            </p>
        </div>
        """, unsafe_allow_html=True)

# Show image below cards
st.image(sample_image, caption="Your Matcha Mood", use_container_width=True)

st.divider()

# Option 7: Timeline Style
st.header("Option 7: Timeline Style")
st.markdown("### 🧠 Whiski's Recommendation Journey")

timeline_items = [
    {"step": "1", "title": "🍵 Your Perfect Drink", "content": sample_drink},
    {"step": "2", "title": "✨ The Vibe", "content": sample_vibe},
    {"step": "3", "title": "📸 Mood Visualization", "content": "See your perfect matcha moment"}
]

for i, item in enumerate(timeline_items):
    st.markdown(f"""
    <div style="display: flex; margin: 20px 0;">
        <div style="
            background: #4CAF50;
            color: white;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            margin-right: 20px;
            flex-shrink: 0;
        ">
            {item['step']}
        </div>
        <div style="
            background: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
            flex-grow: 1;
            border-left: 3px solid #4CAF50;
        ">
            <h4 style="margin: 0 0 10px 0; color: #2c3e50;">{item['title']}</h4>
            <p style="margin: 0; line-height: 1.6;">{item['content']}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Show image at the end
st.image(sample_image, caption="Your Matcha Journey", use_container_width=True)

st.divider()


# Even simpler version using just Streamlit components:

st.divider()

# Option 8: Split Layout with Image Inside Card (Clean Version)
st.header("Option 8: Split Layout with Image Inside Card (Clean Version)")

# Header only
st.markdown("""
<div style="background: white; padding: 15px; border-radius: 15px; text-align: center; margin: 20px 0; font-size: 24px; font-weight: bold; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
🧠 Whiski's Recommendation
</div>
""", unsafe_allow_html=True)

# Content area
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(f"""
    <div style="background: white; padding: 20px; border-radius: 20px; margin-bottom: 20px; font-size: 18px; font-weight: bold; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
    🍵 Drink: {sample_drink}
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="background: white; padding: 20px; border-radius: 20px; line-height: 1.6; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
    <div style="font-weight: bold; margin-bottom: 10px; font-size: 16px;">✨ Vibe:</div>
    <div style="font-size: 14px;">{sample_vibe}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="text-align: center;">
    """, unsafe_allow_html=True)
    
    st.image(sample_image, width=250)
    
    st.markdown("""
        <p style="color: #6c757d; font-style: italic; margin: 10px 0 0 0; font-size: 14px; text-align: center;">✨ Your Matcha Vibe</p>
    </div>
    """, unsafe_allow_html=True)