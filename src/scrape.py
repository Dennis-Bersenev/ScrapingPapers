from scrapegraphai.graphs import SmartScraperGraph
from key import KEY as OPENAI_API_KEY
import json
import os
import pickle


# Define the directory name
directory = './data/json_pages'

# Create the directory if it doesn't exist
if not os.path.exists(directory):
    os.makedirs(directory)
#################################################################################################################
# Run once to scrape the articles

article_name = "SCANPY: large-scale single-cell gene expression data analysis"

graph_config = {
    "llm": {
        "api_key": OPENAI_API_KEY,
        "model": "gpt-4o",
    },
}

pages = [] # list of JSONs for each page
url = "https://citations.springernature.com/item?doi=10.1186/s13059-017-1382-0&start=1&years=&journals=&books=&authors="
    
def scrape_page(url_i):
    citation_graph = SmartScraperGraph(
        prompt="Compile a list of every single article on the webpage provided. Include the title and doi in your entries.",
        source=url_i,
        config=graph_config,
    )

    results = citation_graph.run()
    return results

pages.append(scrape_page(url))

for i in range(1, 257):
    url = f'https://citations.springernature.com/item?doi=10.1186/s13059-017-1382-0&start={i}1&years=&journals=&books=&authors='
    print("iteration: ", i)
    pages.append(scrape_page(url))
    
print("All looped")
# Pickle the object
with open('data.pkl', 'wb') as file:
    pickle.dump(pages, file)

#################################################################################################################
# Unpickle for follow-up work
with open('data.pkl', 'rb') as file:
    pages = pickle.load(file)
#################################################################################################################

print("Writing to JSON")
# Write each page as a JSON to a separate file in the directory
for i, page in enumerate(pages):
    file_path = os.path.join(directory, f'page_{i+1}.json')
    
    try:
        page["articles"].pop(0)
    except:
        continue

    with open(file_path, 'w') as json_file:
        json.dump(page, json_file, indent=4)

print(f"JSON objects have been written to the '{directory}' directory.")