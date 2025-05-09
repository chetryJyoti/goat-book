from django.test import TestCase
from lists.models import Item,List
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()

# Good unit testing practice says that each test should only test one thing
class ItemModelTest(TestCase):
    def test_default_text(self):
        item = Item()
        self.assertEqual(item.text, "")

    def test_item_is_related_to_list(self):
        mylist = List.objects.create()
        item = Item()
        item.list = mylist
        item.save()
        self.assertIn(item, mylist.item_set.all())

    
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
            
    def test_string_representation(self):
        item = Item(text="some text")
        self.assertEqual(str(item),"some text")
            
    def test_list_ordering(self):
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1,text="i1")
        item2 = Item.objects.create(list=list1,text="item2")
        item3 = Item.objects.create(list=list1,text="3")
        self.assertEqual(
            list(Item.objects.all()),
            [item1,item2,item3]
        )
    
   

class ListModelTest(TestCase):
    
    def test_get_absolute_url(self):
        mylist = List.objects.create()
        self.assertEqual(mylist.get_absolute_url(),f"/lists/{mylist.id}/")
        
    def test_duplicate_items_are_invalid(self):
        mylist = List.objects.create()
        Item.objects.create(list=mylist,text="abc")
        with self.assertRaises(ValidationError):
            item = Item(list=mylist,text="abc")
            item.full_clean()
            
    def test_CAN_save_same_item_to_different_lists(self):
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(list=list1,text="hello")
        item = Item(list=list2,text="hello")
        item.full_clean() # should not raise
    
    def test_lists_can_have_owners(self):
        user = User.objects.create(email="a@b.com")
        mylist = List.objects.create(owner = user)
        self.assertIn(mylist,user.lists.all())
        
    def test_list_owner_is_optional(self):
        List.objects.create()  # should not raise