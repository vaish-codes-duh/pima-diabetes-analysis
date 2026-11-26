"""Export the notebook's SAVED outputs as a dependency-free static website.

Run the notebook and save it before rebuilding to refresh the analysis.
This script does not execute Python cells or fetch new patient data.
"""
import base64
import html
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site'
SOURCE = ROOT / 'clinical_data_basics_python(1).ipynb'
notebook = json.loads(SOURCE.read_text())
SITE.mkdir(exist_ok=True)

def text(value):
    return ''.join(value) if isinstance(value, list) else value

def inline(value):
    value = html.escape(value)
    value = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', value)
    value = re.sub(r'`(.+?)`', r'<code>\1</code>', value)
    value = value.replace('$d$', '<em>d</em>')
    return value

def markdown(value, cell):
    """Render the headings, paragraphs and lists used by this notebook safely."""
    result, paragraph, listing = [], [], None
    def flush():
        if paragraph:
            result.append('<p>' + inline(' '.join(paragraph)) + '</p>')
            paragraph.clear()
    def close_list():
        nonlocal listing
        if listing:
            result.append('</' + listing + '>')
            listing = None
    for line_number, line in enumerate(value.splitlines()):
        heading = re.match(r'^(#{1,6})\s+(.+)$', line)
        item = re.match(r'^\s*(?:[-*]|\d+\.)\s+(.+)$', line)
        if heading:
            flush(); close_list()
            level = min(len(heading[1]) + 1, 6)
            result.append(f'<h{level} id="cell-{cell}-{line_number}">{inline(heading[2])}</h{level}>')
        elif item:
            flush()
            kind = 'ol' if re.match(r'^\s*\d', line) else 'ul'
            if listing != kind:
                close_list(); listing = kind; result.append('<' + kind + '>')
            result.append('<li>' + inline(item[1]) + '</li>')
        elif not line.strip():
            flush(); close_list()
        else:
            close_list(); paragraph.append(line.strip())
    flush(); close_list()
    return '\n'.join(result)

cells = []
chart = None
for number, cell in enumerate(notebook['cells']):
    content = text(cell.get('source', ''))
    if cell['cell_type'] == 'markdown':
        cells.append('<section class="markdown-cell">' + markdown(content, number) + '</section>')
    elif cell['cell_type'] == 'code':
        block = '<div class="code-cell"><details class="code"><summary>View Python code</summary><pre><code>' + html.escape(content) + '</code></pre></details>'
        for output in cell.get('outputs', []):
            if 'text' in output:
                block += '<pre class="output">' + html.escape(text(output['text'])) + '</pre>'
            data = output.get('data', {})
            if 'image/png' in data:
                encoded = text(data['image/png']).strip()
                assert base64.b64decode(encoded).startswith(b'\x89PNG\r\n\x1a\n')
                chart = '<img class="analysis-chart" src="data:image/png;base64,' + encoded + '" alt="Notebook chart comparing mean glucose and glucose distributions by recorded diabetes diagnosis">'
                block += chart
            elif 'text/plain' in data:
                block += '<pre class="output">' + html.escape(text(data['text/plain'])) + '</pre>'
        cells.append(block + '</div>')

assert chart, 'Save the notebook with its chart output before exporting.'
page = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="Vaishnavi Shreedhar's Python analysis of the Pima diabetes cohort: data cleaning, Welch's t-test, chi-square testing and effect size.">
<meta name="theme-color" content="#103b3a"><title>Pima Diabetes Analysis · Vaishnavi Shreedhar</title>
<link rel="stylesheet" href="styles.css"><script src="app.js" defer></script></head>
<body><a class="skip" href="#main">Skip to content</a>
<header><a class="brand" href="#">VS <span>RESEARCH PORTFOLIO</span></a><nav aria-label="Main navigation"><a href="#findings">Findings</a><a href="#quality">Data quality</a><a href="#notebook">Notebook</a></nav></header>
<main id="main"><section class="hero"><div class="hero-content"><p class="eyebrow">PYTHON · EXPLORATORY STATISTICS</p>
<h1>Pima Diabetes<br><span>Analysis</span></h1><p class="intro">From raw clinical records to interpretable results. Exploring metabolic and demographic differences by recorded diabetes diagnosis.</p>
<p class="byline">A project by <strong>Vaishnavi Shreedhar</strong></p><div class="actions"><a class="button" href="#findings">Explore the findings</a><a class="button secondary" href="pima-diabetes-analysis.ipynb" download>Download notebook</a></div></div>
<aside class="hero-aside" aria-label="Analysis workflow"><p class="eyebrow">THE ANALYTICAL WORKFLOW</p><div><b>768</b><span>source records audited</span></div><div><b>392</b><span>complete records analyzed</span></div><div><b>2 tests</b><span>Welch’s t-test + chi-square</span></div><p>Data cleaning · Group comparisons · Effect size</p></aside></section>
<section id="findings" class="section"><p class="eyebrow">RESULTS AT A GLANCE</p><h2>A clear glucose difference<br>within the analyzed cohort.</h2><p class="lede">Among complete cases, the recorded diabetes group had higher average glucose. This is an expected association with a diagnostic marker, not a newly validated prediction model.</p>
<div class="metrics"><div><span>Mean glucose difference</span><strong>+33.8 <small>mg/dL</small></strong><p>Diabetes minus no diabetes</p></div><div><span>Standardized mean difference</span><strong>1.28 <small>Cohen’s d</small></strong><p>Computed with pooled sample SD</p></div><div><span>Complete-case retention</span><strong>51.0<small>%</small></strong><p>392 of 768 source records</p></div></div>
<figure>''' + chart + '''<figcaption>Original saved notebook output. Both panels use the 392 complete cases.</figcaption></figure>
<div class="columns"><div><h3>Group comparison</h3><div class="table-scroll"><table><caption>Complete cases by recorded diagnosis</caption><thead><tr><th scope="col">Measure</th><th scope="col">No diabetes</th><th scope="col">Diabetes</th></tr></thead><tbody><tr><th scope="row">Records</th><td>262</td><td>130</td></tr><tr><th scope="row">Glucose, mean (SD), mg/dL</th><td>111.4 (24.6)</td><td>145.2 (29.8)</td></tr><tr><th scope="row">BMI, mean (SD), kg/m²</th><td>31.8 (6.8)</td><td>35.8 (6.7)</td></tr><tr><th scope="row">Age, mean (SD), years</th><td>28.3 (9.0)</td><td>35.9 (10.6)</td></tr></tbody></table></div></div>
<div class="tests"><h3>Statistical methods</h3><p><strong>Welch’s independent-samples t-test</strong><br>Glucose by diagnosis: t = 11.15, p &lt; 0.0001. Equal population variances are not assumed.</p><p><strong>Chi-square test of independence</strong><br>Age group (&lt;40 vs. ≥40) and diagnosis: χ² = 33.40, df = 1, p &lt; 0.0001. SciPy’s default continuity correction is used.</p><p><strong>Cohen’s d</strong><br>The glucose difference is 1.28 pooled standard deviations. Effect size alone does not establish clinical importance.</p></div></div>
<p class="note">Values above are transcribed from the notebook’s saved outputs. Its p-values display as 0.0000 because of rounding; this does not mean the true p-values equal zero. BMI is summarized descriptively, not hypothesis-tested.</p></section>
<section id="quality" class="section quality"><p class="eyebrow">BEFORE THE STATISTICS</p><h2>Make missingness visible.</h2><p class="lede">Zeros in five measurement columns are marked as missing. Complete-case filtering across those columns removes 376 records; pregnancy zeros remain valid.</p>
<div class="columns"><div class="table-scroll"><table><caption>Zero placeholders in the 768 source records</caption><thead><tr><th scope="col">Measurement</th><th scope="col">Zeros</th><th scope="col">Share</th></tr></thead><tbody><tr><th scope="row">Glucose</th><td>5</td><td>0.7%</td></tr><tr><th scope="row">Blood pressure</th><td>35</td><td>4.6%</td></tr><tr><th scope="row">Skin thickness</th><td>227</td><td>29.6%</td></tr><tr><th scope="row">Insulin</th><td>374</td><td>48.7%</td></tr><tr><th scope="row">BMI</th><td>11</td><td>1.4%</td></tr></tbody></table></div><aside class="limits"><h3>Read the results in context</h3><p>Excluding almost half the dataset may introduce selection bias, especially if missingness is systematic. Counts across columns overlap.</p><p>The historical cohort comprises Pima Indian women aged 21 and older. Findings should not be generalized to other populations.</p><p>This observational analysis describes associations. It does not establish causation or assess individual diabetes risk.</p><p>Assertions check the expected shape, duplicates, missingness, and positive values in the retained measurement columns.</p></aside></div></section>
<section id="notebook" class="section"><div class="notebook-heading"><div><p class="eyebrow">THE FULL WORK</p><h2>Explore the notebook.</h2></div><button id="toggle-code" type="button" aria-pressed="false">Expand all Python code</button></div><p class="lede">Original narrative, Python cells, and saved outputs. Expand individual code blocks to follow each step. This page displays saved results; it does not run Python in your browser.</p><p class="note">The original notebook wording is retained below. For interpretation, p-values do not give the probability that results are “due to luck,” and a large standardized effect does not by itself prove clinical significance.</p><article class="notebook">''' + '\n'.join(cells) + '''</article></section>
<footer><div><strong>Pima Diabetes Analysis</strong><p>Python · pandas · NumPy · SciPy · Matplotlib</p></div><div><a href="pima-diabetes-analysis.ipynb" download>Download original notebook</a><a href="https://github.com/vaish-codes-duh/pima-diabetes-analysis">View repository</a></div><p class="source">Data: historical Pima Indians Diabetes dataset, attributed to NIDDK in the notebook. CSV mirror: <a href="https://github.com/jbrownlee/Datasets/blob/master/pima-indians-diabetes.data.csv">jbrownlee/Datasets</a>. Reference: Smith et al. (1988), as cited in the notebook.</p></footer></main></body></html>'''
(SITE / 'index.html').write_text(page)
shutil.copyfile(SOURCE, SITE / 'pima-diabetes-analysis.ipynb')
print(f'Exported {len(notebook["cells"])} saved notebook cells to site/index.html')
