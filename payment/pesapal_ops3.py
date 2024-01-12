import urllib.request

from . import pesapal_processor3

pesapal_processor3.consumer_key = 'qkio1BGGYAXTu2JOfm7XSXNruoZsrqEW'
pesapal_processor3.consumer_secret = 'osGQ364R49cXKeOYSpaOnT++rHs='
pesapal_processor3.testing = False


def post_transaction(Reference,Description, Amount, Type):
    
    post_params = {
        'oauth_callback': 'https://fda9-197-232-61-208.ngrok-free.app/payment/oauth_callback/'
    }

    request_data = {
        'Amount': str(Amount),
        'Description': Description,
        'Type': 'MERCHANT',
        'Reference': Reference,

    }

    url = pesapal_processor3.postDirectOrder(post_params, request_data)

    return url


def get_detailed_order_status(merchant_reference, transaction_tracking_id):

    post_params = {
        'pesapal_merchant_reference': merchant_reference,
        'pesapal_transaction_tracking_id': transaction_tracking_id
    }
    url = pesapal_processor3.queryPaymentDetails(post_params)
    response = urllib.request.urlopen(url)

    return response.read()


def get_payment_status(merchant_reference, transaction_tracking_id):

    post_params = {
        'pesapal_merchant_reference': merchant_reference,
        'pesapal_transaction_tracking_id': transaction_tracking_id
    }
    url = pesapal_processor3.queryPaymentStatus(post_params)
    response = urllib.request.urlopen(url)

    return response.read()
