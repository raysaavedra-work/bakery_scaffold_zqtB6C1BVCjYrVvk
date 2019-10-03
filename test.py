import os
import re
import unittest

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestAcceptanceStripe(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestAcceptanceStripe, self).__init__(*args, **kwargs)
        with open('client/order.html', 'r') as file_descriptor:
            self.order_html_str = file_descriptor.read()

        with open('app.py', 'r') as file_descriptor:
            self.app_py_str = file_descriptor.read()

    def test_acceptance_stripe_public_key_env_has_been_set_in_order_html(self):
        """Check if Stripe public key env was defined in order.html."""
        pattern = re.compile(
            r"Stripe\((\"|')pk_test_\w+(\"|')\);",
            re.I | re.M
        )
        res = re.search(pattern, self.order_html_str)

        self.assertIsNone(
            res,
            msg="You shouldn't hardcode the Stripe key in order.html."
        )

    def test_acceptance_stripe_public_key_env_has_been_set_in_app_py(self):
        """Check if Stripe public key env was defined in app.py."""
        pattern = re.compile(
            r"stripe.api_key = (\"|')pk_test_\w+(\"|')",
            re.I | re.M
        )
        res = re.search(pattern, self.app_py_str)

        self.assertIsNone(
            res,
            msg="You shouldn't hardcode the Stripe key in app.py."
        )

    def test_acceptance_stripe_script_has_been_inserted(self):
        """Check if Stripe script was inserted."""
        pattern = re.compile(
            r"<script src=(\"|')https://js.stripe.com/v3(\"|')></script>",
            re.I | re.M
        )
        res = re.search(pattern, self.order_html_str)

        self.assertTrue(
            hasattr(res, 'group'),
            msg="You didn't insert a Stripe script file."
        )

    def test_acceptance_checkout_button_was_instantiated(self):
        """Check if checkout button was captured."""
        pattern = re.compile(
            r"document.getElementById\((\"|')checkout-button(\"|')\);",
            re.I | re.M
        )

        res = re.search(pattern, self.order_html_str)
        self.assertTrue(
            hasattr(res, 'group'),
            msg="You didn't add a checkout button."
        )

    def test_acceptance_product_defined_on_checkout(self):
        """Check if product was defined on checkout."""
        pattern = re.compile(
            r"product = (\"|')Chocolate Cupcake \w{5}(\"|')",
            re.I | re.M
        )
        res_var = re.search(pattern, self.order_html_str)

        pattern = re.compile(
            r"name: product",
            re.I | re.M
        )
        res_body = re.search(pattern, self.order_html_str)

        self.assertTrue(
            hasattr(res_var, 'group') and hasattr(res_body, 'group'),
            msg="You didn't add the product in the checkout."
        )

    def test_amount_defined_on_checkout(self):
        """Check if amount was defined on checkout."""
        pattern = re.compile(
            r"amount = -?(?:0|[1-9]\d{0,2}(?:,?\d{3})*)(?:\.\d{1,2})?",
            re.I | re.M
        )
        res_var = re.search(pattern, self.order_html_str)

        pattern = re.compile(
            r"amount: amount",
            re.I | re.M
        )
        res_body = re.search(pattern, self.order_html_str)

        self.assertTrue(
            hasattr(res_var, 'group') and hasattr(res_body, 'group'),
            msg="You didn't add the amount code in the checkout."
        )


    def test_acceptance_redirect_to_checkout(self):
        """Check if redirectToCheckout function call is present"""
        pattern = re.compile(
            r".redirectToCheckout",
            re.I | re.M
        )
        res = re.search(pattern, self.order_html_str)

        self.assertTrue(
            hasattr(res, 'group'),
            msg="No checkout redirection was found."
        )

    def test_acceptance_success_url(self):
        """Check if success_url redirects to the /order_success route"""
        pattern = re.compile(
            r"success_url=domain_url \+ (\"|')/order_success\?session_id={CHECKOUT_SESSION_ID}(\"|')",
            re.I | re.M
        )
        res = re.search(pattern, self.app_py_str)

        self.assertTrue(
            hasattr(res, 'group'),
            msg="You didn't define a success URL."
        )

    def test_acceptance_cancel_url(self):
        """Check if cancel_url redirects to the index route"""
        pattern = re.compile(
            r"cancel_url=domain_url \+ (\"|')/(\"|')",
            re.I | re.M
        )
        res = re.search(pattern, self.app_py_str)

        self.assertTrue(hasattr(res, 'group'), msg="You didn't define a cancel URL.")


if __name__ == '__main__':
    unittest.main()
