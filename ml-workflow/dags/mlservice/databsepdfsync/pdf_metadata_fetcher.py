PDF_DIR = "../data/pdf"

# Libraries
import requests
import urllib.request
import re
import feedparser
import boto3
import datetime
from elasticsearch import Elasticsearch
es = Elasticsearch(['https://search-researchkernel-634iskudbbrvfruaytepewyo3i.us-east-1.es.amazonaws.com'])

# clients
s3 = boto3.client('s3')

#elasticsearch config

INDEX_NAME = "paper_metadata"
TYPE_NAME = "papers"
ID_FIELD = "arxiv_id"


# connections
filename = 'data-engineering-service/arxivdailysync/' + \
    str(datetime.date.today()) + '.txt'
path = str(datetime.date.today()) + '.txt'
bucket_name = 'arxivoverload-developement'

# list of filenames
arr = []
DIR_LIST = os.listdir(PDF_DIR)
for filename in DIR_LIST:
    filenames = re.split('(\d+)',filename) # Regex for spliting text and number
    filenames = filenames[0:-1]            # Exclude last null value
    filenames = "/".join(filenames)        # Join filenames with /   
    if filenames[0] == "/":                # if start with "/" then
        # print(filenames)  
        file, file_extension = os.path.splitext(PDF_DIR+"/"+filename) # extract file name. 
        file =file.replace(PDF_DIR, "")                           # remove extension.
        file = file.replace("/", "")
        file = file.replace(".pdf", "")
        # print(file)
        arr.append(file)                                         # append filename to list
    else:                                   
        arr.append(filenames)               # else append to list
        

def extract_metadata(feed):
    '''
                Function: Extract all metadata from arxiv respose

                Input: takes api respose from arxiv, arxiv_id in our database

                Return: list of dictionaries
    '''
    feed_title = feed.feed.title
    feed_upadted = feed.feed.updated
    opensearch_totalresults = feed.feed.opensearch_totalresults
    opensearch_itemsperpage = feed.feed.opensearch_itemsperpage
    opensearch_startindex = feed.feed.opensearch_startindex

    metadata_dict_list = []  # save dicts
    for entry in feed.entries:
        metadata_dict = {}  # save metadata respose into dict.
        arxiv_id = entry.id.split('/abs/')[-1]
        print("fetched id:", arxiv_id)
        published = entry.published
        title = entry.title
        author_string = entry.author
        try:
            author_string += ' (%s)' % entry.arxiv_affiliation
        except AttributeError:
            pass
        last_author = author_string

        # feedparser v5.0.1 correctly handles multiple authors, print them all
        try:
            Authors = (', ').join(author.name for author in entry.authors)
        except AttributeError:
            pass
            # get the links to the abs page and pdf for this e-print
        for link in entry.links:
            if link.rel == 'alternate':
                abs_page_link = link.href
                print(abs_page_link)
            elif link.title == 'pdf':
                # The journal reference, comments and primary_category sections live under # the arxiv namespace
                pdf_link = link.href
        try:
            journal_ref = entry.arxiv_journal_ref
        except AttributeError:
            journal_ref = 'No journal ref found'
        try:
            comment = entry.arxiv_comment
        except AttributeError:
            comment = 'No comment found'
        primary_category = entry.tags[0]['term']
        # Lets get all the categories
        all_cat = [t['term'] for t in entry.tags]
        all_categories = (', ').join(all_cat)
        # The abstract is in the <summary> element
        Abstract = entry.summary
        metadata_dict['arxiv_id'] = arxiv_id
        metadata_dict['title'] = title
        metadata_dict['abstract'] = Abstract
        metadata_dict['primary_category'] = primary_category
        metadata_dict['all_categories'] = all_categories
        metadata_dict['author'] = author_string
        metadata_dict['last_author'] = last_author
        metadata_dict['authors'] = Authors
        metadata_dict['published'] = published
        metadata_dict['journal_ref'] = journal_ref
        metadata_dict['comment'] = comment
        metadata_dict['abs_page_link'] = abs_page_link
        metadata_dict['pdf_link'] = pdf_link
        metadata_dict_list.append(metadata_dict)
    return metadata_dict_list

f2 = open(str(datetime.date.today())+'.txt', 'w')
f2.write(str(arr))
base_url = 'http://export.arxiv.org/api/query?search_query='
urls = ['http://export.arxiv.org/api/query?search_query={0}'.format(str(element)) for element in arr[]]
for url in urls:
    response = urllib.request.urlopen(url).read()
    response = response.decode('utf-8')
    feed = feedparser.parse(response)
    data = extract_metadata(feed)
    for node in data:
        _id = node['arxiv_id']
        es.index(index='data', doc_type='paper_metadata', id=_id, body=node)

s3.upload_file(path, bucket_name, filename)


