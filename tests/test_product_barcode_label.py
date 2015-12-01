# This file is part of the product_barcode_label module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class ProductBarcodeLabelTestCase(ModuleTestCase):
    'Test Product Barcode Label module'
    module = 'product_barcode_label'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        ProductBarcodeLabelTestCase))
    return suite