from flask import Flask, render_template, request
from utils.onpage_scanner import scan_onpage_seo
from utils.technical_scanner import scan_technical_seo
from utils.offpage_research import research_offpage_seo
from utils.ai_agent import generate_seo_suggestions, generate_technical_suggestions, generate_offpage_strategy

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/onpage', methods=['GET', 'POST'])
def onpage():
    report = None
    ai_suggestions = None
    url = None
    error = None

    if request.method == 'POST':
        url = request.form.get('url')
        if url:
            report = scan_onpage_seo(url)
            if 'error' in report:
                error = report['error']
            else:
                ai_suggestions = generate_seo_suggestions(report, url)
                ai_suggestions['score'] = report['calculated_score']
    return render_template('onpage.html', report=report, ai_suggestions=ai_suggestions, url=url, error=error)
@app.route('/technical', methods=['GET', 'POST'])
def technical():
    report = None
    ai_suggestions = None
    url = None
    error = None

    if request.method == 'POST':
        url = request.form.get('url')
        if url:
            report = scan_technical_seo(url)
            if 'error' in report:
                error = report['error']
            else:
                ai_suggestions = generate_technical_suggestions(report, url)
                ai_suggestions['score'] = report['calculated_score']

    return render_template('technical.html', report=report, ai_suggestions=ai_suggestions, url=url, error=error)
@app.route('/offpage', methods=['GET', 'POST'])
def offpage():
    report = None
    ai_suggestions = None
    url = None
    niche_keyword = None
    error = None

    if request.method == 'POST':
        url = request.form.get('url')
        niche_keyword = request.form.get('niche_keyword')
        if url and niche_keyword:
            report = research_offpage_seo(url, niche_keyword)
            if 'error' in report:
                error = report['error']
            else:
                ai_suggestions = generate_offpage_strategy(report, url, niche_keyword)

    return render_template('offpage.html', report=report, ai_suggestions=ai_suggestions, url=url, niche_keyword=niche_keyword, error=error)
@app.route('/full-report', methods=['GET', 'POST'])
def full_report():
    onpage_report = None
    onpage_ai = None
    technical_report = None
    technical_ai = None
    offpage_report = None
    offpage_ai = None
    url = None
    niche_keyword = None
    error = None
    overall_score = None

    if request.method == 'POST':
        url = request.form.get('url')
        niche_keyword = request.form.get('niche_keyword')

        if url and niche_keyword:
            onpage_report = scan_onpage_seo(url)
            if 'error' not in onpage_report:
                onpage_ai = generate_seo_suggestions(onpage_report, url)
                onpage_ai['score'] = onpage_report['calculated_score']

            technical_report = scan_technical_seo(url)
            if 'error' not in technical_report:
                technical_ai = generate_technical_suggestions(technical_report, url)
                technical_ai['score'] = technical_report['calculated_score']

            offpage_report = research_offpage_seo(url, niche_keyword)
            if 'error' not in offpage_report:
                offpage_ai = generate_offpage_strategy(offpage_report, url, niche_keyword)

            scores = []
            if onpage_ai and 'score' in onpage_ai:
                scores.append(onpage_ai['score'])
            if technical_ai and 'score' in technical_ai:
                scores.append(technical_ai['score'])
            if offpage_ai and 'score' in offpage_ai:
                scores.append(offpage_ai['score'])

            if scores:
                overall_score = round(sum(scores) / len(scores))

    return render_template('full_report.html',
                           url=url,
                           niche_keyword=niche_keyword,
                           onpage_ai=onpage_ai,
                           technical_ai=technical_ai,
                           offpage_ai=offpage_ai,
                           overall_score=overall_score)

if __name__ == '__main__':
    app.run(debug=True)