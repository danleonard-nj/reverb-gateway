from framework.serialization import Serializable


class Order(Serializable):
    def __init__(self, data):
        self.order_id = data.get('uuid')
        self.order_number = data.get('order_number')
        self.order_type = data.get('order_type')
        self.product_id = data.get('product_id')
        self.product = data.get('title')
        self.order_status = data.get('status')
        self.buyer_name = data.get('buyer_name')
        self.paid_date = data.get('paid_at')
        self.ship_date = data.get('shipped_at')
        self.shipping_provider = data.get('shipping_provider')
        self.shipping_code = data.get('shipping_code')
        self.shipment_status = data.get('shipment_status')
        self.created_date = data.get('created_at')
        self.updated_date = data.get('updated_at')

        self.shipping_address = OrderAddress(
            data=data.get('shipping_address'))

        subtotal = data.get('amount_product_subtotal') or dict()
        self.subtotal = float(subtotal.get('amount') or 0)

    def to_dict(self):
        return self.__dict__

    def to_json(self):
        return self.__dict__


class OrderAddress(Serializable):
    def __init__(self, data):
        if data is not None:
            self.id = data.get('id')
            self.display_location = data.get('display_location')
            self.recipient = data.get('name')
            self.street_address = data.get('street_address')
            self.city = data.get('locality')
            self.state_code = data.get('region')
            self.postal_code = data.get('postal_code')
            self.country_code = data.get('country_code')
            self.phone_number = data.get('phone')


class ShipOrderRequest(Serializable):
    def __init__(self, data):
        self.tracking_number = data.get('tracking_number')
        self.provider = data.get('carrier')
        self.send_notification = True
