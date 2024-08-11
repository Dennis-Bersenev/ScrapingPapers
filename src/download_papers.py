"""
Downloads all accessible papers (openaccess papers) as PDFs.
"""

from key import SS_KEY as SS_API_KEY
from key import proxies
from urllib.request import Request, urlopen

import os
import json
import os
import time
import requests
import re
import random 


################################################ Setup ################################################

api_key = SS_API_KEY

# Define headers with API key
headers = {'x-api-key': api_key}

# Define the directory name
out_dir = 'papers_all_part2'

# Create the directory if it doesn't exist
if not os.path.exists(out_dir):
    os.makedirs(out_dir)

spoof_agents = [
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
]

actual_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'en-CA,en;q=0.9,de-DE;q=0.8,de;q=0.7,en-GB;q=0.6,en-US;q=0.5,fr;q=0.4,ja;q=0.3',
    'Cache-Control': 'no-cache',
    'Pragma': 'no-cache',
    'Priority': 'u=0, i',
    'Sec-Ch-Ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    'Sec-Ch-Ua-Platform': '"Linux"',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
}



################################################ Helper Functions ################################################
def get_paper_data(paper_id):
    url = 'https://api.semanticscholar.org/graph/v1/paper/' + paper_id

    # Define which details about the paper you would like to receive in the response
    paper_data_query_params = {'fields': 'title,isOpenAccess,openAccessPdf'}

    # Send the API request and store the response in a variable
    response = requests.get(url, params=paper_data_query_params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def download_file(url, filename):
    try:
        session = requests.Session()
        
        # user_agent = random.choice(spoof_agents)
        # session.headers.update({
        #         "User-Agent": user_agent
        # })
        session.headers.update(actual_headers)
        response = requests.get(url=url, verify=True, headers=actual_headers)
        
        response.raise_for_status()  # Check if the request was successful
        
        filepath = os.path.join(out_dir, filename)

        with open(filepath, 'wb') as file:
            file.write(response.content)
        print(f"File downloaded successfully: {filename}")
    
    except requests.exceptions.RequestException as e:
        print(f"Error occurred (no gusto): {e}")
        if '429' in e: # too many requests
            time.sleep(10)
    
    finally:
        session.close()



def strip_special_characters(input_string):
    # Define a regex pattern that matches any character that is not a letter or a digit
    pattern = r'[^A-Za-z0-9]'
    
    # Use re.sub to replace all non-alphanumeric characters with an empty string
    stripped_string = re.sub(pattern, '', input_string)
    
    return stripped_string


def get_paper_text(query_params, url):
    # Send the API request
    search_response = requests.get(url, params=query_params, headers=headers)
    
    if search_response.status_code == 200:
        try:
            search_response = search_response.json()

            # Retrieve the paper id corresponding to the 1st result in the list
            paper_id = search_response['data'][0]['paperId']

            # Retrieve the paper details corresponding to this paper id.
            paper_details = get_paper_data(paper_id)
            
            if paper_details['isOpenAccess']:
                pdf_url = paper_details['openAccessPdf']['url']        
        except:
            pdf_url = None
    else:
        # Handle potential errors or non-200 responses
        print(f"Relevance Search Request failed with status code {search_response.status_code}: {search_response.text}")

    return pdf_url


def query_semantic_scholar(query_params, url):
    # TODO: a generic version
    return
