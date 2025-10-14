# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ProductPricelistItem(models.Model):
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
        via super(). Handles empty and multi-recordsets for robustness in onchange contexts.
        Returns a float for singleton, dict {item_id: price} for multi.
        """
        if not self:
            # Fallback to standard for empty recordset (e.g., in onchange before rule loads).
            return super()._compute_base_price(product, quantity, uom, date, currency)

        prices = {}
        for item in self:
            # Per-item singleton logic.
            item.ensure_one()
            currency.ensure_one()  # Assuming currency is singleton param; safe post-loop.

            rule_base = item.base or "list_price"
            if rule_base == "replenishment_cost":
                src_currency = product.currency_id
                price = product.replenishment_cost
            elif rule_base == "pricelist" and item.base_pricelist_id:
                price = item.base_pricelist_id._get_product_price(
                    product,
                    quantity,
                    currency=item.base_pricelist_id.currency_id,
                    uom=uom,
                    date=date,
                )
                src_currency = item.base_pricelist_id.currency_id
            elif rule_base == "standard_price":
                src_currency = product.cost_currency_id
                price = product._price_compute(rule_base, uom=uom, date=date)[
                    product.id
                ]
            else:  # list_price
                src_currency = product.currency_id
                price = product._price_compute(rule_base, uom=uom, date=date)[
                    product.id
                ]

            if src_currency != currency:
                price = src_currency._convert(
                    price, currency, item.env.company, date, round=False
                )

            prices[item.id] = price

        # Return dict for multi, float for singleton (Odoo-compatible).
        return prices[self.id] if len(self) == 1 else prices
