
import requests
from bs4 import BeautifulSoup as bs
from ScraperExceptions import *
import re
import datetime
import logging
import json


LOG_FILE_NAME = r"C:\PythonExperiments\mambaScraperLog.log"
LOG_FORMAT = "%(levelname)s %(asctime)s  - %(message)s"
logger = None


def pageScrapper(page_id,ncchanged):
    logger.info(f"Starting scrap of page: {page_id}")
    profile_ulr = f"https://www.mamba.ru/mb{page_id}?sp=1&noid={page_id}&nchanged={ncchanged}&nactive=0#/app"

    profile_ulr2 = f"https://www.mamba.ru/mb{page_id}sp=1#/app"
    resp = requests.get(profile_ulr, verify=False)
    logger.info("Activation of soup")
    soup = bs(resp.text, 'html.parser')
    logger.info("Soup completed")


    languages = soup.findAll(class_= "b-list_item rtl-fix-last-symbol")
    #for language in languages:
    #print(language.string)
    #logger.info("After printing")

    #site_form = soup.findAll(class_="b-anketa_inset-form clearfix b-anketa_inset-form-js")
    site_form = soup.findAll(class_ = "b-anketa_field")
    fields = []
    for element in site_form:
        #print("*"*50)
        for subelement in element:
            logger.info(subelement)
            if len (str(subelement))>2:
                #print(str(subelement.string))
                fields.append(str(subelement.string))
                logger.info(str(subelement.string))

    logger.info("End of parsing")
    logger.info("Starting to create form")

    last_key = ""
    form = {}
    index = 0
    for field in fields:
        if index%2 == 0:
            last_key = field
        else:
            form[last_key] = field
        index += 1


#    print(form)
    logger.info(f"Form value: {form}")


    return form


def scrap_list_of_candidates():
    candidates = []


    #candidates.append(create_candidate_tuple(1768083872,1556378214))
    candidates.append(create_candidate_tuple(1769624780, 1561748862))
    #candidates.append(create_candidate_tuple(1743808828, 1486588017))

    logger.info("End of process")

    for candidate in candidates:
        print("*" * 50)
        print(candidate)

    return


def create_candidate_tuple(page_id, ncchanged):
    logger.info(f"Creation of canididate tupe: {page_id}")
    profile_ulr = f"https://www.mamba.ru/mb{page_id}?sp=1&noid={page_id}&nchanged={ncchanged}&nactive=0#/app"
    return (page_id, profile_ulr, pageScrapper(page_id, ncchanged))


def get_list_of_candidates():
    logger.info(f"Starting scrap list of candidates")
    list_url = f"https://www.mamba.ru/search.phtml?rl=1&from_item=1#/app"

    filter_string = "web-search-infinite_search_results"
    # "Mb.ComponentManager.initComponent"
    resp = requests.get(list_url, verify=False)
    logger.info("Activation of soup")
    soup = bs(resp.text, 'html.parser')

    logger.info("Soup completed")
    list_element = soup.findAll("script")
    list_text = ""
    for element in list_element:
        if  filter_string in str(element):
            list_text = element.string.strip()


    start_json_data  = list_text.find("data:")+6
    end_json_data = list_text.find("literals")-10
    list_text = list_text[start_json_data:end_json_data]
    print(list_text)
    list_json = json.loads(list_text)
    print(list_json)
    return

if __name__=="__main__":
    logging.basicConfig(filename=LOG_FILE_NAME, level=logging.DEBUG, format=LOG_FORMAT, filemode="w")
    logger = logging.getLogger()
    logger.info("Start of the process")
    #scrap_list_of_candidates()
    get_list_of_candidates()