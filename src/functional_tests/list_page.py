from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import wait

class ListPage:
    def __init__(self, test):
        self.test = test  
        print("[ListPage] Initialized ListPage")

    def get_table_rows(self):  
        rows = self.test.browser.find_elements(By.CSS_SELECTOR, "#id_list_table tr")
        print(f"[ListPage] Found {len(rows)} rows in table")
        return rows

    @wait
    def wait_for_row_in_list_table(self, item_text, item_number):  
        expected_row_text = f"{item_number}: {item_text}"
        print(f"[ListPage] Waiting for row: '{expected_row_text}'")
        rows = self.get_table_rows()
        row_texts = [row.text for row in rows]
        print(f"[ListPage] Current rows: {row_texts}")
        self.test.assertIn(expected_row_text, row_texts)

    def get_item_input_box(self):  
        print("[ListPage] Looking for item input box")
        return self.test.browser.find_element(By.ID, "id_text")

    def add_list_item(self, item_text):  
        new_item_no = len(self.get_table_rows()) + 1
        print(f"[ListPage] Adding list item: '{item_text}' at position {new_item_no}")
        self.get_item_input_box().send_keys(item_text)
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table(item_text, new_item_no)
        return self  
    
    def get_share_box(self):
        print("[ListPage] Looking for share input box")
        return self.test.browser.find_element(
            By.CSS_SELECTOR,
            'input[name="sharee"]'
        )
        
    def get_shared_with_list(self):
        shared = self.test.browser.find_elements(
            By.CSS_SELECTOR,
            ".list-sharee",
        )
        print(f"[ListPage] Shared with: {[item.text for item in shared]}")
        return shared
    
    def share_list_with(self, email):
        print(f"[ListPage] Sharing list with: {email}")
        self.get_share_box().send_keys(email)
        self.get_share_box().send_keys(Keys.ENTER)
        self.test.wait_for(
            lambda: self.test.assertIn(
                email, [item.text for item in self.get_shared_with_list()]
            )
        )

    @wait
    def get_list_owner(self):
        print("[ListPage] Getting list owner...")
        owner = self.test.browser.find_element(By.ID, "id_list_owner").text
        print(f"[ListPage] List owner is: {owner}")
        return owner
