import os
import time
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

MAX_WAIT = 5

# As a rule of thumb, we usually only run the functional tests once all the unit tests are passing, 
# so if in doubt, try both!

class FunctionalTest(StaticLiveServerTestCase):
    
    
    
    def setUp(self):
        self.browser = webdriver.Firefox()
        test_server = os.environ.get("TEST_SERVER")
        # print(test_server)
        # on mac command is : env TEST_SERVER=localhost:8888 ./manage.py test functional_tests --failfast
        if test_server:
            self.live_server_url = "http://" + test_server
        
    def tearDown(self):
        self.browser.quit()
        
    def wait_for_row_in_list_table(self, row_text):
            start_time = time.time()
            while True:  
                try:
                    table = self.browser.find_element(By.ID, "id_list_table")  
                    rows = table.find_elements(By.TAG_NAME, "tr")
                    self.assertIn(row_text, [row.text for row in rows])
                    return  
                except (AssertionError, WebDriverException):  
                    if time.time() - start_time > MAX_WAIT:  
                        raise  
                    time.sleep(0.5)  
    
    def wait_for(self, fn):
            start_time = time.time()
            while True:  
                try:
                    return  fn()
                except (AssertionError, WebDriverException):  
                    if time.time() - start_time > MAX_WAIT:  
                        raise  
                    time.sleep(0.5)  
    
    def get_item_input_box(self):
        return self.browser.find_element(By.ID,"id_text")