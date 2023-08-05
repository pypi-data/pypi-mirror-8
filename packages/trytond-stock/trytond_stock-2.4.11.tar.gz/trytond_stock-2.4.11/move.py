#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
from decimal import Decimal
from functools import reduce
from trytond.model import ModelView, ModelSQL, fields
from trytond.backend import TableHandler
from trytond.pyson import In, Eval, Not, Equal, If, Get, Bool
from trytond.transaction import Transaction
from trytond.pool import Pool

STATES = {
    'readonly': In(Eval('state'), ['cancel', 'assigned', 'done']),
}
DEPENDS = ['state']


class Move(ModelSQL, ModelView):
    "Stock Move"
    _name = 'stock.move'
    _description = __doc__
    _order_name = 'product'
    product = fields.Many2One("product.product", "Product", required=True,
        select=True, states=STATES,
        on_change=['product', 'currency', 'uom', 'company',
            'from_location', 'to_location'],
        domain=[('type', '!=', 'service')],
        depends=DEPENDS)
    product_uom_category = fields.Function(
        fields.Many2One('product.uom.category', 'Product Uom Category',
            on_change_with=['product']),
        'get_product_uom_category')
    uom = fields.Many2One("product.uom", "Uom", required=True, states=STATES,
        domain=[
            ('category', '=', Eval('product_uom_category')),
            ],
        on_change=['product', 'currency', 'uom', 'company',
            'from_location', 'to_location'],
        depends=['state', 'product_uom_category'])
    unit_digits = fields.Function(fields.Integer('Unit Digits',
        on_change_with=['uom']), 'get_unit_digits')
    quantity = fields.Float("Quantity", required=True,
        digits=(16, Eval('unit_digits', 2)), states=STATES,
        depends=['state', 'unit_digits'])
    internal_quantity = fields.Float('Internal Quantity', readonly=True,
        required=True)
    from_location = fields.Many2One("stock.location", "From Location",
        select=True, required=True, states=STATES, depends=DEPENDS,
        domain=[('type', 'not in', ('warehouse', 'view'))])
    to_location = fields.Many2One("stock.location", "To Location", select=True,
        required=True, states=STATES, depends=DEPENDS,
        domain=[('type', 'not in', ('warehouse', 'view'))])
    shipment_in = fields.Many2One('stock.shipment.in', 'Supplier Shipment',
        domain=[('company', '=', Eval('company'))], depends=['company'],
        readonly=True, select=True, ondelete='CASCADE')
    shipment_out = fields.Many2One('stock.shipment.out', 'Customer Shipment',
        domain=[('company', '=', Eval('company'))], depends=['company'],
        readonly=True, select=True, ondelete='CASCADE')
    shipment_out_return = fields.Many2One('stock.shipment.out.return',
        'Customer Return Shipment', readonly=True, select=True,
        domain=[('company', '=', Eval('company'))], depends=['company'],
        ondelete='CASCADE')
    shipment_in_return = fields.Many2One('stock.shipment.in.return',
        'Supplier Return Shipment', readonly=True, select=True,
        domain=[('company', '=', Eval('company'))], depends=['company'],
        ondelete='CASCADE')
    shipment_internal = fields.Many2One('stock.shipment.internal',
        'Internal Shipment', readonly=True, select=True, ondelete='CASCADE',
        domain=[('company', '=', Eval('company'))], depends=['company'])
    planned_date = fields.Date("Planned Date", states={
            'readonly': (In(Eval('state'), ['cancel', 'assigned', 'done'])
                | Eval('shipment_in') | Eval('shipment_out')
                | Eval('shipment_in_return') | Eval('shipment_out_return')
                | Eval('shipment_internal'))
            }, depends=['state', 'shipment_in', 'shipment_out',
            'shipment_in_return', 'shipment_out_return', 'shipment_internal'],
        select=True)
    effective_date = fields.Date("Effective Date", readonly=True, select=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('assigned', 'Assigned'),
        ('done', 'Done'),
        ('cancel', 'Canceled'),
        ], 'State', select=True, readonly=True)
    company = fields.Many2One('company.company', 'Company', required=True,
        states={
            'readonly': Not(Equal(Eval('state'), 'draft')),
            },
        domain=[
            ('id', If(In('company', Eval('context', {})), '=', '!='),
                Get(Eval('context', {}), 'company', 0)),
            ],
        depends=['state'])
    unit_price = fields.Numeric('Unit Price', digits=(16, 4),
        states={
            'invisible': Not(Bool(Eval('unit_price_required'))),
            'required': Bool(Eval('unit_price_required')),
            'readonly': Not(Equal(Eval('state'), 'draft')),
            },
        depends=['unit_price_required', 'state'])
    cost_price = fields.Numeric('Cost Price', digits=(16, 4), readonly=True)
    currency = fields.Many2One('currency.currency', 'Currency',
        states={
            'invisible': Not(Bool(Eval('unit_price_required'))),
            'required': Bool(Eval('unit_price_required')),
            'readonly': Not(Equal(Eval('state'), 'draft')),
            },
        depends=['unit_price_required', 'state'])
    unit_price_required = fields.Function(fields.Boolean('Unit Price Required',
        on_change_with=['from_location', 'to_location']),
        'get_unit_price_required')

    def __init__(self):
        super(Move, self).__init__()
        self._sql_constraints += [
            ('check_move_qty_pos',
                'CHECK(quantity >= 0.0)', 'Move quantity must be positive'),
            ('check_move_internal_qty_pos',
                'CHECK(internal_quantity >= 0.0)',
                'Internal move quantity must be positive'),
            ('check_from_to_locations',
                'CHECK(from_location != to_location)',
                'Source and destination location must be different'),
            ('check_shipment',
                'CHECK((COALESCE(shipment_in, 0) / COALESCE(shipment_in, 1) ' \
                        '+ COALESCE(shipment_out, 0) / ' \
                            'COALESCE(shipment_out, 1) ' \
                        '+ COALESCE(shipment_internal, 0) / ' \
                            'COALESCE(shipment_internal, 1) ' \
                        '+ COALESCE(shipment_in_return, 0) / ' \
                            'COALESCE(shipment_in_return, 1) ' \
                        '+ COALESCE(shipment_out_return, 0) / ' \
                            'COALESCE(shipment_out_return, 1)) ' \
                        '<= 1)',
                'Move can be on only one Shipment'),
        ]
        self._constraints += [
            ('check_period_closed', 'period_closed'),
        ]
        self._order[0] = ('id', 'DESC')
        self._error_messages.update({
            'set_state_draft': 'You can not set state to draft!',
            'set_state_assigned': 'You can not set state to assigned!',
            'set_state_done': 'You can not set state to done!',
            'del_draft_cancel': 'You can only delete draft ' \
                'or cancelled moves!',
            'period_closed': 'You can not modify move in closed period!',
            'modify_assigned_done_cancel': ('You can not modify a move '
                'in the state: "Assigned", "Done" or "Cancel"'),
            })

    def init(self, module_name):
        cursor = Transaction().cursor
        # Migration from 1.2: packing renamed into shipment
        table = TableHandler(cursor, self, module_name)
        table.drop_constraint('check_packing')
        for suffix in ('in', 'out', 'in_return', 'out_return', 'internal'):
            old_column = 'packing_%s' % suffix
            new_column = 'shipment_%s' % suffix
            if table.column_exist(old_column):
                table.index_action(old_column, action='remove')
            table.drop_fk(old_column)
            table.column_rename(old_column, new_column)

        # Migration from 1.8: new field internal_quantity
        internal_quantity_exist = table.column_exist('internal_quantity')

        super(Move, self).init(module_name)

        # Migration from 1.8: fill new field internal_quantity
        if not internal_quantity_exist:
            offset = 0
            limit = cursor.IN_MAX
            move_ids = True
            while move_ids:
                move_ids = self.search([], offset=offset, limit=limit)
                offset += limit
                for move in self.browse(move_ids):
                    internal_quantity = self._get_internal_quantity(
                            move.quantity, move.uom, move.product)
                    self.write(move.id, {
                        'internal_quantity': internal_quantity,
                        })
            table = TableHandler(cursor, self, module_name)
            table.not_null_action('internal_quantity', action='add')

        # Migration from 1.0 check_packing_in_out has been removed
        table = TableHandler(cursor, self, module_name)
        table.drop_constraint('check_packing_in_out')

        # Add index on create_date
        table.index_action('create_date', action='add')

    def default_planned_date(self):
        return Transaction().context.get('planned_date')

    def default_state(self):
        return 'draft'

    def default_company(self):
        return Transaction().context.get('company')

    def default_currency(self):
        company_obj = Pool().get('company.company')
        company = Transaction().context.get('company')
        if company:
            company = company_obj.browse(company)
            return company.currency.id

    def default_unit_digits(self):
        return 2

    def on_change_with_unit_digits(self, vals):
        uom_obj = Pool().get('product.uom')
        if vals.get('uom'):
            uom = uom_obj.browse(vals['uom'])
            return uom.digits
        return 2

    def get_unit_digits(self, ids, name):
        res = {}
        for move in self.browse(ids):
            res[move.id] = move.uom.digits
        return res

    def on_change_product(self, vals):
        pool = Pool()
        product_obj = pool.get('product.product')
        uom_obj = pool.get('product.uom')
        currency_obj = pool.get('currency.currency')
        company_obj = pool.get('company.company')
        location_obj = pool.get('stock.location')

        res = {
            'unit_price': Decimal('0.0'),
        }
        if vals.get('product'):
            product = product_obj.browse(vals['product'])
            res['uom'] = product.default_uom.id
            res['uom.rec_name'] = product.default_uom.rec_name
            res['unit_digits'] = product.default_uom.digits
            from_location, to_location = None, None
            if vals.get('from_location'):
                from_location = location_obj.browse(vals['from_location'])
            if vals.get('to_location'):
                to_location = location_obj.browse(vals['to_location'])
            unit_price = None
            if from_location and from_location.type in ('supplier',
                    'production'):
                unit_price = product.cost_price
            elif to_location and to_location.type == 'customer':
                unit_price = product.list_price
            if unit_price:
                if vals.get('uom') and vals['uom'] != product.default_uom.id:
                    uom = uom_obj.browse(vals['uom'])
                    unit_price = uom_obj.compute_price(product.default_uom,
                            unit_price, uom)
                if vals.get('currency') and vals.get('company'):
                    currency = currency_obj.browse(vals['currency'])
                    company = company_obj.browse(vals['company'])
                    unit_price = currency_obj.compute(company.currency,
                            unit_price, currency, round=False)
                res['unit_price'] = unit_price
        return res

    def on_change_with_product_uom_category(self, values):
        pool = Pool()
        product_obj = pool.get('product.product')
        if values.get('product'):
            product = product_obj.browse(values['product'])
            return product.default_uom_category.id

    def get_product_uom_category(self, ids, name):
        categories = {}
        for move in self.browse(ids):
            categories[move.id] = move.product.default_uom_category.id
        return categories

    def on_change_uom(self, vals):
        pool = Pool()
        product_obj = pool.get('product.product')
        uom_obj = pool.get('product.uom')
        currency_obj = pool.get('currency.currency')
        company_obj = pool.get('company.company')
        location_obj = pool.get('stock.location')

        res = {
            'unit_price': Decimal('0.0'),
        }
        if vals.get('product'):
            product = product_obj.browse(vals['product'])
            to_location = None
            if vals.get('to_location'):
                to_location = location_obj.browse(vals['to_location'])
            if to_location and to_location.type == 'storage':
                unit_price = product.cost_price
                if vals.get('uom') and vals['uom'] != product.default_uom.id:
                    uom = uom_obj.browse(vals['uom'])
                    unit_price = uom_obj.compute_price(product.default_uom,
                            unit_price, uom)
                if vals.get('currency') and vals.get('company'):
                    currency = currency_obj.browse(vals['currency'])
                    company = company_obj.browse(vals['company'])
                    unit_price = currency_obj.compute(company.currency,
                            unit_price, currency, round=False)
                res['unit_price'] = unit_price
        return res

    def on_change_with_unit_price_required(self, vals):
        location_obj = Pool().get('stock.location')
        if vals.get('from_location'):
            from_location = location_obj.browse(vals['from_location'])
            if from_location.type in ('supplier', 'production'):
                return True
        if vals.get('to_location'):
            to_location = location_obj.browse(vals['to_location'])
            if to_location.type in ('customer', 'production'):
                return True
        return False

    def get_unit_price_required(self, ids, name):
        res = {}
        for move in self.browse(ids):
            res[move.id] = False
            if move.from_location.type in ('supplier', 'production'):
                res[move.id] = True
            if move.to_location.type == 'customer':
                res[move.id] = True
        return res

    def check_period_closed(self, ids):
        period_obj = Pool().get('stock.period')
        period_ids = period_obj.search([
            ('state', '=', 'closed'),
        ], order=[('date', 'DESC')], limit=1)
        if period_ids:
            period, = period_obj.browse(period_ids)
            for move in self.browse(ids):
                date = (move.effective_date if move.effective_date
                    else move.planned_date)
                if date and date < period.date:
                    return False
        return True

    def get_rec_name(self, ids, name):
        if not ids:
            return {}
        res = {}
        moves = self.browse(ids)
        for m in moves:
            res[m.id] = ("%s%s %s"
                % (m.quantity, m.uom.symbol, m.product.rec_name))
        return res

    def search_rec_name(self, name, clause):
        return [('product',) + tuple(clause[1:])]

    def _update_product_cost_price(self, product_id, quantity, uom, unit_price,
            currency, company, date):
        """
        Update the cost price on the given product

        :param product_id: the id of the product
        :param quantity: the quantity of the product, positive if incoming and
                negative if outgoing
        :param uom: the uom id or a BrowseRecord of the uom
        :param unit_price: the unit price of the product
        :param currency: the currency of the unit price
        :param company: the company id ot a BrowseRecord of the company
        :param date: the date for the currency rate calculation
        """
        pool = Pool()
        uom_obj = pool.get('product.uom')
        product_obj = pool.get('product.product')
        product_template_obj = pool.get('product.template')
        location_obj = pool.get('stock.location')
        currency_obj = pool.get('currency.currency')
        company_obj = pool.get('company.company')
        date_obj = pool.get('ir.date')

        if isinstance(uom, (int, long)):
            uom = uom_obj.browse(uom)
        if isinstance(currency, (int, long)):
            currency = currency_obj.browse(currency)
        if isinstance(company, (int, long)):
            company = company_obj.browse(company)

        context = {}
        context['locations'] = location_obj.search([
            ('type', '=', 'storage'),
            ])
        context['stock_date_end'] = date_obj.today()
        with Transaction().set_context(context):
            product = product_obj.browse(product_id)
        qty = uom_obj.compute_qty(uom, quantity, product.default_uom)

        qty = Decimal(str(qty))
        product_qty = Decimal(str(product.template.quantity))
        # convert wrt currency
        with Transaction().set_context(date=date):
            unit_price = currency_obj.compute(currency.id, unit_price,
                    company.currency.id, round=False)
        # convert wrt to the uom
        unit_price = uom_obj.compute_price(uom, unit_price,
                product.default_uom)
        if product_qty + qty != Decimal('0.0'):
            new_cost_price = (
                (product.cost_price * product_qty) + (unit_price * qty)
                ) / (product_qty + qty)
        else:
            new_cost_price = product.cost_price

        if hasattr(product_obj, 'cost_price'):
            digits = product_obj.cost_price.digits
        else:
            digits = product_template_obj.cost_price.digits
        new_cost_price = new_cost_price.quantize(
            Decimal(str(10.0 ** -digits[1])))

        with Transaction().set_user(0, set_context=True):
            product_obj.write(product.id, {
                'cost_price': new_cost_price,
                })

    def _get_internal_quantity(self, quantity, uom, product):
        uom_obj = Pool().get('product.uom')
        internal_quantity = uom_obj.compute_qty(uom, quantity,
                product.default_uom, round=True)
        return internal_quantity

    def create(self, vals):
        pool = Pool()
        location_obj = pool.get('stock.location')
        product_obj = pool.get('product.product')
        uom_obj = pool.get('product.uom')
        date_obj = pool.get('ir.date')

        today = date_obj.today()
        vals = vals.copy()
        effective_date = vals.get('effective_date') or today

        product = product_obj.browse(vals['product'])
        if vals.get('state') == 'done':
            vals['effective_date'] = effective_date
            currency_id = vals.get('currency', self.default_currency())
            company_id = vals.get('company', self.default_company())
            from_location = location_obj.browse(vals['from_location'])
            to_location = location_obj.browse(vals['to_location'])
            if (from_location.type in ('supplier', 'production')
                    and to_location.type == 'storage'
                    and product.cost_price_method == 'average'):
                self._update_product_cost_price(vals['product'],
                        vals['quantity'], vals['uom'], vals['unit_price'],
                        currency_id, company_id, effective_date)
            if (to_location.type == 'supplier'
                    and from_location.type == 'storage'
                    and product.cost_price_method == 'average'):
                self._update_product_cost_price(vals['product'],
                        -vals['quantity'], vals['uom'], vals['unit_price'],
                        currency_id, company_id, effective_date)
            if not vals.get('cost_price'):
                # Re-read product to get the updated cost_price
                product = product_obj.browse(vals['product'])
                vals['cost_price'] = product.cost_price

        elif vals.get('state') == 'assigned':
            vals['effective_date'] = effective_date

        uom = uom_obj.browse(vals['uom'])
        internal_quantity = self._get_internal_quantity(vals['quantity'],
                uom, product)
        vals['internal_quantity'] = internal_quantity
        return super(Move, self).create(vals)

    def write(self, ids, vals):
        date_obj = Pool().get('ir.date')

        if isinstance(ids, (int, long)):
            ids = [ids]
        today = date_obj.today()
        effective_date = vals.get('effective_date') or today

        moves = self.browse(ids)
        if 'state' in vals:
            for move in moves:
                if vals['state'] == 'cancel':
                    vals['effective_date'] = None
                    if (move.from_location.type in ('supplier', 'production')
                            and move.to_location.type == 'storage'
                            and move.state != 'cancel'
                            and move.product.cost_price_method == 'average'):
                        self._update_product_cost_price(move.product.id,
                                -move.quantity, move.uom, move.unit_price,
                                move.currency, move.company, today)
                    if (move.to_location.type == 'supplier'
                            and move.from_location.type == 'storage'
                            and move.state != 'cancel'
                            and move.product.cost_price_method == 'average'):
                        self._update_product_cost_price(move.product.id,
                                move.quantity, move.uom, move.unit_price,
                                move.currency, move.company, today)

                elif vals['state'] == 'draft':
                    if move.state == 'done':
                        self.raise_user_error('set_state_draft')
                elif vals['state'] == 'assigned':
                    if move.state in ('cancel', 'done'):
                        self.raise_user_error('set_state_assigned')
                    vals['effective_date'] = effective_date
                elif vals['state'] == 'done':
                    if move.state in ('cancel'):
                        self.raise_user_error('set_state_done')
                    vals['effective_date'] = effective_date

                    if (move.from_location.type in ('supplier', 'production')
                            and move.to_location.type == 'storage'
                            and move.state != 'done'
                            and move.product.cost_price_method == 'average'):
                        self._update_product_cost_price(move.product.id,
                                move.quantity, move.uom, move.unit_price,
                                move.currency, move.company, effective_date)
                    if (move.to_location.type == 'supplier'
                            and move.from_location.type == 'storage'
                            and move.state != 'done'
                            and move.product.cost_price_method == 'average'):
                        self._update_product_cost_price(move.product.id,
                                -move.quantity, move.uom, move.unit_price,
                                move.currency, move.company, effective_date)

        if reduce(lambda x, y: x or y in vals, ('product', 'uom', 'quantity',
                'from_location', 'to_location', 'company', 'unit_price',
                'currency'), False):
            for move in moves:
                if move.state in ('assigned', 'done', 'cancel'):
                    self.raise_user_error('modify_assigned_done_cancel')
        if reduce(lambda x, y: x or y in vals,
                ('planned_date', 'effective_date'), False):
            for move in moves:
                if move.state in ('done', 'cancel'):
                    self.raise_user_error('modify_assigned_done_cancel')

        res = super(Move, self).write(ids, vals)

        if vals.get('state', '') == 'done':
            #Re-read the move because cost_price has been updated
            for move in self.browse(ids):
                if not move.cost_price:
                    self.write(move.id, {
                        'cost_price': move.product.cost_price,
                        })

        for move in self.browse(ids):
            internal_quantity = self._get_internal_quantity(move.quantity,
                    move.uom, move.product)
            if internal_quantity != move.internal_quantity:
                # Use super to avoid infinite loop
                super(Move, self).write(move.id, {
                    'internal_quantity': internal_quantity,
                    })
        return res

    def delete(self, ids):
        for move in self.browse(ids):
            if move.state not in  ('draft', 'cancel'):
                self.raise_user_error('del_draft_cancel')
        return super(Move, self).delete(ids)

    def pick_product(self, move, location_quantities):
        """
        Pick the product across the location. Naive (fast) implementation.

        :param move: a BrowseRecord of stock.move
        :param location_quantities: a list of tuple (location, available_qty)
            where location is a BrowseRecord of stock.location.
        :return: a list of tuple (location, quantity) for quantities
            that can be picked
        """
        to_pick = []
        needed_qty = move.quantity
        for location, available_qty in location_quantities.iteritems():
            # Ignore available_qty when too small
            if available_qty < move.uom.rounding:
                continue
            if needed_qty <= available_qty:
                to_pick.append((location, needed_qty))
                return to_pick
            else:
                to_pick.append((location, available_qty))
                needed_qty -= available_qty
        # Force assignation for consumables:
        if move.product.consumable:
            to_pick.append((move.from_location, needed_qty))
            return to_pick
        return to_pick

    def assign_try(self, moves):
        '''
        Try to assign moves.
        It will split the moves to assign as much possible.

        :param moves: a BrowseRecordList of stock.move to assign
        :return: True if succeed or False if not
        '''
        pool = Pool()
        product_obj = pool.get('product.product')
        uom_obj = pool.get('product.uom')
        date_obj = pool.get('ir.date')
        location_obj = pool.get('stock.location')

        Transaction().cursor.lock(self._table)

        location_ids = location_obj.search([
            ('parent', 'child_of', [x.from_location.id for x in moves]),
            ])
        with Transaction().set_context(
                stock_date_end=date_obj.today(),
                stock_assign=True):
            pbl = product_obj.products_by_location(location_ids=location_ids,
                    product_ids=[m.product.id for m in moves])

        success = True
        for move in moves:
            if move.state != 'draft':
                continue
            to_location = move.to_location
            location_qties = {}
            child_ids = location_obj.search([
                ('parent', 'child_of', [move.from_location.id]),
                ])
            for location in location_obj.browse(child_ids):
                if (location.id, move.product.id) in pbl:
                    location_qties[location] = uom_obj.compute_qty(
                            move.product.default_uom,
                            pbl[(location.id, move.product.id)], move.uom,
                            round=False)

            to_pick = self.pick_product(move, location_qties)

            picked_qties = 0.0
            for _, qty in to_pick:
                picked_qties += qty

            if picked_qties < move.quantity:
                success = False
                first = False
                self.write(move.id, {
                    'quantity': move.quantity - picked_qties,
                    })
            else:
                first = True
            for from_location, qty in to_pick:
                values = {
                    'from_location': from_location.id,
                    'quantity': qty,
                    'state': 'assigned',
                    }
                if first:
                    self.write(move.id, values)
                    first = False
                else:
                    self.copy(move.id, default=values)

                qty_default_uom = uom_obj.compute_qty(move.uom, qty,
                        move.product.default_uom, round=False)

                pbl[(from_location.id, move.product.id)] = (
                    pbl.get((from_location.id, move.product.id), 0.0)
                    - qty_default_uom)
                pbl[(to_location.id, move.product.id)] = (
                    pbl.get((to_location.id, move.product.id), 0.0)
                    + qty_default_uom)
        return success

Move()
