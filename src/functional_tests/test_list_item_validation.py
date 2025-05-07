from .base import FunctionalTest
from unittest import skip

        
class ItemValidationTest(FunctionalTest):
     
    @skip
    def test_cannot_add_empty_list_items(self):
        # goes to home page
        # an empty list item
        # user hits enter
        # gets warning saying cannot save empty lists
        # enters some text 
        # now again hit enter 
        # can save the item
        
        self.fail()