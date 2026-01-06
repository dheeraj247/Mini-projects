from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
import re
from flask import send_from_directory
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def fetch_codechef_data(username):
    url = f"https://www.codechef.com/users/{username}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

    try:
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            if response.status_code == 404:
                return {"error": f"Could not fetch data: User '{username}' not found on CodeChef."}
            return {"error": f"Failed to fetch CodeChef data for '{username}'. Status code: {response.status_code}"}

        soup = BeautifulSoup(response.content, "html.parser")
        if soup.title and "user not found" in soup.title.text.lower():
            return {"error": f"Could not fetch data: User '{username}' not found on CodeChef."}
        not_found_element = soup.find("div", class_="user-profile-container--placeholder")
        if not_found_element and "could not find a user" in not_found_element.text.lower():
            return {"error": f"Could not fetch data: User '{username}' not found on CodeChef."}

        rating_div = soup.find("div", class_="rating-number")
        rating = rating_div.text.strip() if rating_div else "No rating available"

        if rating == "No rating available":
             
             profile_name_on_page = soup.find("h1", class_="h1-style") 
             if not profile_name_on_page or username.lower() not in profile_name_on_page.text.lower():
                 return {"error": f"Could not fetch data: User '{username}' not found or has an inactive profile on CodeChef."}
        solved_problems = "Not found"
        user_details_div = soup.find("div", class_="user-details-container")
        h3_tags = []
        if user_details_div:
            h3_tags = user_details_div.find_all("h3")
        if h3_tags:
            last_h3 = h3_tags[-1]
            match = re.search(r'\((\d+)\)', last_h3.text)
            if match:
                solved_problems = int(match.group(1))
            else:
                match = re.search(r'\d+', last_h3.text)
                if match:
                    solved_problems = int(match.group())

        global_rank = "Not available"
        country_rank = "Not available"
        ranks_div = soup.find("div", class_="rating-ranks")
        if ranks_div:
            ul = ranks_div.find("ul", class_="inline-list")
            if ul:
                li_tags = ul.find_all("li")
                if len(li_tags) >= 2:
                    global_tag = li_tags[0].find("a")
                    country_tag = li_tags[1].find("a")
                    if global_tag: global_rank = global_tag.text.strip()
                    if country_tag: country_rank = country_tag.text.strip()

        stars, division, highest_rating = "Not available", "Not available", "Not available"
        rating_header = soup.find("div", class_="rating-header")
        if rating_header:
            star_div = rating_header.find("div", class_="rating-star")
            if star_div: stars = star_div.text.strip()
            all_divs = rating_header.find_all("div", recursive=False)
            if len(all_divs) >= 2 and "Div" in all_divs[1].text.strip():
                division = all_divs[1].text.strip()
            small_tag = rating_header.find("small")
            if small_tag:
                match = re.search(r'\d+', small_tag.text)
                if match: highest_rating = int(match.group())

        return {"username": username, "rating": rating, "global_rank": global_rank, "country_rank": country_rank, "solved_problems": solved_problems, "stars": stars, "division": division, "highest_rating": highest_rating}
    except Exception as e:
        return {"error": f"An error occurred while processing CodeChef data for '{username}'."}


def extract_number(text):
    match = re.search(r'\((\d+)\)', text)
    return match.group(1) if match else "0"


def fetch_gfg_data(username):
    url = f"https://www.geeksforgeeks.org/profile/{username}"
    
    page_source = ""
    driver = None
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        driver.get(url)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ScoreContainer_score-grid__zozAO"))
        )
        
        time.sleep(2)
        page_source = driver.page_source
        
    except Exception as e:

        if driver and ("404" in driver.title or "user not found" in driver.title.lower()):
            if driver: driver.quit() 
            return {"error": f"Could not fetch data: User '{username}' not found on GeeksforGeeks."}
        
        if driver: driver.quit()
        return {"error": f"Failed to load GFG page for '{username}'. The site may be protected or has changed."}
    
    finally:
        if driver:
            driver.quit()

    if not page_source:
         return {"error": "Could not retrieve page source from GFG after browser automation."}

    soup = BeautifulSoup(page_source, "html.parser")
    
    institution, rank, coding_score, problems_solved, contest_rating = "N/A", "N/A", "N/A", "0", "N/A"
    difficulty_counts = {label: "0" for label in ["school", "basic", "easy", "medium", "hard"]}

    score_grid = soup.find("div", class_="ScoreContainer_score-grid__zozAO")
    if score_grid:
        score_cards = score_grid.find_all("div", class_="ScoreContainer_score-card__zI4vG")
        for card in score_cards:
            label_element = card.find("p", class_="ScoreContainer_label__aVpLE")
            value_element = card.find("p", class_="ScoreContainer_value__7yy7h")
            if label_element and value_element:
                label_text = label_element.get_text(strip=True).lower()
                value_text = value_element.get_text(strip=True)
                if "coding score" in label_text: coding_score = value_text
                elif "problems solved" in label_text: problems_solved = value_text
                elif "institute rank" in label_text: rank = value_text
    
    inst_parent_container = soup.find("div", class_="Overview_content__kbu3G")
    if inst_parent_container:
        direct_children_divs = inst_parent_container.find_all("div", recursive=False)
        if len(direct_children_divs) > 1:
            classless_wrapper = direct_children_divs[1]
            container_div = classless_wrapper.find("div")
            if container_div and container_div.find("p"):
                institution = container_div.find("p").get_text(strip=True)

    difficulty_parent_container = soup.find("div", class_="ProblemNavbar_head__6ptDV")
    if difficulty_parent_container:
        difficulty_divs = difficulty_parent_container.find_all("div", class_="ProblemNavbar_head_nav__OqbEt")
        for diff_div in difficulty_divs:
            text_div = diff_div.find("div", class_="ProblemNavbar_head_nav--text__7u4wN")
            if text_div:
                full_text = text_div.get_text(strip=True).lower()
                count_match = re.search(r'\((\d+)\)', full_text)
                count = count_match.group(1) if count_match else "0"
                if "school" in full_text: difficulty_counts["school"] = count
                elif "basic" in full_text: difficulty_counts["basic"] = count
                elif "easy" in full_text: difficulty_counts["easy"] = count
                elif "medium" in full_text: difficulty_counts["medium"] = count
                elif "hard" in full_text: difficulty_counts["hard"] = count
    
    # Final check
    if rank == "N/A" and coding_score == "N/A" and problems_solved == "0" and institution == "N/A":
        return {"error": f"Could not fetch meaningful GFG profile data for '{username}'. The page structure has changed."}

    return {"username": username, "institution": institution, "rank": rank, "coding_score": coding_score, "problems_solved": problems_solved, "contest_rating": contest_rating, "difficulty_counts": difficulty_counts}

    
def fetch_hackerrank_data(username):
    url = f"https://www.hackerrank.com/{username}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return {"error": f"Failed to fetch data. Status code: {response.status_code}"}
        soup = BeautifulSoup(response.content, "html.parser")
        badges = []
        badges_section = soup.find("div", class_="badges-list")
        if badges_section:
            badge_divs = badges_section.find_all("div", class_="hacker-badge")
            for badge in badge_divs:
                title_tag = badge.find("text", class_="badge-title")
                title = title_tag.text.strip() if title_tag else "Unknown"
                level_div = badge.find("div", class_="ui-badge")
                level = "Unknown"
                if level_div:
                    for cls in level_div.get("class", []):
                        if cls.startswith("level-"):
                            level = cls.split("level-")[1].capitalize()
                star_section = badge.select_one("g.star-section > svg")
                stars = len(star_section.find_all("svg", class_="badge-star")) if star_section else 0
                badges.append({"title": title, "stars": stars, "level": level})
        certificates = []
        cert_section = soup.find("div", class_="hacker-certificates")
        if cert_section:
            cert_links = cert_section.find_all("a", class_=lambda c: c and "certificate-link" in c and "hacker-certificate" in c)
            for link in cert_links:
                heading = link.find("h2")
                if heading:
                    text = heading.get_text(separator=" ", strip=True).replace("Certificate:", "").strip()
                    if text:
                        certificates.append(text)
        return {"badges": badges, "certificates": certificates}
    except Exception as e:
        return {"error": str(e)}

def fetch_leetcode_data(username):
    url = "https://leetcode.com/graphql"
    query = """
    query userPublicProfile($username: String!) {
        matchedUser(username: $username) {
            username
            submitStats: submitStatsGlobal {
                acSubmissionNum {
                    difficulty
                    count
                    submissions
                }
            }
            profile {
                ranking
                reputation
            }
            languageProblemCount {
                languageName
                problemsSolved
            }
        }
    }
    """
    headers = {'Content-Type': 'application/json', 'Referer': f'https://leetcode.com/{username}', 'Origin': 'https://leetcode.com', 'User-Agent': 'Mozilla/5.0'}
    payload = {'query': query, 'variables': {'username': username}}
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code != 200:
            return {'error': 'Failed to fetch data from LeetCode'}
        data = response.json()
        user_data = data.get('data', {}).get('matchedUser')
        if not user_data:
            return {'error': 'User not found'}
        profile = user_data.get('profile', {})
        submit_stats = user_data.get('submitStats', {}).get('acSubmissionNum', [])
        difficulty = {}
        solved_total = 0
        for item in submit_stats:
            diff = item.get('difficulty', '').lower()
            count = item.get('count', 0)
            if diff in ['easy', 'medium', 'hard']:
                difficulty[diff] = count
                solved_total += count
        language_stats = {lang['languageName']: lang['problemsSolved'] for lang in user_data.get('languageProblemCount', []) if lang.get('problemsSolved', 0) > 0}
        rating = profile.get('reputation')
        rating = rating if rating and rating > 0 else 'N/A'
        return {'username': username, 'rating': rating, 'rank': profile.get('ranking', 'N/A'), 'solved': solved_total, 'difficulty': difficulty, 'languageStats': language_stats}
    except Exception as e:
        return {'error': str(e)}

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/fetch_profile_data', methods=['POST'])
def get_profile_data_route():
    data = request.get_json()
    platform = data.get('platform')
    username = data.get('username')
    if not platform or not username:
        return jsonify({"error": "Platform and username are required"}), 400
    result = {}
    if platform == 'codechef':
        result = fetch_codechef_data(username)
    elif platform == 'gfg':
        result = fetch_gfg_data(username)
    elif platform == 'hackerrank':
        result = fetch_hackerrank_data(username)
    elif platform == 'leetcode':
        result = fetch_leetcode_data(username)
    else:
        return jsonify({"error": "Invalid platform"}), 400
    return jsonify(result)

@app.route('/google12733681e865d7c2.html')
def google_verify():
    return send_from_directory(os.getcwd(), 'google12733681e865d7c2.html')

if __name__ == '__main__':
    app.run(debug=True)