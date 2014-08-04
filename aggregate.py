from bs4 import BeautifulSoup
import urllib2
import json
import math
import sys
import time


def seek_index_url_by_page(page):
    return 'https://api.seek.com.au/v2/jobs/search?&keywords=&hirerId=&hirerGroup=&page={0}&classification=&subclassification=&graduateSearch=false&displaySuburb=&suburb=&location=5126&nation=&area=&isAreaUnspecified=false&worktype=&salaryRange=0-999999&salaryType=annual&dateRange=999&sortMode=ListedDate&include=expanded&_=1407118962922'.format(page)


def get_url(url):
    return urllib2.urlopen(url).read()

def get_seek_index_page(page):
    main = urllib2.urlopen(seek_index_url_by_page(page)).read()
    main = json.loads(main)
    print('Returning page ' + str(page))
    return main

def collectJobs(firstPage=False):
    jobs = []
    main = get_seek_index_page(1)
    jobs += main['data']
    if firstPage is False:
        totalCount = int(main['totalCount'])
        pages = int(math.ceil((totalCount / len(jobs))))
        print 'There should be ' + str(pages) + ' pages'
        for page in range(2,pages):
            jobs += get_seek_index_page(page)['data']
        
    return jobs

jobslist = collectJobs(True)
  
count = 0
with open('out.txt', 'w') as f:
    for job in jobslist:
        url = 'http://www.seek.co.nz/job/{0}'.format(job['id'])
        html_page = get_url(url)
        print('Fetched ' + str(url))
        soup = BeautifulSoup(html_page)
        out = soup.find("div", id="jobTemplate")
        style = out.find("style")
        if style != None:
            style.clear()
        out = out.get_text().strip()
        if out is None:
            print 'None'
            print(html_page)
        else:
            job['page'] = out
        f.write(str(job)+"\n")
        print('Wrote job')
        
