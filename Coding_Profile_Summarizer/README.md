# Coding Profile Summarizer

## Description

A web application that fetches and displays user statistics from various competitive programming and coding platforms like LeetCode, CodeChef, GeeksforGeeks, and HackerRank.

## Live Demo 🚀

You can try out the live application here:
**[View Live Application](https://your-service-name.onrender.com)**
*`https://coding-profile-summarizer.onrender.com`*

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
    *   `gunicorn` (for WSGI server in production)

## Setup and Running Locally

1.  **Clone the parent repository (if not already done):**
    ```bash
    git clone https://github.com/dheeraj247/Mini-projects.git
    cd Mini-projects/Coding_Profile_Summarizer
    ```
    *(Updated to your GitHub username)*

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the Flask development server:**
    ```bash
    python app.py
    ```
4.  Open your browser and navigate to `http://127.0.0.1:5000/`.

## Usage

1.  Select a platform from the dropdown menu.
2.  Enter the username for that platform.
3.  Click "Fetch Profile".
4.  The user's statistics will be displayed.

## Deployment

This application is designed to be deployed with the Flask backend serving the static frontend files.
It has been deployed to Render. A `Procfile` is included for Gunicorn.

*   **Backend API Endpoint:** `/api/fetch_profile_data` (POST request)

---

*This project was created by S.Dheeraj (dheeraj247).*