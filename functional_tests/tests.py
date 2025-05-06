from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
import time

MAX_WAIT = 5

# As a rule of thumb, we usually only run the functional tests once all the unit tests are passing, so if in doubt, try both!
class NewVisitorTest(LiveServerTestCase):
    
    def setUp(self):
        self.browser = webdriver.Firefox()
        
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
                
    
    def test_can_start_a_todo_list(self):
        # Edith has heard about a cool new online to-do app
        # She goes to check out its home page
        self.browser.get(self.live_server_url)
        
        
        # She notices the page title and header mentioned to-do lists
        self.assertIn("To-Do",self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME,'h1').text
        self.assertIn("To-Do", header_text)
        
        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element(By.ID,'id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'),"Enter a to-do item")
        
        # # She types "Buy peacock feathers" into a text box
        # # (Edith's hobby is tying fly-fishing lures)
        inputbox.send_keys('Buy peacock feathers')

        # # When she hit enter, the page updates, and now the page lists
        # # "1: Buy peacock featers" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        # time.sleep(1)
        self.wait_for_row_in_list_table("1: Buy peacock feathers")
        
        # # There is still a text box inviting her to add another item.
        # # She enters "Use peacock feathers to make a fly"
        inputbox = self.browser.find_element(By.ID,'id_new_item')
        inputbox.send_keys("Use peacock feathers to make a fly")
        inputbox.send_keys(Keys.ENTER)
        # time.sleep(1)
        # # This page updates again, and now shows both items on her list
        
        self.wait_for_row_in_list_table("2: Use peacock feathers to make a fly")
        self.wait_for_row_in_list_table("1: Buy peacock feathers")
        
    
    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Edith starts a new 
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element(By.ID,"id_new_item")
        inputbox.send_keys("Buy peacock feathers")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy peacock feathers")

        # She notices that her list has a unique URL
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url,"/lists/.+")
        
        # new user comes in
        self.browser.delete_all_cookies()

        # visists the home page
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(By.TAG_NAME,"body").text
        self.assertNotIn("Buy peacock feathers",page_text)
        self.assertNotIn("make a fly",page_text)

        # enters new item
        inputbox = self.browser.find_element(By.ID,"id_new_item")
        inputbox.send_keys("Buy milk")
        inputbox.send_keys(Keys.ENTER)
        # time.sleep(1)
        self.wait_for_row_in_list_table("1: Buy milk")
        
        

        # gets his own unique url
        unique_url = self.browser.current_url
        self.assertRegex(unique_url,"/lists/.+")
        self.assertNotEqual(unique_url,edith_list_url)

        # check if there any trace of Edith's list
        page_text = self.browser.find_element(By.TAG_NAME,"body").text
        self.assertNotIn("Buy peacock feathers",page_text)
        self.assertIn("Buy milk",page_text)
    
    
    def test_layout_and_styling(self):
        # goes to url
        self.browser.get(self.live_server_url)

        # browser window is set to very specific size
        self.browser.set_window_size(1024,768)

        # input box should be in center
        inputbox = self.browser.find_element(By.ID,'id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width']/2,
            512,
            delta=10
        )
        
        # starts a new list and the input box should be center here also
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: testing')
        inputbox = self.browser.find_element(By.ID,"id_new_item")

        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width']/2,
            512,
            delta=10
        )
        
        