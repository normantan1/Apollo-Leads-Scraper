import re
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--user-data-dir")
chrome_options.add_argument("--allow-running-insecure-content")



user_data_dir = ''  # Update this path to where you want your files stored
chrome_options.add_argument(f"user-data-dir={user_data_dir}")

driver = webdriver.Chrome(options=chrome_options)
# rest of your script


driver.get("") # Insert Apollo link with your defined search parameters here

time.sleep(200) # Change this to 2 later after you have logged in to your Apollo account on browser

def find_email_address(page_source):
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.findall(email_pattern, page_source)

def filter_emails(emails, excluded_domain):
    filtered = [email for email in emails if not email.endswith(excluded_domain)]
    return filtered[:2]

def split_name(name):
    parts = name.split()
    first_name = parts[0] if parts else ''
    last_name = ' '.join(parts[1:]) if len(parts) > 1 else ''
    return first_name, last_name

counter = 0 # Number of leads scraped counter
while True:
    try:
        loaded_section_selector = "[data-cy-loaded='true']"
        loaded_section = driver.find_element(By.CSS_SELECTOR, loaded_section_selector)

        tbodies = loaded_section.find_elements(By.TAG_NAME, 'tbody')
        if not tbodies:
            break

        for tbody in tbodies:
            first_anchor_text = tbody.find_element(By.TAG_NAME, 'a').text
            first_name, last_name = split_name(first_anchor_text)

            linkedin_url = ''
            for link in tbody.find_elements(By.TAG_NAME, 'a'):
                href = link.get_attribute('href')
                if 'linkedin.com' in href:
                    linkedin_url = href
                    break

            job_title_element = tbody.find_element(By.CLASS_NAME, 'zp_Y6y8d')
            job_title = job_title_element.text if job_title_element else ''

            company_name = ''
            for link in tbody.find_elements(By.TAG_NAME, 'a'):
                if 'accounts' in link.get_attribute('href'):
                    company_name = link.text
                    break

            phone_number = tbody.find_elements(By.TAG_NAME, 'a')[-1].text

            button_classes = ["zp-button", "zp_zUY3r", "zp_hLUWg", "zp_n9QPr", "zp_B5hnZ", "zp_MCSwB", "zp_IYteB"]

            button_classes = ["zp-button", "zp_zUY3r", "zp_n9QPr", "zp_MCSwB"]

            
            try:
                button = tbody.find_element(By.CSS_SELECTOR, "." + ".".join(button_classes))
                button_text_div = button.find_element(By.CSS_SELECTOR, "div.zp_kxUTD")
                button_text = button_text_div.text
                if button and button_text != "Save Contact":
                    button.click()
                    wait = WebDriverWait(driver, 5)
                    element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "zp_t08Bv")))
    
                    email_addresses = find_email_address(driver.page_source)
                    filtered_emails = filter_emails(email_addresses, 'sentry.io')
                    with open('Sample.csv', 'a', newline='', encoding='utf-8') as file:  # Rename the csv file to the file you want to write to 
                        writer = csv.writer(file)
                        print(f"{first_name} has been scraped!")
                        if len(filtered_emails) == 1:
                            writer.writerow([first_name, last_name, job_title, company_name, filtered_emails[0], '', linkedin_url, phone_number])
                        elif len(filtered_emails) == 2:
                            writer.writerow([first_name, last_name, job_title, company_name, filtered_emails[0], filtered_emails[1], linkedin_url, phone_number])
                    # Example: Hiding the overlay using JavaScript
                    driver.execute_script("document.querySelector('.zp_CLq57').style.display = 'none';")

                    tbody_height = driver.execute_script("return arguments[0].offsetHeight;", tbody)
                    driver.execute_script("arguments[0].scrollBy(0, arguments[1]);", loaded_section, tbody_height)
                    counter+=1
                    if counter % 100 == 0: # Let script pause for 10 seconds for every 100 leads scraped to prevent getting flagged as bot
                        time.sleep(10)
                else:
                    tbody_height = driver.execute_script("return arguments[0].offsetHeight;", tbody)
                    driver.execute_script("arguments[0].scrollBy(0, arguments[1]);", loaded_section, tbody_height)
            except NoSuchElementException:
                print("No element found")
                continue

        # Pagination Logic
        next_button_selector = ".zp-button.zp_zUY3r.zp_MCSwB.zp_xCVC8[aria-label='right-arrow']"
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, next_button_selector)
            next_button.click()
            time.sleep(1)
        except NoSuchElementException:
            print("No more pages to navigate.")
            break

    except Exception as e:
        error_message = str(e)
        if "element click intercepted" in error_message:
            print("Your leads are ready!")
            break
        else:
            print(f"An error occurred: {error_message}")
            break

driver.quit()