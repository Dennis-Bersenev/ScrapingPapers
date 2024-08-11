# A tool to scrape scientific articles of interest via the Semantic Scholar API.
## https://www.semanticscholar.org/product/api%2Ftutorial#searching-and-retrieving-paper-details

## Can acquire meta information on any paper such as abstracts, authors, citations, and also meta information/text of all citing papers.
### If paper is open access full text can also be obtained. 
### Can also be performed with a keyword search to obtain all articles of interest.

# Setup
## 1. Setup keys in src/key.py (Note: semantic scholar API key is required).
## 2. Setup environment via conda: conda env create -f environment.yml


# Example Usage:
## General Structure: src/python3 main.py --title PaperName --meta_params 'comma-seperated-list'
### python3 src/main.py --title "Large-scale simultaneous measurement of epitopes and transcriptomes in single cells" --meta_params "year,abstract"
### python3 src/main.py --title "Attention is All You Need" --meta_params "year,abstract,authors.name"
