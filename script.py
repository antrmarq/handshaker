import os
import argparse
import json
import signal
import sys
from dotenv import load_dotenv  # Import the dotenv package
from time import sleep  # Import sleep function
from selenium import webdriver
from selenium.webdriver.chrome.options import Options  # Ensure this import is here
from selenium.webdriver.support.ui import WebDriverWait  # Import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC  # Import EC
from selenium.webdriver.common.by import By  # Import By for locating elements
from bot import start_up, apply_to_jobs
import json  # <-- Make sure this line is included

# Initialize a list to store non-Quick Apply URLs for later review
non_quick_apply_urls = []

# Load environment variables from the .env file
load_dotenv()

# Set up argument parser
parser = argparse.ArgumentParser()
parser.add_argument(
    "-q", "--query", type=str, help="Job search query", required=True
)
parser.add_argument(
    "--headless",
    action="store_true",
    default=False,
    help="Run headless (runs with head by default)",
)
args = parser.parse_args()

# Get username and password from environment variables
username = os.getenv("BYU_USERNAME")
password = os.getenv("BYU_PASSWORD")
resume = os.getenv("RESUME_NAME")

# Check if username and password are set
if not username or not password or not resume:
    print("Error: Username and password and resume must be provided in the .env file.")
    exit(1)

# Handle cleanup on interrupt
def cleanup_and_exit(signal, frame):
    print("\nProcess interrupted. Saving results...")
    print(f"Non-Quick Apply URLs found: {len(non_quick_apply_urls)}")
    with open("non_quick_apply_urls.json", "w") as json_file:
        json.dump(non_quick_apply_urls, json_file, indent=4)
    print("Results saved to non_quick_apply_urls.json")
    sys.exit(0)

# Register the signal handler for keyboard interrupt (Ctrl + C)
signal.signal(signal.SIGINT, cleanup_and_exit)

# Initialize web driver
chrome_options = Options()
if args.headless:
    chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()

# Perform the startup process (login and initial page load)
if start_up(driver, username, password, args.query):
    # Apply to jobs on the first page and handle pagination
    while True:
        # Apply to jobs on the current page
        apply_to_jobs(driver, non_quick_apply_urls, resume)

        # Check for next page once all postings on the current page are processed
        def go_to_next_page():
            try:
                next_page_btn = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[@data-hook="search-pagination-next"]'))
                )
                next_page_btn.click()
                print("Moving to the next page...")
                sleep(10)  # Give time for the next page to load
                return True  # Return True if next page is successfully loaded
            except Exception as e:
                print("No next page or error in clicking next page.")
                print(f"Exception: {str(e)}")
                return False  # Return False if there is no next page

        # Call function to go to the next page
        if go_to_next_page():
            # Once next page is loaded, apply to jobs on this page as well
            apply_to_jobs(driver, non_quick_apply_urls, resume)
        else:
            # break the loop if there is no next page
            break

# Close the driver after processing all pages
driver.quit()

# Save non-Quick Apply URLs to a JSON file after processing all pages
with open("non_quick_apply_urls.json", "w") as json_file:
    json.dump(non_quick_apply_urls, json_file, indent=4)

print(f"Saved {len(non_quick_apply_urls)} non-Quick Apply job URLs to 'non_quick_apply_urls.json'.")
