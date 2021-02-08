import frappe
from flutterwave import pyflutterwave

def on_payment_authorized(**kwargs):
    verification_data = verify_flutterwave_transaction(**kwargs)
    if verification_data:
        attempt_to_set_payment_entry_as_paid(verification_data)

def verify_flutterwave_transaction(**kwargs):
    tx_ref = kwargs.get('tx_ref')
    transaction_id = kwargs.get('transaction_id')

    link_log = frappe.get_doc('Flutterwave Link Log', tx_ref)
    settings = frappe.get_doc('Flutterwave Settings', link_log.controller)
    secret_key = settings.get_password(fieldname='secret_key', raise_exception=False)
    Flutterwave = pyflutterwave.TransactionVerification(secret_key=secret_key, public_key=settings.public_key)
    Flutterwave.verify(transaction_id)
    attempt_to_set_payment_entry_as_paid(Flutterwave.ctx.data)

    return True

def attempt_to_set_payment_entry_as_paid(data):
    request_name = data.get('meta').get('payment_request')
    amount_settled = data.get('amount_settled')
    request = frappe.get_doc('Payment Request', request_name)

    if amount_settled >= request.grand_total:
        request.set_as_paid()
