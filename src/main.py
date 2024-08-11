from argparse import ArgumentParser
from download_papers import *

def main():

    ################################################### Arg Parsing #####################################################
    # Parsing model from command line
    parser = ArgumentParser()
    parser.add_argument('--title', type=str, required=True, help='Title of the paper.')
    parser.add_argument('--download', type=bool, required=True, help='Whether or not to attempt to download the full text of the paper.')
    parser.add_argument('--meta_params', type=str, required=True, help='Meta info to be retrieved, see readme for structure. If true saved as json in data dir.')
    args = parser.parse_args()

    ################################################### SS API Query #####################################################
    
    # Define the API endpoint URL
    url = 'https://api.semanticscholar.org/graph/v1/paper/search'

    meta_info = query_semantic_scholar(args.title)
    if args.download:
        pdf_link = get_paper(args.title, url)
        if pdf_link:
            download_file(pdf_link, filename=args.title + '.txt')

            


if __name__ == "__main__":
    main()  