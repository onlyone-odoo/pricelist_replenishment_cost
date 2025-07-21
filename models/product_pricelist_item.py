from odoo import api, fields, models

class PricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    base = fields.Selection(
        selection_add=[
            ("replenishment_cost", "Replenishment Cost"),
        ],
        ondelete={"replenishment_cost": "set default"},
        help="Base price for computation.\n"
        "Sales Price: The base price will be the Sales Price.\n"
        "Cost Price: The base price will be the cost price.\n"
        "Other Pricelist: Computation of the base price based on another Pricelist.\n"
        "Replenishment Cost: The base price will be the replenishment cost.",
    )

    def _compute_base_price(self, product, quantity, uom, date, currency):
        """Compute the base price for a pricelist item, including support for replenishment_cost.
        This method overrides the original completely to handle the new 'replenishment_cost' case
        alongside existing cases, as the conditional logic does not lend itself to partial extension
        via super().
        """
        if not self:
            # Fallback to the product's list price when no pricelist item is available
            src_currency = product.currency_id
            price = product._price_compute('list_price', uom=uom, date=date)[product.id]
            if src_currency != currency:
                price = src_currency._convert(
                    price, currency, self.env.company, date, round=False
                )
            return price

        self.ensure_one()
        currency.ensure_one()

        rule_base = self.base or "list_price"
        if rule_base == "replenishment_cost":
            product = product.with_context(to_date=date)  # Añadido para manejar el contexto de fecha correctamente
            src_currency = product.currency_id
            price = product.replenishment_cost
        elif rule_base == "pricelist" and self.base_pricelist_id:
            price = self.base_pricelist_id._get_product_price(
                product,
                quantity,
                currency=self.base_pricelist_id.currency_id,
                uom=uom,
                date=date,
            )
            src_currency = self.base_pricelist_id.currency_id
        elif rule_base == "standard_price":
            src_currency = product.cost_currency_id
            price = product._price_compute(rule_base, uom=uom, date=date)[product.id]
        else:  # list_price
            src_currency = product.currency_id
            price = product._price_compute(rule_base, uom=uom, date=date)[product.id]

        if src_currency != currency:
            price = src_currency._convert(
                price, currency, self.env.company, date, round=False
            )

        return price
