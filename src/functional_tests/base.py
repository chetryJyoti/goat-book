import os
import time
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.conf import settings
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from .container_commands import reset_database,create_session_on_server
from .management.commands.create_session import create_pre_authenticated_session

MAX_WAIT = 5


def wait(fn):
        def modified_fn(*args,**kwargs):
            start_time = time.time()
            while True:  
                try:
                    return fn(*args,**kwargs)
                except (AssertionError, WebDriverException) as e:  
                    if time.time() - start_time > MAX_WAIT:  
                        raise e
                    time.sleep(0.5)  
        return modified_fn    

# As a rule of thumb, we usually only run the functional tests once all the unit tests are passing, 
# so if in doubt, try both!

class FunctionalTest(StaticLiveServerTestCase):
    
    def setUp(self):
        options = Options()
        options.add_argument("-headless") 
        self.browser = webdriver.Firefox(options=options)
        self.test_server = os.environ.get("TEST_SERVER")
        # print(test_server)
        # on mac command is : env TEST_SERVER=localhost:8888 ./manage.py test functional_tests --failfast
        if self.test_server:
            self.live_server_url = "http://" + self.test_server
            reset_database(self.test_server)
        
    def tearDown(self):
        self.browser.quit()
        
    def get_item_input_box(self):
        return self.browser.find_element(By.ID,"id_text")
    
    def add_list_item(self, item_text):
        num_rows = len(self.browser.find_elements(By.CSS_SELECTOR, "#id_list_table tr"))
        self.get_item_input_box().send_keys(item_text)
        self.get_item_input_box().send_keys(Keys.ENTER)
        item_number = num_rows + 1
        self.wait_for_row_in_list_table(f"{item_number}: {item_text}")
        

    
    @wait
    def wait_for(self,fn):
        return fn()
        
    @wait
    def wait_for_row_in_list_table(self, row_text):
        rows = self.browser.find_elements(By.CSS_SELECTOR, "#id_list_table tr")
        self.assertIn(row_text, [row.text for row in rows])
 
    @wait
    def wait_to_be_logged_in(self, email):
        self.browser.find_element(By.CSS_SELECTOR, "#id_logout"),
        navbar = self.browser.find_element(By.CSS_SELECTOR, ".navbar")
        self.assertIn(email, navbar.text)
        
    @wait
    def wait_to_be_logged_out(self, email):
        self.browser.find_element(By.CSS_SELECTOR, "input[name=email]")
        navbar = self.browser.find_element(By.CSS_SELECTOR, ".navbar")
        self.assertNotIn(email, navbar.text)
        
        
    def create_pre_authenticated_session(self, email):
        # user = User.objects.create(email=email)
        # session = SessionStore()
        # session[SESSION_KEY] = user.pk 
        # session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        # session.save()
        if self.test_server:
            session_key = create_session_on_server(self.test_server, email)
        else:
            session_key = create_pre_authenticated_session(email)
        ## to set a cookie we need to first visit the domain.
        ## 404 pages load the quickest!
        self.browser.get(self.live_server_url + "/404_no_such_url/")
        self.browser.add_cookie(
            dict(
                name=settings.SESSION_COOKIE_NAME,
                value=session_key,  
                path="/",
            )
        )