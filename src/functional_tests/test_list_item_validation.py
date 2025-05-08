from .base import FunctionalTest
from unittest import skip
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class ItemValidationTest(FunctionalTest):
    
    def get_error_element(self):
        return  self.browser.find_element(
                    By.CSS_SELECTOR,".invalid-feedback"
                )

    def test_cannot_add_empty_list_items(self):
        # goes to home page
        # add empty list item
        # user hits enter
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)
        
        # return # Todo : re-enable the rest of this test
        # page refreshes
        # The browser intercepts the request, and does not load the list page
        self.wait_for(
            lambda: self.browser.find_element(By.CSS_SELECTOR,"#id_text:invalid"),
        )
        # enters some text 
        self.get_item_input_box().send_keys("Purchase milk")
        self.wait_for(
            lambda: self.browser.find_element(By.CSS_SELECTOR, "#id_text:valid")  
        )
        # & hit enter it works now
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Purchase milk")
        
        # Perversely, she now decides to submit a second blank list item
        self.get_item_input_box().send_keys(Keys.ENTER)

        # Again, the browser will not comply
        self.wait_for_row_in_list_table("1: Purchase milk")
        self.wait_for(
            lambda: self.browser.find_element(By.CSS_SELECTOR, "#id_text:invalid")
        )

        # And she can make it happy by filling some text in
        self.get_item_input_box().send_keys("Make tea")
        self.wait_for(
            lambda: self.browser.find_element(
                By.CSS_SELECTOR,
                "#id_text:valid",
            )
        )
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("2: Make tea")
        
        
    def test_cannot_add_duplicate_items(self):
         # user goes to home page and starts a new list
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys("Buy fruits")
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy fruits")
        
        # user tries to enter a duplicate list
        self.get_item_input_box().send_keys("Buy fruits")
        self.get_item_input_box().send_keys(Keys.ENTER)
            
        # gets an helpful error message
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_element(By.CSS_SELECTOR,".invalid-feedback").text,
                "You've already got this in your list"
            )
        )
        
    def test_error_messages_are_cleared_on_input(self):
        # start a list and causes an validation error
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys("Exercise")
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Exercise")
        
        self.get_item_input_box().send_keys("Exercise")
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for(
            lambda: self.assertTrue(
                self.get_error_element()
                .is_displayed()
            )
        )
        
        # starts typing in the input box to clear the error
        self.get_item_input_box().send_keys("a")

        # error message disappares 
        self.wait_for(
            lambda:self.assertFalse(
                self.get_error_element().is_displayed()
            )
        )
        