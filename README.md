# Pima Diabetes Analysis

Python exploratory statistics project by Vaishnavi Shreedhar. The static portfolio website includes the saved notebook narrative, code, chart, outputs, key findings, and limitations. It does not execute Python in the browser.

## Deploy on Netlify

Import this GitHub repository into Netlify, choose the `main` branch, leave the build command blank, and set the publish directory to `site`. The included `netlify.toml` already specifies the publish directory. No framework, package installation, environment variables, or Python runtime is required for deployment.

The notebook alone is not a website; `site/index.html` is the entry point. A private GitHub repository can remain private while the deployed website is accessible to visitors, depending on your Netlify access settings. The website includes a downloadable copy of the notebook.

## Update the web report

1. Edit and run `clinical_data_basics_python(1).ipynb`, then save it with outputs.
2. Run `python3 scripts/build_site.py` from this repository.
3. Review the headline summary in the export script if the analysis changes, and commit the updated notebook and generated `site/` files.

The exporter uses only Python's standard library. It renders this notebook's headings, paragraphs, lists, saved text outputs, and PNG chart. It does not execute cells or fetch data. Headline summary values are explicitly transcribed from the supplied notebook, not automatically recalculated.

## Analysis

- Source: 768 historical Pima Indians Diabetes records, loaded from the CSV mirror linked in the notebook.
- Zero placeholders marked missing in glucose, blood pressure, skin thickness, insulin, and BMI.
- Complete-case analysis: 392 records (262 no diabetes; 130 diabetes).
- Welch's t-test for glucose, chi-square test for age group and diagnosis, and Cohen's d for the glucose difference.
- Limitations include complete-case selection, restricted population generalizability, and the observational design. Glucose is already a diagnostic marker; these results do not validate a novel prediction model.

All displayed measurements and results come from the supplied notebook's saved outputs. No synthetic observations were added. Original notebook prose is retained; the page separately clarifies rounded p-values and statistical interpretation.
