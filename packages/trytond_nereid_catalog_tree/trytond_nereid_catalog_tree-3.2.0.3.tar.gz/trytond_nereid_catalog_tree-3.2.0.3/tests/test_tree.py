# -*- coding: utf-8 -*-
"""
test_tree

:copyright: (c) 2013-2014 by Openlabs Technologies & Consulting (P) Limited
:license: BSD, see LICENSE for more details.
"""
from decimal import Decimal
import unittest

from lxml import objectify
import trytond.tests.test_tryton
from trytond.tests.test_tryton import POOL, USER, DB_NAME, CONTEXT, \
    test_view, test_depends
from nereid.testing import NereidTestCase
from trytond.transaction import Transaction
from trytond.exceptions import UserError


class TestTree(NereidTestCase):
    """
    Test Tree
    """

    def setup_defaults(self):
        """
        Setup defaults
        """
        Node = POOL.get('product.tree_node')

        usd, = self.Currency.create([{
            'name': 'US Dollar',
            'code': 'USD',
            'symbol': '$',
        }])

        with Transaction().set_context(company=None):
            party1, = self.Party.create([{
                'name': 'Openlabs',
            }])

            company, = self.Company.create([{
                'party': party1.id,
                'currency': usd.id
            }])

            party2, = self.Party.create([{
                'name': 'Guest User'
            }])

            guest_user, = self.NereidUser.create([{
                'party': party2.id,
                'display_name': 'Guest User',
                'email': 'guest@openlabs.co.in',
                'password': 'password',
                'company': company.id
            }])

        self.category, = self.Category.create([{
            'name': 'CategoryA',
            'uri': 'category-1'
        }])

        url_map, = self.UrlMap.search([], limit=1)
        en_us, = self.Language.search([('code', '=', 'en_US')])

        self.locale_en_us, = self.Locale.create([{
            'code': 'en_US',
            'language': en_us.id,
            'currency': usd.id
        }])
        self.default_node, = Node.create([{
            'name': 'root',
            'slug': 'root',
        }])

        self.Site.create([{
            'name': 'localhost',
            'url_map': url_map.id,
            'company': company.id,
            'application_user': USER,
            'default_locale': self.locale_en_us.id,
            'guest_user': guest_user,
            'currencies': [('add', [usd.id])],
            'root_tree_node': self.default_node,
        }])

    def setUp(self):
        """
        Set up data used in the tests
        this method is called before each test execution
        """
        trytond.tests.test_tryton.install_module('nereid_catalog_tree')

        self.Currency = POOL.get('currency.currency')
        self.Site = POOL.get('nereid.website')
        self.Product = POOL.get('product.product')
        self.Company = POOL.get('company.company')
        self.NereidUser = POOL.get('nereid.user')
        self.UrlMap = POOL.get('nereid.url_map')
        self.Language = POOL.get('ir.lang')
        self.Party = POOL.get('party.party')
        self.Category = POOL.get('product.category')
        self.Template = POOL.get('product.template')
        self.Uom = POOL.get('product.uom')
        self.Locale = POOL.get('nereid.website.locale')

        self.templates = {
            'catalog/node.html':
            '{{ products|length }}||' +
            '{{ make_tree_crumbs(node=node)|safe|escape }}'
        }

    def test_0005_test_view(self):
        """
        Test the views
        """
        test_view('nereid_catalog_tree')

    def test_007_test_depends(self):
        """
        The Depends
        """
        test_depends()

    def test_0010_create_product_node_in_tree(self):
        """
        Test if a product can be created which can be
        associated to a node
        """
        Node = POOL.get('product.tree_node')

        with Transaction().start(DB_NAME, USER, context=CONTEXT):
            self.setup_defaults()
            uom, = self.Uom.search([], limit=1)

            values1 = {
                'name': 'Product-1',
                'category': self.category.id,
                'type': 'goods',
                'list_price': Decimal('10'),
                'cost_price': Decimal('5'),
                'default_uom': uom.id,
                'products': [
                    ('create', [{
                        'uri': 'product-1',
                        'displayed_on_eshop': True
                    }])
                ]
            }

            template1, = self.Template.create([values1])

            node1, = Node.create([{
                'name': 'Node1',
                'slug': 'node1',
                'products': [('add', [template1.id])]
            }])

            self.assert_(node1)

            # Check if default tree node type is 'catalog'
            self.assertEqual(node1.type_, 'catalog')
            # Check if node1 is active by default
            self.assertTrue(node1.active)
            # Check if default display is product variant
            self.assertEqual(node1.display, 'product.product')

    def test_0020_create_product_node_with_children(self):
        """
        Test if a product can be created to find
        its children
        """
        Node = POOL.get('product.tree_node')

        with Transaction().start(DB_NAME, USER, context=CONTEXT):
            self.setup_defaults()
            uom, = self.Uom.search([], limit=1)

            values1 = {
                'name': 'Product-1',
                'category': self.category.id,
                'type': 'goods',
                'list_price': Decimal('10'),
                'cost_price': Decimal('5'),
                'default_uom': uom.id,
                'products': [
                    ('create', [{
                        'uri': 'product-1',
                        'displayed_on_eshop': True
                    }])
                ]
            }

            values2 = {
                'name': 'Product-2',
                'category': self.category.id,
                'list_price': Decimal('10'),
                'cost_price': Decimal('5'),
                'default_uom': uom.id,
                'products': [
                    ('create', [{
                        'uri': 'product-2',
                        'displayed_on_eshop': True
                    }])
                ]
            }

            template1, template2 = self.Template.create([values1, values2])

            node1, = Node.create([{
                'name': 'Node1',
                'type_': 'catalog',
                'slug': 'node1',
                'products': [('add', [template1.id])]
            }])

            self.assert_(node1)

            node2, = Node.create([{
                'name': 'Node2',
                'type_': 'catalog',
                'slug': 'node2',
                'products': [('add', [template2.id])]
            }])

            self.assert_(node2)

            Node.write([node2], {
                'parent': node1
            })
            self.assertEqual(node2.parent, node1)
            self.assertTrue(node2 in node1.children)
            self.assertEqual(len(node2.children), 0)

    def test_0030_nereid_render_method(self):
        """
        Test if the url for the active id of the current node
        returns all the children and its branches
        """
        Node = POOL.get('product.tree_node')

        with Transaction().start(DB_NAME, USER, context=CONTEXT):
            self.setup_defaults()
            uom, = self.Uom.search([], limit=1)

            values1 = {
                'name': 'Product-1',
                'category': self.category.id,
                'type': 'goods',
                'list_price': Decimal('10'),
                'cost_price': Decimal('5'),
                'default_uom': uom.id,
                'products': [
                    ('create', [{
                        'uri': 'product-1',
                        'displayed_on_eshop': True
                    }])
                ]
            }

            values2 = {
                'name': 'Product-2',
                'category': self.category.id,
                'list_price': Decimal('10'),
                'cost_price': Decimal('5'),
                'default_uom': uom.id,
                'products': [
                    ('create', [{
                        'uri': 'product-2',
                        'displayed_on_eshop': True
                    }, {
                        'uri': 'product-21',
                        'displayed_on_eshop': True
                    }])
                ]
            }

            values3 = {
                'name': 'Product-3',
                'category': self.category.id,
                'list_price': Decimal('10'),
                'cost_price': Decimal('5'),
                'default_uom': uom.id,
                'products': [
                    ('create', [{
                        'uri': 'product-3',
                        'displayed_on_eshop': False
                    }])
                ]
            }

            template1, template2, template3, = self.Template.create([
                values1, values2, values3
            ])

            node1, = Node.create([{
                'name': 'Node1',
                'type_': 'catalog',
                'slug': 'node1',
                'products': [('add', template1.products)]
            }])

            self.assert_(node1)

            node2, = Node.create([{
                'name': 'Node2',
                'type_': 'catalog',
                'slug': 'node2',
                'display': 'product.template',
                'products': [('add', template2.products)]
            }])

            self.assert_(node2)

            node3, = Node.create([{
                'name': 'Node3',
                'type_': 'catalog',
                'slug': 'node3',
            }])

            Node.write([node2], {
                'parent': node1
            })

            Node.write([node3], {
                'parent': node2
            })

            self.assert_(node2)

            app = self.get_app()

            with app.test_client() as c:
                url = 'nodes/{0}/{1}/{2}'.format(
                    node1.id, node1.slug, 1
                )
                rv = c.get(url)
                self.assertEqual(rv.status_code, 200)
                # Test is if there are 3 products.
                # 1 from node1 and 2 from node2
                self.assertEqual(rv.data[0], '3')

                url = 'nodes/{0}/{1}/{2}'.format(
                    node2.id, node2.slug, 1
                )
                rv = c.get(url)
                self.assertEqual(rv.status_code, 200)
                # Test if products length is 1 as display of
                # node2 is set to 'product.template'
                self.assertEqual(rv.data[0], '1')

    def test_0040_create_product_with_parent_as_itself(self):
        """
        This test creates a node and sets the product as
        the parent of itself, which shouldn't happen
        """
        Node = POOL.get('product.tree_node')

        with Transaction().start(DB_NAME, USER, context=CONTEXT):
            self.setup_defaults()
            uom, = self.Uom.search([], limit=1)

            values1 = {
                'name': 'Product-1',
                'category': self.category.id,
                'type': 'goods',
                'list_price': Decimal('10'),
                'cost_price': Decimal('5'),
                'default_uom': uom.id,
                'products': [
                    ('create', [{
                        'uri': 'product-1',
                        'displayed_on_eshop': True
                    }])
                ]
            }

            template1, = self.Template.create([values1])

            node1, = Node.create([{
                'name': 'Node1',
                'type_': 'catalog',
                'slug': 'node1',
                'products': [('add', [template1.id])]
            }])

            self.assert_(node1)
            self.assertRaises(UserError, Node.write, [node1], {
                'parent': node1
            })

    def test_0050_product_template_disabled(self):
        """
        Ensure that the products are not listed when the template is
        disabled
        """
        Node = POOL.get('product.tree_node')

        with Transaction().start(DB_NAME, USER, context=CONTEXT):
            self.setup_defaults()
            uom, = self.Uom.search([], limit=1)

            values1 = {
                'name': 'Product-1',
                'category': self.category.id,
                'type': 'goods',
                'list_price': Decimal('10'),
                'cost_price': Decimal('5'),
                'default_uom': uom.id,
                'products': [
                    ('create', [{
                        'uri': 'product-1',
                        'displayed_on_eshop': True
                    }])
                ]
            }

            template1, = self.Template.create([values1])

            node1, = Node.create([{
                'name': 'Node1',
                'type_': 'catalog',
                'slug': 'node1',
                'products': [('add', [template1.id])]
            }])

            app = self.get_app()

            with app.test_client() as c:
                rv = c.get('nodes/%d/_/1' % node1.id)
                self.assertEqual(rv.status_code, 200)
                self.assertEqual(rv.data[0], '1')

            self.assertEqual(node1.get_products().count, 1)
            self.assertEqual(len(node1.products), 1)

            template1.active = False
            template1.save()

            with app.test_client() as c:
                rv = c.get('nodes/%d/_/1' % node1.id)
                self.assertEqual(rv.status_code, 200)
                self.assertEqual(rv.data[0], '0')

            self.assertEqual(node1.get_products().count, 0)
            self.assertEqual(len(node1.products), 1)

    def test_0060_make_tree_crumbs(self):
        """
        Test to get breadcrumbs on node template
        """
        Node = POOL.get('product.tree_node')

        with Transaction().start(DB_NAME, USER, context=CONTEXT):
            self.setup_defaults()
            app = self.get_app()

            parent_node, = Node.create([{
                'name': 'Node1',
                'type_': 'catalog',
                'slug': 'node1',
                'parent': self.default_node,
            }])

            child_node, = Node.create([{
                'name': 'Node2',
                'type_': 'catalog',
                'slug': 'node2',
                'parent': parent_node,
            }])

            with app.test_client() as c:
                rv = c.get('nodes/%d/node2' % child_node.id)
                self.assertEqual(
                    rv.data[3:],
                    "[('/', 'Home'), ('/nodes/1/root', u'root'), " +
                    "('/nodes/2/node1', u'Node1'), " +
                    "('/nodes/3/node2', u'Node2')]"
                )

    def test_0070_tree_sitemap_index(self):
        """
        Assert that the sitemap index returns 1 result
        """
        Node = POOL.get('product.tree_node')

        with Transaction().start(DB_NAME, USER, context=CONTEXT):
            self.setup_defaults()
            uom, = self.Uom.search([], limit=1)
            app = self.get_app()

            values1 = {
                'name': 'Product-1',
                'category': self.category.id,
                'type': 'goods',
                'list_price': Decimal('10'),
                'cost_price': Decimal('5'),
                'default_uom': uom.id,
                'products': [
                    ('create', [{
                        'uri': 'product-1',
                        'displayed_on_eshop': True
                    }])
                ]
            }

            values2 = {
                'name': 'Product-2',
                'category': self.category.id,
                'list_price': Decimal('10'),
                'cost_price': Decimal('5'),
                'default_uom': uom.id,
                'products': [
                    ('create', [{
                        'uri': 'product-2',
                        'displayed_on_eshop': True
                    }])
                ]
            }

            template1, template2 = self.Template.create([values1, values2])

            node1, = Node.create([{
                'name': 'Node1',
                'type_': 'catalog',
                'slug': 'node1',
                'products': [('add', [template1.id, template2.id])]
            }])

            self.assert_(node1)

            with app.test_client() as c:
                rv = c.get('/sitemaps/tree-index.xml')
                xml = objectify.fromstring(rv.data)
                self.assertTrue(xml.tag.endswith('sitemapindex'))
                self.assertEqual(len(xml.getchildren()), 1)

                rv = c.get(
                    xml.sitemap.loc.pyval.split('localhost/', 1)[-1]
                )
                xml = objectify.fromstring(rv.data)
                self.assertTrue(xml.tag.endswith('urlset'))
                self.assertEqual(len(xml.getchildren()), 2)


def suite():
    "Node test suite"
    test_suite = unittest.TestSuite()
    test_suite.addTests(
        unittest.TestLoader().loadTestsFromTestCase(TestTree)
    )
    return test_suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
