from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Initialize the browser
browser = webdriver.Chrome()  # Use the appropriate driver

# Open the website and sign in manually
browser.get("https://ies.fsv.cuni.cz/cs/node/57")
user_input = input("Press Enter after signing in...")

if user_input.lower() != 'y':
    print("uh")
else:
    while True:
        # Find all the links within the specified element
        link_elements = browser.find_elements(By.XPATH, "//div[@class='col-sm-12']/p/a")
        
        # Process each link
        for link_element in link_elements:
            link_text = link_element.text
            link_href = link_element.get_attribute("href")
            
            print("Processing link:", link_text)
            print("Link URL:", link_href)
            
            # You can use link_href to navigate to the link and perform scraping and processing
            
            # Pause briefly to avoid overloading the website
            time.sleep(1)
        
        # Summarize or interact with the user
        user_input = input("Do you want to continue? (y/n): ")
        if user_input.lower() != 'y':
            break

# Close the browser when done
browser.quit()