# This file is part product_barcode_label module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import ModelView, fields
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction
from trytond.wizard import Wizard, StateView, Button
from trytond.pyson import Eval
import tempfile
import logging

__all__ = ['ProductCode', 'ProductCodeLabelFile', 'ProductCodeLabel']
__metaclass__ = PoolMeta

try:
    from barcode import generate
except ImportError:
    logger = logging.getLogger(__name__)
    message = 'Unable to import pyBarcode: pip install pyBarcode'
    logger.error(message)
    raise Exception(message)
    

class ProductCode:
    __name__ = 'product.code'

    @classmethod
    def __setup__(cls):
        super(ProductCode, cls).__setup__()
        cls._buttons.update({
            'label': {
                'invisible': ~(Eval('barcode')),
                },
            })

    @classmethod
    @ModelView.button_action('product_barcode_label.wizard_product_code_label')
    def label(cls, codes):
        pass


class ProductCodeLabelFile(ModelView):
    'Product Code Label File'
    __name__ = 'product.code.label.file'
    label = fields.Binary('Label', filename='file_name')
    file_name = fields.Char('File Name')


class ProductCodeLabel(Wizard):
    'Product Code Label'
    __name__ = 'product.code.label'
    start = StateView('product.code.label.file',
        'product_barcode_label.product_code_label_file', [
            Button('Done', 'end', 'tryton-ok', default=True),
            ])

    @classmethod
    def __setup__(cls):
        super(ProductCodeLabel, cls).__setup__()
        cls._error_messages.update({
            'not_barcode': 'Select a barcode in "%(number)s" code.',
            'label_io_error': 'An IO error when generate barcode in ' \
                '"%(number)s" code.',
            'label_error': 'Error when generate barcode in ' \
                '"%(number)s" code.',
        })

    def default_start(self, fields):
        '''Render a barcode file (by code product)'''
        pool = Pool()
        ProductCode = pool.get('product.code')

        code, = ProductCode.browse([Transaction().context['active_id']])

        if not code.barcode:
            self.raise_user_error('not_barcode', {
                    'number': code.barcode,
                    })

        barcode = code.barcode.upper()
        number = code.number
        level, path = tempfile.mkstemp(prefix='%s-%s-' % (barcode, number))

        # generate barcode svg
        filename = generate(barcode, number, output=path)

        try:
            with open(filename, 'rb') as file_p:
                label = fields.Binary.cast(file_p.read())
        except IOError:
            self.raise_user_error('label_io_error', {
                'number': code.barcode,
                })
        except:
            self.raise_user_error('label_error', {
                'number': code.barcode,
                })

        default = {}
        default['label'] = label
        default['file_name'] = '%s-%s.svg' % (barcode, number)
        return default
