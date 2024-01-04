from . import pesapal_processor


def post_transaction(Reference, FirstName, LastName, Email, PhoneNumber, Description, Amount, Type):
    pesapal = pesapal_processor.PesaPal(OAUTH_CONSUMER_KEY, OAUTH_CONSUMER_SECRET, 'sandbox')
    pesapal.reference = Reference
    pesapal.last_name = LastName
    pesapal.first_name = FirstName
    pesapal.amount = Amount
    pesapal.type_ = Type
    pesapal.phone_number = PhoneNumber
    pesapal.email = Email
    pesapal.callback_url = OAUTH_CALLBACK_URL
    iframe_src = pesapal.generate_iframe_src()
    return iframe_src