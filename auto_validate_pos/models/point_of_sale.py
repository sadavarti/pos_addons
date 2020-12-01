from odoo import models, api

import logging
_logger = logging.getLogger(__name__)


class POSOrderValidate(models.Model):
    _inherit = 'pos.order'

    @api.model
    def create_from_ui(self, orders):
        order_ids = super(POSOrderValidate, self).create_from_ui(orders)
        for order_id in self.browse(order_ids):
            order_id.write({'state': 'done'})
            try:
                order_id.picking_id.do_new_transfer()
            except Exception as e:
                _logger.warning(e.__str__())
            # stock_move = self.env['stock.move'].search([('picking_id', '=', stock_picking_id.id)])
            # stock_move.write({'state', '=', 'done'})
        # for order in orders:
        #     pos_session_id = self.env['pos.session'].browse(order['pos_session_id'])
        #     picking_ids = pos_session_id.order_ids.mapped('picking_id').filtered(lambda x: x.state != 'done')
        #     for picking_id in picking_ids:
        #         try:
        #             picking_id.do_new_transfer()
        #         except Exception as e:
        #             _logger.warn(e.__str__())
        #             continue
        return order_ids
