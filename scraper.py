from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import quote


driver = uc.Chrome()

username = input("Enter Valorant username with tag (e.g., her dawg#W00f): ")

encoded_username = quote(username)

url = f"https://tracker.gg/valorant/profile/riot/{encoded_username}/overview"

driver.get(url)

try:
    # Wait for match rows to load
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.trn-match-row"))
    )

    # Grab the first match row (latest match)
    match = driver.find_element(By.CSS_SELECTOR, "div.trn-match-row")

    # Extract fields:

    agent = match.find_element(By.CSS_SELECTOR, "div.vmr-agent img").get_attribute("alt")
    map_name = match.find_element(By.CSS_SELECTOR, "div.vmr-metadata div.trn-match-row__text-value").text
    result_class = match.get_attribute("class")  # contains 'trn-match-row--outcome-loss' or '...-win'
    result = "Loss" if "trn-match-row--outcome-loss" in result_class else "Win"
    score = match.find_element(By.CSS_SELECTOR, "div.vmr-score .trn-match-row__text-value").text
    kda = match.find_element(By.XPATH, ".//div[.='K / D / A']/following-sibling::div").text
    kd_ratio = match.find_element(By.XPATH, ".//div[.='K/D']/following-sibling::div").text
    adr = match.find_element(By.XPATH, ".//div[.='ADR']/following-sibling::div").text
    acs = match.find_element(By.XPATH, ".//div[.='ACS']/following-sibling::div").text
    hs_percent = match.find_element(By.XPATH, ".//div[.='HS%']/following-sibling::div").text

    print(f"Agent: {agent}")
    print(f"Map: {map_name}")
    print(f"Result: {result}")
    print(f"Score: {score}")
    print(f"K/D/A: {kda}")
    print(f"K/D Ratio: {kd_ratio}")
    print(f"ADR: {adr}")
    print(f"ACS: {acs}")
    print(f"Headshot %: {hs_percent}")

    pass
finally:
    driver.quit()
    del driver