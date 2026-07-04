# 🚀 SEO Commander — AI-Powered SEO Analysis Tool

An AI-powered SEO analysis platform that performs comprehensive On-Page, Technical, and Off-Page SEO audits for any website — combining automated web scanning with AI-generated actionable recommendations.

## 🎯 Features

- **On-Page SEO Analysis** — Scans title tags, meta descriptions, heading structure, image alt tags, word count, and internal/external links. Generates an AI-powered report with a health score, strengths, and prioritized fixes.
- **Technical SEO Analysis** — Checks page load speed, HTTPS security, mobile viewport configuration, robots.txt, sitemap.xml, canonical tags, and broken links.
- **Off-Page SEO Strategy** — Researches real backlink opportunities (guest posting, directories, community engagement) tailored to the website's niche, with an AI-generated outreach strategy.
- **Combined Full Report** — Runs all three analyses together and generates a unified SEO health score with a printable report.

## 🛠️ Tech Stack

- Backend: Python, Flask
- AI: Groq API (Llama 3.3 70B)
- Web Scraping: BeautifulSoup, Requests
- Search Research: DuckDuckGo Search
- Domain Intelligence: python-whois
- Frontend: HTML, CSS, Jinja2 templating

## ⚙️ How It Works

1. User enters a website URL (and niche keyword for off-page analysis)
2. The relevant scanner module collects real data from the live website
3. The scanned data is sent to an AI agent (Groq LLM) which analyzes it and returns a structured report
4. Results are displayed in a clean, color-coded dashboard with severity-based prioritization

## 🚀 Setup and Installation

Step 1 - Clone the repository:

git clone https://github.com/saba5457/SEO-Commander.git
cd SEO-Commander

Step 2 - Create a virtual environment:

python -m venv venv
venv\Scripts\activate

Step 3 - Install dependencies:

pip install -r requirements.txt

Step 4 - Create a .env file in the root directory and add your Groq API key:

GROQ_API_KEY=your_api_key_here

Step 5 - Run the app:

python app.py

Step 6 - Open http://127.0.0.1:5000 in your browser

## 📁 Project Structure

seo-commander/
├── app.py
├── static/
│   ├── css/style.css
│   └── js/
├── templates/
│   ├── home.html
│   ├── onpage.html
│   ├── technical.html
│   ├── offpage.html
│   └── full_report.html
├── utils/
│   ├── onpage_scanner.py
│   ├── technical_scanner.py
│   ├── offpage_research.py
│   └── ai_agent.py
└── requirements.txt

## 💡 Future Improvements

- PDF export functionality
- User authentication for saved reports
- Historical tracking of SEO score improvements over time
- Support for bulk URL analysis

## 👤 Author

Built by Saba — BSCS graduate exploring AI agents, automation, and SEO.

⭐ If you find this project useful, feel free to star the repository!
