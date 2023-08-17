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


# Open the login page
browser.get("https://ies2.fsv.cuni.cz/user")

# Find the username and password fields and enter the credentials
username_field = browser.find_element(By.XPATH, "//*[@id='edit-name']")
password_field = browser.find_element(By.XPATH, "//*[@id='edit-pass']")

# Enter the username and password
username_field.send_keys("30407792")
password_field.send_keys("AzaZ135619009!")

# Find and click the submit button
submit_button = browser.find_element(By.XPATH, "//*[@id='edit-submit']")
submit_button.click()


# Open the website and sign in manually
browser.get("https://ies.fsv.cuni.cz/cs/node/57")


while True:
    # Find all the publication links on the page
    publication_links = browser.find_elements(By.XPATH, "//a[contains(@href, '/sci/publication/show/id/')]")
    blocked = True

    for link in publication_links:
        print(link.get_attribute("href"))

        if link.get_attribute("href") == "https://ies.fsv.cuni.cz/sci/publication/show/id/6717/lang/cs":
            blocked = False

        if blocked: 
            continue
       
        link_href = link.get_attribute("href")
        print(f"Processing link: {link_href}")

        # Extract the node ID from the publication URL
        node_id = link_href.split('/sci/publication/show/id/')[-1].split('/')[0]
        
        print(f"Processing link: {link_href} (Node ID: {node_id})")
        
        # Generate the final URL based on the node ID
        final_url = f"/veda-vyzkum/working-papers/{node_id}"
        
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

                sanitized_file_name = sanitized_file_name + ".pdf"
                
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
        
        # Get the main content from the original page
        try:
            main_content_element = browser.find_element(By.XPATH, "/html/body/section[1]/div/div/div/table")
            main_content_html = main_content_element.get_attribute("outerHTML")

            header_title_element = browser.find_element(By.XPATH, "/html/body/section[1]/div/div/div/h3")
            header_title = header_title_element.text


        except Exception as e:
            print(f"Error extracting main content: {e}")
            main_content_html = "<p>Default content</p>"  # Provide a default content if extraction fails

            header_title = "Default title"
        
        # Close the current tab and switch back to the main tab
        browser.close()
        browser.switch_to.window(browser.window_handles[0])
        
        print("------------")
        

        # Open new page for data transfer
        new_page_url = "https://ies2.fsv.cuni.cz/node/add/basic_page"
        browser.execute_script("window.open('', '_blank');")
        browser.switch_to.window(browser.window_handles[-1])
        browser.get(new_page_url)


        title_input = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='edit-title-0-value']"))
        )
        title_input.clear()
        title_input.send_keys(header_title)

        # Click on the button to show the input area for the URL alias
        url_alias_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='edit-path-0']/summary"))
        )
        url_alias_button.click()


        # Find the checkbox element and toggle it off
        url_alias_checkbox = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='edit-path-0-pathauto']"))
        )
        # Check if the checkbox is already checked, and toggle it if needed
        if url_alias_checkbox.is_selected():
            url_alias_checkbox.click()

        # Set the URL alias
        url_alias_field = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.ID, "edit-path-0-alias"))
        )
        url_alias_field.clear()  # Clear any existing value
        url_alias_field.send_keys(final_url)



        # add_file_button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.ID, "cke_39")))
        # add_file_button.click()


        # Locate the file input field and send the path of the downloaded file
        file_input = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.NAME, "files[fid]")))
        # file_path = f"~/Downloads/{sanitized_file_name}"  # Update with the actual file path
        file_path = f"/Users/ivananikin/Downloads/{sanitized_file_name}"
        print("file_path")

        print(file_path)
        file_input.send_keys(file_path)

        # # Locate and click the "Upload" button
        # upload_button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div[3]/div/button")))
        # upload_button.click()


        # Switch to the content editor iframe
        content_iframe = WebDriverWait(browser, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//*[@id='cke_1_contents']/iframe"))
        )

        # Find the content editor element and get the content from the clipboard
        content_editor = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//body[@class='cke_editable cke_editable_themed cke_contents_ltr cke_show_borders']"))
        )

        # Clear the default content and paste the copied content from the clipboard
        content_editor.clear()
        browser.execute_script("arguments[0].innerHTML = arguments[1];", content_editor, main_content_html)

        # Switch back to the default content
        browser.switch_to.default_content()


        # Wait for the element to be present and interactable
        wait = WebDriverWait(browser, 10)  # Adjust the timeout as needed
        submit_button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.ID, "edit-submit")))
        
        print("final_url: ")
        print(final_url)
        print("header title:")
        print(header_title)
        print("main_content_html:")
        print(main_content_html)

        # Submit the form
        user_input = input("Press y to submit the content")
        
        if user_input.lower() == 'y':
            submit_button.click()
            print("submitted")
        else:
            print("skipping submit")
        
        # Close the current tab and switch back to the main tab
        browser.close()
        browser.switch_to.window(browser.window_handles[0])

    # Summarize or interact with the user
    user_input = input("Do you want to continue? (y/n): ")
    if user_input.lower() != 'y':
        break

# Close the browser when done
browser.quit()