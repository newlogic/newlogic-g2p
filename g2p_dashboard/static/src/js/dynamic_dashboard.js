odoo.define("g2p_dashboard.Dashboard", function (require) {
    "use strict";

    var odoo_dynamic_dashboard = require("odoo_dynamic_dashboard.Dashboard");
    //var AbstractAction = require('web.AbstractAction');
    //var ajax = require('web.ajax');
    //var core = require('web.core');
    var rpc = require("web.rpc");
    //var session = require('web.session');
    //var web_client = require('web.web_client');
    //var _t = core._t;
    //var QWeb = core.qweb;
    var ctx = {};

    odoo_dynamic_dashboard.include({
        init: function (parent, context) {
            ctx = context;
            //console.log('Context: '+ctx);
            if (ctx["context"]["active_id"]) {
                this.active_id = ctx["context"]["active_id"];
            } else {
                this.active_id = false;
            }
            this._super(parent, context);
        },

        fetch_data: function () {
            var self = this;
            //console.log('Context2: ' +ctx.id);
            var def1 = this._rpc({
                model: "dashboard.block",
                method: "get_dashboard_vals",
                args: [[], this.action_id, this.active_id],
            }).then(function (result) {
                self.block_ids = result;
            });
            return $.when(def1);
        },
    });
});
