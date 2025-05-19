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
```

Fill the .env file with the appropriate values. Refer to the example in .env.example.
You will need to put your BYU username, BYU password and the name of the resume you have uploaded to Handshake in your env file.

🚀 Usage
Run Auto Apply

```bash
python script.py -q "YOUR DESIRED JOB TITLE TO SEARCH FOR HERE"
```
-q or --query specifies the job you're searching for. Fill in the job title you are searching for in the quotes.

A browser window will open, and you’ll be prompted to complete DUO authentication.

At the end, it creates an HTML file a generated json file with jobs that couldn't be auto-applied.

To view it, copy the path of the generated HTML file and open it in your browser.

🧰 Built With Python and Selenium

Feel free to submit issues, branch/copy this project or suggestions to improve the script!

Make sure to leave a review and a rating! It helps me out!
