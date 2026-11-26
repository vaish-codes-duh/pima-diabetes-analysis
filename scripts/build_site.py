"""Build the academic HTML report from saved notebook summaries; no cell execution."""
import json
import shutil
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site'
SOURCE = ROOT / 'clinical_data_basics_python(1).ipynb'
notebook = json.loads(SOURCE.read_text())
outputs = '\n'.join(''.join(out.get('text', [])) for cell in notebook['cells'] for out in cell.get('outputs', []))
for required in ['Clean dataset: 392 patients.', 'Difference: 33.8 mg/dL', "Cohen's d = 1.28", 'chi² = 33.40']:
    assert required in outputs, 'Notebook results changed; review the report summary before rebuilding.'

def figure(kind):
    glucose = kind == 'glucose'
    title = 'Mean glucose by recorded diabetes diagnosis' if glucose else 'Recorded diabetes by age group'
    description = ('No diabetes: mean 111.4, SD 24.6 mg/dL, 262 records. Diabetes: mean 145.2, SD 29.8 mg/dL, 130 records. Whiskers show one standard deviation, not confidence intervals.' if glucose else 'Under 40: 83 of 316 records, 26.3 percent. Age 40 and older: 47 of 76 records, 61.8 percent. Complete cases only.')
    parts = [f'<svg viewBox="0 0 560 345" role="img" aria-labelledby="{kind}-title {kind}-desc"><title id="{kind}-title">{title}</title><desc id="{kind}-desc">{description}</desc>']
    def y(value): return 260 - value * (1.02 if glucose else 2.04)
    for tick in ([0,50,100,150,200] if glucose else [0,25,50,75,100]):
        parts.append(f'<line class="grid" x1="65" x2="535" y1="{y(tick)}" y2="{y(tick)}"/><text class="tick" x="51" y="{y(tick)+5}" text-anchor="end">{tick}</text>')
    axis = 'Glucose (mg/dL)' if glucose else 'Records with diabetes (%)'
    parts.append(f'<text class="axis-label" x="65" y="24">{axis}</text>')
    values = [(197,111.4,24.6,'No diabetes','n = 262','#718b9c'),(410,145.2,29.8,'Diabetes','n = 130','#934a56')] if glucose else [(197,83/316*100,0,'Under 40 years','83 of 316 records','#934a56'),(410,47/76*100,0,'40 years and older','47 of 76 records','#934a56')]
    for x,mean,sd,label,n,colour in values:
        parts.append(f'<rect x="{x-45}" y="{y(mean)}" width="90" height="{260-y(mean)}" rx="2" fill="{colour}" fill-opacity="{.18 if glucose else .8}"/>')
        if glucose:
            parts.append(f'<line x1="{x}" x2="{x}" y1="{y(mean-sd)}" y2="{y(mean+sd)}" stroke="{colour}" stroke-width="2"/>')
            for value in [mean-sd,mean+sd]:
                parts.append(f'<line x1="{x-10}" x2="{x+10}" y1="{y(value)}" y2="{y(value)}" stroke="{colour}" stroke-width="2"/>')
            parts.append(f'<circle cx="{x}" cy="{y(mean)}" r="6" fill="{colour}"/><text class="value" x="{x+17}" y="{y(mean)+5}">{mean}</text>')
        else:
            parts.append(f'<text class="value" x="{x}" y="{y(mean)-13}" text-anchor="middle">{mean:.1f}%</text>')
        parts.append(f'<text class="chart-label" x="{x}" y="294" text-anchor="middle">{label}</text><text class="tick" x="{x}" y="318" text-anchor="middle">{n}</text>')
    return ''.join(parts) + '</svg>'
page = (ROOT / 'scripts/report.html').read_text()
page = page.replace('<!-- GLUCOSE_FIGURE -->', figure('glucose')).replace('<!-- AGE_FIGURE -->', figure('age'))
SITE.mkdir(exist_ok=True)
(SITE / 'index.html').write_text(page)
shutil.copyfile(SOURCE, SITE / 'pima-diabetes-analysis.ipynb')
print('Built academic HTML report with two accessible figures; no code cells are displayed.')
