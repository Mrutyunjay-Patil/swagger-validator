# File path: app.py

import streamlit as st
import requests
import yaml
import json
from prance import ResolvingParser
from openapi_spec_validator import validate_spec
from collections import deque

# Configure the Streamlit app to remove the main menu and toolbar
st.set_page_config(
    page_title="Swagger Validator App",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hide the main menu and footer with CSS
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

# Initialize session state for history if not already done
if 'history' not in st.session_state:
    st.session_state.history = []

# Function to validate Swagger specification
def validate_swagger_spec(spec):
    try:
        parser = ResolvingParser(spec_string=spec, backend='openapi-spec-validator')
        validate_spec(parser.specification)
        return True, "Valid Swagger Specification"
    except Exception as e:
        return False, parse_validation_error(e)

# Function to convert JSON to YAML
def json_to_yaml(json_data):
    return yaml.dump(json_data, sort_keys=False)

# Function to convert YAML to JSON
def yaml_to_json(yaml_data):
    return yaml.safe_load(yaml_data)

# Function to parse validation errors into a human-readable format
def parse_validation_error(e):
    if isinstance(e, tuple):
        message, keyword, path, schema_path, validation_errors, _, instance, schema = e
        error_message = f"Validation failed due to: {message}\n"
        error_message += f"Keyword: {keyword}\n"
        error_message += f"Path: {' -> '.join(map(str, path))}\n"
        if schema_path:
            error_message += f"Schema Path: {' -> '.join(map(str, schema_path))}\n"
        if validation_errors:
            error_message += "Validation Errors:\n"
            for ve in validation_errors:
                error_message += f"  - {str(ve)}\n"
        error_message += f"Instance: {json.dumps(instance, indent=2)}\n"
        error_message += f"Schema: {json.dumps(schema, indent=2)}\n"
        return error_message
    else:
        return str(e)

# Function to save history
def save_history(action, spec, result):
    st.session_state.history.append({
        "action": action,
        "spec": spec,
        "result": result
    })

# About Page
def about_page():
    st.title("About This App")
    st.write("""
    This Swagger Validator App helps users validate, convert, and visualize Swagger (OpenAPI) specifications.
    
    ### Features:
    - Paste Swagger specifications in JSON/YAML format
    - Upload Swagger files
    - Enter URL to fetch Swagger specification
    - Convert between JSON and YAML
    - Validate Swagger specifications
    - Display valid specifications using Swagger UI
    - Syntax highlighting
    - Download options for validated/converted specifications
    - Session-based history

    Created by **Mrutyunjay Patil** - **mrutyunjay.patil@infosysequinox.com**
    """)

# Main Application
def main():
    st.sidebar.title("Swagger Validator App")
    st.sidebar.markdown("Select an option:")
    page = st.sidebar.selectbox("Page", ["Swagger Validator", "About"])

    if page == "About":
        about_page()
        return

    st.title("Swagger Validator App")
    st.write("Validate and convert Swagger (OpenAPI) specifications")

    # Display history
    st.sidebar.title("History")
    for i, item in enumerate(st.session_state.history):
        with st.sidebar.expander(f"Action {i+1}: {item['action']}"):
            st.write("Specification:")
            st.code(item['spec'], language="yaml")
            st.write("Result:")
            st.code(item['result'], language="yaml")

    # Input method selection
    input_method = st.radio("Choose input method:", ["Paste", "File Upload", "URL"])

    spec = None
    if input_method == "Paste":
        spec = st.text_area("Paste your Swagger specification here (JSON or YAML)", height=300)
    elif input_method == "File Upload":
        uploaded_file = st.file_uploader("Upload Swagger specification file", type=["json", "yaml", "yml"])
        if uploaded_file:
            spec = uploaded_file.read().decode('utf-8')
    elif input_method == "URL":
        url = st.text_input("Enter URL of Swagger specification")
        if url:
            try:
                response = requests.get(url)
                response.raise_for_status()
                spec = response.text
            except Exception as e:
                st.error(f"Error fetching URL: {e}")
                return

    if st.button("Validate"):
        if spec:
            is_json = spec.strip().startswith("{")
            if is_json:
                try:
                    json_data = json.loads(spec)
                    valid, message = validate_swagger_spec(spec)
                except json.JSONDecodeError as e:
                    st.error(f"Invalid JSON: {e}")
                    return
            else:
                try:
                    yaml_data = yaml.safe_load(spec)
                    json_data = yaml_to_json(spec)
                    valid, message = validate_swagger_spec(json.dumps(json_data))
                except yaml.YAMLError as e:
                    st.error(f"Invalid YAML: {e}")
                    return
            
            if valid:
                st.success("Swagger specification is valid")
                result = "Valid Swagger Specification"
                save_history("Validate", spec, result)
                # Embed Swagger UI with white background and scrollable
                swagger_ui_html = f"""
                <html>
                <head>
                  <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/4.1.3/swagger-ui.css" >
                  <script src="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/4.1.3/swagger-ui-bundle.js"></script>
                  <script src="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/4.1.3/swagger-ui-standalone-preset.js"></script>
                  <style>
                    body {{
                        margin: 0;
                        padding: 0;
                        overflow: hidden;
                    }}
                    #swagger-ui {{
                        background-color: white;
                    }}
                    .swagger-container {{
                        height: 800px;
                        overflow-y: scroll;
                    }}
                  </style>
                  <script>
                  window.onload = function() {{
                    const ui = SwaggerUIBundle({{
                      spec: {json.dumps(json_data)},
                      dom_id: '#swagger-ui',
                      presets: [
                        SwaggerUIBundle.presets.apis,
                        SwaggerUIStandalonePreset
                      ],
                      layout: "StandaloneLayout"
                    }})
                  }}
                  </script>
                </head>
                <body>
                  <div id="swagger-ui" class="swagger-container"></div>
                </body>
                </html>
                """
                st.components.v1.html(swagger_ui_html, height=800)
            else:
                summary = parse_validation_error(message)
                st.error(f"Validation failed:\n\n{summary}")
                result = summary
                save_history("Validate", spec, result)

    if st.button("Convert JSON to YAML"):
        if spec and spec.strip().startswith("{"):
            try:
                json_data = json.loads(spec)
                yaml_data = json_to_yaml(json_data)
                st.download_button("Download YAML", yaml_data, file_name="swagger.yaml")
                st.write(f"### Converted YAML\n```yaml\n{yaml_data}\n```")
                save_history("Convert JSON to YAML", spec, yaml_data)
            except json.JSONDecodeError as e:
                st.error(f"Invalid JSON: {e}")

    if st.button("Convert YAML to JSON"):
        if spec and not spec.strip().startswith("{"):
            try:
                yaml_data = yaml.safe_load(spec)
                json_data = json.dumps(yaml_data, indent=2)
                st.download_button("Download JSON", json_data, file_name="swagger.json")
                st.write(f"### Converted JSON\n```json\n{json_data}\n```")
                save_history("Convert YAML to JSON", spec, json_data)
            except yaml.YAMLError as e:
                st.error(f"Invalid YAML: {e}")

if __name__ == "__main__":
    main()
