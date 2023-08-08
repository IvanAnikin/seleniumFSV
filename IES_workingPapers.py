from selenium import webdriver
from selenium.webdriver.common.by import By

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
            link_text = link.text
            link_href = link.get_attribute("href")
            print(f"Processing link: {link_text}")
            print(f"Link URL: {link_href}")
            
            # Open the link in a new tab
            browser.execute_script("window.open('', '_blank');")
            browser.switch_to.window(browser.window_handles[-1])
            browser.get(link_href)
            
            # Allow you to manually interact with the opened page
            input("Press Enter to continue...")
            
            # Close the current tab and switch back to the main tab
            browser.close()
            browser.switch_to.window(browser.window_handles[0])
            
            print("------------")
            
        # Summarize or interact with the user
        user_input = input("Do you want to continue? (y/n): ")
        if user_input.lower() != 'y':
            break

# Close the browser when done
browser.quit()