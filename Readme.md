# 🌐 Automated Website Interaction with Playwright (Python)

This project automates the process of visiting multiple websites using Playwright in Python, simulating real-user behavior by:

- Randomizing user agents and geolocation
- Performing site-specific interactions (scrolling or clicking)
- Logging all actions in structured JSON format (or CSV)
- Running multiple browser instances concurrently

---

## 🚀 Features

- ✅ Random user agent assignment
- 🌍 Random geolocation simulation (e.g., Paris, Tokyo, San Francisco)
- 🖱️ Website-specific interaction functions
- 📜 Scroll to bottom on selected websites
- 🔘 Click button and wait for the page to load
- ⏱️ Logs time spent per website
- 🗂️ Logs stored in structured JSON format
- 🧠 Uses async concurrency with Playwright
- 🖥️ Launches multiple browser instances with maximized screen size

---

## 🏗️ Project Structure

```
project/
├── interaction_logger.py     # Handles structured logging (JSON/CSV)
├── main.py                   # Main logic with interaction functions
├── websites.xlsx             # Excel file with a list of URLs

```

---

## 📥 Prerequisites

Install dependencies:

```bash
pip install playwright openpyxl
playwright install
```

---

## ⚙️ How It Works

### 1. **Website Loader**
Loads all websites from an Excel file (`websites.xlsx`), expecting a column of URLs starting from the second row.

### 2. **User-Agent & Geolocation**
For each browser instance, a **random user agent** and **geolocation** is assigned from predefined lists.

```python
USER_AGENTS = [...]
GEO_LOCATIONS = [...]
```

### 3. **Interaction Rules**
Custom interaction logic is handled based on domain match:

| Website              | Action                                |
|----------------------|----------------------------------------|
| `jamescropper.com`   | Scroll to bottom slowly                |
| `code.org`           | Scroll to bottom slowly                |
| `ittehad.com.pk`     | Click a specific button and wait       |

### 4. **Actions Logged**
Every interaction is logged with details:

| Action Type   | Description                                  |
|---------------|----------------------------------------------|
| `visit`       | Website opened with UA and GEO info          |
| `scroll`      | Scroll action initiated                      |
| `click`       | Element clicked (with selector)              |
| `time_spent`  | Time spent on the current page               |
| `click_failed`| Failed click with error reason               |
| `visit_failed`| Failed page load with error message          |

### 5. **Time Measurement**
The script records the time from when the page is loaded to when all interactions are complete, and logs it in seconds:
To Note the time on each website ignore the time with null in log json
- **Time Spent** It Will appear on 30 urls, because every action is logged, e.g scrolling or clicking its time spent is not logged.

```json
"time_spent": "8.23s"
```

---

## 📄 Example JSON Log Entry

```json
{
  "browser": "Browser-1",
  "url": "https://code.org",
  "action": "scroll",
  "details": "scroll",
  "timestamp": "2025-07-08 16:30:01"
}
```

Or for a complete visit:

```json
{
  "browser": "Browser-2",
  "url": "https://ittehad.com.pk",
  "action": "click",
  "details": "Clicked '#header > div > div > nav > div.header-quote > a'",
  "timestamp": "2025-07-08 16:32:10"
}
```

---

## 🧪 How to Run

Place your websites inside `websites.xlsx` (1 per row starting from the second row). Then run:

```bash
python main.py
```

---

## 📌 Notes

- The script supports **up to 10 concurrent browser sessions** by default.
- **Structured logging** supports both JSON and CSV. You can toggle formats from the `Virtoxed` constructor:

```python
Virtoxed(excel_path="websites.xlsx", log_format="json") 
```

---

## 🔒 Exception Handling

Custom error handling ensures clean logs:

- If a selector is not found → logs `"click_failed"` with `"TimeoutError"`
- Other Playwright or unexpected errors are caught with appropriate messages

---


## 🤝 Author

Abdul Mohiz
