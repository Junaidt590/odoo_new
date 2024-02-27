/* @odoo-module */

import { registry } from "@web/core/registry";

import { Component, useState, onMounted } from  "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

class MyReportAction extends Component {
    setup(){
        this.state = useState({
            taxDetails: [],
            fromDateValue: undefined,
            toDateValue: undefined,

        });

        console.log('hhhhhh');
        this.orm = useService('orm');
        // this.action = useService("action");
        onMounted(() => {
            this.getDateAndSet();
            this.getTaxDetails();
//            this.action_print_pdf();
        });
        }
         getDateAndSet(){
            console.log('date')
            var today = new Date();
            var firstDayOfMonth = new Date(today.getFullYear(), today.getMonth(), 1);
            var lastDayOfMonth = new Date(today.getFullYear(), today.getMonth() + 1, 0);
//            console.log(firstDayOfMonth)
            // Format the dates as 'YYYY-MM-DD'
            var formattedFirstDay = firstDayOfMonth.toISOString().split('T')[0];
            var formattedLastDay = lastDayOfMonth.toISOString().split('T')[0];
            console.log(formattedFirstDay)
            // Set the values to the input fields
            $('#fromDate').val(formattedFirstDay);
            $('#toDate').val(formattedLastDay);
            this.state.fromDateValue = formattedFirstDay
            this.state.toDateValue = formattedLastDay

        }
        async getTaxDetails(){
            console.log('tax')
            let data = await this.orm.call('account.move.line', 'get_action_print_report', {}, {
                context: {
                    from_date: this.state.fromDateValue,
                    to_date: this.state.toDateValue,
                },
            });
            console.log(this.state.fromDateValue)
//            console.log(this.state.toDateValue)
//            this.writeState({ taxDetails: data });
            this.state.taxDetails = data
            console.log(this.state.taxDetails);
        }
        action_print_pdf(){
            console.log('Button clicked!');
            var content = $("#report").html();
            var printWindow = window.open('', '_blank');
            printWindow.document.open();
            printWindow.document.write('<html><head><title>Print</title></head><body>' + content + '</body></html>');
            printWindow.document.close();
            printWindow.print();
        }
        async handleInput() {
            await this.getTaxDetails();
}
}
MyReportAction.template = "tax_wise_sales_report.TaxReport";


// remember the tag name we put in the first step
registry.category("actions").add("tax_wise_sales_report.report_tax", MyReportAction);