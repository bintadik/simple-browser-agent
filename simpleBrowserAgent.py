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
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

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
    for i in range(0, 10):
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
    make sure to use the exact same element names as in the page source.
    do action with the exact same element you find in the page source.
    Suggest exactly ONE Selenium Python command to do next (e.g., click a button, fill a form).
    Respond ONLY with Python code.
    """


    client = genai.Client()
    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents = prompt1
        )
    print(response.text)

    action = response.text.strip()

    # prompt2 = f"""
    # You are a browser agent.
    # Your task:
    # {task_description}
    # This is the element list: 
    # {action}
    # using this element.
    # Suggest exactly ONE Selenium Python command to do next (e.g., click a button, fill a form).
    # Respond ONLY with Python code.
    # """

    # response = client.models.generate_content(
    #     model="gemini-2.5-flash", 
    #     contents = prompt2
    #     )
    # print(response.text)
    # model = response.text.strip()

    # action = response.text.strip()

    print("\n=== Gemini suggested action ===")
    print(action[9:-3])

    # ----------------------------
    # Run the suggested ACTION
    # ----------------------------
    print("\n=== Executing action ===")
    # for i in range(0, 10):
    try:
        exec(action[9:-3])
        time.sleep(1)
    except Exception as e:
        print(f"Error executing action: {e}")
    time.sleep(1)

# ----------------------------
# Close browser
# ----------------------------
looping = 0
while looping < 30:
    action()
    looping += 1
driver.quit()
