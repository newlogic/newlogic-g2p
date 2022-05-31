odoo.define("g2p_program_dashboard.ProgramDashBoard", function (require) {
    "use strict";
    var AbstractAction = require("web.AbstractAction");
    var ajax = require("web.ajax");
    var core = require("web.core");
    var rpc = require("web.rpc");
    var web_client = require("web.web_client");
    var _t = core._t;
    var QWeb = core.qweb;
    var self = this;
    var currency;
    var ActionMenu = AbstractAction.extend({
        contentTemplate: "ProgramDashBoard",
        events: {
            "click .program_dashboard": "onclick_dashboard",
            "click #prog_bar": "onclick_prog_bar",
            "click #total_number_active_programs": "show_active_programs",
            "click #total_number_ended_programs": "show_ended_programs",
            "click #total_number_new_cycles": "show_new_cycles",
            "click #total_number_approved_cycles": "show_approved_cycles",
            "click #total_number_new_vouchers": "show_new_vouchers",
            "click #total_number_approved_vouchers": "show_approved_vouchers",
        },
        //Top Panel
        //Programs
        show_active_programs: function (ev) {
            var state = ["active"];
            var self = this;
            rpc.query({
                model: "g2p.program",
                method: "get_program_ids",
                args: [state],
            }).then(function (result) {
                self.do_action({
                    res_model: "g2p.program",
                    name: _t("Active Programs"),
                    views: [
                        [false, "list"],
                        [false, "form"],
                    ],
                    type: "ir.actions.act_window",
                    domain: [["id", "in", result]],
                });
            });
        },
        show_ended_programs: function (ev) {
            var state = ["ended"];
            var self = this;
            rpc.query({
                model: "g2p.program",
                method: "get_program_ids",
                args: [state],
            }).then(function (result) {
                self.do_action({
                    res_model: "g2p.program",
                    name: _t("Ended Programs"),
                    views: [
                        [false, "list"],
                        [false, "form"],
                    ],
                    type: "ir.actions.act_window",
                    domain: [["id", "in", result]],
                });
            });
        },

        //Cycles
        show_new_cycles: function (ev) {
            var state = ["draft", "to_approve", "active"];
            var self = this;
            rpc.query({
                model: "g2p.cycle",
                method: "get_cycle_ids",
                args: [state],
            }).then(function (result) {
                self.do_action({
                    res_model: "g2p.cycle",
                    name: _t("Draft, Active, and To be Approved Cycles"),
                    views: [
                        [false, "list"],
                        [false, "form"],
                    ],
                    type: "ir.actions.act_window",
                    domain: [["id", "in", result]],
                });
            });
        },
        show_approved_cycles: function (ev) {
            var state = ["approved"];
            var self = this;
            rpc.query({
                model: "g2p.cycle",
                method: "get_cycle_ids",
                args: [state],
            }).then(function (result) {
                self.do_action({
                    res_model: "g2p.cycle",
                    name: _t("Approved Cycles"),
                    views: [
                        [false, "list"],
                        [false, "form"],
                    ],
                    type: "ir.actions.act_window",
                    domain: [["id", "in", result]],
                });
            });
        },
        //Vouchers
        show_new_vouchers: function (ev) {
            var state = ["draft", "pending_validation"];
            var self = this;
            rpc.query({
                model: "g2p.voucher",
                method: "get_voucher_ids",
                args: [state],
            }).then(function (result) {
                self.do_action({
                    res_model: "g2p.voucher",
                    name: _t("Draft and Pending Validation Vouchers"),
                    views: [
                        [false, "list"],
                        [false, "form"],
                    ],
                    type: "ir.actions.act_window",
                    domain: [["id", "in", result]],
                });
            });
        },
        show_approved_vouchers: function (ev) {
            var state = ["approved"];
            var self = this;
            rpc.query({
                model: "g2p.voucher",
                method: "get_voucher_ids",
                args: [state],
            }).then(function (result) {
                self.do_action({
                    res_model: "g2p.voucher",
                    name: _t("Approved Vouchers"),
                    views: [
                        [false, "list"],
                        [false, "form"],
                    ],
                    type: "ir.actions.act_window",
                    domain: [["id", "in", result]],
                });
            });
        },

        renderElement: function (ev) {
            var self = this;
            $.when(this._super()).then(function (ev) {
                //Program Counts
                //Total Active Programs
                var state = ["active"];
                rpc.query({
                    model: "g2p.program",
                    method: "count_programs",
                    args: [state],
                }).then(function (result) {
                    if (result["value"] == undefined) {
                        result["value"] = 0;
                    }
                    var total_count = result["value"];
                    $("#total_number_active_programs").empty();
                    $("#total_number_active_programs").append(
                        "<span>" + total_count + '</span> <div class="title">Active</div>'
                    );
                });
                //Total Ended Programs
                var state = ["ended"];
                rpc.query({
                    model: "g2p.program",
                    method: "count_programs",
                    args: [state],
                }).then(function (result) {
                    if (result["value"] == undefined) {
                        result["value"] = 0;
                    }
                    var total_count = result["value"];
                    $("#total_number_ended_programs").empty();
                    $("#total_number_ended_programs").append(
                        "<span>" + total_count + '</span> <div class="title">Ended</div>'
                    );
                });

                //Cycle Counts
                //Total Draft, Active, and To be Approved Cycles
                var state = ["draft", "to_approve", "active"];
                rpc.query({
                    model: "g2p.cycle",
                    method: "count_cycles",
                    args: [state],
                }).then(function (result) {
                    if (result["value"] == undefined) {
                        result["value"] = 0;
                    }
                    var total_count = result["value"];
                    $("#total_number_new_cycles").empty();
                    $("#total_number_new_cycles").append(
                        "<span>" + total_count + '</span> <div class="title">New</div>'
                    );
                });
                //Total Approved Cycles
                var state = ["approved"];
                rpc.query({
                    model: "g2p.cycle",
                    method: "count_cycles",
                    args: [state],
                }).then(function (result) {
                    if (result["value"] == undefined) {
                        result["value"] = 0;
                    }
                    var total_count = result["value"];
                    $("#total_number_approved_cycles").empty();
                    $("#total_number_approved_cycles").append(
                        "<span>" + total_count + '</span> <div class="title">Approved</div>'
                    );
                });

                //Voucher Counts
                //Total Draft and Pending Validation Programs
                var state = ["draft", "pending_validation"];
                rpc.query({
                    model: "g2p.voucher",
                    method: "count_vouchers",
                    args: [state],
                }).then(function (result) {
                    if (result["value"] == undefined) {
                        result["value"] = 0;
                    }
                    var total_count = result["value"];
                    $("#total_number_new_vouchers").empty();
                    $("#total_number_new_vouchers").append(
                        "<span>" + total_count + '</span> <div class="title">New</div>'
                    );
                });
                //Total Approved Vouchers
                var state = ["approved"];
                rpc.query({
                    model: "g2p.voucher",
                    method: "count_vouchers",
                    args: [state],
                }).then(function (result) {
                    if (result["value"] == undefined) {
                        result["value"] = 0;
                    }
                    var total_count = result["value"];
                    $("#total_number_approved_vouchers").empty();
                    $("#total_number_approved_vouchers").append(
                        "<span>" + total_count + '</span> <div class="title">Approved</div>'
                    );
                });

                //Programs Graph
                rpc.query({
                    model: "g2p.program",
                    method: "get_programs_month",
                    args: [],
                }).then(function (result) {
                    var ctx = document.getElementById("canvas").getContext("2d");
                    // Define the data
                    var programs = result.programs; // Add data values to array
                    var ended = result.ended;

                    var labels = result.date; // Add labels to array
                    // End Defining data

                    // End Defining data
                    if (window.myCharts != undefined) window.myCharts.destroy();
                    window.myCharts = new Chart(ctx, {
                        //var myChart = new Chart(ctx, {
                        type: "bar",
                        data: {
                            labels: labels,
                            datasets: [
                                {
                                    label: "Programs", // Name the series
                                    data: programs, // Specify the data values array
                                    backgroundColor: "#66aecf",
                                    borderColor: "#66aecf",

                                    borderWidth: 1, // Specify bar border width
                                    type: "bar", // Set this data to a line chart
                                    fill: false,
                                },
                                {
                                    label: "Ended Programs", // Name the series
                                    data: ended, // Specify the data values array
                                    backgroundColor: "#6993d6",
                                    borderColor: "#6993d6",

                                    borderWidth: 1, // Specify bar border width
                                    type: "bar", // Set this data to a line chart
                                    fill: false,
                                },
                            ],
                        },
                        options: {
                            responsive: true, // Instruct chart js to respond nicely.
                            maintainAspectRatio: false, // Add to prevent default behaviour of full-width/height
                        },
                    });
                });

                //Vouchers and Funds Charts
                rpc.query({
                    model: "g2p.voucher",
                    method: "get_vouchers_month",
                    args: [],
                }).then(function (result) {
                    $("#total_voucher").hide();
                    $("#total_voucher_paid").hide();
                    $("#tot_voucher").hide();

                    $("#total_voucher_paid_current_month").empty();
                    $("#total_voucher_current_month").empty();
                    $("#tot_voucher_current_month").empty();

                    $("#total_voucher_paid_current_year").hide();
                    $("#total_voucher_current_year").hide();
                    $("#tot_voucher_current_year").hide();

                    $("#total_voucher_paid_current_month").show();
                    $("#total_voucher_current_month").show();
                    $("#tot_voucher_current_month").show();

                    var tot_voucher_current_month = result[0][0];
                    var tot_paid_voucher_current_month = result[1][0];
                    var total_voucher_current_month = tot_voucher_current_month.toFixed(2);
                    var total_voucher_paid_current_month = tot_paid_voucher_current_month.toFixed(2);
                    var voucher_percentage_current_month = (
                        (total_voucher_current_month / total_voucher_paid_current_month) *
                        100
                    ).toFixed(2);

                    $("#tot_voucher_current_month").attr("value", total_voucher_paid_current_month);
                    $("#tot_voucher_current_month").attr("max", total_voucher_current_month);

                    currency = result[2];
                    total_voucher_paid_current_month = self.format_currency(
                        currency,
                        total_voucher_paid_current_month
                    );
                    total_voucher_current_month = self.format_currency(currency, total_voucher_current_month);

                    $("#total_voucher_paid_current_month").append(
                        '<div class="logo">' +
                            "<span>" +
                            total_voucher_paid_current_month +
                            "</span><span> Total Paid<span></div>"
                    );
                    $("#total_voucher_current_month").append(
                        '<div" class="logo">' +
                            "<span>" +
                            total_voucher_current_month +
                            "</span><span> Total Vouchers<span></div>"
                    );
                });
            });
        },

        format_currency: function (currency, amount) {
            if (typeof amount != "number") {
                amount = parseFloat(amount);
            }
            var formatted_value = parseInt(amount).toLocaleString(currency.language, {
                minimumFractionDigits: 2,
            });
            if (currency.position === "after") {
                return (formatted_value += " " + currency.symbol);
            } else {
                return currency.symbol + " " + formatted_value;
            }
        },

        willStart: function () {
            var self = this;
            self.drpdn_show = false;
            return Promise.all([ajax.loadLibs(this), this._super()]);
        },
    });
    core.action_registry.add("program_dashboard", ActionMenu);
});
