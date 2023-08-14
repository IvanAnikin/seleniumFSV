import os
import requests
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def sanitize_filename(filename):
    # Replace characters that are not suitable for filenames
    sanitized_filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    return sanitized_filename

# Initialize the browser
browser = webdriver.Chrome()  # Use the appropriate driver

# Open the website and sign in manually
browser.get("https://ies.fsv.cuni.cz/cs/node/57")
user_input = input("Press Enter after signing in...")

if user_input.lower() != 'y':
    print("uh")
else:
    while True:
        # Find all the publication links on the page
        publication_links = browser.find_elements(By.XPATH, "//a[contains(@href, '/sci/publication/show/id/')]")
        
        for link in publication_links:
            link_href = link.get_attribute("href")
            print(f"Processing link: {link_href}")
            
            # Open the link in a new tab
            browser.execute_script("window.open('', '_blank');")
            browser.switch_to.window(browser.window_handles[-1])
            browser.get(link_href)
            
            # Check if the link for downloading the file is present
            try:
                download_link = browser.find_element(By.XPATH, "//a[contains(@href, '/default/file/download/')]")
                file_name = download_link.text
                file_url = download_link.get_attribute("href")
                
                # Download the file
                response = requests.get(file_url)
                if response.status_code == 200:
                    # Sanitize the filename
                    sanitized_file_name = sanitize_filename(file_name)
                    
                    # Save the file to the Downloads folder
                    downloads_folder = os.path.expanduser("~/Downloads")
                    file_path = os.path.join(downloads_folder, sanitized_file_name)
                    with open(file_path, "wb") as f:
                        f.write(response.content)
                    
                    print(f"File '{sanitized_file_name}' downloaded to '{downloads_folder}'")
                else:
                    print(f"Failed to download the file '{file_name}'")
            except Exception as e:
                print(f"Error downloading file: {e}")
            
            # Close the current tab and switch back to the main tab
            browser.close()
            browser.switch_to.window(browser.window_handles[0])
            
            print("------------")
            
            # Open new page for data transfer
            new_page_url = "https://ies2.fsv.cuni.cz/node/add/basic_page"
            browser.execute_script("window.open('', '_blank');")
            browser.switch_to.window(browser.window_handles[-1])
            browser.get(new_page_url)
            
            # Wait for the user input before proceeding
            input("Press Enter after filling in content...")
            
            # Set the URL alias
            url_alias_field = WebDriverWait(browser, 10).until(
                EC.visibility_of_element_located((By.ID, "edit-path-0-domain-path-ies-fsv-cuni-cz-path"))
            )
            url_alias_value = f"https://ies2.fsv.cuni.cz/veda-vyzkum/working-papers/{sanitized_file_name}"
            url_alias_field.clear()  # Clear any existing value
            url_alias_field.send_keys(url_alias_value)
            print(url_alias_value)
            print("could be")
            url_alias_value2 = f"/veda-vyzkum/working-papers/{sanitized_file_name}"
            print(url_alias_value2)
            
            # Wait for the element to be present and interactable
            wait = WebDriverWait(browser, 10)  # Adjust the timeout as needed
            submit_button = wait.until(EC.element_to_be_clickable((By.ID, "edit-submit")))
            
            # Submit the form
            submit_button.click()
            
            # Close the current tab and switch back to the main tab
            browser.close()
            browser.switch_to.window(browser.window_handles[0])

        # Summarize or interact with the user
        user_input = input("Do you want to continue? (y/n): ")
        if user_input.lower() != 'y':
            break

# Close the browser when done
browser.quit()
