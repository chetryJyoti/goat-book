from .base import FunctionalTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class LayoutAndStylingTest(FunctionalTest):
     def test_layout_and_styling(self):
        # goes to url
        self.browser.get(self.live_server_url)

        # browser window is set to very specific size
        self.browser.set_window_size(1024,768)

        # input box should be in center
        inputbox = self.get_item_input_box()
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width']/2,
            512,
            delta=10
        )
        
        # starts a new list and the input box should be center here also
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: testing')
        inputbox = self.get_item_input_box()

        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width']/2,
            512,
            delta=10
        )
        
        
