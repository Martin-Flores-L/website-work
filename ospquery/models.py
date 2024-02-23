# import os
# import pandas
# import time
# from datetime import datetime
# import pathlib
# from selenium import webdriver
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from selenium.common.exceptions import NoSuchElementException
# from selenium.common.exceptions import StaleElementReferenceException

# from django.db import models

# # Create your models here.

# prefs = {
#       "download.default_directory": "/content/Download/",
#       "download.directory_upgrade": True,
#       "download.prompt_for_download": False,
#   }

# service = Service(executable_path=r'/usr/bin/chromedriver')
# options = webdriver.ChromeOptions()
# options.add_argument('--headless')
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-blink-features=AutomationControlled')
# options.add_argument('--disable-dev-shm-usage')
# driver = webdriver.Chrome(service=service, options=options)
# ignored_exceptions_e =(NoSuchElementException,StaleElementReferenceException,)



# class OSP(models.Model):

#     osp_id = models.CharField(max_length=100)

#     def __str__(self):
#         return self.osp_id    

# class OSPQuery(models.Model):

#     osp_id = models.ForeignKey(OSP, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.osp_id
    
