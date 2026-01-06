import json
import time
from app import fetch_gfg_data # This imports your function from your Flask app file

def test_single_user(username):
    """Fetches and prints data for a single GFG user."""
    print(f"\n{'='*20} TESTING USER: {username} {'='*20}")
    try:
        data = fetch_gfg_data(username)

        if data.get("error"):
            print(f"!!! ERROR returned for {username}: {data['error']}")
        else:
            # Pretty-print the returned dictionary using json.dumps for nice formatting
            print(json.dumps(data, indent=4))
            print(f"--- Test for {username} complete ---")

    except Exception as e:
        print(f"!!! CRITICAL ERROR during fetch for {username}: {e}")
        import traceback
        traceback.print_exc()

# The main part of the script that runs when you execute `python test_gfg_scraper.py`
if __name__ == "__main__":
    # --- List of GFG usernames to test ---
    # It's good to have a few different types of profiles
    test_usernames = [
        "dheerajsirzf2m",  # Your profile
        "geeksforgeeks",   # An official/active profile
        "sahoosourav",     # Just another example user, find one with visible stats
        "nonexistentuser123456789xyz" # A username that definitely does not exist
    ]

    # Loop through each username and test it
    for user in test_usernames:
        test_single_user(user)
        # Add a small delay between requests to be respectful to GFG's servers
        time.sleep(2)