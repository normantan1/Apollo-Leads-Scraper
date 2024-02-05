# Apollo Leads Scraper

## Overview
**This Python script automates the process of scraping lead information from Apollo.** It utilizes Selenium for web automation and operates by navigating through Apollo's interface to extract details such as names, job titles, company names, email addresses, and phone numbers.

## Features
- **Scrapes lead data from Apollo** using Selenium.
- **Filters and captures email addresses.**
- **Extracts additional lead details** like job title, company name, LinkedIn URL, and phone number.
- **Handles pagination** to navigate through multiple pages of leads.
- **Incorporates a counter** to manage scraping sessions and prevent bot detection.
- **Saves the scraped data in a CSV file.**

## Prerequisites
- **Python 3.x**
- **Selenium**
- **Chrome WebDriver**
- **A valid Apollo account**

## Setup and Installation
1. **Ensure Python 3.x is installed on your system.**
2. **Install Selenium using pip:**
3. **Download and set up the Chrome WebDriver.**
4. **Update the `user_data_dir` variable** in the script with the path to your Chrome user data directory.

## Usage
1. **Set the desired Apollo URL with search parameters** in the script.
2. **Run the script using Python:**
3. **The script will start scraping data** based on the defined parameters.

## Important Notes
- The script includes a `time.sleep(200)` delay for the initial login. **This should be reduced to 2 seconds after logging into your Apollo account.**
- The script uses **explicit waits** to handle dynamic content loading.
- A **sample CSV file will be generated** to store the scraped data. Ensure to rename the file as required in the script.

## Limitations
- The script is **tailored to the specific structure of Apollo's web pages**; any changes in their layout may require updates to the script.
- **Excessive usage might flag your account** for bot-like activity; hence, it uses a pause mechanism after every 100 leads.

## Disclaimer
**This script is provided for educational purposes only.** Using automated scripts for scraping can violate the terms of service of the website. Please use this responsibly and ethically.

