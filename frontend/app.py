"""
Waste Reuse Intelligence System - Streamlit Frontend
AI-powered waste object analysis and reuse recommendation system
"""

import streamlit as st
from PIL import Image
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from backend.utils import (
    load_image_from_bytes,
    check_api_key,
    get_setup_instructions
)
from backend.scoring import get_score_color
from backend.orchestrator import (
    run_complete_analysis_with_transformation,
    generate_transformation_intelligence
)


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
        4. **Generate Transformation Guide**: Get step-by-step procedure and market value (NEW!)
        
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
        
        # Transformation Intelligence Section (NEW FEATURE)
        if 'analysis_result' in st.session_state and st.session_state['analysis_result'].get('reuse_feasible'):
            st.markdown("---")
            
            # Check if transformation already generated
            if 'transformation_intelligence' not in st.session_state.get('analysis_result', {}):
                if st.button("🔧 Generate Reuse Procedure & Market Value", 
                           type="secondary", 
                           use_container_width=True,
                           help="AI will create a step-by-step transformation guide and estimate market value"):
                    generate_transformation_view(st.session_state['analysis_result'])
            else:
                # Display transformation intelligence
                display_transformation_intelligence(
                    st.session_state['analysis_result']['transformation_intelligence']
                )
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
        result = run_complete_analysis_with_transformation(image)
    
    # Check for errors
    if result.get("status") == "error":
        st.error(f"❌ Analysis Failed: {result.get('error', 'Unknown error')}")
        return
    
    # Store in session state for transformation feature
    st.session_state['analysis_result'] = result
    
    # Display results
    display_results(result)


def generate_transformation_view(analysis_result):
    """Generate and display transformation intelligence"""
    with st.spinner("🔬 EcoScan AI is designing transformation procedure..."):
        extended_result = generate_transformation_intelligence(analysis_result)
        st.session_state['analysis_result'] = extended_result
    
    if 'transformation_intelligence' in extended_result:
        st.success("✅ Transformation Intelligence Generated!")
        st.rerun()


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


def display_transformation_intelligence(transformation_data: dict):
    """
    Display transformation intelligence including procedure and pricing
    
    Args:
        transformation_data: Transformation intelligence dictionary
    """
    st.markdown("---")
    st.markdown("## 🔧 Waste-to-Product Transformation Intelligence")
    
    target = transformation_data['target_selection']
    procedure = transformation_data['procedure']
    quality = transformation_data['quality_assessment']
    pricing = transformation_data['pricing']
    trace = transformation_data['decision_trace']
    
    # Target Product
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 1.5rem; border-radius: 10px; color: white; margin-bottom: 1rem;">
        <h3 style="margin: 0; color: white;">🎯 Target Product</h3>
        <h2 style="margin: 0.5rem 0; color: white;">{target['target_product']}</h2>
        <p style="margin: 0; opacity: 0.9;">{target['reason_for_selection']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Transformation Procedure
    st.markdown("### 📋 Step-by-Step Transformation Procedure")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("⏱️ Estimated Time", f"{procedure['estimated_time_minutes']} min")
    with col2:
        st.metric("📊 Difficulty", procedure['difficulty_level'])
    with col3:
        st.metric("🔧 Tools Needed", len(procedure['required_tools']))
    
    # Procedure steps
    st.markdown("#### Transformation Steps:")
    for i, step in enumerate(procedure['procedure_steps'], 1):
        st.markdown(f"""
        <div style="background-color: #f0f2f6; padding: 0.8rem; 
                    border-radius: 8px; margin: 0.5rem 0; border-left: 4px solid #667eea;">
            <strong>Step {i}:</strong> {step}
        </div>
        """, unsafe_allow_html=True)
    
    # Tools and Materials
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🛠️ Required Tools")
        for tool in procedure['required_tools']:
            st.markdown(f"- {tool}")
    
    with col2:
        st.markdown("#### 📦 Required Materials")
        for material in procedure['required_materials']:
            st.markdown(f"- {material}")
    
    # Safety notes
    st.warning(f"⚠️ **Safety Note:** {procedure['safety_notes']}")
    
    # Quality Assessment
    st.markdown("---")
    st.markdown("### 📊 Post-Transformation Quality Assessment")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🕐 Expected Lifespan", f"{quality['expected_lifespan_months']} months")
    with col2:
        stability_emoji = {"High": "🟢", "Medium": "🟡", "Low": "🔴"}
        st.metric("🏗️ Structural Stability", 
                 f"{stability_emoji.get(quality['structural_stability'], '🟡')} {quality['structural_stability']}")
    with col3:
        st.metric("💪 Durability", "Good" if quality['expected_lifespan_months'] >= 12 else "Moderate")
    
    st.info(f"**Usage Limitations:** {quality['usage_limitations']}")
    
    # Market Pricing
    st.markdown("---")
    st.markdown("### 💰 Fair Market Value Assessment")
    
    price_range = pricing['suggested_price_range']
    avg_price = (price_range['min'] + price_range['max']) // 2
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); 
                padding: 2rem; border-radius: 10px; color: white; text-align: center;">
        <h4 style="margin: 0; color: white; opacity: 0.9;">Suggested Price Range</h4>
        <h1 style="margin: 0.5rem 0; color: white;">₹{price_range['min']} - ₹{price_range['max']}</h1>
        <p style="margin: 0; opacity: 0.9;">Average: ₹{avg_price} | Confidence: {pricing['pricing_confidence']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Pricing reasoning
    st.markdown("#### 💡 Pricing Factors:")
    for reason in pricing['pricing_reasoning']:
        st.markdown(f"- {reason}")
    
    # Show pricing calculation breakdown
    with st.expander("🔍 View Pricing Calculation Breakdown"):
        factors = pricing.get('pricing_factors', {})
        st.markdown(f"""
        **Pricing Formula:**
        - Base Price: ₹{factors.get('base_price', 0)}
        - Lifespan Multiplier: {factors.get('lifespan_multiplier', 1.0)}x
        - Labor Multiplier: {factors.get('labor_multiplier', 1.0)}x
        - Sustainability Premium: {factors.get('sustainability_premium', 1.0)}x
        
        This demonstrates EcoScan AI's transparent pricing algorithm.
        """)
    
    # Explainability Section
    st.markdown("---")
    st.markdown("### 🧠 How EcoScan AI Arrived at This Result")
    
    with st.expander("📊 View Complete Decision Trace", expanded=False):
        # Observation Layer
        st.markdown(f"#### {trace['observation_layer']['title']}")
        st.markdown(f"**Source:** {trace['observation_layer']['source']}")
        st.info(trace['observation_layer']['content'])
        
        # Inference Layer
        st.markdown(f"#### {trace['inference_layer']['title']}")
        for inference in trace['inference_layer']['inferences']:
            st.markdown(f"- {inference}")
        
        # Decision Layer
        st.markdown(f"#### {trace['decision_layer']['title']}")
        for decision in trace['decision_layer']['decisions']:
            st.markdown(f"**{decision['decision']}**")
            st.markdown(f"→ {decision['reasoning']}")
            st.markdown("")
        
        # Transparency note
        st.caption(trace['transparency_note'])
    
    # Download option
    st.markdown("---")
    if st.button("📥 Download Transformation Guide (Coming Soon)", disabled=True):
        st.info("PDF export feature will be available in the next update")


# Sidebar information
with st.sidebar:
    st.title("ℹ️ About")
    st.markdown("""
    **AI Waste Reuse Analyzer**
    
    This application uses advanced AI vision and reasoning to:
    - Identify waste objects
    - Assess physical condition
    - Recommend practical reuse options
    - **NEW:** Generate transformation procedures
    - **NEW:** Estimate market value
    
    **Technology:**
    - Vision: Google Gemini Vision API
    - Reasoning: Large Language Models
    - Pricing: Custom algorithm
    - Interface: Streamlit
    
    **Hackathon Project**  
    Demo-ready MVP for sustainable waste management
    """)
    
    st.markdown("---")
    st.caption("Built with ♻️ for sustainability")


if __name__ == "__main__":
    main()