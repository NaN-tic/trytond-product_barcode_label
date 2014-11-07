# This file is part product_barcode_label module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.model import ModelView, fields
from trytond.pool import PoolMeta
from trytond.pyson import Eval


import logging

__all__ = ['ProductCode']
__metaclass__ = PoolMeta


try:
    from barcode import generate
except ImportError:
    message = 'Unable to import pyBarcode: pip install pyBarcode'
    logging.getLogger('product_barcode_label').error(message)
    raise Exception(message)
    

class ProductCode:
    'ProductCode'
    __name__ = 'product.code'
    data = fields.Function(fields.Binary('Label', filename='number', states={
                'invisible': ~(Eval('barcode')),
                }, depends=['barcode']), 'get_data')

    @classmethod
    def __setup__(cls):
        super(ProductCode, cls).__setup__()
        cls._buttons.update({
            'label': {
                'invisible': ~(Eval('barcode')),
                },
            })

    @classmethod
    @ModelView.button
    def label(cls, values):
        '''Get label from barcode'''
        for value in values:
            barcode = value.barcode.upper()
            number = value.number
            output = '/tmp/%s-%s' % (barcode, number) 
            generate(barcode, number, output=output)

    def get_data(self, name):
        value = None
        if not self.barcode or not self.number:
            return value

        barcode = self.barcode.upper()
        number = self.number

        filename = '/tmp/%s-%s.svg' % (barcode, number) 
        try:
            with open(filename, 'rb') as file_p:
                value = buffer(file_p.read())
        except IOError:
            pass
        return value
