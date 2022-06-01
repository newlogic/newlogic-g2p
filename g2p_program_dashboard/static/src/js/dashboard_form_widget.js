odoo.define("g2p_program_dashboard.form_dashboard", function (require) {
    "use strict";

    /**
     * This widget adds a dashboard in the section of the form it was loaded
     *
     *        This currently support only the g2p models.
     */

    var widgetRegistry = require("web.widget_registry");
    var Widget = require("web.Widget");
    var rpc = require("web.rpc");

    var G2PProgramDashboardWidget = Widget.extend({
        template: "G2PProgramDashboardWidget",
        xmlDependencies: ["/g2p_program_dashboard/static/src/xml/form_dashboard_template.xml"],

        /**
         * @param {Object} options
         */
        init: function (parent, data, options) {
            this._super.apply(this, arguments);
        },

        renderElement: function (ev) {
            var self = this;
            $.when(this._super()).then(function (ev) {
                //Program Counts
                //Total Active Programs
                var state = ["draft", "paused", "exited", "not_eligible"];
                rpc.query({
                    model: "g2p.program",
                    method: "count_beneficiaries",
                    args: [state],
                }).then(function (result) {
                    if (result["value"] == undefined) {
                        result["value"] = 0;
                    }
                    var total_count = result["value"];
                    $("#total_beneficiaries").empty();
                    $("#total_beneficiaries").append(
                        "<span>" + total_count + '</span> <div class="title">Beneficiaries</div>'
                    );
                });
                //Total Ended Programs
                var state = ["enrolled"];
                rpc.query({
                    model: "g2p.program",
                    method: "count_beneficiaries",
                    args: [state],
                }).then(function (result) {
                    if (result["value"] == undefined) {
                        result["value"] = 0;
                    }
                    var total_count = result["value"];
                    $("#total_enrolled_beneficiaries").empty();
                    $("#total_enrolled_beneficiaries").append(
                        "<span>" + total_count + '</span> <div class="title">Enrolled</div>'
                    );
                });
            });
        },
    });

    widgetRegistry.add("program_form_dashboard", G2PProgramDashboardWidget);

    return G2PProgramDashboardWidget;
});
