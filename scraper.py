# scraper.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import quote

def get_valorant_stats(username):
    encoded_username = quote(username)
    url = f"https://tracker.gg/valorant/profile/riot/{encoded_username}/overview"

    options = Options()
    options.headless = True
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
   
    # On Render the paths are usually:
    options.binary_location = "/usr/bin/chromium"
    driver_path = "/usr/bin/chromedriver"

    driver = webdriver.Chrome(executable_path=driver_path, options=options)

    try:
        driver.get(url)

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.trn-match-row"))
        )

        match = driver.find_element(By.CSS_SELECTOR, "div.trn-match-row")
        agent = match.find_element(By.CSS_SELECTOR, "div.vmr-agent img").get_attribute("alt")
        map_name = match.find_element(By.CSS_SELECTOR, "div.vmr-metadata div.trn-match-row__text-value").text
        result_class = match.get_attribute("class")
        result = "Loss" if "trn-match-row--outcome-loss" in result_class else "Win"
        score = match.find_element(By.CSS_SELECTOR, "div.vmr-score .trn-match-row__text-value").text
        kda = match.find_element(By.XPATH, ".//div[.='K / D / A']/following-sibling::div").text
        kd_ratio = match.find_element(By.XPATH, ".//div[.='K/D']/following-sibling::div").text
        adr = match.find_element(By.XPATH, ".//div[.='ADR']/following-sibling::div").text
        acs = match.find_element(By.XPATH, ".//div[.='ACS']/following-sibling::div").text
        hs_percent = match.find_element(By.XPATH, ".//div[.='HS%']/following-sibling::div").text

        return {
            "agent": agent,
            "map": map_name,
            "result": result,
            "score": score,
            "kda": kda,
            "kd_ratio": kd_ratio,
            "adr": adr,
            "acs": acs,
            "hs_percent": hs_percent
        }

    finally:
        driver.quit()
