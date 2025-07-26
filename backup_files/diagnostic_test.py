#!/usr/bin/env python3
"""
Diagnostic test for Whiski app integration
Checks imports, backend modules, and basic functionality
"""

import sys
import os

def test_imports():
    """Test all import statements"""
    print("🔍 Testing imports...")
    
    try:
        from ui import init_session_state, navigate_to_scene, get_current_scene, SCENES
        print("✅ UI core imports successful")
    except Exception as e:
        print(f"❌ UI core import failed: {e}")
        return False
        
    try:
        from ui.scenes import (
            render_welcome_scene,
            render_mood_selection_scene, 
            render_location_input_scene,
            render_custom_location_scene,
            render_results_scene,
            render_cafe_details_scene,
            render_chat_scene
        )
        print("✅ Scene imports successful")
    except Exception as e:
        print(f"❌ Scene import failed: {e}")
        return False
        
    try:
        from styles import apply_global_styles, hide_streamlit_ui
        print("✅ Styles import successful")
    except Exception as e:
        print(f"❌ Styles import failed: {e}")
        return False
    
    try:
        from ui.components import render_progress_bar, render_action_buttons
        print("✅ Components import successful")
    except Exception as e:
        print(f"❌ Components import failed: {e}")
        return False
        
    return True

def test_backend_modules():
    """Test backend module availability"""
    print("\n🔍 Testing backend modules...")
    
    modules_to_test = [
        ('whiski_agent', 'agent'),
        ('cafe_search', 'search_matcha_cafes'), 
        ('weather_api', 'get_nyc_weather'),
        ('location_cards', 'display_expandable_cafe_cards'),
        ('mood_drink_map', 'get_drink_for_mood')
    ]
    
    available = []
    missing = []
    
    for module_name, func_name in modules_to_test:
        try:
            module = __import__(module_name)
            if hasattr(module, func_name):
                print(f"✅ {module_name}.{func_name} available")
                available.append(module_name)
            else:
                print(f"⚠️  {module_name} available but missing {func_name}")
                available.append(module_name)
        except Exception as e:
            print(f"❌ {module_name} not available: {e}")
            missing.append(module_name)
    
    return available, missing

def test_file_structure():
    """Test if required files exist"""
    print("\n🔍 Testing file structure...")
    
    required_files = [
        'styles.py',
        'ui/__init__.py',
        'ui/utils.py',
        'ui/scenes/__init__.py',
        'ui/components/__init__.py',
        'ui/scenes/welcome.py',
        'ui/scenes/mood_selection.py',
        'ui/scenes/location_input.py',
        'ui/scenes/results.py',
        'ui/scenes/cafe_details.py',
        'ui/scenes/chat.py',
        'ui/components/progress_bar.py',
        'ui/components/navigation.py',
        'ui/components/cards.py',
        'ui/components/buttons.py',
        'Welcome_Image2.PNG'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} exists")
        else:
            print(f"❌ {file_path} missing")
            missing_files.append(file_path)
    
    return missing_files

def test_mood_mapping():
    """Test the mood mapping functionality"""
    print("\n🔍 Testing mood mapping...")
    
    try:
        from mood_drink_map import get_drink_for_mood
        
        test_moods = ['chill', 'anxious', 'creative', 'reflective', 'energized', 'cozy']
        
        for mood in test_moods:
            drink = get_drink_for_mood(mood)
            print(f"✅ {mood} → {drink}")
        
        return True
    except Exception as e:
        print(f"❌ Mood mapping test failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Whiski App Integration Diagnostic Test")
    print("=" * 50)
    
    # Test imports
    imports_ok = test_imports()
    
    # Test backend availability  
    available, missing = test_backend_modules()
    
    # Test file structure
    missing_files = test_file_structure()
    
    # Test mood mapping
    mood_ok = test_mood_mapping()
    
    print("\n" + "=" * 50)
    print("📊 DIAGNOSTIC SUMMARY:")
    print("=" * 50)
    
    if imports_ok:
        print("✅ All imports working")
    else:
        print("❌ Import issues detected")
    
    print(f"✅ Backend modules available: {len(available)}")
    if missing:
        print(f"⚠️  Missing backend modules: {missing}")
    
    if not missing_files:
        print("✅ All required files present")
    else:
        print(f"❌ Missing files: {missing_files}")
    
    if mood_ok:
        print("✅ Mood mapping functional")
    else:
        print("❌ Mood mapping issues")
    
    print("\n🎯 NEXT STEPS:")
    if imports_ok and not missing_files:
        print("✅ Ready to test: streamlit run app_new.py")
    else:
        print("❌ Fix the issues above first")
    
    print("=" * 50)
