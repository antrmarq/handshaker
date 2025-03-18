# handshaker - Handshake quick apply bot made using Selenium as the head

A script that automatically applies to jobs for me and you!

Scrapes the BYU Handshake website when you search for any job and applies to all the jobs with quick apply. 

Jobs that are not easy applys are saved and shown in an html file for you to review!


Written in Python using Selenium.

## Installation

```
touch .env
```

> Make sure to fill `.env` with correct contents (see [`.env.example`](/.env.example)).

## Usage

```
python script.py -q "Web developer"
```

`-q` or `--query` is the flag where you can enter the job you're interested in.

```
 python html_gen.py
```

This creates the html file of the job postings to review once non_quick_apply_urls,json is created. In order to view it, just copy the path of the html file and put it in a browser.
