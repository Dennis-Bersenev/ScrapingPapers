"""
Obtains abstracts for all papers citing the paper of interest, and gets a LM to decide which, if any, of those are relevant to some research topic.
(User specifies the paper and the research topic.)
"""

from key import SS_KEY as SS_API_KEY
from key import OPEN_AI_KEY
from urllib.request import Request, urlopen

import os
import json
import os
import time
from agent import Agent


# Directory containing the abstracts
directory = 'citing_paper_abstracts'
out_dir = 'relevant_articles'
if not os.path.exists(out_dir):
  os.makedirs(out_dir)

# Loop over each file in the directory
i = 0
for filename in os.listdir(directory):
    # Construct the full file path
    file_path = os.path.join(directory, filename)
    
    # Open and read the JSON file
    with open(file_path, 'r') as file:
        data = json.load(file).get('citingPaper')
    
    title = (data.get('title', 'No title available')).replace('/', '')
    abstract = data.get('abstract', 'No abstract available')
    
    print(f"Title: {title}")
    print(f"Abstract: {abstract}\n\n")
    
    # Next, query GPT: ask it which abstracts seem relevant and prune based off that!!!
    # Only for papers with an abstracts
    if abstract:
        query_out = os.path.join(out_dir, 'reader_out.txt')
        try:
            prompt_one = f"Identify whether the paper, based on the title and abstract provided, is pertinent to the research goal of interpolating single cell RNA expression from cell surface protein measurements. Title: {title}. Abstracts: {abstract}"
            print(prompt_one)
            query_agent = Agent(key=OPEN_AI_KEY)
            query_thread, run = query_agent.create_thread_and_run(user_message=prompt_one)
            query_agent.wait_on_run(run=run, thread=query_thread)
            analysis_out = query_agent.get_final_response(query_thread)

            prompt_two = "If you are certain that the paper is pertinent, answer with a single word: 'Pertinent', and if it is not then answer simply with 'Irrelevant'. Be highly critical of the relevance, only classify a paper as 'Pertinent' if you are ABSOLUTELY certain it is pertinent."
            run_two = query_agent.submit_message(thread=query_thread, user_message=prompt_two) 
            query_agent.wait_on_run(run=run_two, thread=query_thread)
            sentiment_out = query_agent.get_final_response(query_thread)
            print(analysis_out)
            print("------------------------------------------------------------\n\n")
        
            if 'pertinent' in sentiment_out.lower():
                outpath = os.path.join(out_dir, title + '.txt')
                with open(outpath, 'w') as file:
                    file.write(analysis_out)
        except:
            continue

    
    # # for debugging
    # if i > 2:
    #     break
    
    # i += 1

    