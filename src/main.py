from download_papers import *

def main():

    
    pdf_link = query_semantic_scholar(pub_title)
    if pdf_link:
        filename = strip_special_characters(pub_title) + ".pdf"
        download_file(pdf_link, filename=filename)

            


if __name__ == "__main__":
    main()  