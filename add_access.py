from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
import csv

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 3)

driver.get("https://fsu-flvc.primo.exlibrisgroup.com/discovery/search?query=any,contains,&tab=Everything&search_scope=MyInst_and_CI&vid=01FALSC_FSU:Home&facet=rtype,include,books,lk&facet=tlevel,include,online_resources,lk&lang=en&offset=0")

# open the csv file loop and through the ISBN values
with open('data/alma_linked_list.csv', newline='') as etextbooks:
    reader = csv.DictReader(etextbooks)

    previous_entry = {
        'isbn': '',
        'access_model': ''
    }

    with open('data/access_models.csv', 'a', newline='') as output:
        writer = csv.writer(output)

        # loop through the imported values: search by ISBN, view item record, grab access model, add to list
        for index, row in enumerate(reader):
            # if program crashes, check generated csv for last value n and update condition to ignore first n rows: (if index < n)
            # NOTE: if output file has 100 rows, it FOUND 99 entries (because of the header), which means IGNORE indicies 0-98, which is index < 99
            if index < 0:
                continue

            # if current book is same as previous book, copy access info and continue to next iteration
            if row['FSU_TXBK_ISBN'] == previous_entry['isbn']:
                writer.writerow([previous_entry['access_model']])
                continue

            #add slight delay to avoid Primo reloading too quickly
            time.sleep(1)

            isbn_search = driver.find_element(By.ID, 'searchBar')
            isbn_search.clear()
            isbn_search.send_keys([row['FSU_TXBK_ISBN']])
            isbn_search.send_keys(Keys.RETURN)

            # if book is found, add the record; otherwise, mark it to be reviewed later
            try:
                record_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'h3.item-title>a.md-primoExplore-theme')))
            except:
                isbn_search.clear()
                isbn_search.send_keys([row['FSU_TXBK_TITLE']])
                isbn_search.send_keys(Keys.RETURN)
                try:
                    record_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'h3.item-title>a.md-primoExplore-theme')))
                except:
                    writer.writerow(['MANUAL REVIEW TITLE'])
                    previous_entry['access_model'] = 'MANUAL REVIEW TITLE'
                    continue

            record_link.click()

            try:
                access = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'h4>span')))[1]
                writer.writerow([access.text])
                previous_entry['access_model'] = access.text
            except:
                writer.writerow(['MANUAL REVIEW ACCESS MODEL'])
                previous_entry['access_model'] = 'MANUAL REVIEW ACCESS MODEL'
            
            previous_entry['isbn'] = row['FSU_TXBK_ISBN']