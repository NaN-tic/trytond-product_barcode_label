# This file is part product_barcode_label module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.pool import Pool
from .product import *


def register():
    Pool.register(
        ProductCode,
        module='product_barcode_label', type_='model')
