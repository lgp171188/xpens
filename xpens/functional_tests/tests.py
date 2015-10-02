from django.test import LiveServerTestCase
from django.contrib.auth.models import User

from selenium import webdriver


class UserLoginLogoutTestCase(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(2)

        self.user1 = User.objects.create_user('joe',
                                              'joe@example.com',
                                              'IamJoe!')

    def test_user_able_to_login_after_opening_xpens_and_logout(self):
        '''
        Test that a user can login after opening xpens with his credentials
        and then logout.
        '''

        # Joe is a user who would like to log his expenses
        # using the Xpens web application. So he visits the
        # home page of the Xpens web application.

        self.browser.get(self.live_server_url + '/')

        # The page redirects to the login page.

        self.assertEqual('{}/login/?next=/'.format(self.live_server_url),
                         self.browser.current_url)

        # He knows that he is in the right place since he can
        # see the name of the site in the title bar.

        self.assertIn('Xpens', self.browser.title)

        # He sees a form in the page and understands that it is a login
        # from from its title

        legend_element = self.browser.find_element_by_css_selector(
            'fieldset > legend'
        )
        self.assertIn('Login', legend_element.text)

        # He sees the inputs of the login form including the labels
        # placeholders.

        username_input = self.browser.find_element_by_css_selector(
            'input#id_username'
        )
        self.assertIsNotNone(self.browser.find_element_by_css_selector(
            'label[for="id_username"]'
        ))
        password_input = self.browser.find_element_by_css_selector(
            'input#id_password'
        )
        self.assertIsNotNone(
            self.browser.find_element_by_css_selector(
                'label[for="id_password"]'
            )
        )

        # He enters his username and password and submits the login form
        username_input.send_keys('joe')
        password_input.send_keys('IamJoe!')

        self.browser.find_element_by_css_selector(
            'form input[type="submit"]'
        ).click()

        # The login attempt was successful and he got redirected to the
        # overview page which he can see from the URL and page title

        self.assertEqual(self.browser.current_url,
                         '{}/overview/'.format(self.live_server_url))
        self.assertIn('Overview', self.browser.title)

        # He clicks the dropdown on the right side of the top navbar
        # to see the logout link

        self.browser.find_element_by_css_selector(
            'ul.navbar-right li.dropdown a.dropdown-toggle'
        ).click()

        # He then clicks the logout link and gets logged out and
        # redirected to the login page.

        self.browser.find_element_by_css_selector(
            'a#logout-link'
        ).click()
        self.assertEqual(self.browser.current_url,
                         "{}/login/".format(self.live_server_url))

    def tearDown(self):
        self.browser.quit()
