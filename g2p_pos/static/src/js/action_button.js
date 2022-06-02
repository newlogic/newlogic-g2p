odoo.define("g2p_pos.VoucherButton", function (require) {
    "use strict";

    const {Gui} = require("point_of_sale.Gui");
    const PosComponent = require("point_of_sale.PosComponent");
    const AbstractAwaitablePopup = require("point_of_sale.AbstractAwaitablePopup");
    const Registries = require("point_of_sale.Registries");
    const ProductItem = require("point_of_sale.ProductItem");
    const ProductScreen = require("point_of_sale.ProductScreen");
    class OrderLineVoucher extends PosComponent {
        display_popup_voucher() {
            var core = require("web.core");
            var _t = core._t;
            Gui.showPopup("VoucherPopup", {
                title: _t("Select Voucher"),
                confirmText: _t("Close"),
                searchText: _t("Search"),
            });
        }
    }

    ProductScreen.addControlButton({
        component: OrderLineVoucher,
        condition: function () {
            return this.env.pos;
        },
    });
    Registries.Component.add(OrderLineVoucher);
    return OrderLineVoucher;
});
