from .base import Resource
from ..constants.url import URL


class PaymentMethod(Resource):
    def __init__(self, client=None):
        super(PaymentMethod, self).__init__(client)
        self.base_url = URL.PAYMENT_METHOD_URL

    def all(self, data={}, **kwargs):
        """"
        Fetch all customer

        Returns:
            Dictionary of Customers data
        """
        return super(PaymentMethod, self).all(data, **kwargs)
    
    def delete(self, card_id, **kwargs):
        """"
        Delete an invoice
        You can delete an invoice which is in the draft state.

        Args:
            invoice_id : Id for delete the invoice
        Returns:
            The response is always be an empty array like this - []
        """
        url = "{}/{}".format(self.base_url, card_id)
        return self.delete_url(url, {}, **kwargs)
