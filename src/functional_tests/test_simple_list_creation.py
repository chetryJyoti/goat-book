from .base import FunctionalTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
                
class NewVisitorTest(FunctionalTest):
   
    def test_can_start_a_todo_list(self):
        # Edith has heard about a cool new online to-do app
        # She goes to check out its home page
        self.browser.get(self.live_server_url)
        
        
        # She notices the page title and header mentioned to-do lists
        self.assertIn("To-Do",self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME,'h1').text
        self.assertIn("To-Do", header_text)
        
        # She is invited to enter a to-do item straight away
        inputbox = self.get_item_input_box()
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
        inputbox = self.get_item_input_box()
        inputbox.send_keys("Use peacock feathers to make a fly")
        inputbox.send_keys(Keys.ENTER)
        # time.sleep(1)
        # # This page updates again, and now shows both items on her list
        
        self.wait_for_row_in_list_table("2: Use peacock feathers to make a fly")
        self.wait_for_row_in_list_table("1: Buy peacock feathers")
        
    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Edith starts a new 
        self.browser.get(self.live_server_url)
        inputbox = self.get_item_input_box()
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
        inputbox = self.get_item_input_box()
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
    
