# Pima Diabetes Analysis

Academic statistics project by Vaishnavi Shreedhar.

**Live report:** https://pima-diabetes-analysis.netlify.app/

The website is a readable HTML research report with an abstract, methods, results, tables, figures, discussion, and limitations. Python source cells and console output are not displayed on the page. The original notebook remains available as a separate download for reproducibility.

## Analysis

- 768 historical Pima Indians Diabetes records.
- Zero placeholders marked missing in five measurement fields.
- 392 complete cases: 262 without diabetes and 130 with diabetes.
- Welch’s t-test for glucose, chi-square test for age group and diagnosis, and Cohen’s d for the glucose difference.
- Figures redraw the notebook’s saved summaries. Glucose whiskers show ±1 standard deviation, not confidence intervals. Age-group percentages use saved contingency-table counts.
- No synthetic observations, prediction model, or causal claims.

## Update the report

1. Run and save `clinical_data_basics_python(1).ipynb` if changing the analysis.
2. Review `scripts/report.html` and summary values in `scripts/build_site.py`.
3. Run `python3 scripts/build_site.py` to export `site/index.html` and refresh the downloadable notebook.
4. Commit the generated `site/` files along with source changes.

The exporter uses only Python’s standard library and never executes notebook cells. It checks key saved outputs before building to flag changed results for review. Narrative and summary tables are maintained in the HTML template.

## Netlify

Netlify deploys `main` and publishes `site/`, as configured in `netlify.toml`. The build command is blank: all HTML, CSS and figures are prebuilt and committed. No runtime, packages, or environment variables are required. The HTML report supports narrow screens, keyboard navigation, and browser printing.
