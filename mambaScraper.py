
import requests
from bs4 import BeautifulSoup as bs
from ScraperExceptions import *
import re
import datetime
import logging

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
    #    print(language.string)
    #logger.info("After printing")

    #site_form = soup.findAll(class_="b-anketa_inset-form clearfix b-anketa_inset-form-js")
    site_form = soup.findAll(class_ = "b-anketa_field")
    fields = []
    for element in site_form:
        #print("*"*50)
        for subelement in element:
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


def get_list_of_candidates():
    candidates = []

    temp_candidate = (1768083872,pageScrapper(1768083872, 1556378214) )
    candidates.append(temp_candidate)
    temp_candidate = (1769624780, pageScrapper(1769624780, 1561748862))
    candidates.append(temp_candidate)
    temp_candidate = (1743808828, pageScrapper(1743808828, 1486588017))
    candidates.append(temp_candidate)

    logger.info("End of process")

    for candidate in candidates:
        print("*" * 50)
        print(candidate)

    return



if __name__=="__main__":
    logging.basicConfig(filename=LOG_FILE_NAME, level=logging.DEBUG, format=LOG_FORMAT, filemode="w")
    logger = logging.getLogger()
    logger.info("Start of the process")
    get_list_of_candidates()