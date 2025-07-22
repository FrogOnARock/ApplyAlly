import time
import warnings

from google.adk.agents.llm_agent import Agent
from google.adk.tools.tool_context import ToolContext
from google.genai import types
import undetected_chromedriver as uc
from PIL import Image
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import asyncio
from ...shared_data import env_variables
from . import prompt

warnings.filterwarnings("ignore", category=UserWarning)

def login_page(tool_context: ToolContext) -> None:
    """
    Open a login page for the users to sign in to LinkedIn.
    Browser will be visible to the user to login and will exit one the user reaches the main feed page.
    Cookies are stored in the session state for use in the scraping tool.
    """

    visible_driver = uc.Chrome()
    visible_driver.get("https://www.linkedin.com/login")

    # Wait until user reaches LinkedIn homepage (/feed/)
    max_wait = 60  # max seconds to wait
    start = time.time()
    while True:
        current_url = visible_driver.current_url
        if "/feed" in current_url:
            print("Logged in successfully.")
            break
        if time.time() - start > max_wait:
            print("Timeout waiting for login.")
            visible_driver.quit()
            raise TimeoutError("Login not completed within 60 seconds.")
        time.sleep(2)

        # PROBABLY HAVE TO ADD THIS TO THE SESSION STATE
        cookies = visible_driver.get_cookies()
        tool_context.state["linkedin_cookies"] = cookies

    # Close the visible window
    visible_driver.quit()



def scrape_linkedin(tool_context: ToolContext) -> dict:
    """
    Scrapes a LinkedIn job URL. Extracts the job description via HTML parsing
    and takes a screenshot of the top-right for job title/company extraction.
    Stores job description text in 'linkedin_description' state and screenshot as 'job_title_company.png' artifact.
    """


    ### CALLBACK SOMEWHERE IN HERE TO DEAL WITH MISFORMATTED OR NON-EXISTENT LINKEDIN URLS???

    job_url_dict = tool_context.state.get("job_description_url", None)
    job_url = job_url_dict.get("LinkedinURL", None)
    print(job_url)

    # Start undetected Chrome
    options = uc.ChromeOptions()
    options.add_argument("--headless=new")  # 'new' headless mode in Chrome >= 109
    options.add_argument("--window-size=1920,1080")  # Ensures full rendering
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = uc.Chrome(options=options)

    # 2. Load LinkedIn homepage
    driver.get("https://www.linkedin.com")
    time.sleep(3)

    # 3. Inject cookies
    cookies = tool_context.state.get("linkedin_cookies", None)

    if cookies == None:
        raise RuntimeError("LinkedIn cookies not found. Please log in first.")

    for cookie in cookies:
        cookie.pop("sameSite", None)  # Avoid unsupported field
        driver.add_cookie(cookie)


    # Step 2: Navigate to the job
    driver.get(job_url)
    time.sleep(5)

    # Wait for the job description to load
    desc_elem = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, "job-details"))
    )
    description_text = desc_elem.text

    title_elem = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, "ember51"))
    )

    company_elem = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located(
            (By.CLASS_NAME, "job-details-jobs-unified-top-card__company-name")
        )
    )

    # Then grab the text from the <a> tag inside it
    company_name = company_elem.find_element(By.TAG_NAME, "a").text

    tool_context.state["linkedin_description"] = description_text
    tool_context.state["linkedin_title"] = title_elem.text
    tool_context.state["linkedin_company"] = company_name

    return {"status": "ok", "description": description_text}

search_agent = Agent(
        model=env_variables.GOOGLE_MODEL,
        name="search_agent",
        description="You will utilize the provided URL to scrape text of a LinkedIn job posting."
            "You will save both of these in your context.",
        instruction=prompt.SEARCH_AGENT_PROMPT,
        tools=[scrape_linkedin, login_page]
    )


