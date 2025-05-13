from selenium import webdriver
from selenium.webdriver.common.by import By

from .base import FunctionalTest
from .list_page import ListPage
from .my_lists_page import MyListsPage

def quit_if_possible(browser):
    try:
        browser.quit()
    except:
        pass

class SharingTest(FunctionalTest):
    def test_can_share_a_list_with_another_user(self):
        # Edith is a logged-in user
        self.create_pre_authenticated_session("edith@example.com")
        edith_browser = self.browser
        self.addCleanup(lambda: quit_if_possible(edith_browser))

        # Edith goes to the home page and starts a list
        self.browser = edith_browser
        self.browser.get(self.live_server_url)
        list_page = ListPage(self).add_list_item("Get help")

        # She notices a "Share this list" option
        share_box = self.browser.find_element(By.CSS_SELECTOR, 'input[name="sharee"]')
        self.assertEqual(
            share_box.get_attribute("placeholder"),
            "your-friend@example.com",
        )
        # shares her list with Onesiphorus
        list_page.share_list_with('onesiphorus@example.com')
        
        # Now we simulate Onesiphorus browsing the site in the same test run (using a different session)
        # Simulate Onesiphorus as if it's another browser session
        self.browser = webdriver.Firefox()
        self.addCleanup(lambda: quit_if_possible(self.browser))
        self.create_pre_authenticated_session("onesiphorus@example.com")
    
        # Onesiphorus goes to his browser and visits the "My Lists" page
        MyListsPage(self).go_to_my_lists_page('onesiphorus@example.com')

        # He sees Edith's list in his "My Lists"
        self.browser.find_element(By.LINK_TEXT, 'Get help').click()

        # On the list page, Onesiphorus sees that it's Edith's list
        self.wait_for(
            lambda: self.assertEqual(list_page.get_list_owner(), "edith@example.com")
        )

        # He adds an item to the list
        list_page.add_list_item("Hi Edith!")

        # Now we check if Onesiphorus's email is next to the item he added
        self.wait_for(
            lambda: self.assertIn(
                "onesiphorus@example.com", [row.text for row in list_page.get_table_rows()]
            )
        )

        # When Edith refreshes the page, she sees Onesiphorus's addition
        self.browser = edith_browser
        self.browser.refresh()
        list_page.wait_for_row_in_list_table("Hi Edith!", 2)

        # Clean up both browser sessions
        quit_if_possible(edith_browser)
        quit_if_possible(self.browser)
