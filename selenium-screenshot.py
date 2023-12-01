import sys
import os
import concurrent.futures
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

def capture_screenshot(url, idx):
    try:
        chrome_service = Service(executable_path='chromedriver.exe')
        cdriver = webdriver.ChromeOptions()
        cdriver.add_argument('--headless')
        driver = webdriver.Chrome(service=chrome_service, options=cdriver)
        
        driver.get(url)
        
        screenshot_path = os.path.join(out_folder, f'screenshot_{url.replace("://", "_").replace(".", "_")}.png')
        driver.save_screenshot(screenshot_path)
        print(f"Screenshot {idx + 1} captured successfully and saved at: {screenshot_path}")

    except Exception as e:
        print(f"Error occurred while capturing screenshot for URL {url}: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the path to the file containing the list of URLs as the first argument.")
        sys.exit(1)

    url_file = sys.argv[1] + '/fulldomains.txt'

    if not os.path.exists(url_file):
        print("URL file does not exist.")
        sys.exit(1)

    out_folder = os.path.join(os.path.dirname(url_file), 'out')
    os.makedirs(out_folder, exist_ok=True)

    try:
        with open(url_file, 'r') as file:
            urls = file.readlines()
            urls = [url.strip() for url in urls]

            with concurrent.futures.ThreadPoolExecutor() as executor:
                future_to_url = {executor.submit(capture_screenshot, url, idx): url for idx, url in enumerate(urls)}
                for future in concurrent.futures.as_completed(future_to_url):
                    url = future_to_url[future]
                    try:
                        future.result()
                    except Exception as e:
                        print(f"URL {url} generated an exception: {str(e)}")

    except Exception as ex:
        print(f"An error occurred: {str(ex)}")
