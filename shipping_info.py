class Shipping_Info:
    self.product_order_number
    self.billing_landing_info

    def __init__(self):
        self.product_order_number = {}
        self.billing_landing_info = {}

    def check_po_number(self,po_number):
        if po_number in self.product_order_number.keys()
            return True
        else:
            return False

    def check_invoice_number(self, invoice_number):
        if invoice_number in self.billing_landing_info.keys():
            return True
        else:
            return False

    def update_po_number(self, po_number):
        self.product_order_number[po_number] = {}
