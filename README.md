# Handshaker – Handshake Quick Apply Bot 🤖

**Handshaker** is a Python-based automation script that applies to jobs for you on the BYU Handshake platform using Selenium.

It scrapes job listings based on your search query and automatically applies to all jobs with the "Quick Apply" option. Jobs that require additional steps are saved and displayed in a reviewable HTML file.

---

## ✨ Features

- 🔍 Searches Handshake with a custom job query
- ⚡ Automatically applies to all "Quick Apply" jobs
- 📝 Saves non-quick-apply jobs to an HTML file for manual review
- 🌐 Opens a browser window so you can watch it work
- 🔐 Requires DUO push authentication

---

## 📦 Installation

```bash
touch .env
Fill the .env file with the appropriate values. Refer to the example in .env.example.

🚀 Usage
Run Auto Apply
bash
Copy
Edit
python script.py -q "Web Developer"
-q or --query specifies the job you're searching for.

A browser window will open, and you’ll be prompted to complete DUO authentication.

Generate HTML for Manual Applications
bash
Copy
Edit
python html_gen.py
This creates an HTML file from non_quick_apply_urls.json with jobs that couldn't be auto-applied.

To view it, copy the path of the generated HTML file and open it in your browser.

🧰 Built With
Python

Selenium

Feel free to submit issues or suggestions to improve the script!

vbnet
Copy
Edit

Let me know if you'd like badges, installation screenshots, or a `requirements.txt` mention added.
