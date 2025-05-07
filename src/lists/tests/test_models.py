from django.test import TestCase
from lists.models import Item,List
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError

# Good unit testing practice says that each test should only test one thing
class ListAndItemModelTest(TestCase):
    def test_saving_and_retrieving_item(self):
        myList = List()
        myList.save()
        first_item = Item()
        first_item.text = "The first (ever) list item"
        first_item.list = myList
        first_item.save()

        second_item = Item()
        second_item.text = "Item the second"
        second_item.list = myList
        second_item.save()
        
        saved_list= List.objects.get()
        self.assertEqual(saved_list,myList)
        
        
        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(),2)
        
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text,"The first (ever) list item")
        self.assertEqual(first_saved_item.list,myList)
        self.assertEqual(second_saved_item.text,"Item the second")
        self.assertEqual(second_saved_item.list,myList)

    
    def test_can_save_a_POST_request(self):
        self.client.post("/lists/new",data={'text':'A new list item'})
        self.assertEqual(Item.objects.count(),1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text,"A new list item")
        
    def test_redirects_after_POST(self):
        response = self.client.post("/lists/new",data={"text":"A new list item"})
        new_list = List.objects.get()
        self.assertRedirects(response,f"/lists/{new_list.id}/")
        
        
    def test_cannot_save_null_list_item(self):
        mylist = List.objects.create()
        item = Item(list=mylist,text=None)
        with self.assertRaises(IntegrityError):
            item.save()
            
    def test_cannot_save_empty_list_item(self):
        mylist = List.objects.create()
        item = Item(list=mylist,text="")
        with self.assertRaises(ValidationError):
            item.full_clean()
    
    def test_get_absolute_url(self):
        mylist = List.objects.create()
        self.assertEqual(mylist.get_absolute_url(),f"/lists/{mylist.id}/")