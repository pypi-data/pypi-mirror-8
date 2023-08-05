import paypalrestsdk.util as util
from paypalrestsdk.resource import List, Find, Delete, Create, Update, Post, Resource
from paypalrestsdk.api import default as default_api


class Invoice(List, Find, Create, Delete, Update, Post):
    """Invoice class wrapping the REST v1/invoices/invoice endpoint

    Usage::

        >>> invoice_histroy = Invoice.all({"count": 5})

        >>> invoice = Invoice.new({})
        >>> invoice.create()     # return True or False
    """
    path = "v1/invoicing/invoices"

    def send(self):
        return self.post('send', {}, self)

    def remind(self, attributes):
        return self.post('remind', attributes, self)

    def cancel(self, attributes):
        return self.post('cancel', attributes, self)

    def record_payment(self, attributes):
        return self.post('record-payment', attributes, self)

    def record_refund(self, attributes):
        return self.post('record-refund', attributes, self)

    def get_qr_code(self, height=500, width=500, api=None):

        # height and width have default value of 500 as in the APIs
        api = api or default_api()

        # Construct url similar to
        # /invoicing/invoices/<INVOICE-ID>/qr-code?height=<HEIGHT>&width=<WIDTH>
        endpoint = util.join_url(self.path, str(self['id']), 'qr-code')
        image_attributes = [('height', height), ('width', width)]
        url = util.join_url_params(endpoint, image_attributes)

        return Resource(self.api.get(url), api=api)

    @classmethod
    def search(cls, params=None, api=None):
        api = api or default_api()
        params = params or {}

        url = util.join_url(cls.path, 'search')

        return Resource(api.post(url, params), api=api)

Invoice.convert_resources['invoices'] = Invoice
Invoice.convert_resources['invoice'] = Invoice
