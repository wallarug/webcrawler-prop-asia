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
    

# main function
def main():
    # search for all blog posts in range 1 to 10,000 until no more blog posts are found (404 error)
    for i in range(1, 10000):
        url = f'https://www.example.com/blog/{i}'
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
