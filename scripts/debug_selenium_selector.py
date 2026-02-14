from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

URL = "https://www.apec.fr/candidat/recherche-emploi.html/emploi/detail-offre/178077294W"

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--window-size=1920,1080')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    print(f"Loading {URL} ...")
    driver.get(URL)
    
    # Wait for body
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(5) # Give JS time to render content
    
    print("Page Title:", driver.title)
    
    # Try multiple selectors
    selectors = [
        "div.row.border-light.offer-content", 
        "div.col-lg-8.border-light",
        "div.container-fluid.details-offer",
        "p.text-content",
        "div.card-body", 
        "main"
    ]
    
    found_any = False
    for sel in selectors:
        try:
            els = driver.find_elements(By.CSS_SELECTOR, sel)
            print(f"\nSelector '{sel}' found {len(els)} elements.")
            for i, el in enumerate(els):
                txt = el.text
                if len(txt) > 200:
                    print(f"  [Element {i}] Length: {len(txt)}")
                    print(f"  Start: {txt[:100]}...")
                    found_any = True
        except Exception as e:
            print(f"  Error with {sel}: {e}")
            
    if not found_any:
        print("\nFallback: BODY text length:", len(driver.find_element(By.TAG_NAME, "body").text))

finally:
    driver.quit()
