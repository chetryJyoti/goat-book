from django.test import TestCase
from accounts.models import Token
from unittest import mock
from django.contrib import auth

class SendLoginEmailViewTest(TestCase):
    def test_redirects_to_home_page(self):
        response = self.client.post(
            "/accounts/send_login_email",data={"email":"jyotichetry087@gmail.com"}
        )
        self.assertRedirects(response,"/")
    
    # mocking
    # def test_sends_mail_to_address_from_post(self):
    #     self.send_mail_called = False
        
    #     def fake_send_mail(subject,body,from_email,to_list):
    #         self.send_mail_called = True
    #         self.subject = subject
    #         self.body = body
    #         self.from_email = from_email
    #         self.to_list = to_list
        
    #     accounts.views.send_mail = fake_send_mail
        
    #     self.client.post(
    #         "/accounts/send_login_email",data={'email':"jyotichetry087@gmail.com"}
    #     )
        
    #     self.assertTrue(self.send_mail_called)
    #     self.assertEqual(self.subject,"Your login link for Superlists")
    #     self.assertEqual(self.from_email,"jyotichetry087@gmail.com")
    #     self.assertEqual(self.to_list,["jyotichetry087@gmail.com"])
    @mock.patch("accounts.views.send_mail")  
    def test_sends_mail_to_address_from_post(self, mock_send_mail):  
        self.client.post(  
            "/accounts/send_login_email", data={"email": "jyotichetry087@gmail.com"}
        )

        self.assertEqual(mock_send_mail.called, True)  
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args  
        self.assertEqual(subject, "Your login link for Superlists")
        self.assertEqual(from_email, "jyotichetry087@gmail.com")
        self.assertEqual(to_list, ["jyotichetry087@gmail.com"])
        
    def test_adds_success_message(self):
        response = self.client.post(
            "/accounts/send_login_email",
            data={"email": "edith@example.com"},
            follow=True, 
            # Testing Django messages is a bit contorted—​we have to pass 
            # follow=True to the test client to tell it to get the page after the 302-redirect,
            # and examine its context for a list of messages (which we have to listify before it’ll play nicely).
        )

        message = list(response.context["messages"])[0]
        self.assertEqual(
            message.message,
            "Check your email, we've sent you a link you can use to log in.",
        )
        self.assertEqual(message.tags, "success")
    
        
    def test_creates_token_associated_with_email(self):
        self.client.post(
            "/accounts/send_login_email", data={"email": "edith@example.com"}
        )
        token = Token.objects.get()
        self.assertEqual(token.email, "edith@example.com")

    @mock.patch("accounts.views.send_mail")
    def test_sends_link_to_login_using_token_uid(self, mock_send_mail):
        self.client.post(
            "/accounts/send_login_email", data={"email": "edith@example.com"}
        )

        token = Token.objects.get()
        expected_url = f"http://testserver/accounts/login?token={token.uid}"
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertIn(expected_url, body)

class LoginViewTest(TestCase):
    
    def test_redirects_to_home_page(self):
        response = self.client.get("/accounts/login?token=adfdf32")
        self.assertRedirects(response,"/")
    
    def test_logs_in_if_given_valid_token(self):
        #Given we are not logged in
        anon_user = auth.get_user(self.client)
        print(anon_user)
        self.assertEqual(anon_user.is_authenticated, False)
        
        #When we have a valid token
        token = Token.objects.create(email="test@test.com")
        self.client.get(f"/accounts/login?token={token.uid}")
        
        #Then should log in
        user = auth.get_user(self.client)
        self.assertEqual(user.is_authenticated, True)
        self.assertEqual(user.email, "test@test.com")
        
    def test_shows_login_error_if_token_invalid(self):
        response = self.client.get("/accounts/login?token=invalid-token", follow=True)
        user = auth.get_user(self.client)
        self.assertEqual(user.is_authenticated, False)
        message = list(response.context["messages"])[0]
        self.assertEqual(
            message.message,
            "Invalid login link, please request a new one",
        )
        self.assertEqual(message.tags, "error")
        
    @mock.patch("accounts.views.auth")  
    def test_calls_django_auth_authenticate(self, mock_auth):  
        self.client.get("/accounts/login?token=abcd123")
        self.assertEqual(
            mock_auth.authenticate.call_args,  
            mock.call(uid="abcd123"),  
        )
    

        mock_auth.authenticate.return_value = None  

        response = self.client.get("/accounts/login?token=abcd123", follow=True)

        message = list(response.context["messages"])[0]
        self.assertEqual(  
            message.message,
            "Invalid login link, please request a new one",
        )
        self.assertEqual(message.tags, "error")