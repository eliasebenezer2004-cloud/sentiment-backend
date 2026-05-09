from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from textblob import TextBlob
import time

def get_sentiment(text):
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0: return "Positive"
    elif polarity < 0: return "Negative"
    else: return "Neutral"

def scrape_reviews(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless') # Runs in the background
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    driver.get(url)
    time.sleep(3) # Wait for page to load
    
    reviews_data = []
    try:
        # Generic locator for Amazon reviews
        elements = driver.find_elements(By.CSS_SELECTOR, "span[data-hook='review-body']")
        for el in elements:
            text = el.text.strip()
            if text:
                reviews_data.append({
                    "review": text,
                    "sentiment": get_sentiment(text)
                })
    except Exception as e:
        print("Error scraping:", e)
    finally:
        driver.quit()
        
    return reviews_data