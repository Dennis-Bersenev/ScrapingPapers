from argparse import ArgumentParser
from download_papers import *

def main():

    ################################################### Arg Parsing #####################################################
    # Parsing model from command line
    parser = ArgumentParser()
    parser.add_argument('--title', type=str, required=True, help='Title of paper of interest.')
    parser.add_argument('--meta_params', type=str, required=True, help='Meta info to be retrieved, see readme for structure, query result saved as json in data dir.')
    args = parser.parse_args()

    ################################################### SS API Query #####################################################
    
    query_params = {'fields': args.meta_params}
    
    # Define the API endpoint URL
    url = 'https://api.semanticscholar.org/graph/v1/paper/search'
    
    # Download information of interest
    # paper_id = get_paper(args.title, url, filename=args.title + '.pdf')
    paper_id = "e6ac2e5fdeb3f2d94efeeee5639c06cba2248f4e"
    print(paper_id)
    if paper_id:
        time.sleep(5)
        query_semantic_scholar(query_params, paper_id, filename=args.title + '.json')
    
    return

if __name__ == "__main__":
    main()  