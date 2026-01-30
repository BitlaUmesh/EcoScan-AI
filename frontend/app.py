#Camera-enabled web interface
"""
Waste Reuse Intelligence System - Streamlit Frontend
AI-powered waste object analysis and reuse recommendation system
"""

import streamlit as st
from PIL import Image
import sys
import os
from dotenv import load_dotenv

# Load .env file immediately
load_dotenv()

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from backend.utils import (
    run_complete_analysis,
    load_image_from_bytes,
    check_api_key,
    get_setup_instructions
)
from backend.scoring import get_score_color


# Page configuration
st.set_page_config(
    page_title="AI Waste Reuse Analyzer",
    page_icon="♻️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .score-display {
        text-align: center;
        font-size: 3rem;
        font-weight: bold;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .verdict-badge {
        text-align: center;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 1.2rem;
        font-weight: bold;
        margin: 1rem 0;
    }
    .suggestion-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
    }
    .info-box {
        background-color: #e7f3ff;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #2196F3;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


def main():
    """Main application function"""
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>♻️ AI Waste Reuse Analyzer</h1>
        <p>Intelligent waste assessment for sustainable reuse</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check API key
    if not check_api_key():
        st.error("⚠️ API Key Not Configured")
        st.code(get_setup_instructions(), language="bash")
        st.stop()
    
    # Instructions
    with st.expander("ℹ️ How to Use", expanded=False):
        st.markdown("""
        1. **Capture Image**: Use your device camera to capture a waste object
        2. **Analyze**: Click the "Analyze Object" button
        3. **Review Results**: View AI-generated reuse recommendations
        
        **Note**: This system provides AI-assisted recommendations based on visual analysis.
        Always use your judgment for safety and hygiene considerations.
        """)
    
    # Camera input section
    st.subheader("📸 Capture Waste Object")
    
    camera_image = st.camera_input(
        "Point your camera at a waste object and take a picture",
        help="Ensure good lighting and the object is clearly visible"
    )
    
    # Analysis section
    if camera_image is not None:
        # Display captured image
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(camera_image, caption="Captured Image", use_container_width=True)
        
        # Analyze button
        if st.button("🔍 Analyze Object", type="primary", use_container_width=True):
            analyze_waste_object(camera_image)
    else:
        st.info("👆 Capture an image of a waste object to begin analysis")


def analyze_waste_object(camera_image):
    """
    Perform analysis on captured image
    
    Args:
        camera_image: Streamlit UploadedFile object from camera input
    """
    # Load image
    image_bytes = camera_image.getvalue()
    image = load_image_from_bytes(image_bytes)
    
    if image is None:
        st.error("❌ Failed to load image. Please try again.")
        return
    
    # Run analysis with progress indicator
    with st.spinner("🤖 AI is analyzing the object..."):
        result = run_complete_analysis(image)
    
    # Check for errors
    if result.get("status") == "error":
        st.error(f"❌ Analysis Failed: {result.get('error', 'Unknown error')}")
        return
    
    # Display results
    display_results(result)


def display_results(result: dict):
    """
    Display analysis results in a user-friendly format
    
    Args:
        result: Analysis result dictionary
    """
    st.success("✅ Analysis Complete!")
    
    # Score and verdict section
    st.markdown("---")
    st.subheader("📊 Reuse Assessment")
    
    # Score display
    score = result["score"]
    score_color = get_score_color(score)
    
    st.markdown(f"""
    <div class="score-display" style="background-color: {score_color}20; color: {score_color};">
        {score}/100
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"**{result['score_interpretation']}**")
    
    # Verdict badge
    verdict_display = result["verdict_display"]
    verdict_color = verdict_display["color"]
    
    st.markdown(f"""
    <div class="verdict-badge" style="background-color: {verdict_color}; color: white;">
        {verdict_display['emoji']} {result['verdict']}
    </div>
    """, unsafe_allow_html=True)
    
    st.info(verdict_display["message"])
    
    # Object information
    st.markdown("---")
    st.subheader("🔍 Object Information")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Object Type", result["object_type"])
    with col2:
        st.metric("Reusable", "Yes" if result["reuse_feasible"] else "No")
    
    # Condition summary
    st.markdown("**Condition Summary:**")
    st.info(result["condition_summary"])
    
    # Detailed analysis sections
    st.markdown("---")
    
    # Visual description
    with st.expander("👁️ Visual Analysis Details", expanded=False):
        st.write(result["visual_description"])
    
    # Reasoning
    with st.expander("🧠 AI Reasoning", expanded=True):
        st.write(result["reasoning"])
        
        if result["key_factors"]:
            st.markdown("**Key Factors:**")
            for factor in result["key_factors"]:
                st.markdown(f"- {factor}")
    
    # Reuse suggestions
    if result["suggestions"]:
        st.markdown("---")
        st.subheader("💡 Reuse Suggestions")
        
        for i, suggestion in enumerate(result["suggestions"], 1):
            st.markdown(f"""
            <div class="suggestion-card">
                <h4>{i}. {suggestion['use_case']}</h4>
                <p>{suggestion['explanation']}</p>
                <small>Category: {suggestion.get('category', 'general').replace('_', ' ').title()}</small>
            </div>
            """, unsafe_allow_html=True)
    
    # Disclaimer
    st.markdown("---")
    st.markdown("""
    <div class="warning-box">
        <strong>⚠️ Important Disclaimer:</strong><br>
        This analysis is AI-generated based on visual inspection only. 
        For food safety, chemical safety, or structural engineering applications, 
        please consult appropriate professionals. Always prioritize safety and hygiene.
    </div>
    """, unsafe_allow_html=True)


# Sidebar information
with st.sidebar:
    st.title("ℹ️ About")
    st.markdown("""
    **AI Waste Reuse Analyzer**
    
    This application uses advanced AI vision and reasoning to:
    - Identify waste objects
    - Assess physical condition
    - Recommend practical reuse options
    
    **Technology:**
    - Vision: Google Gemini Vision API
    - Reasoning: Large Language Models
    - Interface: Streamlit
    
    **Hackathon Project**  
    Demo-ready MVP for sustainable waste management
    """)
    
    st.markdown("---")
    st.caption("Built with ♻️ for sustainability")


if __name__ == "__main__":
    main()