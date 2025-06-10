from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def search_flights(origin, destination, date=None):
    # Headless browser
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        url = "https://www.kiwi.com/en/"
        driver.get(url)

        wait = WebDriverWait(driver, 20)

        # Close cookie popup
        try:
            cookie_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Accept all')]")))
            cookie_button.click()
        except:
            pass  # Might not appear every time

        # Click and type origin
        from_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='From?']")))
        from_field.clear()
        from_field.send_keys(origin)
        time.sleep(1)
        from_field.send_keys(Keys.ENTER)

        # Click and type destination
        to_field = driver.find_element(By.XPATH, "//input[@placeholder='To?']")
        to_field.clear()
        to_field.send_keys(destination)
        time.sleep(1)
        to_field.send_keys(Keys.ENTER)

        # If a specific date was given, set it
        if date and date.lower() != "any":
            # Open date picker
            date_input = driver.find_element(By.XPATH, "//input[contains(@placeholder, 'Departure')]")
            date_input.click()
            time.sleep(1)

            # Send the date directly (Kiwi allows typing YYYY-MM-DD)
            date_input.send_keys(Keys.CONTROL + "a")  # Select all
            date_input.send_keys(date)
            date_input.send_keys(Keys.ENTER)

        # Submit search
        search_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Search')]")))
        search_button.click()

        # Wait for results to load
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ResultCard")))

        time.sleep(5)  # Wait a bit for all results

        # Get first 3 flight results
        flights = driver.find_elements(By.CLASS_NAME, "ResultCard")[:3]
        results = []

        for flight in flights:
            try:
                price = flight.find_element(By.CLASS_NAME, "Price__PriceContainer").text
                times = flight.find_element(By.CLASS_NAME, "SegmentTimes").text
                route = flight.find_element(By.CLASS_NAME, "SegmentRoute__Cities").text
                results.append(f"{route}\n🕒 {times}\n💸 {price}")
            except:
                continue

        return results if results else ["No flights found."]

    except Exception as e:
        return [f"Error: {str(e)}"]

    finally:
        driver.quit()
