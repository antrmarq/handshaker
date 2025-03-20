from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def start_up(driver, username, password, query, num_results=50):
    # Go to search URL (will redirect for auth)
    job_query = query.replace(" ", "%20")
    driver.get(f"https://byu.joinhandshake.com/postings?page=1&per_page={num_results}&job.salary_types%5B%5D=1&sort_direction=desc&sort_column=default&query={job_query}&employment_type_names%5B%5D=Full-Time")

    # Handle login
    byu_login_btn = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "sso-button"))
    )
    byu_login_btn.click()

    # Wait for the username and password fields to be visible
    username_input = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.ID, "username"))
    )
    username_input.send_keys(username)

    password_input = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.ID, "password"))
    )
    password_input.send_keys(password)

    password_input.send_keys(Keys.ENTER)  # Submit login

    # Wait for DUO authentication and other redirects
    sleep(10)

    try:
        # Wait for the trust-browser-button to be visible
        trust_browser_btn = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.ID, "trust-browser-button"))
        )
        trust_browser_btn.click()
    except Exception as e:
        print("Error: Trust browser button not found or not clickable")
        print(f"Exception: {str(e)}")
        return False

    sleep(10)

    # Check if we are on the explore page
    current_url = driver.current_url
    if "explore" in current_url:  # If we're on the explore page
        print("Redirecting to job postings page...")
        # Manually navigate to the job postings page
        driver.get(f"https://byu.joinhandshake.com/postings?page=1&per_page={num_results}&sort_direction=desc&sort_column=default&query={job_query}&job.salary_types%5B%5D=1&employment_type_names%5B%5D=Full-Time&job.job_types%5B%5D=9")
        sleep(5)  # Wait for the page to load

    return True


def apply_to_jobs(driver, non_quick_apply_urls, resume):
    # Wait for postings section to be visible on the job search page
    try:
        postings_section = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//a[@data-hook='jobs-card']"))
        )
        print("Job postings found!")
    except Exception as e:
        print("Error: Job postings not found.")
        print(f"Exception: {str(e)}")
        driver.quit()
        return

    # Find all job postings on the current page
    postings = driver.find_elements(By.XPATH, "//a[@data-hook='jobs-card']")
    print(f"Finding postings on the current page...")

    for posting in postings:
        # Ensure that the overlay is invisible
        WebDriverWait(driver, 20).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "style__overlay___2uoRf"))
        )

        # Scroll into view if necessary
        driver.execute_script("arguments[0].scrollIntoView(true);", posting)
        sleep(1)

        try:
            # Try clicking the posting
            posting.click()
            sleep(2)
        except Exception as e:
            print("Apply button not found or not clickable, skipping.")
            print(f"Exception: {str(e)}")
            continue

        # Check for the 'Apply' button using its aria-label
        try:
            apply_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Apply"]'))
            )
            apply_btn.click()
            sleep(2)
        except Exception as e:
            print("Apply button not found or not clickable, skipping.")
            # Save the job URL for manual review
            job_url = driver.current_url
            non_quick_apply_urls.append(job_url)
            print(f"Saved for review: {job_url}")
            continue

        # Look for the 'Submit Application' button
        submit_btn_results = driver.find_elements(By.XPATH, '//button[@data-hook="button"]//span[text()="Submit Application"]')

        if len(submit_btn_results) > 0:
            submit_btn = submit_btn_results[0]
            submit_btn.click()
            sleep(2)

            # Look for the modal content
            apply_modal = driver.find_elements(By.XPATH, '//span[@data-hook="apply-modal-content"]')

            if len(apply_modal) > 0:  # If the modal is still visible, it means it hasn't closed
                try:
                    # Check for the resume button
                    resume_btn = driver.find_elements(By.XPATH, f'//button[@aria-label="{resume}"]')

                    if len(resume_btn) > 0:
                        resume_btn[0].click()  # Click the resume button
                        print("Clicked resume button to submit application.")

                        # Try submitting the application again
                        submit_btn_results = driver.find_elements(By.XPATH, '//button[@data-hook="button"]//span[text()="Submit Application"]')
                        if len(submit_btn_results) > 0:
                            submit_btn = submit_btn_results[0]
                            submit_btn.click()  # Click the submit button
                            # if modal is still visible, it means the submit button didn't work, so dismiss the modal
                            sleep(2)
                            apply_modal = driver.find_elements(By.XPATH, '//span[@data-hook="apply-modal-content"]')
                            if len(apply_modal) > 0:
                                try:
                                    dismiss_btn = WebDriverWait(driver, 10).until(
                                        EC.element_to_be_clickable((By.CLASS_NAME, "style__dismiss___Zotdc"))
                                    )
                                    dismiss_btn.click()
                                    print("Dismissed the popup after trying to submit again.")
                                except Exception as e:
                                    print("Dismiss button not found, continuing.")
                                # Save the job URL for manual review
                                job_url = driver.current_url
                                non_quick_apply_urls.append(job_url)
                                print(f"Submit failed after resume, saved for review: {job_url}")
                                continue
                            print(f"Successfully applied: {driver.current_url}")
                        else:
                            # If the submit button isn't available even after clicking resume, dismiss the modal
                            try:
                                dismiss_btn = WebDriverWait(driver, 10).until(
                                    EC.element_to_be_clickable((By.CLASS_NAME, "style__dismiss___Zotdc"))
                                )
                                dismiss_btn.click()
                                print("Dismissed the popup after trying to submit again.")
                            except Exception as e:
                                print("Dismiss button not found, continuing.")
                            # Save the job URL for manual review
                            job_url = driver.current_url
                            non_quick_apply_urls.append(job_url)
                            print(f"Submit failed after resume, saved for review: {job_url}")
                            continue  # Skip to the next posting

                    else:
                        # If no resume button is found, dismiss the modal and save the job for manual review
                        try:
                            dismiss_btn = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.CLASS_NAME, "style__dismiss___Zotdc"))
                            )
                            dismiss_btn.click()
                            print("Dismissed the popup due to no resume button.")
                        except Exception as e:
                            print("Dismiss button not found, continuing.")

                        # Save the job URL for manual review
                        job_url = driver.current_url
                        non_quick_apply_urls.append(job_url)
                        print(f"Submit disabled or modal not closed, saved for review: {job_url}")
                        continue  # Skip to the next posting

                except Exception as e:
                    print(f"Error processing modal: {str(e)}")
                    # In case of error, dismiss the modal and save for manual review
                    try:
                        dismiss_btn = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.CLASS_NAME, "style__dismiss___Zotdc"))
                        )
                        dismiss_btn.click()
                        print("Dismissed the popup due to error.")
                    except Exception as dismiss_error:
                        print("Dismiss button not found, continuing.")

                    # Save the job URL for manual review
                    job_url = driver.current_url
                    non_quick_apply_urls.append(job_url)
                    print(f"Error encountered, saved for review: {job_url}")
                    continue  # Skip to the next posting

            else:
                # If the modal closed, proceed to print success
                print(f"Successfully applied: {driver.current_url}")

            # Check if the 'You applied on' banner is visible
            applied_banner = driver.find_elements(By.XPATH, "//h2[text()='You applied on']")
            if len(applied_banner) > 0:
                print(f"Already applied to: {driver.current_url}. Skipping.")
                continue  # Skip to next posting if already applied

            sleep(2)
