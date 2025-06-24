from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)

@app.route('/get_code', methods=['POST'])
def get_code():
    data = request.json
    user_id = data.get('user_id')
    password = data.get('password')

    # Setup Chrome options (headless optional)
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    # chrome_options.add_argument("--headless")  # Uncomment if you want no browser popup

    service = Service(r"C:\Users\User\Downloads\chromedriver-win64 (1)\chromedriver-win64\chromedriver.exe")

    driver = webdriver.Chrome(service=service, options=chrome_options)
    wait = WebDriverWait(driver, 20)

    try:
        login_url = "https://www.tax.service.gov.uk/account/sign-in"
        driver.get(login_url)

        user_input = wait.until(EC.visibility_of_element_located((By.ID, "user_id")))
        user_input.clear()
        user_input.send_keys(user_id)

        pass_input = wait.until(EC.visibility_of_element_located((By.ID, "password")))
        pass_input.clear()
        pass_input.send_keys(password)

        submit_btn = wait.until(EC.element_to_be_clickable((By.ID, "continue")))
        submit_btn.click()

        last4_elem = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "p.govuk-body > b")))
        last4 = last4_elem.text.strip()

        return jsonify({'last4': last4})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        driver.quit()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
