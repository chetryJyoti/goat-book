from .base import FunctionalTest
from unittest import skip
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # goes to home page
        # add empty list item
        # user hits enter
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)
        
        # return # Todo : re-enable the rest of this test
        # page refreshes
        # gets warning saying cannot save empty lists
        self.wait_for(
            lambda: self.assertEqual(
            self.browser.find_element(By.CSS_SELECTOR,".invalid-feedback").text,
            "You can't have an empty list item"
        )
        )
        # enters some text & hit enter it works now
        self.get_item_input_box().send_keys("Purchase milk")
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Purchase milk")
        
    
        # again tries to enter blank item
        self.get_item_input_box().send_keys(Keys.ENTER)
        # receives a similar warning on the list page
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_element(By.CSS_SELECTOR, ".invalid-feedback").text,
                "You can't have an empty list item",
            )
        )
     
        
        # she can correct it by filling some text in
        self.get_item_input_box().send_keys("Make tea")
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("2: Make tea")
            