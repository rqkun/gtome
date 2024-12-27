[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint)

# GTOME Streamlit App

Welcome to the GTOME Streamlit App! This user-friendly application is designed to streamline your GTOME by seamlessly importing data from Google Sheets. With this app, you can track expenses, manage budgets, and generate insightful financial reports effortlessly.

## Features

- **Google Sheets Integration**: Easily import your financial data from Google Sheets.
- **Expense Tracking**: Keep track of your expenses with ease.
- **Data Grid**: Set and manage budgets using data grids.
- **Intuitive Visualizations**: Visualize your financial data with charts and graphs for better understanding.

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Streamlit
- Google Sheets API credentials
- Firebase API credentials

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/rqkun/gtome.git
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Set up Google Sheets API credentials:
    - Follow the instructions [here](https://github.com/streamlit/gsheets-connection?tab=readme-ov-file#service-account--crud-example) to create your credentials and save it to your `.streamlit/secrets.toml` file.

4. Set up Google Firebase API credentials:
    - Go to [here](https://firebase.google.com/) and create an authentication app and add your API_KEY to `.streamlit/secrets.toml` file.
    - Open your firebase console and go to Authentication > Sign-in methods and the Email/Password provider.

### Running the App

1. Start the Streamlit app:
    ```sh
    streamlit run app.py
    ```

2. Open your web browser and navigate to `http://localhost:8501` to access the app.

## Usage

1. **Import Data**: Use the app to import your financial data from Google Sheets.
2. **Track Expenses**: Add, edit, and delete expense entries to keep your records up to date.
3. **Visualize Data**: View your financial data through various charts and graphs for better insights.

---

Thank you for using the GTOME Streamlit App! We hope it helps you manage your finances more effectively.