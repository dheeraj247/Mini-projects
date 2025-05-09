from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
import re
def fetch_codechef_data(username):
    url = f"https://www.codechef.com/users/{username}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            return {"error": f"Failed to fetch data. Status code: {response.status_code}"}

        soup = BeautifulSoup(response.content, "html.parser")

        # Rating
        rating_div = soup.find("div", class_="rating-number")
        rating = rating_div.text.strip() if rating_div else "No rating available"

        # Solved problems
        solved_problems = "Not found"
        user_details_div = soup.find("div", class_="user-details-container")
        if user_details_div:
            h3_tags = user_details_div.find_all("h3")
        if h3_tags:
            last_h3 = h3_tags[-1]
            match = re.search(r'\d+', last_h3.text)
            if match:
                solved_problems = int(match.group())

        # Global and Country Rank
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
                    if global_tag:
                        global_rank = global_tag.text.strip()
                    if country_tag:
                        country_rank = country_tag.text.strip()

        # Rating header info: stars, division, highest rating
        stars = "Not available"
        division = "Not available"
        highest_rating = "Not available"
        rating_header = soup.find("div", class_="rating-header")
        if rating_header:
            # Stars
            star_div = rating_header.find("div", class_="rating-star")
            if star_div:
                stars = star_div.text.strip()

            # Division — second div without class
            all_divs = rating_header.find_all("div", recursive=False)
            if len(all_divs) >= 2:
                div_text = all_divs[1].text.strip()
                if "Div" in div_text:
                    division = div_text

            # Highest rating — in <small>
            small_tag = rating_header.find("small")
            if small_tag:
                match = re.search(r'\d+', small_tag.text)
                if match:
                    highest_rating = int(match.group())


        return {
            "username": username,
            "rating": rating,
            "global_rank": global_rank,
            "country_rank": country_rank,
            "solved_problems": solved_problems,
            "stars": stars,
            "division": division,
            "highest_rating": highest_rating
        }

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return {"error": f"An error occurred: {str(e)}"}


def extract_number(text):
    match = re.search(r'\((\d+)\)', text)
    return match.group(1) if match else "0"

def fetch_gfg_data(username):
    url = f"https://www.geeksforgeeks.org/user/{username}/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            return {"error": f"Failed to fetch data. Status code: {response.status_code}"}

        soup = BeautifulSoup(response.content, "html.parser")

        # Institution
        inst_div = soup.find("div", class_="educationDetails_head_left--text__tgi9I")
        institution = inst_div.text.strip() if inst_div else "N/A"

        # Rank
        rank_span = soup.select_one(
            "div.educationDetails_head_left_userRankContainer__tyT6H a span.educationDetails_head_left_userRankContainer--text__wt81s b"
        )
        rank = rank_span.text.strip().replace(" Rank", "") if rank_span else "N/A"

        # Coding Score, Problems Solved, Contest Rating
        scoreCard_div = soup.find("div", class_="scoreCards_head__G_uNQ")
        score_divs = scoreCard_div.find_all("div", class_="scoreCard_head_left--score__oSi_x") if scoreCard_div else []

        coding_score = score_divs[0].text.strip() if len(score_divs) > 0 else "N/A"
        problems_solved = score_divs[1].text.strip() if len(score_divs) > 2 else "N/A"
        contest_rating = score_divs[2].text.strip() if len(score_divs) > 2 else "N/A"

        # Difficulty Counts
        difficulty_tags = soup.find_all("div", class_="problemNavbar_head_nav--text__UaGCx")
        difficulty_counts = {}

        labels = ["school", "basic", "easy", "medium", "hard"]
        for label, tag in zip(labels, difficulty_tags):
            difficulty_counts[label] = extract_number(tag.text.strip())

        return {
            "institution": institution,
            "rank": rank,
            "coding_score": coding_score,
            "problems_solved": problems_solved,
            "contest_rating": contest_rating,
            "difficulty_counts": difficulty_counts
        }

    except Exception as e:
        print(f"An error occurred: {e}")
        return {"error": str(e)}
data=fetch_gfg_data("deekshithk4fb")
print(data)
def fetch_hackerrank_data(username):
    url = f"https://www.hackerrank.com/{username}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

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

                # Determine badge level from class
                level_div = badge.find("div", class_="ui-badge")
                level = "Unknown"
                if level_div:
                    for cls in level_div.get("class", []):
                        if cls.startswith("level-"):
                            level = cls.split("level-")[1].capitalize()

                # Count stars
                star_section = badge.select_one("g.star-section > svg")
                stars = len(star_section.find_all("svg", class_="badge-star")) if star_section else 0

                badges.append({
                    "title": title,
                    "stars": stars,
                    "level": level
                })

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
        return {
            "badges": badges,
            "certificates": certificates
        }

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

    headers = {
        'Content-Type': 'application/json',
        'Referer': f'https://leetcode.com/{username}',
        'Origin': 'https://leetcode.com',
        'User-Agent': 'Mozilla/5.0'
    }

    payload = {
        'query': query,
        'variables': {'username': username}
    }

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

        language_stats = {
            lang['languageName']: lang['problemsSolved']
            for lang in user_data.get('languageProblemCount', [])
            if lang.get('problemsSolved', 0) > 0
        }

        rating = profile.get('reputation')
        rating = rating if rating and rating > 0 else 'N/A'

        return {
            'username': username,
            'rating': rating,
            'rank': profile.get('ranking', 'N/A'),
            'solved': solved_total,
            'difficulty': difficulty,
            'languageStats': language_stats
        }

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

if __name__ == '__main__':
    app.run(debug=True)