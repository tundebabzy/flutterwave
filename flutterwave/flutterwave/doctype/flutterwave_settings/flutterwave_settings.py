# -*- coding: utf-8 -*-
# Copyright (c) 2021, Babatunde Akinyanmi and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
import paystakk
from frappe import _
from frappe.integrations.utils import create_payment_gateway, create_request_log
from frappe.model.document import Document
from frappe.utils import call_hook_method, nowdate, get_url
from requests import RequestException, ConnectionError
from flutterwave import pyflutterwave

SUPPORTED_CURRENCIES = ['NGN']

class FlutterwaveSettings(Document):
	supported_currencies = SUPPORTED_CURRENCIES

	def validate(self):
		if not self.flags.ignore_mandatory:
			self.validate_credentials()

	def on_update(self):
		name = 'Flutterwave-{0}'.format(self.gateway_name)
		create_payment_gateway(
			name,
			settings='Flutterwave Settings',
			controller=self.gateway_name
		)
		call_hook_method('payment_gateway_enabled', gateway=name)

	def validate_credentials(self):
		secret_key = self.get_password(fieldname='secret_key', raise_exception=False)
		Flutterwave = pyflutterwave.AccountVerification(secret_key=secret_key, public_key=self.public_key)
		try:
			Flutterwave.verify(self.merchant_id, 'flutterwave')
		except ConnectionError:
			frappe.throw('There was a connection problem. Please ensure that'
						 ' you have a working internet connection.')

		if not Flutterwave.ctx.status.lower() == 'success':
			frappe.throw(api.ctx.message, title=_("Failed Credentials Validation"))

	def validate_transaction_currency(self, currency):
		if currency not in self.supported_currencies:
			frappe.throw(
				_('{0} is not supported by Flutterwave at the moment.').format(currency))

	def get_payment_url(self, **kwargs):
		amount = kwargs.get('amount')
		description = kwargs.get('description')
		slug = kwargs.get('reference_docname')
		email = kwargs.get('payer_email')
		identifier = hash('{0}{1}{2}'.format(amount, description, slug))
		metadata = {
			'payment_request': kwargs.get('order_id'),
			'customer_name': kwargs.get('payer_name'),
			'identifier': identifier
		}
		customer = {'email': email}
		customizations = {"title": 'Payment request: {0}'.format(slug)}

		secret_key = self.get_password(fieldname='secret_key', raise_exception=False)

		Flutterwave = pyflutterwave.Payment(secret_key=secret_key, public_key=self.public_key)
		redirect_url = get_url('/api/method/flutterwave.flutterwave.doctype.flutterwave_settings.flutterwave_settings.payment_done')
		Flutterwave.initiate(
			tx_ref=identifier, amount=amount, payment_options='card',
			redirect_url=redirect_url, customer=customer, customizations=customizations,
			meta=metadata
		)
		# self.integration_request = create_request_log(kwargs, "Host", "Flutterwave")
		if not Flutterwave.ctx.status == 'success':
			frappe.throw(Flutterwave.ctx.message)
		else:
			print('got a link -> ', Flutterwave.ctx.data, Flutterwave.ctx.message, Flutterwave.ctx.status)
			self.make_log(identifier, slug)
			return Flutterwave.ctx.data['link']

	def make_log(self, tx_ref, ref_docname):
		link_log = frappe.new_doc('Flutterwave Link Log')
		link_log.ref = ref_docname
		link_log.tx_ref = tx_ref
		link_log.controller = self.name
		link_log.insert()

@frappe.whitelist(allow_guest=True)
def payment_done(tx_ref=None, transaction_id=None, status=None):
	if not status == 'successful':
		frappe.response['http_status_code'] = 404
	if not tx_ref or not transaction_id:
		frappe.response['http_status_code'] = 404
	if tx_ref and transaction_id and status:
		do_payment_done(tx_ref, transaction_id, status)
		frappe.response['http_status_code'] = 200
		return """
		<p>Payment was successful. Thank you. You can close the window.</p>
		"""
	return

def do_payment_done(tx_ref, transaction_id, status):
	link_log = frappe.get_doc('Payment Link Log', tx_ref)
	settings = frappe.get_doc('Flutterwave Settings', link_log.controller)
	secret_key = settings.get_password(fieldname='secret_key', raise_exception=False)
	Flutterwave = pyflutterwave.TransactionVerification(secret_key=secret_key, public_key=settings.public_key)
	Flutterwave.verify(transaction_id)
	print (Flutterwave.ctx.data)

def queue_do_payment_done(tx_ref, transaction_id, status):
	pass