from . import pesapal_processor


def post_transaction(Reference, FirstName, LastName, Email, PhoneNumber, Description, Amount, Type):
    oauth_consumer_key = "qkio1BGGYAXTu2JOfm7XSXNruoZsrqEW"
    oauth_consumer_secret = "osGQ364R49cXKeOYSpaOnT++rHs="
    oauth_callback = "https://fda9-197-232-61-208.ngrok-free.app/payment/oauth_callback/"

    pesapal = pesapal_processor.PesaPal(oauth_consumer_key, oauth_consumer_secret, 'sandbox')
    pesapal.reference = Reference
    pesapal.last_name = LastName
    pesapal.first_name = FirstName
    pesapal.amount = Amount
    pesapal.type_=Type
    pesapal.phone_number = PhoneNumber
    pesapal.email = Email
    pesapal.callback_url = oauth_callback
    iframe_src = pesapal.generate_iframe_src()
    return iframe_src