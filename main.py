#main.py

import base64
import requests
import streamlit as st
import streamlit.components.v1 as components
from collections import defaultdict
import os
from dotenv import load_dotenv

from code_model import create_code_model_prompt, get_code_model, response_to_markdown
from guidence_model import create_guidence_prompt, get_guidence
from test_cases import create_test_cases_prompt, get_test_cases, get_test_cases_azure, get_test_cases_google, get_test_cases_mistral, get_test_cases_ollama, get_test_cases_anthropic

# ------------------ Helper Functions ------------------ #

# Function to get user input for the application description and key details
def get_input():
    input_text_app_desc = st.text_area(
        label="Describe the project use case and working",
        value=st.session_state.get('specific_requirements', ''),
        placeholder="Enter your application details...",
        height=150,
        key="app_desc",
        help="Please provide a detailed description of the application, including the purpose of the application, the technologies used, and any other relevant information.",
    )
    input_text_code = st.text_area(
    label="Optional Code Context/Existing Fragments",
    value=st.session_state.get('specific_requirements', ''),
    placeholder="Enter your existing code...",
    height=150,
    key="app_code",
    help="Please provide existing code that you would like to integrate or optimize for the application. This can include code snippets, functions, or modules.",
)

    st.session_state['input_text_app_desc'] = input_text_app_desc
    st.session_state['input_text_code'] = input_text_code

    return input_text_app_desc, input_text_code

def load_env_variables():
    # Try to load from .env file
    if os.path.exists('.env'):
        load_dotenv('.env')

    google_api_key = os.getenv('GOOGLE_API_KEY')
    if google_api_key:
        st.session_state['google_api_key'] = google_api_key

# Call this function at the start of your app
load_env_variables()

# ------------------ Streamlit UI Configuration ------------------ #

st.set_page_config(
    page_title="Hexorcist",
    page_icon=":shield:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------ Sidebar ------------------ #

st.sidebar.image("hexorcistLogo.webp")
st.sidebar.header("How to use Hexorcist")


with st.sidebar:
    model_provider = "Google AI API"
    
    if model_provider == "Google AI API":
        st.markdown(
        """
    1. Provide details of the application that you would like to get code of  📝
    2. Generate a code for your application with instructions to build and run along with performance optimizations 🚀
    """
    )

        # Add model selection input field to the sidebar
        google_model = "gemini-1.5-flash"

    st.markdown("""---""")
    google_api_key = st.session_state.get('google_api_key', '')

# Add "About" section to the sidebar
st.sidebar.header("About")
with st.sidebar:
    st.markdown(
        "Welcome to Hexorcist, an AI-powered tool for embedded systems development."
    )
    st.markdown(
        "Hexorcist generates hardware-specific code and development guidance for embedded systems, with a focus on Rust. It supports various hardware platforms and uses powerful LLMs to assist developers in their embedded development journey."
    )
    st.markdown("""---""")

# Add "Example Hardware and Use Case" section to the sidebar
st.sidebar.header("Example Hardware and Use Case")

with st.sidebar:
    st.markdown(
        "Below is an example hardware configuration that you can use to test Hexorcist:"
    )
    st.markdown(
        "> A microcontroller with Raspberry Pi 4, running an embedded operating system (RTOS). The project is written in Rust and targets low-power applications such as sensor monitoring and data transmission."
    )
    st.markdown("""---""")

# Add "FAQs" section to the sidebar
st.sidebar.header("FAQs")

with st.sidebar:
    st.markdown(
        """
    ### **What is Hexorcist?**
    Hexorcist is an AI-powered tool designed to assist in embedded systems development by generating hardware-specific code and providing development guidance. It emphasizes Rust for embedded systems and supports various hardware platforms.
    """
    )
    st.markdown(
        """
    ### **How does Hexorcist work?**
    You can choose your target hardware, and Hexorcist will generate optimized code and development instructions tailored to that hardware. It also suggests best practices and offers multi-modal input options such as architecture diagrams and flowcharts.
    """
    )
    st.markdown(
        """
    ### **Which hardware platforms does Hexorcist support?**
    Hexorcist supports a wide range of hardware platforms. You can select from the available hardware options, and the tool will generate code specific to the selected platform.
    """
    )
    st.markdown(
        """
    ### **How can I use Hexorcist?**
    You can run Hexorcist either locally by installing the required Python packages or via Docker. Check the [installation](#installation) section for detailed instructions.
    """
    )
    st.markdown(
        """
    ### **Do you store the hardware or code generated?**
    No, Hexorcist does not store your hardware configurations or generated code. The tool runs locally, and all data is discarded once the session ends.
    """
    )
    st.markdown(
        """
    ### **Why does it take time to generate code?**
    Depending on the complexity of the hardware and the code, it may take time for Hexorcist to generate the appropriate output. Using a more powerful API or providing more specific inputs can help speed up the process.
    """
    )
    st.markdown(
        """
    ### **Is the generated code always accurate?**
    While Hexorcist uses advanced LLMs, the generated code may not always be perfect. It is important to review the code and optimize it further based on your specific requirements.
    """
    )
    st.markdown(
        """
    ### **How can I improve the accuracy of the generated code?**
    You can improve the quality of the generated code by providing detailed hardware descriptions and configurations. The more precise your input, the better the generated code will be.
    """
    )

# -------------FAQs----- Main App UI ------------------ #

tab1, tab2, tab3 = st.tabs([ "Code Generation", "Development Guidence", "Test Cases"])


# ------------------ Code Generation------------------ #

with tab1:
    st.markdown("""
Generate code and documentation and performance optimizations for your application. Provide the necessary details.
""")
    st.markdown("""---""")
    
    # Two column layout for the main app content
    col1, col2 = st.columns([1, 1])

    # Initialize input_text_app_desc in the session state if it doesn't exist
    if 'input_text_app_desc' not in st.session_state:
        st.session_state['input_text_app_desc'] = ''
        st.session_state['input_text_code'] = ''

    with col1:
        # Use the get_input() function to get the application description and GitHub URL
        input_text_app_desc, input_text_code = get_input()
        # Update session state only if the text area content has changed
        if input_text_app_desc != st.session_state['input_text_app_desc'] or input_text_code != st.session_state['input_text_code']:
            st.session_state['input_text_app_desc'] = input_text_app_desc
            st.session_state['input_text_code'] = input_text_code

    # Ensure input_text_app_desc is always up to date in the session state
    input_text_app_desc = st.session_state['input_text_app_desc']
    input_text_code = st.session_state['input_text_code']



        # Create input fields for additional details
    with col2:
            language_type = st.selectbox(
                label="Select the language of the application",
                options=[
                    "Rust",
                    "C",
                    "C++",
                    "Assembly",
                    "VHDL",
                ],
                key="app_type",
            )

            hardware_name = st.selectbox(
                label="Select the hardware you are using?",
                options=[
                    "Arduino Uno",
                    "Arduino Nano",
                    "Arduino Mega",
                    "ESP32",
                    "ESP8266",
                    "STM32",
                    "ATmega328P (AVR)",
                    "PIC Microcontrollers (Microchip)",
                    "TI MSP430",
                    "Raspberry Pi 4",
                    "Raspberry Pi Zero",
                    "BeagleBone Black",
                    "Xilinx Zynq"
                ],
                key="hardware_type",
            )

    # ------------------ Threat Model Generation ------------------ #

    # Create a submit button for Threat Modelling
    generate_code_submit_button = st.button(label="Generate Code")

    # If the Generate Threat Model button is clicked and the user has provided an application description
    if generate_code_submit_button and st.session_state.get('input_text_app_desc'):
        input_text_app_desc = st.session_state['input_text_app_desc']  # Retrieve from session state
        input_text_code = st.session_state['input_text_code']  # Retrieve from session state
        # Generate the prompt using the create_prompt function
        code_model_prompt = create_code_model_prompt(language_type, hardware_name, input_text_app_desc, input_text_code)

        # Show a spinner while generating the threat model
        with st.spinner("Generating your code..."):
            max_retries = 3
            retry_count = 0
            while retry_count < max_retries:
                try:
                   
                    model_output = get_code_model(google_api_key, google_model, code_model_prompt)
                   

                    # Access the threat model and improvement suggestions from the parsed content
                    code = model_output.get("source_code", "")
                    documentation = model_output.get("documentation", "")
                    optimization_recommendations = model_output.get("optimization_recommendations", [])

                    # Save the threat model to the session state for later use in mitigations
                    st.session_state['code'] = code
                    st.session_state['language_type'] = language_type
                    st.session_state['hardware_name'] = hardware_name
                    break  # Exit the loop if successful
                except Exception as e:
                    retry_count += 1
                    if retry_count == max_retries:
                        st.error(f"Error generating threat model after {max_retries} attempts: {e}")
                        code = ""
                        documentation = ""
                        optimization_recommendations = []
                    else:
                        st.warning(f"Error generating code. Retrying attempt {retry_count+1}/{max_retries}...")

        # Convert the threat model JSON to Markdown
        markdown_output = response_to_markdown( documentation, optimization_recommendations)

        # Display the threat model in Markdown
        st.code(code, language=language_type)
        st.markdown(markdown_output)

        # Add a button to allow the user to download the output as a Markdown file
        st.download_button(
            label="Download Documentation",
            data=markdown_output,  # Use the Markdown output
            file_name="hexorcist_code_model.md",
            mime="text/markdown",
       )

# If the submit button is clicked and the user has not provided an application description
if generate_code_submit_button and not st.session_state.get('input_text_app_desc'):
    st.error("Please enter your application details before submitting.")



# ------------------ Development Guidence ------------------ #

with tab2:
    st.markdown("""
Development Guidence techniques, and additional resources to help you improve and maintain your application effectively.""")
    st.markdown("""---""")
    
    # Create a submit button for Mitigations
    get_guidence_submit_button = st.button(label="Get Guidence")

    # If the Suggest Mitigations button is clicked and the user has identified threats
    if get_guidence_submit_button:
        # Check if threat_model data exists
        if 'code' in st.session_state and st.session_state['code'] and 'language_type' in st.session_state and st.session_state['language_type'] and 'hardware_name' in st.session_state and st.session_state['hardware_name']:

            code = st.session_state['code']
            language = st.session_state['language_type']
            hardware = st.session_state['hardware_name']

            # Generate the prompt using the create_guidence_prompt function
            guidence_prompt = create_guidence_prompt(code, language, hardware, input_text_app_desc)

            # Show a spinner while suggesting guidence
            with st.spinner("Generating Guidence..."):
                max_retries = 3
                retry_count = 0
                while retry_count < max_retries:
                    try:
                        # Call the relevant get_guidence function with the generated prompt
                        guidence_markdown = get_guidence(google_api_key, google_model, guidence_prompt)
                        # Display the suggested guidence in Markdown
                        st.markdown(guidence_markdown)
                        break  # Exit the loop if successful
                    except Exception as e:
                        retry_count += 1
                        if retry_count == max_retries:
                            st.error(f"Error suggesting guidence after {max_retries} attempts: {e}")
                            guidence_markdown = ""
                        else:
                            st.warning(f"Error suggesting guidence. Retrying attempt {retry_count+1}/{max_retries}...")
            
            st.markdown("")

            # Add a button to allow the user to download the guidence as a Markdown file
            st.download_button(
                label="Download guidence",
                data=guidence_markdown,
                file_name="guidence.md",
                mime="text/markdown",
            )
        else:
            st.error("Please generate a threat model first before suggesting guidence.")

# ------------------ Test Cases Generation ------------------ #

with tab3:
    st.markdown("""
Test cases are essential to validate the functionality, security, and reliability of your application. This section allows you to generate 
test cases tailored to your application's requirements and threat scenarios.
""")
    st.markdown("""---""")
    
    # Create a submit button for Test Case Generation
    generate_test_cases_submit_button = st.button(label="Generate Test Cases")

    # If the Generate Test Cases button is clicked
    if generate_test_cases_submit_button:
        # Check if the necessary inputs are available
        if 'code' in st.session_state and st.session_state['code'] and 'language_type' in st.session_state and st.session_state['language_type'] and 'hardware_name' in st.session_state and st.session_state['hardware_name']:
            code = st.session_state['code']
            language = st.session_state['language_type']
            hardware = st.session_state['hardware_name']

            # Generate the prompt using the create_test_cases_prompt function
            test_cases_prompt = create_test_cases_prompt(code, language, hardware, input_text_app_desc)

            # Show a spinner while generating test cases
            with st.spinner("Generating Test Cases..."):
                max_retries = 3
                retry_count = 0
                while retry_count < max_retries:
                    try:
                        # Call the relevant get_test_cases function with the generated prompt
                        test_cases_markdown = get_test_cases(google_api_key, google_model, test_cases_prompt)
                        
                        # Display the generated test cases in Markdown
                        st.markdown(test_cases_markdown)
                        break  # Exit the loop if successful
                    except Exception as e:
                        retry_count += 1
                        if retry_count == max_retries:
                            st.error(f"Error generating test cases after {max_retries} attempts: {e}")
                            test_cases_markdown = ""
                        else:
                            st.warning(f"Error generating test cases. Retrying attempt {retry_count+1}/{max_retries}...")
            
            st.markdown("")

            # Add a button to allow the user to download the test cases as a Markdown file
            st.download_button(
                label="Download Test Cases",
                data=test_cases_markdown,
                file_name="test_cases.md",
                mime="text/markdown",
            )
        else:
            st.error("Please ensure code, language type, and hardware name are provided before generating test cases.")
