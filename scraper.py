import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape_first_public_notice(search_input, start_date, end_date, state, country, notice_type):
    chrome_options = Options()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        driver.maximize_window()
        driver.get("https://publicnotices.washingtonpost.com/")
        wait = WebDriverWait(driver, 10)

        wait.until(EC.element_to_be_clickable((By.ID, 'searchbtn'))).send_keys(search_input)
        driver.execute_script(f"document.getElementById('dateStart').value = '{start_date}';")
        driver.execute_script(f"document.getElementById('dateEnd').value = '{end_date}';")

        state_dropdown = wait.until(EC.element_to_be_clickable((By.ID, 'react-select-2-input')))
        state_dropdown.clear()
        state_dropdown.send_keys(state)
        state_dropdown.send_keys(Keys.RETURN)

        country_dropdown = wait.until(EC.element_to_be_clickable((By.ID, 'react-select-3-input')))
        country_dropdown.clear()
        country_dropdown.send_keys(country)
        country_dropdown.send_keys(Keys.RETURN)

        notice_type_dropdown = wait.until(EC.element_to_be_clickable((By.ID, 'react-select-4-input')))
        notice_type_dropdown.clear()
        notice_type_dropdown.send_keys(notice_type)
        notice_type_dropdown.send_keys(Keys.RETURN)

        search_btn = wait.until(EC.element_to_be_clickable((By.ID, 'search')))
        search_btn.click()

        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".cursor-pointer.col-span-1.public-notice-result")))
        results = driver.find_elements(By.CSS_SELECTOR, ".cursor-pointer.col-span-1.public-notice-result")

        wait.until(EC.presence_of_all_elements_located((By.ID, "result-count")))
        result_count_wrappers = driver.find_elements(By.ID, 'result-count')

        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'w-full.flex.items-center.my-10')))
        all_load_more_btns = driver.find_elements(By.CLASS_NAME, 'w-full.flex.items-center.my-10')

        actual_load_more_btn = ''

        for all_load_more_btn in all_load_more_btns:
            if all_load_more_btn.text:
                actual_load_more_btn = all_load_more_btn

        total_results = ''
        for result in result_count_wrappers:
            if result.text:
                total_results = int(result.text.split(' ')[1])

        total_present_result = []
        for actual_result in results:
            if actual_result.text:
                total_present_result.append(actual_result)

        while len(total_present_result) <= total_results:
            try:
                if actual_load_more_btn.text:
                    actual_load_more_btn.click()
                    results = driver.find_elements(By.CSS_SELECTOR, ".cursor-pointer.col-span-1.public-notice-result")
                    time.sleep(2)
            except Exception as e:
                break

        all_results = []
        for result in results:
            if result.text:
                ActionChains(driver).move_to_element(result).click(result).perform()
                time.sleep(1)

                wait.until(EC.presence_of_element_located((By.CLASS_NAME, "h-full.w-200.flex.flex-col.space-y-6.pb-6.bg-white.dark\\:bg-gray-800.shadow-xl.overflow-y-scroll")))
                data_to_be_scrapped = driver.find_element(By.CLASS_NAME, "h-full.w-200.flex.flex-col.space-y-6.pb-6.bg-white.dark\\:bg-gray-800.shadow-xl.overflow-y-scroll")

                if data_to_be_scrapped:
                    notice_header = data_to_be_scrapped.find_element(By.TAG_NAME, 'h2').text
                    publication = data_to_be_scrapped.find_element(By.CLASS_NAME, 'mt-1.max-w-2xl.text-sm.leading-5.text-gray-800.dark\\:text-gray-200').text
                    location = data_to_be_scrapped.find_element(By.CLASS_NAME, 'mt-1.text-sm.leading-5.text-gray-800.dark\\:text-gray-300').text
                    notice_text_wrapper = data_to_be_scrapped.find_element(By.CLASS_NAME, 'mt-1.text-sm.leading-5.text-gray-800.dark\\:text-gray-300.md\\:overflow-scroll')

                    notice_texts = notice_text_wrapper.find_elements(By.TAG_NAME, 'p')
                    notice_texts_arr = [notice_text.text for notice_text in notice_texts]

                    all_results.append({
                        "Notice Type": notice_header,
                        "Publication": publication,
                        "Location": location,
                        "Notice Text": " ".join(f"{i + 1}. {text}" for i, text in enumerate(notice_texts_arr))
                    })

                time.sleep(0.5)

        if all_results:
            df = pd.DataFrame(all_results)
            df.to_csv('public_notice_data.csv', index=False)
            return f"Scraped {len(all_results)} results and saved to public_notices.csv"
        else:
            return "No results found."
    except Exception as e:
        return f"An error occurred: {e}"
    finally:
        driver.quit()
