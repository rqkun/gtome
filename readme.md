[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://rqkun-gtome.streamlit.app/)
[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/rqkun/gtome/blob/main/readme.md)
[![vi](https://img.shields.io/badge/lang-vn-yellow.svg)](https://github.com/rqkun/gtome/blob/main/readme_vn.md)
# GTOME Streamlit App

Welcome to the GTOME Streamlit App! This user-friendly application is designed to streamline your GTOME by seamlessly importing data from Google Sheets. With this app, you can track expenses, manage budgets, and generate insightful financial reports effortlessly.
Checkout the website [here](https://rqkun-gtome.streamlit.app/)
## Features

- **Google Sheets Integration**: Easily store your financial data from Google Sheets.
- **Expense Tracking**: Keep track of your expenses with ease.
- **Data Grid**: Set and manage budgets using data grids.
- **Intuitive Visualizations**: Visualize your financial data with charts and graphs for better understanding.

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Streamlit
- Google API credentials
- Firebase API credentials
- Supabase API credentials

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/rqkun/gtome.git
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Set up Google API credentials:
    - Follow the instructions [here](https://github.com/streamlit/gsheets-connection?tab=readme-ov-file#service-account--crud-example) to create your credentials and save it to your `.streamlit/secrets.toml` file.
    - Go to [here](https://console.cloud.google.com/) and create an authentication Client and copy your credentials and save it to your `.streamlit/secrets.toml` file.
    - Go to [here](https://firebase.google.com/) and create an authentication app and add your API_KEY to `.streamlit/secrets.toml` file.
    - Open your firebase console and go to Authentication > Sign-in methods and add the Google provider, fill the `client_id`, `client_secret` and `secret` field.

4. Set up Supabase credentials:
    - Follow the instructions [here](https://docs.streamlit.io/develop/tutorials/databases/supabase) to create your credentials and save it to your `.streamlit/secrets.toml` file.

5. Your `.streamlit/secrets.toml` or cloud secrets should look like this:
    ```
    [auth]
    redirect_uri = "http://localhost:8501/oauth2callback"
    cookie_secret = "" # self generated
    client_id = ""
    client_secret = ""
    server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration"

    [connections.google_api]
    spreadsheet = "<googlesheet_url>"
    type = "service_account"
    project_id = ""
    private_key_id= ""
    private_key=""
    client_email= ""
    client_id= ""
    auth_uri = "https://accounts.google.com/o/oauth2/auth"
    token_uri ="https://oauth2.googleapis.com/token"
    auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
    client_x509_cert_url =""
    #authentication secrets
    secret = ""
    javascript_origins = ""
    redirect_url = ""
    endpoint = "https://www.googleapis.com/identitytoolkit/v3/relyingparty"
    #firebase api key
    api_key = ""

    [supabase]
    url = ""
    key = ""

    ```
### Running the App

1. Start the Streamlit app:
    ```sh
    streamlit run app.py
    ```

2. Open your web browser and navigate to `http://localhost:8501` to access the app.

## Usage

1. **Google Sheet**: Use the app to store your financial data to Google Sheets.
2. **Track Expenses**: Add, edit, and delete expense entries to keep your records up to date.
3. **Visualize Data**: View your financial data through various charts and graphs for better insights.

---

Thank you for using the GTOME Streamlit App! We hope it helps you manage your finances more effectively.