#This file is part of Tryton.  The COPYRIGHT file at the top level
#of this repository contains the full copyright notices and license terms.
from trytond.model import Workflow, ModelView, ModelSQL, fields
from trytond.pyson import Not, Equal, Eval, Or, Bool
from trytond.backend import TableHandler
from trytond.transaction import Transaction
from trytond.pool import Pool

STATES = {
    'readonly': Not(Equal(Eval('state'), 'draft')),
}
DEPENDS = ['state']


class Inventory(Workflow, ModelSQL, ModelView):
    'Stock Inventory'
    _name = 'stock.inventory'
    _description = __doc__

    location = fields.Many2One(
        'stock.location', 'Location', required=True,
        domain=[('type', '=', 'storage')], states={
            'readonly': Or(Not(Equal(Eval('state'), 'draft')),
                Bool(Eval('lines'))),
            },
        depends=['state', 'lines'])
    date = fields.Date('Date', required=True, states={
            'readonly': Or(Not(Equal(Eval('state'), 'draft')),
                Bool(Eval('lines'))),
            },
        depends=['state', 'lines'])
    lost_found = fields.Many2One(
        'stock.location', 'Lost and Found', required=True,
        domain=[('type', '=', 'lost_found')], states=STATES, depends=DEPENDS)
    lines = fields.One2Many(
        'stock.inventory.line', 'inventory', 'Lines', states=STATES,
        depends=DEPENDS)
    company = fields.Many2One('company.company', 'Company', required=True,
        states={
            'readonly': Or(Not(Equal(Eval('state'), 'draft')),
                Bool(Eval('lines'))),
            },
        depends=['state', 'lines'])
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
        ('cancel', 'Canceled'),
        ], 'State', readonly=True, select=True)

    def __init__(self):
        super(Inventory, self).__init__()
        self._order.insert(0, ('date', 'DESC'))
        self._error_messages.update({
                'delete_cancel': 'Inventory "%s" must be cancelled before ' \
                    'deletion!',
                })
        self._transitions |= set((
                ('draft', 'done'),
                ('draft', 'cancel'),
                ))
        self._buttons.update({
                'confirm': {
                    'invisible': Eval('state').in_(['done', 'cancel']),
                    },
                'cancel': {
                    'invisible': Eval('state').in_(['cancel', 'done']),
                    },
                'complete_lines': {
                    'readonly': Eval('state') != 'draft',
                    },
                })

    def init(self, module_name):
        super(Inventory, self).init(module_name)
        cursor = Transaction().cursor

        # Add index on create_date
        table = TableHandler(cursor, self, module_name)
        table.index_action('create_date', action='add')

    def default_state(self):
        return 'draft'

    def default_date(self):
        date_obj = Pool().get('ir.date')
        return date_obj.today()

    def default_company(self):
        return Transaction().context.get('company')

    def default_lost_found(self):
        location_obj = Pool().get('stock.location')
        location_ids = location_obj.search(self.lost_found.domain)
        if len(location_ids) == 1:
            return location_ids[0]

    def delete(self, ids):
        if isinstance(ids, (int, long)):
            ids = [ids]
        # Cancel before delete
        self.cancel(ids)
        for inventory in self.browse(ids):
            if inventory.state != 'cancel':
                self.raise_user_error('delete_cancel', inventory.rec_name)
        return super(Inventory, self).delete(ids)

    @ModelView.button
    @Workflow.transition('done')
    def confirm(self, ids):
        line_obj = Pool().get('stock.inventory.line')
        for inventory in self.browse(ids):
            for line in inventory.lines:
                line_obj.create_move(line)

    @ModelView.button
    @Workflow.transition('cancel')
    def cancel(self, ids):
        line_obj = Pool().get("stock.inventory.line")
        inventories = self.browse(ids)
        line_obj.cancel_move([l for i in inventories for l in i.lines])

    def copy(self, ids, default=None):
        date_obj = Pool().get('ir.date')
        line_obj = Pool().get('stock.inventory.line')

        int_id = False
        if isinstance(ids, (int, long)):
            int_id = True
            ids = [ids]

        if default is None:
            default = {}
        default = default.copy()
        default['date'] = date_obj.today()
        default['lines'] = None

        new_ids = []
        for inventory in self.browse(ids):
            new_id = super(Inventory, self).copy(inventory.id, default=default)
            line_obj.copy([x.id for x in inventory.lines],
                    default={
                        'inventory': new_id,
                        'move': None,
                        })
            self.complete_lines(new_id)
            new_ids.append(new_id)

        if int_id:
            return new_ids[0]
        return new_ids

    def complete_lines(self, ids):
        '''
        Complete or update the inventories

        :param ids: the ids of stock.inventory
        :param context: the context
        '''
        pool = Pool()
        line_obj = pool.get('stock.inventory.line')
        product_obj = pool.get('product.product')

        if isinstance(ids, (int, long)):
            ids = [ids]

        inventories = self.browse(ids)

        for inventory in inventories:
            # Compute product quantities
            with Transaction().set_context(stock_date_end=inventory.date):
                pbl = product_obj.products_by_location(
                        [inventory.location.id])

            # Index some data
            product2uom = {}
            product2type = {}
            product2consumable = {}
            for product in product_obj.browse([line[1] for line in pbl]):
                product2uom[product.id] = product.default_uom.id
                product2type[product.id] = product.type
                product2consumable[product.id] = product.consumable

            product_qty = {}
            for (location, product), quantity in pbl.iteritems():
                product_qty[product] = (quantity, product2uom[product])

            # Update existing lines
            for line in inventory.lines:
                if not (line.product.active and
                        line.product.type == 'goods'
                        and not line.product.consumable):
                    line_obj.delete(line.id)
                    continue
                if line.product.id in product_qty:
                    quantity, uom_id = product_qty.pop(line.product.id)
                elif line.product.id in product2uom:
                    quantity, uom_id = 0.0, product2uom[line.product.id]
                else:
                    quantity, uom_id = 0.0, line.product.default_uom.id
                values = line_obj.update_values4complete(line, quantity,
                    uom_id)
                if values:
                    line_obj.write(line.id, values)

            # Create lines if needed
            for product_id in product_qty:
                if (product2type[product_id] != 'goods'
                        or product2consumable[product_id]):
                    continue
                quantity, uom_id = product_qty[product_id]
                values = line_obj.create_values4complete(product_id, inventory,
                        quantity, uom_id)
                line_obj.create(values)

Inventory()


class InventoryLine(ModelSQL, ModelView):
    'Stock Inventory Line'
    _name = 'stock.inventory.line'
    _description = __doc__
    _rec_name = 'product'

    product = fields.Many2One('product.product', 'Product', required=True,
        domain=[
            ('type', '=', 'goods'),
            ('consumable', '=', False),
            ],
        on_change=['product'])
    uom = fields.Function(fields.Many2One('product.uom', 'UOM'), 'get_uom')
    unit_digits = fields.Function(fields.Integer('Unit Digits'),
            'get_unit_digits')
    expected_quantity = fields.Float('Expected Quantity', required=True,
            digits=(16, Eval('unit_digits', 2)), readonly=True,
            depends=['unit_digits'])
    quantity = fields.Float('Quantity', required=True,
        digits=(16, Eval('unit_digits', 2)), depends=['unit_digits'])
    move = fields.Many2One('stock.move', 'Move', readonly=True)
    inventory = fields.Many2One('stock.inventory', 'Inventory', required=True,
            ondelete='CASCADE')

    def __init__(self):
        super(InventoryLine, self).__init__()
        self._sql_constraints += [
            ('check_line_qty_pos',
                'CHECK(quantity >= 0.0)', 'Line quantity must be positive!'),
            ('inventory_product_uniq', 'UNIQUE(inventory, product)',
                'Product must be unique by inventory!'),
        ]
        self._order.insert(0, ('product', 'ASC'))

    def default_unit_digits(self):
        return 2

    def default_expected_quantity(self):
        return 0.

    def on_change_product(self, vals):
        product_obj = Pool().get('product.product')
        res = {}
        res['unit_digits'] = 2
        if vals.get('product'):
            product = product_obj.browse(vals['product'])
            res['uom'] = product.default_uom.id
            res['uom.rec_name'] = product.default_uom.rec_name
            res['unit_digits'] = product.default_uom.digits
        return res

    def get_uom(self, ids, name):
        res = {}
        for line in self.browse(ids):
            res[line.id] = line.product.default_uom.id
        return res

    def get_unit_digits(self, ids, name):
        res = {}
        for line in self.browse(ids):
            res[line.id] = line.product.default_uom.digits
        return res

    def cancel_move(self, lines):
        move_obj = Pool().get('stock.move')
        move_obj.write([l.move.id for l in lines if l.move], {
            'state': 'cancel',
            })
        move_obj.delete([l.move.id for l in lines if l.move])
        self.write([l.id for l in lines if l.move], {
            'move': None,
            })

    def create_move(self, line):
        '''
        Create move for an inventory line

        :param line: a BrowseRecord of inventory.line
        :return: the stock.move id or None
        '''
        move_obj = Pool().get('stock.move')
        uom_obj = Pool().get('product.uom')

        delta_qty = uom_obj.compute_qty(line.uom,
            line.expected_quantity - line.quantity,
            line.uom)
        if delta_qty == 0.0:
            return
        from_location = line.inventory.location.id
        to_location = line.inventory.lost_found.id
        if delta_qty < 0:
            (from_location, to_location, delta_qty) = \
                (to_location, from_location, -delta_qty)

        move_id = move_obj.create({
            'from_location': from_location,
            'to_location': to_location,
            'quantity': delta_qty,
            'product': line.product.id,
            'uom': line.uom.id,
            'company': line.inventory.company.id,
            'state': 'done',
            'effective_date': line.inventory.date,
            })
        self.write(line.id, {
            'move': move_id,
            })
        return move_id

    def update_values4complete(self, line, quantity, uom_id):
        '''
        Return update values to complete inventory

        :param line: a BrowseRecord of inventory.line
        :param quantity: the actual product quantity for the inventory location
        :param uom_id: the UoM id of the product line
        :return: a dictionary
        '''
        res = {}
        # if nothing changed, no update
        if line.quantity == line.expected_quantity == quantity \
                and line.uom.id == uom_id:
            return {}
        res['expected_quantity'] = quantity
        res['uom'] = uom_id
        # update also quantity field if not edited
        if line.quantity == line.expected_quantity:
            res['quantity'] = max(quantity, 0.0)
        return res

    def create_values4complete(self, product_id, inventory, quantity, uom_id):
        '''
        Return create values to complete inventory

        :param product_id: the product.product id
        :param inventory: a BrowseRecord of inventory.inventory
        :param quantity: the actual product quantity for the inventory location
        :param uom_id: the UoM id of the product_id
        :return: a dictionary
        '''
        return {
            'inventory': inventory.id,
            'product': product_id,
            'expected_quantity': quantity,
            'quantity': max(quantity, 0.0),
            'uom': uom_id,
        }

InventoryLine()
