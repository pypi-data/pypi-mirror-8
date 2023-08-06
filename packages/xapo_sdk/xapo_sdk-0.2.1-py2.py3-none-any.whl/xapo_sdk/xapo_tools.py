#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, \
    with_statement, unicode_literals

from future.standard_library import hooks
with hooks():
    from urllib.parse import urlencode

import time
import textwrap
import json
from xapo_sdk import xapo_utils


class PaymentType:
    NONE = ''
    TIP = 'Tip'
    DEPOSIT = 'Deposit'
    PAY = 'Pay'
    DONATE = 'Donate'


class MicroPaymentConfig:
    """ Micro payment button configuration options.

    This class is intended to be a placeholder for micro payments
    buttons configuration but also serves for documenting. A dictionary
    with the intended fields would give the same results.

    Attributes:
        sender_user_id (str): The id of the user sending the payment.

        sender_user_email (str, optional): The email of the user sending
        the payment.

        sender_user_cellphone (str, optional): The celphone number of the
        user sending the payment.

        receiver_user_id (str): The id of the user receiving the payment.

        receiver_user_email (str): The email of the user receiving the payment.

        pay_object_id (str): A payment identifier in the TPA context.

        amount_BIT (float, optional): The amount of bitcoins to be payed by the
        widget. If not specified here, it must be entered on payment basis.

        pay_type (str): The string representing the type of operation
        ("Tip", "Pay", "Deposit" or "Donate").
    """
    def __init__(self, sender_user_id="", sender_user_email="",
                 sender_user_cellphone="", receiver_user_id="",
                 receiver_user_email="", pay_object_id="", amount_BIT=0,
                 timestamp=int(round(time.time() * 1000)),
                 pay_type=PaymentType.NONE):
        self.sender_user_id = sender_user_id
        self.sender_user_email = sender_user_email
        self.sender_user_cellphone = sender_user_cellphone
        self.receiver_user_id = receiver_user_id
        self.receiver_user_email = receiver_user_email
        self.pay_object_id = pay_object_id
        self.amount_BIT = amount_BIT
        self.timestamp = timestamp
        self.pay_type = pay_type


class MicroPayment:
    """ Xapo's payment buttons snippet builder.

    This class allows the construction of 2 kind of widgets, *div* and
    *iframe*. The result is a HTML snippet that could be embedded in a
    web page for doing micro payments though a payment button.

    Attributes:
        service_url (str): The endpoint URL that returns the payment widget.

        app_id (str, optional): The id of the TPA for which the widget will
        be created.

        app_secret (str, optional): The TPA secret used to encrypt widget
        configuration.
    """

    def __init__(self, service_url, app_id=None, app_secret=None):
        self.service_url = service_url
        self.app_id = app_id
        self.app_secret = app_secret

    def __build_url(self, config):
        json_config = json.dumps(config.__dict__)

        if (self.app_id is None or self.app_secret is None):
            query = {
                "payload": json_config,
                "customization": json.dumps({"button_text": config.pay_type})
            }
            query_str = urlencode(query)
        else:
            encrypted_config = xapo_utils.encrypt(json_config, self.app_secret,
                                                  xapo_utils.pkcs7_padding)
            query = {
                "app_id": self.app_id, "button_request": encrypted_config,
                "customization": json.dumps({"button_text": config.pay_type})
            }

        query_str = urlencode(query)
        widget_url = self.service_url + "?" + query_str

        return widget_url

    def build_iframe_widget(self, config):
        """ Build an iframe HTML snippet in order to be embedded in apps.

        Args:
            config (MicroPaymentConfig): The button configuration options.
            See @MicroPaymentConfig.

        Returns:
            str: the iframe HTML snippet ot be embedded in a page.
        """
        widget_url = self.__build_url(config)
        snippet = """
                <iframe id="tipButtonFrame" scrolling="no" frameborder="0"
                    style="border:none; overflow:hidden; height:22px;"
                    allowTransparency="true" src="{url}">
                </iframe>
              """.format(url=widget_url)

        return textwrap.dedent(snippet)

    def build_div_widget(self, config):
        """ Build div HTML snippet in order to be embedded in apps.

        Args:
            config (MicroPaymentConfig): The button configuration options.
            See @MicroPaymentConfig.

        Returns:
            str: the div HTML snippet ot be embedded in a page.
        """
        widget_url = self.__build_url(config)
        snippet = r"""
                <div id="tipButtonDiv" class="tipButtonDiv"></div>
                <div id="tipButtonPopup" class="tipButtonPopup"></div>
                <script>
                    $(document).ready(function() {{
                        $("#tipButtonDiv").load("{url}");
                    }});
                </script>
              """.format(url=widget_url)

        return textwrap.dedent(snippet)
