from django.test import TestCase
from lists.models import Item,List
from django.utils.html import escape
from django.urls import reverse
from lists.forms import (
    DUPLICATE_ITEM_ERROR,
    EMPTY_ITEM_ERROR,
    ExistingListItemForm,
    ItemForm,
)
from django.contrib.auth import get_user_model

User = get_user_model()

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
            data={"text":"A new item for an existing list"},
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
            data={"text":"A new item for an existing list"},
        )
        
        self.assertRedirects(response,f"/lists/{correct_list.id}/")
        
    # def test_validation_errors_end_up_on_lists_page(self):
    #     # given
    #     list_ = List.objects.create()
    #     # when
    #     response = self.client.post(f"/lists/{list_.id}/",data={'text':""})
    #     # then
    #     # print(response.content.decode())
    #     self.assertEqual(response.status_code,200)
    #     self.assertTemplateUsed(response,"list.html")
    #     expected_error = escape(EMPTY_ITEM_ERROR)
    #     self.assertContains(response,expected_error)
    
    def post_invalid_input(self):
        mylist = List.objects.create()
        return self.client.post(f"/lists/{mylist.id}/",data={"text":""})
    
    def test_for_invalid_input_nothing_saved_to_db(self):
         self.post_invalid_input()
         self.assertEqual(Item.objects.count(),0)
    
    def test_for_invalid_input_renders_list_template(self):
        response = self.post_invalid_input()
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"list.html")
        
    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context["form"],ItemForm)
        
    def test_for_invalid_input_shows_error_on_page(self):
        response = self.post_invalid_input()
        self.assertContains(response,escape(EMPTY_ITEM_ERROR))
    
    # @skip
    def test_duplicate_item_validation_errors_end_up_on_lists_page(self):
        list1 = List.objects.create()
        Item.objects.create(list=list1, text="textey")
        response = self.client.post(
            f"/lists/{list1.id}/",
            data={"text": "textey"},
        )

        expected_error = escape(DUPLICATE_ITEM_ERROR)
        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response, "list.html")
        self.assertEqual(Item.objects.all().count(), 1)
        
    def test_displays_item_form(self):
        mylist = List.objects.create()
        response = self.client.get(f"/lists/{mylist.id}/")
        self.assertIsInstance(response.context["form"], ExistingListItemForm)
        self.assertContains(response, 'name="text"')
        
    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context["form"], ExistingListItemForm)
        
        
class NewListTest(TestCase):
    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post("/lists/new",data={"text":""})
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"home.html")
        self.assertIsInstance(response.context["form"],ItemForm)
        self.assertContains(response,escape(EMPTY_ITEM_ERROR))
        
    def test_invalid_list_items_arent_saved(self):
        self.client.post("/lists/new",data={'text':""})
        self.assertEqual(List.objects.count(),0)
        self.assertEqual(Item.objects.count(),0)
        
    def test_list_owner_is_saved_if_user_is_authenticated(self):
        user = User.objects.create(email="a@b.com")
        self.client.force_login(user)  
        self.client.post("/lists/new", data={"text": "new item"})
        new_list = List.objects.get()
        self.assertEqual(new_list.owner, user)

class MyListsTest(TestCase):
    def test_my_lists_url_renders_my_lists_template(self):
        User.objects.create(email="a@b.com")
        response = self.client.get("/lists/users/a@b.com/")
        self.assertTemplateUsed(response, "my_lists.html")
    
    def test_passes_correct_owner_to_template(self):
        User.objects.create(email="wrong@owner.com")
        correct_user = User.objects.create(email="a@b.com")
        response = self.client.get("/lists/users/a@b.com/")
        self.assertEqual(response.context["owner"], correct_user)
        
        
class ShareListViewTest(TestCase):
    def test_POST_redirects_after_sharing(self):
        owner = User.objects.create(email='owner@example.com')
        sharee = User.objects.create(email='sharee@example.com')
        list_ = List.objects.create(owner=owner)

        response = self.client.post(
            f'/lists/{list_.id}/share/',
            data={'sharee': 'sharee@example.com'}
        )

        self.assertRedirects(response, f'/lists/{list_.id}/')
    
    def test_adds_user_to_shared_with_list(self):
        owner = User.objects.create(email='owner@example.com')
        sharee = User.objects.create(email='sharee@example.com')
        list_ = List.objects.create(owner=owner)

        self.client.post(f'/lists/{list_.id}/share/', data={'sharee': 'sharee@example.com'})
        
        self.assertIn(sharee, list_.shared_with.all())
        

    def test_saves_created_by_user_on_item_if_user_logged_in(self):
        user = User.objects.create(email='edith@example.com')
        self.client.force_login(user)

        list_ = List.objects.create()
        self.client.post(
            reverse('view_list', args=[list_.id]),
            data={'text': 'A new shared item'}
        )

        item = Item.objects.get(text='A new shared item')
        self.assertEqual(item.created_by, user)