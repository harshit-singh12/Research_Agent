# Handle SQLite for ChromaDB
try:
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except (ImportError, KeyError):
    pass

import streamlit as st
from utils.output_handler import capture_output
from main import main_research_flow
import os
import certifi
os.environ["SSL_CERT_FILE"] = certifi.where()


# Configure the page
st.set_page_config(
    page_title="CrewAI Research Assistant",
    page_icon="🕵️‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar menu
with st.sidebar:
    col1, col2, col3 = st.columns([0.1, 3.8, 0.1])
    with col2:
        st.image(
            "https://cdn.prod.website-files.com/6481bf7bc1b01843dd1ced2b/6486e1c21b809d25782b7554_LATENTBRIDGE%20LOGO3%20TRANSPARENT%20(1)%203.png",
            width=220
        )
        st.header("Pre-Sales Agent Crew")
        st.markdown(
            """
            Our **Pre-Sales Agent Crew** specializes in comprehensive research services tailored to your needs.  
            Currently, we offer:
            - Detailed **company research**
            - In-depth **person research**
            
            We provide you with the insights and data necessary to make informed decisions and drive your business forward.
            """
        )


# Main layout
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st.title("🔍 Pre-Sales Agent", anchor=False)


input_col1, input_col2, input_col3 = st.columns([0.5, 3, 0.5])
with input_col2:
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        company_input = st.text_input("Company you'd like me to research:")
    with col2:
        person_input = st.text_input("Person you'd like me to research:")
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        start_research = st.button("🚀 Start Research", use_container_width=False, type="primary")

research_flow = main_research_flow()
result_text = ""
result = []
if start_research and (company_input.strip() or person_input.strip()):
    with st.status("🤖 Researching...", expanded=True) as status:
        try:
            # Create persistent container for process output with fixed height.
            process_container = st.container(height=300, border=True)
            output_container = process_container.container()
            # Single output capture context.
            with capture_output(output_container):
                if company_input.strip() and person_input.strip():
                    result = research_flow.startCrew(company_name=company_input, person_name=person_input)
                elif company_input.strip():
                    result = research_flow.startCrew(company_name=company_input, person_name="")
                elif person_input.strip():
                    result = research_flow.startCrew(company_name="", person_name=person_input)
                status.update(label="✅ Research completed!", state="complete", expanded=False)
        except Exception as e:
            status.update(label="❌ Error occurred", state="error")
            st.error(f"An error occurred: {str(e)}")
            st.stop()
    # Convert CrewOutput to string for display and download
    if company_input.strip() and person_input.strip():
        # First expandable container: Company Research Report
        with st.expander("📊 Company Research Report", expanded=True):
            st.markdown(str(result[0]))

        # Second expandable container: Person Research Report
        with st.expander("👤 Person Research Report", expanded=True):
            st.markdown(str(result[1]))
    else:
        if company_input.strip():
            with st.expander("📊 Company Research Report", expanded=True):
                st.markdown(str(result))
        elif person_input.strip():
            with st.expander("👤 Person Research Report", expanded=True):
                st.markdown(str(result))

st.divider()