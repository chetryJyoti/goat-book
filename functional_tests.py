# from selenium import webdriver
# browser = webdriver.Firefox()

# # Edith has heard about a cool new online to-do app
# # She goes to check out its home page
# browser.get("http://localhost:8000")

# # She notices the page title and header mentioned to-do lists
# assert "To-do" in browser.title

# # She is invited to enter a to-do ite straight away

# # She types "Buy peacock feathers" into a text box
# # (Edith's hobby is tying fly-fishing lures)

# # When she hit enter, the page updates, and now the page lists
# # "1: Buy peacock featers" as an item in a to-do list

# # There is still a text box inviting her to add another item.
# # She enters "Use peacock feathers to make a fly"

# # This page updates again, and now shows both items on her list

# # Satisfied, she goes back to sleep

# browser.quit()


# using unittest
import unittest
from selenium import webdriver

class NewVisitorTest(unittest.TestCase):
    
    def setUp(self):
        self.browser = webdriver.Firefox()
        
    def tearDown(self):
        self.browser.quit()
    
    def test_can_start_a_todo_list(self):
        # Edith has heard about a cool new online to-do app
        # She goes to check out its home page
        self.browser.get("http://localhost:8000")
        
        
        # She notices the page title and header mentioned to-do lists
        # assert "To-do" in browser.title
        self.assertIn("To-Do",self.browser.title)
        
        # She is invited to enter a to-do item straight away
        self.fail("Finish the test!")
        
        

if __name__ == "__main__":
     unittest.main()