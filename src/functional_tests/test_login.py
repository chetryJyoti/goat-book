import re
from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from django.core import mail
from unittest import skip

TEST_EMAIL = 'jyotichetry087@gmail.com'
SUBJECT = "Your login link for Superlists"

# todo : remove skip
# @skip
class LoginTest(FunctionalTest):
    def test_login_uses_magic_link(self):
        self.browser.get(self.live_server_url)
        self.browser.find_element(By.CSS_SELECTOR, "input[name=email]").send_keys(
            TEST_EMAIL, Keys.ENTER
        )
        
        # A message appears telling her an email has been sent
        self.wait_for(
            lambda: self.assertIn(
                "Check your email",
                self.browser.find_element(By.CSS_SELECTOR, "body").text,
            )
        )
        
        if self.test_server:
            # Testing real email sending from the server is not worth it.
            # Email itself is a well-understood protocol and Django
            # has supported sending email for more than a decade
            return 
    
        # checks email
        email = mail.outbox.pop()  
        self.assertIn(TEST_EMAIL, email.to)
        self.assertEqual(email.subject, SUBJECT)
        
        # it has a Url link to log in
        
        self.assertIn("Use this link to log in", email.body)
        url_search = re.search(r"http://.+/.+$", email.body)
        if not url_search:
            self.fail(f"Could not find url in email body:\n{email.body}")
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)
        
        # clicks it 
        self.browser.get(url)
        
        # she is logged in!
        self.wait_to_be_logged_in(email=TEST_EMAIL)

        # Now she logs out
        self.browser.find_element(By.CSS_SELECTOR, "#id_logout").click()

        # She is logged out
        self.wait_to_be_logged_out(email=TEST_EMAIL)
        
        