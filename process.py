
jobs_tmp = []
with open('out.txt', 'r') as f:
    for line in f:
        eval("jobs_tmp.append("+line+")")

jobs = []
for job in jobs_tmp:
    jobs.append({
        'page': job['page'].replace('\r',' ').replace('\n', ' ').replace('\xa0',' '),
        'location': job['location'],
        'teaser': job['teaser'],
        'title': job['title'],
        'area': job['area'],
        'salary': job['salary'],
        'type': job['workType'],
        'suburb': job['suburb'],
        'class': job['classification']['description'],
        'subclass': job['subClassification']['description'],
        'points': job['bulletPoints']
    })

for job in jobs:
    print('')
    print(job)

