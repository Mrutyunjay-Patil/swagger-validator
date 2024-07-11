
# Swagger Validator App

## Overview

The Swagger Validator App is a powerful tool built with Streamlit that allows users to validate, convert, and visualize Swagger (OpenAPI) specifications. The app provides a user-friendly interface for handling Swagger specifications in both JSON and YAML formats, with additional features to enhance the user experience.

## Features

- **Input Methods**:
  - Paste Swagger specifications directly into a text area (JSON or YAML).
  - Upload Swagger specification files (JSON or YAML).
  - Enter a URL pointing to a Swagger specification, which the app will fetch and validate.

- **Conversion Features**:
  - Convert JSON Swagger specifications to YAML format.
  - Convert YAML Swagger specifications to JSON format.

- **Validation and Output**:
  - Validate Swagger specifications using a Python library that supports both JSON and YAML formats.
  - Display detailed error messages and suggestions for resolving issues within the Swagger specification.
  - If the Swagger specification is valid, display it using an integrated Swagger UI component.

- **Additional Features**:
  - Syntax highlighting in the input area for better readability.
  - Download options for validated or converted Swagger specifications.
  - Session-based history of user activities, accessible during the session.

## Installation

To install and run the Swagger Validator App, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/swagger-validator-app.git
   cd swagger-validator-app
   ```

2. **Create a virtual environment and activate it**:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows, use `env\Scripts\activate`
   ```

3. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Streamlit app**:
   ```bash
   streamlit run app.py
   ```

## Usage

1. **Select Input Method**:
   - Choose from "Paste", "File Upload", or "URL" to provide the Swagger specification.

2. **Validate**:
   - Click the "Validate" button to validate the Swagger specification.
   - If the specification is valid, it will be displayed using Swagger UI.
   - If there are errors, detailed error messages will be shown.

3. **Convert**:
   - Convert JSON to YAML or YAML to JSON using the respective buttons.
   - Download the converted specification using the provided download button.

4. **History**:
   - View the session-based history of your actions in the sidebar.
   - Expand each action to see the specification and the result.

## Example

To validate a Swagger specification:

1. Select the input method (Paste, File Upload, or URL).
2. Provide the Swagger specification.
3. Click "Validate".
4. View the result in the main area or check the history in the sidebar.

## Contact

Created by **Mrutyunjay Patil** - [patilmrutyunjay2@gmail.com](mailto:patilmrutyunjay2@gmail.com)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
