from framework.serialization import Serializable


class GetOrdersRequest(Serializable):
    def __init__(self, request):
        self.page_number = request.args.get('page_number')
