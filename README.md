# Nutrition Tracker

A professional health and nutrition management application built with Python and Streamlit. It helps users track their daily intake, manage food databases, and calculate macros with precision using Supabase as a cloud database backend.

🚀 Key Features

Custom Menu Builder: Easily add foods to your daily log with automatic macronutrient calculation.

Persistent Data: Powered by Supabase (PostgreSQL) via SQLAlchemy for reliable cloud storage.

Data Visualization: Interactive charts and analytics using Plotly.

Smart Caching: Optimized performance with Streamlit caching mechanisms.

Data Analysis: Efficient data processing with Pandas.

🛠 Tech Stack

Frontend: Streamlit

Backend/Database: Supabase, SQLAlchemy

Data Processing: Pandas

Visualization: Plotly

Language: Python 3.12+

📦 Setup & Installation

Follow these steps to get the project running on your machine:

1. Clone the repository:
    ```bash
    git clone https://github.com/gaidukarturio37-lab/gym-tracker.git

    cd gym-tracker

2. Create a virtual environment:

    #Windows
    ```bash
    python -m venv .venv

    .venv\Scripts\activate

    #macOS/Linux
    ```bash
    python3 -m venv .venv

    source .venv/bin/activate

3. Install dependencies:
    ```bash
    pip install -r requirements.txt

4. Configuration:

This application uses Streamlit's secrets management. To run the app locally, create a file named .streamlit/secrets.toml in your project root directory and add your Supabase credentials:

    SUPABASE_URL = "your_url_here"

    SUPABASE_KEY = "your_key_here"

5. Run the application:
    ```bash
    streamlit run main.py

📈 Roadmap (Future Improvements)

[ ] Implement maintenance macros calculation logic.

[ ] Add user authentication system.

[ ] Export reports to PDF/CSV.

📝 License

This project is for educational/personal use.