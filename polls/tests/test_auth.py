from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from mysite import settings
from polls.models import Question, Choice


class AuthenticationTest(TestCase):
    def setUp(self):
        """
        Set up essential components to be used in authentication tests.
        Create a test user, a test question, and choices.
        """
        self.username = 'tester'
        self.password = 'testpassword123'
        self.user = User.objects.create_user(username=self.username,
                                             password=self.password)
        self.user.save()
        self.question = Question.objects.create(question_text='Test Question')
        for count in range(1, 5):
            choice = Choice(choice_text=f'Choice {count}',
                            question=self.question)
            choice.save()
        self.question.save()

    def test_login_page(self):
        """
        Login page testing for both GET and POST methods.
        GET request should return a 200 OK response.
        POST request should return a 302 redirect to the polls index page.
        """
        login_url = reverse("login")
        response = self.client.get(login_url)
        self.assertEqual(200, response.status_code)
        form_data = {'username': self.username, 'password': self.password}
        response = self.client.post(login_url, form_data)
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse(settings.LOGIN_REDIRECT_URL))

    def test_log_out(self):
        """
        Log out testing for correct redirecting.
        Check if the user can log out successfully,
        and redirect to the login page.
        """
        logout_url = reverse('logout')
        self.assertTrue(
            self.client.login(username=self.username, password=self.password)
        )
        response = self.client.get(logout_url)
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse(settings.LOGOUT_REDIRECT_URL))

    def test_auth_required_to_vote(self):
        """
        Test for voting without log in to redirect to log in page.
        Unauthenticated user will be redirected to log in page.
        """
        vote_url = reverse('polls:vote', args=[self.question.id])
        choice = self.question.choice_set.first()
        form_data = {'choice': f'{choice.id}'}
        response = self.client.post(vote_url, form_data)
        self.assertEqual(response.status_code, 302)
        login_next_url = f"{reverse('login')}?next={vote_url}"
        self.assertRedirects(response, login_next_url)
