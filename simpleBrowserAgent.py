import os
import configparser
import dotenv

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By 
from bs4 import BeautifulSoup
import time
from google import genai
from selenium.webdriver.chrome.options import Options


# ----------------------------
# Load ENV
# ----------------------------
dotenv.load_dotenv()

# ----------------------------
# Load CONFIG
# ----------------------------
config = configparser.ConfigParser()
config.read('.config')

print(config)
url = config['default']['first_url']
task_description = config['default']['task_description']
other_information = config['default']['other_information']


# ----------------------------
# Setup SELENIUM
# ----------------------------
options = Options()
options.add_argument("--log-level=3")  # Menyembunyikan log error
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)

# ----------------------------
# Open URL
# ----------------------------
print(f"Opening URL: {url}")
driver.get(url)
time.sleep(15)
# ----------------------------
# Get Page Source
# ----------------------------
def action():
    prev_action = ""
    for i in range(0, 3):
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        time.sleep(1)

    # ----------------------------
    # Use GEMINI to get next ACTION
    # ----------------------------

    prompt1 = f"""
    You are a browser agent.
    Your task:
    {task_description}
    Other information:
    {other_information}
    This is the page HTML right now: 
    {soup}
    only use elements from the page source above.
    List the elements you want to use in the next Selenium Python command.
    Double check that the elements are correct.
    Make sure to use the exact same element names as in the page source.
    Do action with the exact same element you find in the page source.
    i have import this: 
    from selenium.webdriver.common.by import By
    Suggest exactly ONE Selenium Python command to do next(e.g., click a button, fill a form).
    Respond ONLY with Python code.
    IF YOU THINK YOU HAVE FINISHED AND NOTHING TO DO, PRINT "***FINISHED***" AND INFORM WHERE YOU ARE NOW.
    PRINT "***INFORMATION***"  AND THE INFORMATION NEEDED FOR USERS TO COMPLETE ACTION IF YOU THINK THIS ACTION NEED USER ACTION NOT YOURS (e.g. verification code etc).
    {prev_action}
    """


    client = genai.Client()

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents = prompt1
            )
        print(response.text)
        action = response.text.strip()
    except Exception as e:
        action = "FAILED TO FETCH ACTION"
        print(f"Error executing action: {e}")
        time.sleep(15) # Sleep for 15 seconds before trying again, Refill free credits.


    print("\n=== Gemini suggested action ===")
    print(action)
    if action.__contains__("python"):
        actionable = action[9:-3]
    else:
        actionable = action
    # ----------------------------
    # Run the suggested ACTION
    # ----------------------------
    print("\n=== Executing action ===")
    if action.__contains__("***INFORMATION***"):
        print(response.text)
    elif action.__contains__("***FINISHED***"):
        print(f"Action completed")
        break
    else:
    # for i in range(0, 10):
        try:
            exec(actionable)
            prev_action =""
            time.sleep(1)
        except Exception as e:
            prev_action = f"Your previous action is : {actionable} and it  is failed" 
            print(f"Error executing action: {e}")
        time.sleep(15)

# ----------------------------
# Close browser
# ----------------------------
looping = 0
while looping < 30:
    action()
    looping += 1
driver.quit()
