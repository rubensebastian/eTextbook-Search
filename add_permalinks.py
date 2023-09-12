import requests
import csv

count = 0

api_key = 'REPLACE_WITH_PASSWORD'

new_etext_list = []

# with open('/data/full_isbn_etexts.csv', newline='') as etext_list:
with open('data/isbn_mini.csv', newline='') as etext_list:
    etext_reader = csv.DictReader(etext_list)

    for etext_row in etext_reader:
        try:
            print(etext_row['FSU_TXBK_ISBN'])
            # SEND REQUEST TO API AND CONVERT RESPONSE TO JSON OBJECT
            response = requests.get('https://api-na.hosted.exlibrisgroup.com/primo/v1/search?vid=01FALSC_FSU:Home&tab=default_tab&scope=default_scope&q=isbn,exact,' + str(
                etext_row['FSU_TXBK_ISBN']) + '&qInclude=facet_tlevel,exact,online_resources&apikey=' + str(api_key)).json()
            #while looping, set FOUND to true when found, after one bad pass, set FLAGGED to true
            # READ 'recordid' FIELD FROM RESPONSE JSON
            recordid = str(response['docs'][0]['pnx']
                           ['control']['recordid'][0])

            # CREATE PUBLIC LINK USING RECORDID VALUE
            matchURL = 'https://fsu-flvc.primo.exlibrisgroup.com/discovery/fulldisplay?docid=' + \
                recordid + '&vid=01FALSC_FSU:Home&lang=en&search_scope=MyInst_and_CI'

        except:
            matchURL = 'NONE'
        new_etext_list.append(matchURL)

#First files contains unlinked list of etexts, writing results to second file
def add_permalink_data(non_permalinked_etexts, permalinked_etexts):
    with open(permalinked_etexts, 'w', newline='') as permalinked_list:
        fieldnames = ['Prefix','Number','Section','ISBN','Author','Title','Edition','Permalink']
        permalinked_writer = csv.DictWriter(permalinked_list, fieldnames=fieldnames)

        with open(non_permalinked_etexts, newline='') as etext_list:
            etext_reader = csv.DictReader(etext_list)
            for etext_row in etext_reader:
                #find the alternate ISBNs for a given ISBN here or use given if none found
                possible_ISBNs = [etext_row['FSU_TXBK_ISBN']]
                found = False
                flagged = False
                for isbn in possible_ISBNs:
                    try:
                        # SEND REQUEST TO API AND CONVERT RESPONSE TO JSON OBJECT
                        response = requests.get('https://api-na.hosted.exlibrisgroup.com/primo/v1/search?vid=01FALSC_FSU:Home&tab=default_tab&scope=default_scope&q=isbn,exact,' + str(
                            isbn) + '&qInclude=facet_tlevel,exact,online_resources&apikey=' + str(api_key)).json()
                        #while looping, set FOUND to true when found, after one bad pass, set FLAGGED to true
                        # READ 'recordid' FIELD FROM RESPONSE JSON
                        alma_record_id = str(response['docs'][0]['pnx']
                                    ['control']['recordid'][0])

                        # CREATE PUBLIC LINK USING RECORDID VALUE
                        permalink_URL = 'https://fsu-flvc.primo.exlibrisgroup.com/discovery/fulldisplay?docid=' + \
                            alma_record_id + '&vid=01FALSC_FSU:Home&lang=en&search_scope=MyInst_and_CI'
                        found = True#how to use value from outside the loop

                    except:
                        flagged = True