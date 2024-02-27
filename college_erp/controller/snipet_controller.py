from odoo import http
from odoo.http import request


class Sales(http.Controller):
    @http.route(['/most_product_sold'], type="json", auth="public")
    def sold_product(self):
        products = request.env['product.template'].search([
            ('sale_ok', '=', True),
        ]).sorted(key=lambda r: -r.sales_count)
        records = products[:4]

        for rec in records:
            print(rec.name, rec.sales_count)

        # total_sold = sum(sale_obj.mapped('order_line.product_uom_qty'))
        return products
