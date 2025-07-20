import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import json


# 1. Launch visible Chrome
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
        print("❌ Timeout waiting for login.")
        visible_driver.quit()
        raise TimeoutError("Login not completed within 60 seconds.")
    time.sleep(2)

# Save cookies after login
cookies = visible_driver.get_cookies()
with open("linkedin_cookies.json", "w") as f:
    json.dump(cookies, f)
print("Cookies saved.")

# Close the visible window
visible_driver.quit()

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
with open("linkedin_cookies.json") as f:
    cookies = json.load(f)

for cookie in cookies:
    cookie.pop("sameSite", None)  # Avoid unsupported field
    driver.add_cookie(cookie)


# Step 2: Navigate to the job
job_url = "https://www.linkedin.com/jobs/collections/recommended/?currentJobId=4240406175"
driver.get(job_url)
time.sleep(5)

# Create folder for screenshots
os.makedirs("job_screenshots", exist_ok=True)

# Wait for right-side job description container

driver.save_screenshot("job_title.png")
time.sleep(2)

# Wait for the job description to load
desc_elem = WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.ID, "job-details"))
)
description_text = desc_elem.text


import json
with open("job_description.json", "w", encoding="utf-8") as f:
    json.dump({"url": job_url, "description": description_text}, f, ensure_ascii=False, indent=2)


driver.quit()
