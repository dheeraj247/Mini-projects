# Coding Profile Summarizer

## Description

A web application that fetches and displays user statistics from various competitive programming and coding platforms like LeetCode, CodeChef, GeeksforGeeks, and HackerRank.

## Features

*   Fetches user rating, rank, problems solved, etc.
*   Supports:
    *   LeetCode
    *   CodeChef
    *   GeeksforGeeks
    *   HackerRank

## Tech Stack

*   **Backend:** Python, Flask
*   **Frontend:** HTML, CSS, Vanilla JavaScript
*   **Libraries:**
    *   `requests` (for HTTP calls)
    *   `BeautifulSoup4` (for web scraping)
    *   `Flask-CORS` (for Cross-Origin Resource Sharing)

## Setup and Running Locally

1.  **Clone the parent repository (if not already done):**
    ```bash
    git clone https://github.com/YOUR_USERNAME/Mini-projects.git
    cd Mini-projects/Coding_Profile_Summarizer
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the Flask development server:**
    ```bash
    python app.py
    ```
5.  Open your browser and navigate to `http://127.0.0.1:5000/`.

## Usage

1.  Select a platform from the dropdown menu.
2.  Enter the username for that platform.
3.  Click "Fetch Profile".
4.  The user's statistics will be displayed.

*   **Backend API Endpoint:** `/api/fetch_profile_data` (POST request)

---

*This project was created by [S.Dheeraj/dheeraj247].*