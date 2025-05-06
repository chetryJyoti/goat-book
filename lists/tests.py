from django.test import TestCase
from django.http import HttpRequest
from lists.views import home_page
from lists.models import Item,List

# Good unit testing practice says that each test should only test one thing
class HomePageTest(TestCase):
    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response,"home.html")
    
    def test_only_saves_items_when_necessary(self):
        self.client.get("/")
        self.assertEqual(Item.objects.count(),0)
        
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

class ListViewTest(TestCase):
    def test_uses_list_template(self):
        my_list = List.objects.create()
        response = self.client.get(f"/lists/{my_list.id}/")
        self.assertTemplateUsed(response,'list.html')
        
    def test_displays_all_list_items(self):
        correct_list = List.objects.create()
        Item.objects.create(text="item111",list=correct_list)
        Item.objects.create(text="item222",list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text="other list item",list=other_list)
        
        response = self.client.get(f"/lists/{correct_list.id}/")
        # /lists/234343
        
        self.assertContains(response,"item111")
        self.assertContains(response,"item222")
        self.assertNotContains(response,"other list item")
        
    def test_passes_correct_list_to_tempalte(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f"/lists/{correct_list.id}/")
        self.assertEqual(response.context['list'],correct_list)
        
class NewListTest(TestCase):
    
    def test_can_save_a_POST_request(self):
        self.client.post("/lists/new",data={'item_text':'A new list item'})
        self.assertEqual(Item.objects.count(),1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text,"A new list item")
        
    def test_redirects_after_POST(self):
        response = self.client.post("/lists/new",data={"item_text":"A new list item"})
        new_list = List.objects.get()
        self.assertRedirects(response,f"/lists/{new_list.id}/")
        
    def test_can_save_a_POST_request_to_an_existing_list(self):
        # Given
        other_list = List.objects.create()
        correct_list = List.objects.create()
        # When
        self.client.post(
            f"/lists/{correct_list.id}/add_item",
            data={"item_text":"A new item in an existing list"}
        )
        # Then
        self.assertEqual(Item.objects.count(),1)
        new_item = Item.objects.get()
        self.assertEqual(new_item.text,"A new item in an existing list")
        self.assertEqual(new_item.list,correct_list)
        
    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f"/lists/{correct_list.id}/add_item",
            data={"item_text": "A new item for an existing list"},
        )

        self.assertRedirects(response, f"/lists/{correct_list.id}/")