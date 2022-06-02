odoo.define("g2p_pos.VoucherPopup", function (require) {
    "use strict";
    var rpc = require("web.rpc");
    var productid = 0;
    var voucherid = 0;
    rpc.query({
        model: "pos.category",
        method: "get_voucher_categ",
    }).then(function (data) {
        voucherid = data;
    });

    const AbstractAwaitablePopup = require("point_of_sale.AbstractAwaitablePopup");
    const Registries = require("point_of_sale.Registries");
    const PosComponent = require("point_of_sale.PosComponent");
    const ControlButtonsMixin = require("point_of_sale.ControlButtonsMixin");
    const NumberBuffer = require("point_of_sale.NumberBuffer");
    const {useListener} = require("web.custom_hooks");
    const {onChangeOrder, useBarcodeReader} = require("point_of_sale.custom_hooks");
    const {useState} = owl.hooks;
    class VoucherPopup extends AbstractAwaitablePopup {
        constructor() {
            super(...arguments);
        }

        async get_voucher(event) {
            var qr_code = $("#qr_code").val();
            console.log("Search was clicked search: " + qr_code);
            var productid = this.env.pos.db.get_product_by_category(voucherid);
            var order = this.env.pos.get_order();
            if (!order) {
                order = this.env.pos.add_new_order();
            }
            rpc.query({
                model: "g2p.voucher",
                method: "get_voucher_code",
                args: [
                    {
                        code: qr_code,
                    },
                ],
            }).then(function (data) {
                if (data["status"] == "QR Doesn't Exist") {
                    console.log("Returned: " + data["status"]);
                    alert(data["status"]);
                } else {
                    console.log("Voucher Amount: " + data["amount"]);
                    console.log("Trying to Add Product with Voucher:" + data["code"]);
                    console.log(productid[0]);
                    const product = productid[0];
                    let total_price = data["amount"] * -1;
                    let description = data["code"];

                    console.log(description);
                    // Add the product after having the extra information.
                    order.add_product(product, {
                        price: total_price,
                        description: description,
                    });
                    alert("Voucher Added!");
                }
            });
        }
    }
    //Create voucher popup
    VoucherPopup.template = "VoucherPopup";
    VoucherPopup.defaultProps = {
        confirmText: "Ok",
        cancelText: "Cancel",
        title: "Select Vouchers",
        body: "",
    };
    Registries.Component.add(VoucherPopup);
    return VoucherPopup;
});
