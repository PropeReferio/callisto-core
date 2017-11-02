from unittest import skip

from selenium.webdriver.support.ui import Select

from django.test import override_settings

from .. import models, view_helpers
from .base import FunctionalTest


class ElementHelper(object):

    def __init__(self, browser):
        self.browser = browser

    @property
    def done(self):
        return self.browser.find_element_by_css_selector(
            '[value="{}"]'.format(view_helpers.StepsHelper.review_name))

    @property
    def next(self):
        return self.browser.find_element_by_css_selector(
            '[value="{}"]'.format(view_helpers.StepsHelper.next_name))

    @property
    def back(self):
        return self.browser.find_element_by_css_selector(
            '[value="{}"]'.format(view_helpers.StepsHelper.back_name))

    @property
    def extra_input(self):
        return self.browser.find_element_by_css_selector(
            '#id_question_1_0')

    @property
    def extra_dropdown(self):
        return self.browser.find_element_by_css_selector(
            '#id_question_1_1')

    @property
    def dropdown_select(self):
        return self.browser.find_element_by_css_selector(
            'select.extra-widget-dropdown')

    @property
    def choice_1(self):
        return self.choice_number(0)

    @property
    def choice_3(self):
        return self.choice_number(2)

    @property
    def text_input(self):
        return self.browser.find_element_by_css_selector(
            '[type="text"]')

    def wait_for_display(self):
        # / really unreliable way to wait for the element to be displayed
        self.next.click()
        self.back.click()

    def choice_number(self, number):
        return self.browser.find_elements_by_css_selector(
            '[type="checkbox"]')[number]


class FunctionalBase(FunctionalTest):

    @property
    def element(self):
        return ElementHelper(self.browser)


class ExtraInfoNameClashTest(FunctionalBase):

    def setUp(self):
        # add a second extra info question on the 1st page
        models.Choice.objects.filter(text='sugar').update(
            extra_info_text='what type???')
        super().setUp()

        self.browser.find_elements_by_css_selector(
            '.extra-widget-text [type="checkbox"]')[0].click()
        self.browser.find_elements_by_css_selector(
            '.extra-widget-text [type="checkbox"]')[1].click()
        self.element.wait_for_display()

        self.text_input_one = 'brown cinnamon'
        self.text_input_two = 'white diamond'
        self.browser.find_elements_by_css_selector(
            '.extra-widget-text [type="text"]')[0].send_keys(self.text_input_one)
        self.browser.find_elements_by_css_selector(
            '.extra-widget-text [type="text"]')[1].send_keys(self.text_input_two)

    def test_input_one_persists(self):
        self.element.next.click()
        self.element.back.click()
        element = self.browser.find_elements_by_css_selector(
            '.extra-widget-text [type="text"]')[0]
        self.assertEqual(
            element.get_attribute('value'),
            self.text_input_one,
        )

    def test_input_two_persists(self):
        self.element.next.click()
        self.element.back.click()
        element = self.browser.find_elements_by_css_selector(
            '.extra-widget-text [type="text"]')[1]
        self.assertEqual(
            element.get_attribute('value'),
            self.text_input_two,
        )

    def test_review_page_has_input_one(self):
        self.element.next.click()
        self.element.next.click()
        self.element.done.click()
        self.assertSelectorContains('body', self.text_input_one)

    def test_review_page_has_input_two(self):
        self.element.next.click()
        self.element.next.click()
        self.element.done.click()
        self.assertSelectorContains('body', self.text_input_two)


class FrontendTest(FunctionalBase):

    def test_first_page_text(self):
        self.assertSelectorContains('form', 'food options')

    def test_second_page_text(self):
        self.element.next.click()
        self.assertSelectorContains(
            'form', 'do androids dream of electric sheep?')

    def test_third_page_text(self):
        self.element.next.click()
        self.element.next.click()
        self.assertSelectorContains('form', 'whats on the radios?')

    def test_forwards_and_backwards_navigation(self):
        self.element.next.click()
        self.element.back.click()
        self.assertSelectorContains('form', 'food options')
        self.element.next.click()
        self.element.next.click()
        self.element.back.click()
        self.assertSelectorContains(
            'form', 'do androids dream of electric sheep?')

    def test_first_page_questions(self):
        self.assertSelectorContains('form', 'food options')
        self.assertSelectorContains('form', 'choose some!')
        self.assertSelectorContains('form', 'eat it now???')
        self.assertSelectorContains('form', '')

    def test_first_page_choices(self):
        self.assertSelectorContains('form', 'vegetables')
        self.assertSelectorContains('form', 'apples')
        self.assertSelectorContains('form', 'sugar')

    def test_extra_info(self):
        self.assertCss('[placeholder="extra information here"]')

    def test_extra_dropdown(self):
        self.element.extra_dropdown.click()
        self.element.wait_for_display()
        self.assertSelectorContains('option', 'green')
        self.assertSelectorContains('option', 'red')

    def test_extra_dropdown_persists(self):
        self.element.extra_dropdown.click()
        self.element.wait_for_display()

        self.assertEqual(
            self.element.dropdown_select.get_attribute('value'),
            '1',
        )

        select = Select(self.element.dropdown_select)
        select.select_by_value('2')

        self.element.next.click()
        self.element.back.click()

        self.assertEqual(
            self.element.dropdown_select.get_attribute('value'),
            '2',
        )

    def test_can_select_choice(self):
        self.assertFalse(self.element.extra_input.is_selected())
        self.element.extra_input.click()
        self.assertTrue(self.element.extra_input.is_selected())

    def test_choice_1_persists_after_changing_page(self):
        self.element.extra_input.click()
        self.element.next.click()
        self.element.back.click()
        self.assertTrue(self.element.extra_input.is_selected())

    def test_ghost_choices_not_populated(self):
        self.element.next.click()
        self.element.back.click()
        self.assertFalse(self.element.extra_input.is_selected())
        self.assertFalse(self.element.extra_dropdown.is_selected())
        self.assertFalse(self.element.choice_3.is_selected())

    def test_choice_2_persists_after_changing_page(self):
        self.element.extra_dropdown.click()
        self.element.next.click()
        self.element.back.click()
        self.assertTrue(self.element.extra_dropdown.is_selected())

    def test_all_choices_persist_after_changing_page(self):
        self.element.extra_input.click()
        self.element.extra_dropdown.click()
        self.element.next.click()
        self.element.back.click()
        self.assertTrue(self.element.extra_input.is_selected())
        self.assertTrue(self.element.extra_dropdown.is_selected())

    def test_mulitple_answers_reflected_on_review_page(self):
        self.element.extra_input.click()
        self.element.extra_dropdown.click()
        self.element.next.click()
        self.element.next.click()
        self.element.done.click()
        self.assertSelectorContains('body', 'apples')
        self.assertSelectorContains('body', 'vegetables')

    def test_textbox_array_regression(self):
        self.element.next.click()
        self.element.text_input.send_keys('text input content!!!')
        self.element.back.click()
        self.element.next.click()
        self.assertNotEqual(
            ['text input content!!!'],
            self.element.text_input.get_attribute('value'),
        )

    def test_text_persists_after_changing_page(self):
        self.element.next.click()
        self.element.text_input.send_keys('text input content!!!')
        self.element.back.click()
        self.element.next.click()
        self.assertEqual(
            'text input content!!!',
            self.element.text_input.get_attribute('value'),
        )

    def test_can_render_done_page(self):
        self.element.next.click()
        self.element.next.click()
        self.element.done.click()
        self.assertSelectorContains('h2', 'Question Review')

    def test_choice_present_on_done_page(self):
        self.element.choice_1.click()
        self.element.next.click()
        self.element.next.click()
        self.element.done.click()
        self.assertSelectorContains('body', 'vegetables')

    def test_text_input_present_on_done_page(self):
        self.element.next.click()
        self.element.text_input.send_keys('text input content!!!')
        self.element.next.click()
        self.element.done.click()
        self.assertSelectorContains('body', 'text input content!!!')

    def test_unanswered_questions_present_on_done_page(self):
        self.element.next.click()
        self.element.next.click()
        self.element.done.click()
        self.assertSelectorContains('body', 'food options')
        self.assertSelectorContains(
            'body', 'do androids dream of electric sheep?')
        self.assertSelectorContains('body', '[ Not Answered ]')
