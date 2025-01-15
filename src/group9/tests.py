from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class UserAuthTests(TestCase):
    def setUp(self):
        """
        setUp() runs before each test. 
        We'll create a test user here for login tests.
        """
        self.client = Client()  # Django test client
        self.test_username = "testuser"
        self.test_password = "testpass123"
        self.test_user = User.objects.create_user(
            username=self.test_username, 
            email="testuser@example.com", 
            password=self.test_password
        )
    
    def test_signup_view_get(self):
        """
        Example: GET request to 'signup' should return a 200 status (OK) 
        and render the signup.html template (or your sign-up template).
        """
        url = reverse("group9:Signup")  # or whatever your URL name is
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "signup.html")  # or the template you use
    
    def test_signup_view_post(self):
        """
        Example: POST valid data to 'signup' and ensure it creates a user 
        and redirects to 'login' or wherever you want.
        """
        url = reverse("group9:Signup")
        response = self.client.post(url, {
            "username": "new_user",
            "email": "new_user@example.com",
            "password1": "newpassword123",
            "password2": "newpassword123",
            "name": "Alice",
            "age": "25",
        })
        # Check for redirect on success
        self.assertEqual(response.status_code, 302)  
        # Now confirm the user was actually created
        self.assertTrue(User.objects.filter(username="new_user").exists())
    
    def test_login_view_get(self):
        """
        GET request to 'login' should return 200 and 
        render the login.html template.
        """
        url = reverse("group9:login")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")
    
    def test_login_view_post_valid(self):
        """
        POST a valid username/password should authenticate 
        and possibly redirect or show success in the template.
        """
        url = reverse("group9:login")
        response = self.client.post(url, {
            "username": self.test_username,
            "password": self.test_password
        })
        # If your login redirects on success, check the code:
        self.assertIn(response.status_code, [302, 200])
        # Also check if user is actually logged in
        self.assertTrue("_auth_user_id" in self.client.session)
    
    def test_login_view_post_invalid(self):
        """
        POST an invalid password should show an error and remain on login page.
        """
        url = reverse("group9:login")
        response = self.client.post(url, {
            "username": self.test_username,
            "password": "wrongpassword"
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")
        self.assertContains(response, "Invalid username or password")
        # Make sure user is NOT logged in
        self.assertFalse("_auth_user_id" in self.client.session)

class StartExamViewTests(TestCase):
    def setUp(self):
        """
        Create a user and some test data. 
        """
        self.client = Client()
        self.test_username = "examuser"
        self.test_password = "exampass"
        self.test_user = User.objects.create_user(
            username=self.test_username, 
            password=self.test_password
        )
        # Optionally, you could create test questions in DB if needed.
    
    def test_start_exam_redirect_if_not_logged_in(self):
        """
        If the view is protected by @login_required, 
        an anonymous user should be redirected to login.
        """
        url = reverse("group9:start_exam")
        response = self.client.get(url)
        # Typically, Django redirects to /login/?next=/group9/start_exam/ 
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.url)
    
    def test_start_exam_loads_for_logged_in_user(self):
        """
        If the user is logged in, the start_exam page should load with status 200.
        """
        self.client.login(username=self.test_username, password=self.test_password)
        url = reverse("group9:start_exam")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "start_exam.html")
    
    def test_start_exam_submit_answers(self):
        """
        A sample test of the POST logic. We'll simulate providing question_ids 
        and answers, then check the response or DB changes.
        """
        self.client.login(username=self.test_username, password=self.test_password)
        url = reverse("group9:start_exam")
        
        # Simulate user fetching random questions first (GET)
        response_get = self.client.get(url)
        self.assertEqual(response_get.status_code, 200)
        
        # Now we mimic a POST with some question IDs & answers
        response_post = self.client.post(url, {
            "question_ids": ["1", "2", "3"],
            "answer_1": "My answer for question 1",
            "answer_2": "Another answer",
            "answer_3": "One more answer"
        })
        # Check if it renders exam_result.html or if it redirects
        self.assertIn(response_post.status_code, [200, 302])
        # You could also test if the exam result is in the DB or the context
        # For example, if you store it in group9_exam, check that a row was created.
        # This is just a placeholder assertion:
        self.assertTemplateUsed(response_post, "exam_result.html")