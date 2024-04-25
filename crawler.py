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
    start_index = html.find(">" + 24, pt_index)
    # extract the title
    title = html[start_index:end_index]

    ## PUBLISHED DATE - 1st part of the meta block ("Published on" date)
    meta_start_index = html.find('<ul class="post-meta">')
    # find the end of the ul block (nearby)
    meta_end_index = html.find('</ul>', meta_start_index)

    # find the end of the date (nearby) - before </a>
    end_index = html.find('</a>', meta_start_index, meta_end_index)
    # search for the ">" before the date
    start_index = html.rfind('>', meta_start_index, end_index)
    # extract the date
    published_date = html[start_index:end_index]

    ## AUTHOR - 2nd part of the meta block
    # find the end of the author (nearby) - before </a>




    pass



# main function
def main():
    # search for all blog posts in range 1 to 10,000 until no more blog posts are found (404 error)
    for i in range(2110, 10000):
        url = f'https://propertycloud.asia/news/{i}'
        r = requests.get(url)
        if r.status_code == 404:
            break

        # search for keyword in the blog post - replace 'keyword' with the actual keyword
        if 'keyword' in r.text:
            # create a record for the blog post
            entry = Entry(url, 'title', 'published_date', 'author', 'tags', 'document_url')
            print(entry)
            # download the document
            #entry.download_document(f'docs/{entry.id}.pdf')
