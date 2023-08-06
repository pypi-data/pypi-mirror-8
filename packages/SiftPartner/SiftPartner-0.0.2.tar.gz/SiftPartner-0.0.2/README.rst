============================
Sift Science Parntership API
============================

Bindings for Sift Science's `Partnerships API <https://siftscience.com/resources/references/partner-api.html>`_.

Installation
============

Set up a virtual environment with virtualenv (otherwise you will need to make the pip calls as sudo):
::

    virtualenv venv
    source venv/bin/activate

Get the latest released package from pip:

Python 2:
::

    pip install siftpartner

Python 3:
::

    pip3 install siftpartner

or install newest source directly from GitHub:

Python 2:
::

    pip install git+https://github.com/SiftScience/sift-partner-python

Python 3:
::

    pip3 install git+https://github.com/SiftScience/sift-partner-python

Usage
=====

Here's an example:

::

    import siftpartner

    partner_client = siftpartner.Client(api_key = '<your_rest_api_key_here>', partner_id = '<your_rest_api_key_here>')

    # create a new account for a given merchant
    response = partner_client.new_account(
                                          "merchantsite.com", # the url for the merchant's site
                                          "shopowner@merchantsite.com", # an email belonging to the merchant
                                          "johndoe@merchantsite.com", # an email used to log in to Sift
                                          "s0m3l0ngp455w0rd" # password associated with that log in
                                         )


    response.is_ok()  # returns True of False

    print response # prints entire response body and http status code


    # Get a list of all merchant accounts created by you
    response = partner_client.get_accounts()

    response.is_ok()  # returns True of False

    print response # prints entire response body and http status code

    # configure notification endpoint and threshold for you merchants
    cfg = {
            "http_notification_url": "http://api.partner.com/notify?id=%s", # The url template to send notifications too
                                                                            # The %s is replaced with the merchants Customer ID
            "http_notification_threshold": 0.60     # The threshold to set the notifications for.  This is the Sift Score/100
          }
    response = partner_client.update_notification_config(cfg)

    response.is_ok()  # returns True of False

    print response # prints entire response body and http status code

Testing
=======

Before submitting a change, make sure the following commands run without errors from the root dir of the repository:

::

    PYTHONPATH=. python tests/client_test.py
    PYTHONPATH=. python3 tests/client_test.py