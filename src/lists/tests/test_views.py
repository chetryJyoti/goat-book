from django.test import TestCase
from lists.models import Item,List
from django.utils.html import escape
from lists.forms import ItemForm

# Good unit testing practice says that each test should only test one thing
class HomePageTest(TestCase):
    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response,"home.html")
    
    def test_only_saves_items_when_necessary(self):
        self.client.get("/")
        self.assertEqual(Item.objects.count(),0)
    
    def test_home_page_uses_item_form(self):
        response = self.client.get("/")
        self.assertIsInstance(response.context["form"],ItemForm)
        

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
        
    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f"/lists/{correct_list.id}/",
            data={"item_text":"A new item for an existing list"},
        )
        
        self.assertEqual(Item.objects.count(),1)
        new_item = Item.objects.get()
        self.assertEqual(new_item.text,"A new item for an existing list")
        self.assertEqual(new_item.list,correct_list)
    
    def test_POST_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        
        response = self.client.post(
            f"/lists/{correct_list.id}/",
            data={"item_text":"A new item for an existing list"},
        )
        
        self.assertRedirects(response,f"/lists/{correct_list.id}/")
        
    def test_validation_errors_end_up_on_lists_page(self):
        # given
        list_ = List.objects.create()
        # when
        response = self.client.post(f"/lists/{list_.id}/",data={'item_text':""})
        # then
        # print(response.content.decode())
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"list.html")
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response,expected_error)
        
        
class NewListTest(TestCase):
    
    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post("/lists/new",data={"item_text":""})
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"home.html")
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response,expected_error)
        
    def test_invalid_list_items_arent_saved(self):
        self.client.post("/lists/new",data={'item_text':""})
        self.assertEqual(List.objects.count(),0)
        self.assertEqual(Item.objects.count(),0)