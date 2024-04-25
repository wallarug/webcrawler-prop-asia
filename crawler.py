#!/usr/bin/env python

import requests

# This script searches all blog posts on the site and then searches for the keyword.
# If the keyword is found in the blog post, the script will print the URL of the blog post and
#  create a record for it.  
# A later version of the script will then download the relevant document

class Entry:
    def __init__(self, url, title, published_date, author, tags, document_url):
        self.url = url
        self.id = title

        self.published_date = published_date
        self.author = author
        self.tags = tags
        self.document_url = document_url

    def __str__(self):
        return f'{self.id} - {self.published_date}'
    
    def __repr__(self):
        return f'{self.id} - {self.published_date}'
    
    # export a line for a CSV export file
    def csv_line(self):
        return f'{self.id},{self.published_date},{self.author},{self.tags},{self.document_url},{self.url}'
    
    # download the document and save into give path
    def download_document(self, path):
        r = requests.get(self.document_url)
        with open(path, 'wb') as f:
            f.write(r.content)
    

# HTML website parser (specific to the website)
def parse_html(html):
    # parse the HTML and return the data
    
    ## TITLE
    # find <div class="post-title"> and extract the title from the h2 tag
    pt_index = html.find('<div class="post-title">')
    # find the end of the h2 block (nearby)
    end_index = html.find('</h2>', pt_index)
    # find the start of the title (nearby)
    start_index = html.find(">", pt_index + 24)
    # extract the title
    title = html[start_index+1:end_index]

    ## META BLOCK
    meta_start_index = html.find('<ul class="post-meta">')
    meta_end_index = html.find('</ul>', meta_start_index)

    ## PUBLISHED DATE - 1st part of the meta block ("Published on" date)
    # find the text "Published on" in the meta block, then do a fine grained search for the date
    published_index = html.find('Published on', meta_start_index, meta_end_index)
    start_index = html.find('>', published_index)
    end_index = html.find('</', start_index)
    published_date = html[start_index+1:end_index]
    
    ## AUTHOR - 2nd part of the meta block ("Written by" author)
    # find the text "Written by" in the meta block, then do a fine grained search for the date
    author_index = html.find('Written by', meta_start_index, meta_end_index)
    start_index = html.find('>', author_index)
    end_index = html.find('</', start_index)
    author = html[start_index+1:end_index]

    ## TAGS - 3rd part of the meta block ("Tagged as" tags)
    # find the text "Tagged as" in the meta block, then do a fine grained search for the date
    tags_index = html.find('Tagged as', meta_start_index, meta_end_index)
    start_index = html.find('>', tags_index)
    end_index = html.find('</', start_index)
    tags = html[start_index+1:end_index]

    ## DOCUMENT URL - find the text "Document: " after meta block and extract from a href tag
    doc_index = html.find('Document:', meta_end_index)
    start_index = html.find('href="', doc_index)
    end_index = html.find('">', start_index + 6)
    document_url = html[start_index + 6:end_index]

    return title, published_date, author, tags, document_url


# main function
def main():
    # storage for entries
    entries = []

    # search for all blog posts in range 1 to 10,000 until no more blog posts are found (404 error)
    for i in range(1, 5000):
        url = f'https://propertycloud.asia/news/{i}'
        r = requests.get(url)
        if r.status_code == 404:
            break

        # search for keyword in the blog post - replace 'keyword' with the actual keyword
        if 'Mangioni Property' in r.text:
            # create a record for the blog post
            #print("Found keyword in", url)
            title, published_date, author, tags, document_url = parse_html(r.text)
            entry = Entry(url, title, published_date, author, tags, document_url)
            entries.append(entry)
            print(str(i) + " " + entry)
            # download the document
            #entry.download_document(f'docs/{entry.id}.pdf')
        else:
            print("Not found in: ", i)

    # save all records to a CSV file
    with open('entries.csv', 'w') as f:
        f.write('id,published_date,author,tags,document_url,url\n')
        for entry in entries:
            f.write(entry.csv_line() + '\n')


if __name__ == '__main__':
    main()
    print("Completed.")