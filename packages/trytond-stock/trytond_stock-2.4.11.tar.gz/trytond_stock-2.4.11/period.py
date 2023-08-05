#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
from itertools import chain
from trytond.model import ModelView, ModelSQL, fields
from trytond.pyson import Equal, Eval, If, In, Get
from trytond.transaction import Transaction
from trytond.pool import Pool


class Period(ModelSQL, ModelView):
    'Stock Period'
    _name = 'stock.period'
    _description = __doc__
    _rec_name = 'date'
    date = fields.Date('Date', required=True, states={
        'readonly': Equal(Eval('state'), 'closed'),
        }, depends=['state'])
    company = fields.Many2One('company.company', 'Company', required=True,
        domain=[
            ('id', If(In('company', Eval('context', {})), '=', '!='),
                    Get(Eval('context', {}), 'company', 0)),
        ])
    caches = fields.One2Many('stock.period.cache', 'period', 'Caches')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('closed', 'Closed'),
        ], 'State', select=True, readonly=True)

    def __init__(self):
        super(Period, self).__init__()
        self._error_messages.update({
            'close_period_future_today': ('You can not close a period '
                'in the future or today!'),
            'close_period_assigned_move': ('You can not close a period when '
                'there is still assigned moves!'),
        })
        self._buttons.update({
                'draft': {
                    'invisible': Eval('state') == 'draft',
                    },
                'close': {
                    'invisible': Eval('state') == 'closed',
                    },
                })

    @ModelView.button
    def draft(self, ids):
        cache_obj = Pool().get('stock.period.cache')
        cache_ids = []
        for i in xrange(0, len(ids), Transaction().cursor.IN_MAX):
            cache_ids.append(cache_obj.search([
                ('period', 'in', ids[i:i + Transaction().cursor.IN_MAX]),
            ], order=[]))
        cache_obj.delete(list(chain(*cache_ids)))
        self.write(ids, {
            'state': 'draft',
        })

    @ModelView.button
    def close(self, ids):
        pool = Pool()
        product_obj = pool.get('product.product')
        location_obj = pool.get('stock.location')
        cache_obj = pool.get('stock.period.cache')
        move_obj = pool.get('stock.move')
        date_obj = pool.get('ir.date')

        location_ids = location_obj.search([
            ('type', 'not in', ['warehouse', 'view']),
        ], order=[])
        today = date_obj.today()
        periods = self.browse(ids)

        recent_date = max(period.date for period in periods)
        if recent_date >= today:
            self.raise_user_error('close_period_future_today')
        if move_obj.search([
                ('state', '=', 'assigned'),
                ['OR', [
                    ('effective_date', '=', None),
                    ('planned_date', '<=', recent_date),
                ],
                    ('effective_date', '<=', recent_date),
                ]]):
            self.raise_user_error('close_period_assigned_move')

        for period in periods:
            with Transaction().set_context(
                stock_date_end=period.date,
                stock_date_start=None,
                stock_assign=False,
                forecast=False,
                stock_destinations=None,
            ):
                pbl = product_obj.products_by_location(location_ids)
            for (location_id, product_id), quantity in pbl.iteritems():
                cache_obj.create({
                    'period': period.id,
                    'location': location_id,
                    'product': product_id,
                    'internal_quantity': quantity,
                })
        self.write(ids, {
            'state': 'closed',
        })

Period()


class Cache(ModelSQL, ModelView):
    '''
    Stock Period Cache

    It is used to store cached computation of stock quantities.
    '''
    _name = 'stock.period.cache'
    _description = __doc__.splitlines()[0]

    period = fields.Many2One('stock.period', 'Period', required=True,
        readonly=True, select=True, ondelete='CASCADE')
    location = fields.Many2One('stock.location', 'Location', required=True,
        readonly=True, select=True, ondelete='CASCADE')
    product = fields.Many2One('product.product', 'Product', required=True,
        readonly=True, select=True, ondelete='CASCADE')
    internal_quantity = fields.Float('Internal Quantity', readonly=True)

Cache()
