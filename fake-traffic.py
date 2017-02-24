import csv, random, os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

member_guids = []
with open('license-data.csv', 'rb') as csvfile:
    sniffer = csv.Sniffer()
    dialect = sniffer.sniff(csvfile.read(4096))
    csvfile.seek(0)
    reader = csv.reader(csvfile, dialect)
    first = True
    for row in reader:
        if first and sniffer.has_header:
            first = False
            continue
        member_guids.append(row[0])

chromedriver = "/opt/webdriver/chromedriver.exe"
os.environ["webdriver.chrome.driver"] = chromedriver

guids_len = len(member_guids)
print "Total member IDs: {}".format(guids_len)
guids_len = 350 # override to get only a subset of guids that we selected
total = 1
counts = {}
while total <= 30:
    guid = member_guids[total - 1]
    if not guid in counts:
        counts[guid] = 0
    counts[guid] += 1
    url = 'http://www.adobemarketinglab.com/content/hackathon3/en/brand/the-team.html?member_guid={}'.format(guid)

    print '({} total) Hitting url {} for the {} time'.format(total, url, counts[guid])
    driver = webdriver.Chrome(chromedriver)
    driver.set_page_load_timeout(10)
    try:
        driver.get(url)
        # driver.find_element_by_css_selector("a img").click()
        # element_present = EC.presence_of_element_located((By.ID, 'containerTTMbox'))
        # WebDriverWait(driver, 10).until(element_present)
    except Exception as e:
        print 'Encountered exception: {}'.format(e)
    finally:
        try:
            driver.quit()
        except:
            print 'Timed out: {}'.format(e)
    total += 1