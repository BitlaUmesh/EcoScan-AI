#Camera-enabled web interface
"""
Waste Reuse Intelligence System - Streamlit Frontend
AI-powered waste object analysis and reuse recommendation system
"""

import streamlit as st
from PIL import Image
import sys
import os
import time
import base64
from io import BytesIO
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
    page_title="EcoGen AI - Waste Intelligence",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# CUSTOM CSS (React UI Replication)
# ==========================================
def get_css(theme="light"):
    if theme == "dark":
        variables = """
        :root {
            --primary-50: #064e3b;
            --primary-100: #065f46;
            --primary-500: #10b981;
            --primary-600: #34d399;
            --primary-700: #6ee7b7;
            --secondary-50: #0c4a6e;
            --secondary-500: #38bdf8;
            --text-900: #f9fafb;
            --text-600: #d1d5db;
            --bg-color: #111827;
            --card-bg: #1f2937;
            --border-color: #374151;
        }
        """
    else:
        variables = """
        :root {
            --primary-50: #ecfdf5;
            --primary-100: #d1fae5;
            --primary-500: #10b981;
            --primary-600: #059669;
            --primary-700: #047857;
            --secondary-50: #f0f9ff;
            --secondary-500: #0ea5e9;
            --text-900: #111827;
            --text-600: #4b5563;
            --bg-color: #f8fafc;
            --card-bg: #ffffff;
            --border-color: #e5e7eb;
        }
        """

    return f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* Global Reset & Theme */
    {variables}

    .stApp {{
        background-color: var(--bg-color);
        font-family: 'Inter', sans-serif;
        color: var(--text-900);
    }}

    /* Hide standard Streamlit elements */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}

    /* Custom Header */
    .custom-header {{
        background: var(--card-bg);
        border-bottom: 1px solid var(--border-color);
        padding: 1rem 2rem;
        position: sticky;
        top: 0;
        z-index: 999;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 2rem;
        opacity: 0.95;
    }}

    .logo-container {{
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }}

    .logo-icon {{
        width: 40px;
        height: 40px;
        background: linear-gradient(135deg, #10b981, #0d9488);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(16, 185, 129, 0.2);
    }}

    .logo-text h1 {{
        font-size: 1.5rem;
        font-weight: 700;
        margin: 0;
        background: linear-gradient(to right, var(--primary-600), var(--primary-500));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.2;
    }}

    .logo-text p {{
        font-size: 0.75rem;
        color: var(--text-600);
        margin: 0;
    }}

    .nav-badges {{
        display: flex;
        gap: 1.5rem;
    }}

    .nav-item {{
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.875rem;
        color: var(--text-600);
        font-weight: 500;
    }}

    /* Hero Section */
    .hero-section {{
        text-align: center;
        padding: 3rem 1rem;
        margin-bottom: 2rem;
    }}

    .hero-title {{
        font-size: 3rem;
        font-weight: 800;
        color: var(--text-900);
        margin-bottom: 1rem;
        line-height: 1.1;
    }}

    .hero-highlight {{
        background: linear-gradient(to right, var(--primary-600), var(--primary-500));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}

    .hero-subtitle {{
        font-size: 1.125rem;
        color: var(--text-600);
        max-width: 42rem;
        margin: 0 auto;
        line-height: 1.6;
    }}

    /* Cards & Containers */
    .result-card {{
        background: var(--card-bg);
        border-radius: 1rem;
        border: 1px solid var(--border-color);
        padding: 1.5rem;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
        transition: all 0.2s;
        color: var(--text-900);
    }}
    
    .result-card:hover {{
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transform: translateY(-2px);
    }}
    
    .result-card h3 {{
        color: var(--text-900) !important;
    }}

    /* Recommendation Cards */
    .rec-card {{
        border: 1px solid var(--border-color);
        border-radius: 1rem;
        overflow: hidden;
        margin-bottom: 1rem;
        background: var(--card-bg);
        transition: all 0.2s;
    }}

    .rec-card:hover {{
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }}

    .rec-header {{
        padding: 1.25rem;
        cursor: pointer;
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
    }}

    .rec-badges {{
        display: flex;
        gap: 0.5rem;
        margin-bottom: 0.5rem;
    }}

    .badge {{
        display: inline-flex;
        align-items: center;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        gap: 0.25rem;
    }}

    .badge-purple {{ background: #f3e8ff; color: #7e22ce; border: 1px solid #e9d5ff; }}
    .badge-emerald {{ background: #ecfdf5; color: #047857; border: 1px solid #d1fae5; }}
    .badge-blue {{ background: #eff6ff; color: #1d4ed8; border: 1px solid #dbeafe; }}
    .badge-amber {{ background: #fffbeb; color: #b45309; border: 1px solid #fde68a; }}
    .badge-red {{ background: #fef2f2; color: #991b1b; border: 1px solid #fecaca; }}
    
    .rec-title {{
        font-size: 1.125rem;
        font-weight: 600;
        color: var(--text-900);
        margin-bottom: 0.25rem;
    }}

    .rec-desc {{
        font-size: 0.875rem;
        color: var(--text-600);
    }}

    .rec-stats {{
        display: flex;
        gap: 1rem;
        margin-top: 1rem;
        font-size: 0.875rem;
        color: var(--text-600);
    }}

    .rec-stat-item {{
        display: flex;
        align-items: center;
        gap: 0.25rem;
    }}

    /* Environmental Impact Card */
    .impact-card {{
        background: linear-gradient(135deg, #10b981, #0f766e);
        color: white;
        border-radius: 1rem;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }}

    .impact-title {{
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }}

    .impact-row {{
        display: flex;
        justify-content: space-between;
        margin-bottom: 0.5rem;
        font-size: 0.9rem;
    }}

    .impact-row span:first-child {{ opacity: 0.9; }}
    .impact-row span:last-child {{ font-weight: 600; }}

    /* Button Styling */
    div.stButton > button {{
        background: linear-gradient(to right, #10b981, #0d9488);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 0.75rem;
        font-weight: 600;
        width: 100%;
        transition: all 0.2s;
    }}

    div.stButton > button:hover {{
        transform: translateY(-1px);
        box-shadow: 0 4px 6px -1px rgba(16, 185, 129, 0.4);
    }}

    /* File Uploader Customization */
    .stFileUploader {{
        border: 2px dashed var(--border-color);
        border-radius: 1rem;
        padding: 2rem;
        background: var(--bg-color);
        transition: border-color 0.2s;
    }}
    
    .stFileUploader:hover {{
        border-color: #10b981;
    }}

    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 24px;
    }}

    .stTabs [data-baseweb="tab"] {{
        height: 50px;
        white-space: pre-wrap;
        background-color: var(--card-bg);
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
        color: var(--text-600);
    }}

    .stTabs [aria-selected="true"] {{
        background-color: var(--card-bg);
        color: var(--primary-600);
    }}

</style>
"""

# ==========================================
# HEADER COMPONENT
# ==========================================
def render_header(theme_toggle):
    st.markdown(f"""
    <div class="custom-header">
        <div class="logo-container">
            <div class="logo-icon">♻️</div>
            <div class="logo-text">
                <h1>EcoGen AI</h1>
                <p>Waste-to-Resource Intelligence</p>
            </div>
        </div>
        <div class="nav-badges">
            <div class="nav-item">🍃 Eco-Friendly</div>
            <div class="nav-item">🛡️ Human-Safe</div>
            <div class="nav-item">❤️ Social Impact</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def main():
    if "analysis_result" not in st.session_state:
        st.session_state.analysis_result = None
    if "is_analyzing" not in st.session_state:
        st.session_state.is_analyzing = False
    if "theme" not in st.session_state:
        st.session_state.theme = "light"

    # Theme Toggle
    with st.sidebar:
        st.title("Settings")
        theme_option = st.radio("Theme Mode", ["Light", "Dark"], index=0 if st.session_state.theme == "light" else 1)
        st.session_state.theme = theme_option.lower()
        
        st.markdown("---")
        st.image("https://img.icons8.com/color/96/000000/recycle-sign--v1.png", width=80)
        st.title("About EcoScan")
        st.markdown("""
        **EcoScan AI** helps you make sustainable choices by analyzing waste objects for reuse potential.
        """)

    # Apply CSS
    st.markdown(get_css(st.session_state.theme), unsafe_allow_html=True)
    
    # Render Header
    render_header(None)

    # Check API key
    if not check_api_key():
        st.error("⚠️ GEMINI_API_KEY not found. Please check setup instructions.")
        return

    # ==========================================
    # UPLOAD / HERO SECTION
    # ==========================================
    if not st.session_state.analysis_result:
        # Hero
        st.markdown("""
        <div class="hero-section">
            <div class="hero-title">
                Transform Waste Into<br>
                <span class="hero-highlight">Valuable Resources</span>
            </div>
            <p class="hero-subtitle">
                Upload any item and our AI will analyze it, assess safety, and generate 
                personalized eco-friendly upcycling ideas with step-by-step instructions.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Upload Container
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("### Upload Waste Item")
            
            tab1, tab2 = st.tabs(["📁 Upload Image", "📸 Use Camera"])
            
            with tab1:
                uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
                if uploaded_file:
                    image = Image.open(uploaded_file)
                    st.image(image, use_container_width=True, caption="Uploaded Item")
                    if st.button("✨ Analyze Upload", use_container_width=True):
                        perform_analysis(uploaded_file)
            
            with tab2:
                camera_image = st.camera_input("Take a photo", label_visibility="collapsed")
                if camera_image:
                    # st.image(camera_image, use_container_width=True, caption="Captured Photo")
                    if st.button("✨ Analyze Photo", use_container_width=True):
                        perform_analysis(camera_image)

        # Features Grid
        st.markdown("---")
        f1, f2, f3 = st.columns(3)
        with f1:
            st.markdown("""
            <div class="result-card" style="text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 1rem;">✨</div>
                <h3 style="font-weight: 600;">AI-Powered Analysis</h3>
                <p style="color: var(--text-600); font-size: 0.9rem;">Computer vision identifies objects and assesses material composition</p>
            </div>
            """, unsafe_allow_html=True)
        with f2:
            st.markdown("""
            <div class="result-card" style="text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 1rem;">🛡️</div>
                <h3 style="font-weight: 600;">Safety First</h3>
                <p style="color: var(--text-600); font-size: 0.9rem;">Every recommendation is checked for human safety and eco-friendliness</p>
            </div>
            """, unsafe_allow_html=True)
        with f3:
            st.markdown("""
            <div class="result-card" style="text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 1rem;">📈</div>
                <h3 style="font-weight: 600;">Real Impact</h3>
                <p style="color: var(--text-600); font-size: 0.9rem;">Track CO₂ savings and environmental impact of your upcycling projects</p>
            </div>
            """, unsafe_allow_html=True)

    # ==========================================
    # RESULTS DASHBOARD
    # ==========================================
    else:
        result = st.session_state.analysis_result
        vision = result['vision_result']
        analysis = result['analysis_result']
        final = result['final_output']
        
        # Back Button
        if st.button("← Analyze Another Item"):
            st.session_state.analysis_result = None
            st.rerun()

        # Layout: Left Info | Right Recommendations
        left_col, right_col = st.columns([1, 2])

        with left_col:
            # Object Card
            safety_score = analysis.get('safety_score', final['score'])
            recyclability = analysis.get('recyclability', True)
            verdict = final['verdict']
            materials = ', '.join(analysis.get('material_composition', ['Unknown']))
            
            st.markdown(f"""
            <div class="result-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <h3 style="font-size: 1.5rem; font-weight: 700; margin: 0;">{final['object_type']}</h3>
                    <span class="badge badge-{'emerald' if recyclability else 'amber'}">
                        { 'Recyclable' if recyclability else 'Special Handling' }
                    </span>
                </div>
                <div style="margin-bottom: 1rem; border-radius: 0.75rem; overflow: hidden;">
                    <img src="data:image/png;base64,{result['image_b64']}" style="width: 100%; object-fit: cover;">
                </div>
                <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid var(--border-color);">
                    <span style="color: var(--text-600);">Verdict</span>
                    <span style="font-weight: 500;">{verdict}</span>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 0.5rem 0;">
                    <span style="color: var(--text-600);">Materials</span>
                    <span style="font-weight: 500; text-align: right;">{materials}</span>
                </div>
                <div style="margin-top: 1rem; padding: 0.75rem; background: var(--primary-50); border: 1px solid var(--primary-100); border-radius: 9999px; display: flex; align-items: center; justify-content: center; gap: 0.5rem; color: var(--primary-700); font-weight: 600;">
                    🛡️ Safety Score: {safety_score}/100
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Impact Card
            co2_saved = analysis.get('estimated_co2_saved_kg', 0.5)
            # Ensure co2_saved is a number
            if isinstance(co2_saved, str):
                try:
                    co2_saved = float(co2_saved.replace('kg', '').strip())
                except:
                    co2_saved = 0.5
            
            st.markdown(f"""
            <div class="impact-card">
                <div class="impact-title">
                    🍃 Environmental Impact
                </div>
                <div class="impact-row">
                    <span>CO₂ per kg</span>
                    <span>{co2_saved} kg</span>
                </div>
                <div class="impact-row">
                    <span>Total Potential</span>
                    <span>{(co2_saved * 2.5):.2f} kg</span>
                </div>
                <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid rgba(255,255,255,0.2); font-size: 0.875rem; opacity: 0.9;">
                    Upcycling this item can save significant energy compared to manufacturing new materials!
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Condition Summary
            st.markdown(f"""
            <div class="result-card">
                 <h4 style="font-weight: 600; margin-bottom: 0.5rem; color: var(--text-900);">📝 Condition Summary</h4>
                 <p style="color: var(--text-600); font-size: 0.9rem;">{result['condition_summary']}</p>
            </div>
            """, unsafe_allow_html=True)

        with right_col:
            st.markdown("""
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
                <h3 style="font-size: 1.5rem; font-weight: 700; margin: 0; color: var(--text-900);">AI-Generated Eco Ideas</h3>
                <span style="color: var(--text-600); font-size: 0.9rem;">Powered by Gemini</span>
            </div>
            """, unsafe_allow_html=True)

            suggestions = analysis.get('suggestions', [])
            if not suggestions:
                st.info("No specific recommendations found.")
            
            for i, rec in enumerate(suggestions):
                # Render expandable card using Streamlit expander for interactivity
                title = rec.get('title', rec.get('use_case', 'Suggestion'))
                desc = rec.get('description', rec.get('explanation', ''))
                difficulty = rec.get('difficulty', 'Medium')
                category = rec.get('category', 'Upcycle')
                time_req = rec.get('time_required', '30 mins')
                co2 = rec.get('co2_saved', 0.1)

                # Badge colors
                cat_color = 'purple' if category == 'Upcycle' else 'blue'
                diff_color = 'emerald' if difficulty == 'Easy' else 'amber' if difficulty == 'Medium' else 'red'

                with st.expander(f"{title}"):
                    st.markdown(f"""
                    <div style="margin-bottom: 1rem;">
                        <div class="rec-badges">
                            <span class="badge badge-{cat_color}">{category}</span>
                            <span class="badge badge-{diff_color}">{difficulty}</span>
                        </div>
                        <p class="rec-desc">{desc}</p>
                        <div class="rec-stats">
                            <span class="rec-stat-item">⚡ {time_req}</span>
                            <span class="rec-stat-item">🌍 {co2} kg CO₂ saved</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown("**📦 Materials Needed**")
                        for mat in rec.get('materials', []):
                            st.markdown(f"- {mat}")
                    
                    with c2:
                        st.markdown("**✅ Instructions**")
                        for idx, step in enumerate(rec.get('steps', []), 1):
                            st.markdown(f"{idx}. {step}")

                    if rec.get('safety_notes'):
                        st.markdown("""
                        <div style="margin-top: 1rem; padding: 1rem; background: #fffbeb; border: 1px solid #fcd34d; border-radius: 0.5rem;">
                            <strong style="color: #92400e; display: flex; align-items: center; gap: 0.5rem;">⚠️ Safety Precautions</strong>
                            <ul style="margin: 0.5rem 0 0 1.5rem; color: #b45309; font-size: 0.9rem;">
                        """ + "".join([f"<li>{note}</li>" for note in rec['safety_notes']]) + """
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)

            # Call to Action
            st.markdown("""
            <div class="result-card" style="background: linear-gradient(to right, #fdf4ff, #fae8ff); border-color: #e9d5ff;">
                <div style="display: flex; gap: 1rem; align-items: start;">
                    <div style="font-size: 1.5rem;">💜</div>
                    <div>
                        <h4 style="font-weight: 600; color: #111827; margin: 0 0 0.25rem 0;">Share Your Creation!</h4>
                        <p style="font-size: 0.9rem; color: #4b5563; margin: 0;">
                            Made something amazing? Share your upcycled creation with our community 
                            and inspire others to reduce waste!
                        </p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)


def perform_analysis(uploaded_file):
    # Progress Display
    progress_container = st.empty()
    
    steps = [
        ("📤 Image Preprocessing", "Enhancing quality..."),
        ("📦 Object Detection", "Identifying waste type..."),
        ("🛡️ Safety Analysis", "Checking hazards..."),
        ("✨ GenAI Reasoning", "Generating reuse ideas...")
    ]
    
    for i, (title, desc) in enumerate(steps):
        progress_container.info(f"**{title}**\n\n{desc}")
        time.sleep(0.8) # Simulate processing time for UX
    
    # Actual Processing
    try:
        bytes_data = uploaded_file.getvalue()
        image = load_image_from_bytes(bytes_data)
        
        # Convert to b64 for display
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        # Run Backend
        vision_result, analysis_result, final_output = run_complete_analysis(image)
        
        # Store in session
        st.session_state.analysis_result = {
            'vision_result': vision_result,
            'analysis_result': analysis_result,
            'final_output': final_output,
            'image_b64': img_str,
            'condition_summary': final_output.get('condition_summary', '')
        }
        
        progress_container.empty()
        st.rerun()
        
    except Exception as e:
        progress_container.error(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
