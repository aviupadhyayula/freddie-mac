# Doc-Reader
- This folder contains codes that handles "document reading" tasks, including scraping, parsing, and question-answering


## Codebase
- src: 
    - utils.py: some util function to load word embeddings
    - tree_spider.py: scrapper for ecode360
- notebooks:
    - 1-pdf-processing: process pdf files (archieve, reference only)
    - 7-zoning-code-matching: parse the websites and check if known zoning codes are presented in the zoning document
- data:
    - scrapped: scrapped content from ecode360 (using tree_scraper)
        - pickles_ts: pickle files (localized object, you can read it with python `pickle` package)
        - tables: txt files for the "tables" in the website
        - other txt files: some sub-sections of websites to run question-answering on
    - za_ordinates_links.csv: the local version of shered google sheet that contains relevant links to zoning ordinates
    - md_zoning_codes.csv: zoning codes/names from MD
    - zoning_codes_julia.csv: zoning codes/names from Julia (this is the one currently in used in notebook #7)
    - all_counts_results_df.csv: matching result from notebook #7
    - all_doc_results_df.csv: document classification result (not related to zoning code extraction)

## Get started
- Clone this repo and start all the notebook files (.ipynb files) in [jupyter notebook](https://jupyter.org/install) (see link for ways to install).
- Start with `7-zoning-code-matching.ipynb` for zoning code matching purpose