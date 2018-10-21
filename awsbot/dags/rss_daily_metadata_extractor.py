import requests
import urllib.request
import re
import time
import argparse
import pymysql.cursors
import pandas as pd
import feedparser
import datetime
import boto3 
now = datetime.datetime.now()
start = time.time()

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='password123',
                             db='arxivOverload',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
# create cursor to database
cursor = connection.cursor()

query = "SELECT arxiv_id FROM arxivOverload.METADATA"
metadata_table_dataframe = pd.read_sql(query, con=connection)

# Helper functions

db_arxiv_id = None


def extract_metadata(feed):
    '''
                Function: Extract all metadata from arxiv respose

                Input: takes api respose from arxiv, arxiv_id in our database

                Return: list of dictionaries
    '''
    global db_arxiv_id

    feed_title = feed.feed.title
    feed_upadted = feed.feed.updated
    opensearch_totalresults = feed.feed.opensearch_totalresults
    opensearch_itemsperpage = feed.feed.opensearch_itemsperpage
    opensearch_startindex = feed.feed.opensearch_startindex

    metadata_dict_list = []  # save dicts
    for entry in feed.entries:
        metadata_dict = {}  # save metadata respose into dict.
        arxiv_id = entry.id.split('/abs/')[-1]
        if arxiv_id not in db_arxiv_id:
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
        else:
            print(arxiv_id, " -> Alredy present in the database")
    return metadata_dict_list


try:
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='password123',
                                 db='arxivOverload',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    print("Connected with Database")
    # query = "SELECT arxiv_id FROM arxivOverload.METADATA"
    # metadata_table_dataframe = pd.read_sql(query, con=connection)
    # db_arxiv_id = metadata_table_dataframe['arxiv_id'].values
    # print(db_arxiv_id)
except RuntimeError as identifier:
    print(identifier.__cause__)
    print("Not able to connect with database")
    exit()


apis = [
    'astro-ph', 'cond-mat', 'cs', 'econ', 'eess', 'gr-qc', 'hep-ex', 'hep-lat',
    'hep-ph', 'hep-th', 'math', 'math-ph', 'nlin', 'nucl-ex', 'nucl-th',
    'physics', 'q-bio', 'q-fin', 'quant-ph', 'stat'
]
arr = []

for api in apis:
    response = requests.get("http://export.arxiv.org/rss/" + api)

    # f = open('response.txt', 'w')
    # f.write(str(response.text).replace('\n', ''))

    items = str(response.text).replace('\n', '')

    # f1 = open('response.txt', 'r')
    # items = f1.read()
    m = re.search('<rdf:Seq>(.+?)</rdf:Seq>', items)
    # print(m.group(1))
    print('doing for ' + api)
    a = re.split('"', m.group(1))
    a = a[1::2]
    for i in range(len(a)):
        a[i] = a[i].replace('http://arxiv.org/abs/', '')
    arr.extend(a)
    print('done for {} got {} records'.format(api, len(a)))

print('found total {} records'.format(len(arr)))


f2 = open(now.strftime("%Y-%m-%d %H:%M")+'.txt', 'w')
f2.write(str(arr))
end = time.time()
print(len(arr))
print(end - start)

base_url = 'http://export.arxiv.org/api/query?search_query='
urls = [
    'http://export.arxiv.org/api/query?search_query={0}'.format(str(element)) for element in arr]

for url in urls:
    response = urllib.request.urlopen(url).read()
    response = response.decode('utf-8')
    feed = feedparser.parse(response)
    data = extract_metadata(feed)
    print(data)
    print(len(data))
    cursor.executemany("""
			INSERT INTO METADATA (arxiv_id, title, abstract, primary_category, all_categories, author, last_author, authors, published, journal_ref, comment, abs_page_link, pdf_link)
			VALUES (%(arxiv_id)s, %(title)s, %(abstract)s, %(primary_category)s, %(all_categories)s, %(author)s, %(last_author)s, %(authors)s, %(published)s, %(journal_ref)s, %(comment)s, %(abs_page_link)s, %(pdf_link)s""", data)
    connection.commit()
connection.close()



