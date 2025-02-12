# Selenium UI Testing with Allure Reports

## 📂 Folder Structure

```bash
SeleniumPythonFunctional/
│── tests/                 
│   ├── test_checkout.py   # Selenium checkout test
│   ├── test_login.py      # Selenium login test
│── conftest.py            # Selenium browser setup
│── pytest.ini             # pytest configuration
│── requirements.txt       # Dependencies
│── allure-results/        # Allure test results            
│── README.md              # Project documentation
```

## 📌 Prerequisites
Before running the tests, ensure you have the following installed:

- **Python** (>=3.7)
- **Google Chrome, Firefox, Edge, or Safari (Selenium 4 includes a built-in browser, so no additional setup is needed)**
- **Selenium & Allure dependencies, refer to https://allurereport.org/docs/install-for-windows**

### Install Dependencies
```bash
pip install pytest selenium allure-pytest
```
or 
```bash
pip install -r requirements.txt
```
---

## 🚀 Running Tests

### Run All Tests
```bash
pytest .\tests\test_login.py --alluredir=allure-results
```

### Run a Specific Test (`-k`)
Run tests that match a keyword:
```bash
pytest -k "login" --alluredir=allure-results
```
👉 This runs tests like `test_checkout_process`.

### Run Tests in a Specific Browser
```bash
pytest --browser-type=firefox --alluredir=allure-results
```
👉 Supports **`chromium`**, **`firefox`**, **`edge`**, and **`safari`**.

### Run Tests in Headless Mode
```bash
pytest --headless --alluredir=allure-results
```

---

## 📊 Viewing Allure Reports
After running tests, generate and open the report:
```bash
allure serve allure-results
```
This launches a web-based report.

---

## ⚙️ Advanced Options
| Command | Description |
|---------|------------|
| `--headed` | Run in visible mode |
| `--headless` | Run in headless mode |

Example running in visible mode:
```bash
pytest --headed --browser-type=edge --alluredir=allure-results
```
---

## 🎥✅ Results 

https://github.com/user-attachments/assets/d5bbb00f-a65e-4644-935d-6ced6c54a299

---

## 🎯 Conclusion
This guide helps you quickly set up, run, and analyze Selenium UI tests with Allure reports. 🚀

