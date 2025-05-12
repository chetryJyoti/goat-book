# There’s no need for every single FT to test the login/logout mechanisms. If we can figure out a way to "cheat" 
# and skip that part,  we’ll spend less time waiting for duplicated test paths.

# Skipping the Login Process by Pre-creating a Session

# from django.conf import settings
from django.contrib.auth import get_user_model
from selenium.webdriver.common.by import By
from .base import FunctionalTest
# from .container_commands import create_session_on_server
# from .management.commands.create_session import create_pre_authenticated_session
User = get_user_model()


class MyListsTest(FunctionalTest):
    # def create_pre_authenticated_session(self, email):
    #     # user = User.objects.create(email=email)
    #     # session = SessionStore()
    #     # session[SESSION_KEY] = user.pk 
    #     # session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
    #     # session.save()
    #     if self.test_server:
    #         session_key = create_session_on_server(self.test_server, email)
    #     else:
    #         session_key = create_pre_authenticated_session(email)
    #     ## to set a cookie we need to first visit the domain. 
    #     ## 404 pages load the quickest!
    #     self.browser.get(self.live_server_url + "/404_no_such_url/")
    #     self.browser.add_cookie(
    #         dict(
    #             name=settings.SESSION_COOKIE_NAME,
    #             value=session_key,  
    #             path="/",
    #         )
    #     )
    
    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        # Edith is a logged-in user
        self.create_pre_authenticated_session("testemail@test.com")

        # She goes to the home page and starts a list
        self.browser.get(self.live_server_url)
        self.add_list_item("Reticulate splines")  
        self.add_list_item("Immanentize eschaton")
        first_list_url = self.browser.current_url

        # She notices a "My lists" link, for the first time.
        self.browser.find_element(By.LINK_TEXT, "My lists").click()

        # She sees her email is there in the page heading
        self.wait_for(
            lambda: self.assertIn(
                "testemail@test.com",
                self.browser.find_element(By.CSS_SELECTOR, "h1").text,
            )
        )

        # And she sees that her list is in there,
        # named according to its first list item
        self.wait_for(
            lambda: self.browser.find_element(By.LINK_TEXT, "Reticulate splines")
        )
        self.browser.find_element(By.LINK_TEXT, "Reticulate splines").click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, first_list_url)
        )
        
        # She decides to start another list, just to see
        self.browser.get(self.live_server_url)
        self.add_list_item("Click cows")
        second_list_url = self.browser.current_url

        # Under "my lists", her new list appears
        self.browser.find_element(By.LINK_TEXT, "My lists").click()
        self.wait_for(lambda: self.browser.find_element(By.LINK_TEXT, "Click cows"))
        self.browser.find_element(By.LINK_TEXT, "Click cows").click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, second_list_url)
        )

        # She logs out.  The "My lists" option disappears
        self.browser.find_element(By.CSS_SELECTOR, "#id_logout").click()
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_elements(By.LINK_TEXT, "My lists"),
                [],
            )
        )