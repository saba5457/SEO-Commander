import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_seo_suggestions(scan_results, url):
    prompt = f"""You are a professional SEO expert. Analyze the following on-page SEO scan results for the website: {url}

Scan Data:
{scan_results}

Return ONLY a valid JSON object (no markdown, no extra text) with this exact structure:

{{
  "score": <number 0-100>,
  "summary": "<2-3 line summary of the site's SEO health>",
  "issues": [
    {{
      "title": "<short issue name>",
      "severity": "High or Medium or Low",
      "why_it_matters": "<1-2 lines explaining impact>",
      "how_to_fix": "<clear, specific fix instructions>"
    }}
  ],
  "strengths": ["<thing the site is already doing well>"]
}}

Include an issue entry for every problem found in the scan data. Include at least 2-3 strengths if applicable. Be specific and professional."""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are an expert SEO consultant. You always respond with valid JSON only, nothing else."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            response_format={"type": "json_object"}
        )
        content = response.choices[0].message.content
        return json.loads(content)

    except Exception as e:
        return {
            "score": 0,
            "summary": f"Error generating report: {str(e)}",
            "issues": [],
            "strengths": []
        }


def generate_technical_suggestions(scan_results, url):
    prompt = f"""You are a professional technical SEO expert. Analyze the following technical SEO scan results for the website: {url}

Scan Data:
{scan_results}

Return ONLY a valid JSON object (no markdown, no extra text) with this exact structure:

{{
  "score": <number 0-100>,
  "summary": "<2-3 line summary of the site's technical SEO health>",
  "issues": [
    {{
      "title": "<short issue name>",
      "severity": "High or Medium or Low",
      "why_it_matters": "<1-2 lines explaining impact>",
      "how_to_fix": "<clear, specific fix instructions>"
    }}
  ],
  "strengths": ["<thing the site is already doing well>"]
}}

Include an issue entry for every problem found in the scan data. Include at least 2-3 strengths if applicable. Be specific and professional."""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are an expert technical SEO consultant. You always respond with valid JSON only, nothing else."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            response_format={"type": "json_object"}
        )
        content = response.choices[0].message.content
        return json.loads(content)

    except Exception as e:
        return {
            "score": 0,
            "summary": f"Error generating report: {str(e)}",
            "issues": [],
            "strengths": []
        }


def generate_offpage_strategy(research_data, url, niche_keyword):
    prompt = f"""You are a professional off-page SEO and link-building strategist. The website is: {url}
Niche or Industry keyword: {niche_keyword}

Live search research data (may be incomplete):
{research_data}

Create a practical off-page SEO strategy. Rules:
1. If real URLs are present in the research data above, prioritize using those exact URLs.
2. If research data is empty or thin, fall back to recommending well-known, genuinely real platforms you are confident actually exist and are relevant to this niche and region (for example, Reddit communities, Quora, Google Business Profile, well-known industry-specific directories, or well-known local business directories for the country involved). Do not invent obscure directory names you are not confident exist.
3. Never present a made-up or uncertain website name as if it definitely exists.

Return ONLY a valid JSON object (no markdown, no extra text) with this exact structure:

{{
  "score": <number 0-100>,
  "summary": "<2-3 line summary of off-page SEO priorities for this site>",
  "backlink_opportunities": [
    {{
      "type": "<e.g. Guest Posting or Directory Listing or Community Engagement>",
      "site_url": "<a real URL if you are confident it exists, otherwise empty string>",
      "description": "<specific, actionable description of how to pursue this opportunity>",
      "difficulty": "Easy or Medium or Hard"
    }}
  ],
  "outreach_tips": ["<practical tip for reaching out to site owners>"],
  "competitor_insight": "<1-2 lines about what competitors in this niche likely do for backlinks>"
}}

Provide at least 5 specific, actionable backlink_opportunities relevant to this niche and region. Include at least 3 outreach_tips."""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are an expert off-page SEO strategist. You always respond with valid JSON only, nothing else. You only claim a URL exists if you are genuinely confident about it."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            response_format={"type": "json_object"}
        )
        content = response.choices[0].message.content
        return json.loads(content)

    except Exception as e:
        return {
            "score": 0,
            "summary": f"Error generating report: {str(e)}",
            "backlink_opportunities": [],
            "outreach_tips": [],
            "competitor_insight": ""
        }