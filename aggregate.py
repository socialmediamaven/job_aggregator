from bs4 import BeautifulSoup
import json
import math
import sys
import time
import os

pause = 2

# Python 3 urllib import with Python 2 fallback
try:
    import urllib.request as urllib2
except:
    import urllib2

def seek_index_url_by_page(page, location_id):
    return 'https://api.seek.com.au/v2/jobs/search?&keywords=&hirerId=&hirerGroup=&page={0}&classification=&subclassification=&graduateSearch=false&displaySuburb=&suburb=&location={1}&nation=3001&area=&isAreaUnspecified=false&worktype=&salaryRange=0-999999&salaryType=annual&dateRange=999&sortMode=ListedDate&include=expanded&_=1407118962922'.format(page, location_id)
    # return 'http://www.seek.co.nz/jobs/in-new-zealand/#dateRange=999&workType=0&industry=&occupation=&graduateSearch=false&salaryFrom=0&salaryTo=999999&salaryType=annual&advertiserID=&advertiserGroup=&keywords=&page={0}&displaySuburb=&seoSuburb=&isAreaUnspecified=false&location=&area=&nation=3001&sortMode=ListedDate&searchFrom=quick&searchType='.format(page, location_id)


def get_url(url):
    return urllib2.urlopen(url).read()

def get_seek_index_page(page, location_id):
    main = urllib2.urlopen(seek_index_url_by_page(page, location_id)).read()
    main = json.loads(str(main, encoding='UTF-8'))
    print('Returning page ' + str(page))
    return main

def dump_index(data):
    with open('index.json', 'a') as f:
        for job in data:
            bp = job['bulletPoints']
            bullets = "["
            comma = ''
            for b in bp:
                bullets += comma + '"' + b.replace("\\","\\\\").replace('"','\\"') + '"'
                comma = ','
            bullets += "]"
            

            f.write('{' + '"id":{0},"title":"{1}","teaser":"{2}","classification":"{3}","subClassification":"{4}","bulletPoints":{5},"salary":"{6}","workType":"{7}","location":"{8}","area":"{9}","suburb":"{10}","advertiser":"{11}","listingDate":"{12}"'.format(job['id'],
                                                                                                                                                                                                                                                                  job['title'].replace("\\","\\\\").replace('"','\\"'),
                                                                                                                                                                                                                                                                  job['teaser'].replace("\\","\\\\").replace('"','\\"'),
                                                                                                                                                                                                                                                                  job['classification']['description'].replace("\\","\\\\").replace('"','\\"'),
                                                                                                                                                                                                                                                                  job['subClassification']['description'].replace("\\","\\\\").replace('"','\\"'),
                                                                                                                                                                                                                                                                  bullets,
                                                                                                                                                                                                                                                                  job['salary'].replace("\\","\\\\").replace('"','\\"'),
                                                                                                                                                                                                                                                                  job['workType'].replace("\\","\\\\").replace('"','\\"'),
                                                                                                                                                                                                                                                                  job['location'].replace("\\","\\\\").replace('"','\\"'),
                                                                                                                                                                                                                                                                  job['area'].replace("\\","\\\\").replace('"','\\"'),
                                                                                                                                                                                                                                                                  job['suburb'].replace("\\","\\\\").replace('"','\\"'),
                                                                                                                                                                                                                                                                  job['advertiser']['description'].replace("\\","\\\\").replace('"','\\"'),
                                                                                                                                                                                                                                                                  job['listingDate'].replace("\\","\\\\").replace('"','\\"')) + "},\n")

def dump_job(job):
    with open('listings.json', 'a') as f:
        bp = job['bulletPoints']
        bullets = "["
        comma = ''
        for b in bp:
            bullets += comma + '"' + b.replace("\\","\\\\").replace('"','\\"') + '"'
            comma = ','
        bullets += "]"
        f.write('{' + '"id":{0},"title":"{1}","teaser":"{2}","classification":"{3}","subClassification":"{4}","bulletPoints":{5},"salary":"{6}","workType":"{7}","location":"{8}","area":"{9}","suburb":"{10}","advertiser":"{11}","listingDate":"{12}","listing":"{13}"'.format(job['id'],
                                                                                                                                                                                                                                                              job['title'].replace("\\","\\\\").replace('"','\\"'),
                                                                                                                                                                                                                                                              job['teaser'].replace("\\","\\\\").replace('"','\\"'),
                                                                                                                                                                                                                                                              job['classification'].replace("\\","\\\\").replace('"','\\"'),
                                                                                                                                                                                                                                                              job['subClassification'].replace("\\","\\\\").replace('"','\\"'),
                                                                                                                                                                                                                                                              bullets,
                                                                                                                                                                                                                                                              job['salary'].replace("\\","\\\\").replace('"','\\"'),
                                                                                                                                                                                                                                                              job['workType'].replace("\\","\\\\").replace('"','\\"'),
                                                                                                                                                                                                                                                              job['location'].replace("\\","\\\\").replace('"','\\"'),
                                                                                                                                                                                                                                                              job['area'].replace("\\","\\\\").replace('"','\\"'),
                                                                                                                                                                                                                                                              job['suburb'].replace("\\","\\\\").replace('"','\\"'),
                                                                                                                                                                                                                                                              job['advertiser'].replace("\\","\\\\").replace('"','\\"'),
                                                                                                                                                                                                                                                              job['listingDate'].replace("\\","\\\\").replace('"','\\"'),
                                                                                                                                                                                                                                                              job['listing'].replace("\\","\\\\").replace('"', '\\"')) + "},\n")

def collectJobs(location_id, pause, firstPage=False):
    try:
        print('Retreving index pages for ' + str(location_id))
        main = get_seek_index_page(1, location_id)
        dump_index(main['data'])

        if firstPage is False:
            totalCount = int(main['totalCount'])
            pages = int(math.ceil((totalCount / len(main['data']))))
            print('There are a total of ' + str(totalCount) + ' jobs')
            print('There should be ' + str(pages) + ' pages')
            print('Which should take ' + str(pages * pause) + ' seconds to scan or ' + str((pages*pause)/60.0) + ' minutes')
            for page in range(2,pages):
                time.sleep(pause)
                dump_index(get_seek_index_page(page, location_id)['data'])
        print("Finished scanning index")
    except KeyboardInterrupt:
        with open('index.json', 'a') as f:
            f.write("{}\n]")
        sys.exit()
    else:
        with open('index.json', 'a') as f:
            f.write("{}\n]")
    return True

def get_page_by_jobId(jobId):
    url = 'http://www.seek.co.nz/job/{0}'.format(job['id'])
    return get_url(url)


locations = {
    'Everywhere': ''
    # 'Auckland': 1018,
    # 'Hamilton': 5126,
}


# try:
#     os.remove('index.json')
# except FileNotFoundError:
#     pass
# with open('index.json', 'w') as f:
#     f.write("[\n")

# for location in locations:
#     collectJobs(locations[location], pause, False)

with open('index.json', 'r') as f:
    jobs = json.loads(f.read())

try:
    os.remove('full_list.json')
except FileNotFoundError:
    pass
with open('listings.json', 'w') as f:
    f.write("[\n")

totalCount = len(jobs)
print('There are a total of ' + str(totalCount) + ' jobs')
print('Which should take ' + str(totalCount * pause) + ' seconds to scan or ' + str((totalCount*pause)/60.0) + ' minutes')
hours = (totalCount*pause)/60.0/60.0
hours_per_job = hours/totalCount
print('Or ' + str((totalCount*pause)/60.0/60.0) + ' hours')

try:
    count = 0
    for job in jobs:
        count += 1
        page = get_page_by_jobId(job['id'])
        soup = BeautifulSoup(page)
        out = soup.find("div", id="jobTemplate")
        style = out.find("style")
        if style != None:
            style.clear()
        out = out.get_text().strip()
        if out is None:
            print('None')
        else:
            job['listing'] = out
        dump_job(job)
        time_remaining = hours - (hours_per_job*count)
        print("{0:0.3f}% complete, {1:0.3f} hours left".format((count/float(totalCount))*100, time_remaining))
        time.sleep(pause)
except KeyboardInterrupt:
    with open('listings.json', 'a') as f:
        f.write("{}\n]")
    sys.exit()
else:
    with open('listings.json', 'a') as f:
        f.write("{}\n]")
print("Finished fetching jobs")
