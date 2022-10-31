
from models.order import Order, OrderAddress
from framework.serialization import Serializable


class ShipEngineShipmentDetail:
    def __init__(self, data: dict):
        self.length = data.get('length')
        self.width = data.get('width')
        self.height = data.get('height')
        self.weight = data.get('weight')


class ShipEngineShipment(Serializable):
    def __init__(self, order: Order, shipment_detail: ShipEngineShipmentDetail):
        self.dimensions = self.get_dimensions(
            shipment_detail=shipment_detail)

        self.weight = shipment_detail.weight

        self.destination = self.get_destination(
            order_address=order.shipping_address)

        self.origin = self.get_shipper()

        self.carrier_id = 'UPS'
        self.service_code = 'ups_ground'
        self.insurance_provider = 'carrier'
        self.insured_value = order.subtotal

    def get_destination(self, order_address: OrderAddress):
        return {
            'name': order_address.recipient,
            'address_line1': order_address.street_address,
            'city_locality': order_address.city,
            'state_province': order_address.state_code,
            'postal_code': order_address.postal_code,
            'country_code': order_address.country_code,
            'phone': order_address.phone_number
        }

    def get_shipper(self):
        return {
            'name': 'Dan Leonard',
            'address_line1': '4202 E Cactus Rd',
            'city_locality': 'Phoenix',
            'state_province': 'AZ',
            'postal_code': '85032',
            'country_code': 'US',
            'phone': '856-332-3608'
        }

    def get_dimensions(self, shipment_detail: ShipEngineShipmentDetail):
        return {
            'length': shipment_detail.length,
            'width': shipment_detail.width,
            'height': shipment_detail.height
        }
