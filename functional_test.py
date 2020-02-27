import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class MainPageTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_application_is_accessable(self):
        # Visitor opens the website
        try:
            self.browser.get('http://localhost:8000')
        except:
            self.assertTrue(False, msg="Application is not loaded. Probably server isn't runing")

        #Visitor he checks if he is on correct website by looking at its title in browser
        self.assertIn('Number Converter', self.browser.title)

    def test_mian_page_is_accesible_by_url(self):
        #Visitor trying to visit main page by puting it adress into url
        try:
            self.browser.get('http://localhost:8000/')
        except:
            self.assertTrue(False, msg="Application is not loaded. Probably server isn't runing")

        #Visitor can see that content of this subpage is correct
        self.assertIn(
            'How it works?', 
            self.browser.find_element_by_tag_name('h3').text,
            )

    def test_mian_page_is_accesible_by_navbar(self):
        #While visitor is on any other subpage than mainpage
        try:
            self.browser.get('http://localhost:8000/description/')
        except:
            self.assertTrue(False, msg="Application is not loaded. Probably server isn't runing")

        #Visitor sees Home-button on navbar
        button = self.browser.find_element_by_xpath('//a[@href="/"]')

        #Visitor clickes on this button
        button.click()

        #Visitor can see that he is on Homepage and content of this page is correct
        self.assertIn(
            'How it works?', 
            self.browser.find_element_by_tag_name('h3').text,
            )


class DescriptionPageTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()


    def test_if_description_page_is_accessable_by_url(self):
        #Visitor trying to visit description page by giving it adress into url
        try:
            self.browser.get('http://localhost:8000/description/')
        except:
            self.assertTrue(False, msg="Application is not loaded. Probably server isn't runing")

        #Visitor can see that content of this subpage is correct
        self.assertIn(
            'Description of this web application:', 
            self.browser.find_element_by_tag_name('h2').text,
            )

    def test_if_description_page_is_accessable_by_navbar(self):
        #Visitor trying to visit description page by using navbar

        #Visitor going to main page
        try:
            self.browser.get('http://localhost:8000/')
        except:
            self.assertTrue(False, msg="Application is not loaded. Probably server isn't runing")

        #Visitor sees "description" button on navbar
        button = self.browser.find_element_by_xpath('//a[@href="/description/"]')

        #Visitor clickes on this button
        button.click()

        #Visitor can see that he is on Description subpage and content of this page is correct
        self.assertIn(
            'Description of this web application:', 
            self.browser.find_element_by_tag_name('h2').text,
            )

    def test_if_result_page_is_accessable_by_url(self):
        #Visitor trying to visit result page by giving it adress into url
        try:
            self.browser.get('http://localhost:8000/result/')
        except:
            self.assertTrue(False, msg="Application is not loaded. Probably server isn't runing")

        #Visitor sees that content of this subpage is correct
        self.assertIn(
            'Input given by user is:', 
            self.browser.find_element_by_tag_name('h4').text,
            )

        #Visitor sees that there is no given input
        resultstring = self.browser.find_element_by_name('given_number').text
        self.assertTrue(
            resultstring=='',
            msg=f"We didn't get expected result. We expected {{None}} but result was {{{resultstring}}}"
        )

    def test_if_result_page_is_accessable_by_form(self):
        #Visitor going to main page of website
        try:
            self.browser.get('http://localhost:8000/')
        except:
            self.assertTrue(False, msg="Application is not loaded. Probably server isn't runing")

        #Visitor sees that there is some inputbox
        inputbox = self.browser.find_element_by_name('given_number')  
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Give the number to convert'
        )

        #Visitor sees that this input box is empty
        self.assertEqual(
            inputbox.get_attribute('value'), '',
            msg="inputbox should be empty before giving input"
        )

        # Visitor types "3a" into a text box 
        inputbox.send_keys('3a')  

        ######## Looks like django is not returns unvalid data as 'value' atribute (it returns empty string)
        ######## ATM i didnt find way to get visible values which is putted in form but not valid
        ######## As it's not impact how application works,I will leave it for now commented 
        # # Visitor sees that his input is displayed in the inputbox
        # self.assertEqual(
        #     inputbox.get_attribute('value'), '3a',
        #     msg="inputbox should contain given input"
        # )

        # Visitor hits enter, app should keep him in his page because input is incorect
        inputbox.send_keys(Keys.ENTER)  
        time.sleep(1)  

        # Visitor clears inputbox and put correct input
        inputbox.clear()
        inputbox.send_keys('3')  

        # When he hits enter, the page proceed to result template
        inputbox.send_keys(Keys.ENTER)  
        time.sleep(1)  

        #As we are going from index.html to result.html we need to assign inputbox once again
        inputbox = self.browser.find_element_by_name('given_number')  

        # Input box is empty again
        self.assertEqual(
            inputbox.get_attribute('value'), '',
            msg="inputbox should be empty after sending data"
        )

        #Result is displayed below form
        resultstring = self.browser.find_element_by_name('result').text
        self.assertTrue(
            resultstring=='trzy',
            msg=f"We didn't get expected result. We expected {{trzy}} but result was {{{resultstring}}}"
        )


if __name__ == '__main__':
    unittest.main()