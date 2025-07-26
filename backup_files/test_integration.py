"""
Test script to verify the integrated Whiski app functionality
Run this script to test the modular UI integration.
"""

import os
import sys

def test_imports():
    """Test that all imports work correctly"""
    try:
        print("Testing imports...")
        
        # Test styles import
        from styles import apply_global_styles, hide_streamlit_ui
        print("✅ Styles import successful")
        
        # Test UI utils import
        from ui import init_session_state, navigate_to_scene, SCENES
        print("✅ UI utils import successful")
        
        # Test components import  
        from ui.components import render_progress_bar, render_action_buttons
        print("✅ Components import successful")
        
        # Test scenes import
        from ui.scenes import (
            render_welcome_scene,
            render_mood_selection_scene,
            render_location_input_scene,
            render_results_scene
        )
        print("✅ Scenes import successful")
        
        print("\n🎉 All imports successful! The modular UI integration is ready.")
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_backend_availability():
    """Test backend module availability"""
    print("\nTesting backend module availability...")
    
    modules_to_test = [
        'whiski_agent',
        'cafe_search', 
        'weather_api',
        'splashpage',
        'location_cards'
    ]
    
    available_modules = []
    missing_modules = []
    
    for module in modules_to_test:
        try:
            __import__(module)
            available_modules.append(module)
            print(f"✅ {module} - Available")
        except ImportError:
            missing_modules.append(module)
            print(f"⚠️  {module} - Not available (will use fallback)")
    
    print(f"\nBackend Status: {len(available_modules)}/{len(modules_to_test)} modules available")
    return available_modules, missing_modules

if __name__ == "__main__":
    print("=" * 50)
    print("🍵 Whiski App Integration Test")
    print("=" * 50)
    
    # Test imports
    imports_ok = test_imports()
    
    # Test backend availability  
    available, missing = test_backend_availability()
    
    print("\n" + "=" * 50)
    if imports_ok:
        print("✅ Integration test PASSED")
        print("The app is ready to run with Streamlit!")
        print("\nTo start the app, run:")
        print("streamlit run app.py")
    else:
        print("❌ Integration test FAILED")
        print("Check the import errors above.")
    
    print("=" * 50)
