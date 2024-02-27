/** @odoo-module **/

import { registry } from "@web/core/registry";

import { Component, useState, onMounted } from  "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

class MyCrmAction extends Component {
     async setup(){
        this.state = useState({
            selectVal:'all',
            thisMonthTableData:[]
        });
        console.log(Chart,"chart.................")
        this.orm = useService('orm');
        this.action = useService("action");
        this.getDataAndSetDashboard();

        onMounted(() => {
            // this.fadeInDiv()
            this.renderLeadGraph();
            this.renderActivityPieChart();
            this.get_table_data();

        });

    }

    async getDataAndSetDashboard(){
        let lead = await this.orm.call('crm.lead', 'get_dashboard_details',[this.state.selectVal]);
        this.lead_details = lead;
        $('#my-lead').text(lead.myleads)
        $('#my-opportunity').text(lead.myopportunity)
        $('.currency_id').text(lead.currency)
        $('#expected-revenue').text(lead.expected_revenue)
        $('#revenue').text(lead.revenue)
        $('#win-ratio').text(lead.win_ratio.toFixed(2))
    }
    changeFilter(){
        this.getDataAndSetDashboard()
    }

    getMyLeadsAndOpp(thisValue,value){
        let action = {
            type: 'ir.actions.act_window',
            target: 'current',
            res_model: 'crm.lead',
            views: [[false, 'tree'],[false, 'form']],
        }
        if (value === 'lead'){
            action.domain = [['id','=', thisValue.lead_details.lead_ids]];
            action.name = thisValue.env._t('My Leads');
        }
        else if (value === 'opportunity'){
            action.domain = [['id','=', thisValue.lead_details.opportunity_ids]];
            action.name = thisValue.env._t('My Opportunity');
        }
        thisValue.action.doAction(action);
    }

    async renderActivityPieChart(){
       let graph_data = await this.orm.call('crm.lead', 'get_pie_chart_data');
        let canvas = $('#myPieChart');
        new Chart(canvas, {
              type: "doughnut",
              data: graph_data,
              options: {
                title: {
                  display: true,
                  text: "Activity Pie Chart"
                }
              }
            });


    }
    async renderLeadGraph(){
        let graph_data = await this.orm.call('crm.lead', 'get_lead_lost_graph_data');
        console.log(graph_data,"**********")
        let canvas = $('#myChart');
        let chart = new Chart(canvas, {
            type: "bar",
            data: graph_data,
            options: {
//                scales: {
//                    yAxis: {
//                      title: {
//                        display: true,
//                        text: "Lost Lead Counts",
//                        color: "black",
//                        padding: {
//                          top: 10,
//                          bottom: 10,
//                        },
//                        font: {
//                          size: 20,
//                        },
//                      },
//                    },
//                  },

            }

        });

    }
    async get_table_data(){
        let table_data = await this.orm.call('crm.lead', 'get_lead_table_data');
        console.log(table_data,"table_data000000000000000000")
        this.state.thisMonthTableData = table_data;
    }
    // fadeInDiv() {
    //      let div = $('.fade-in');
    //     div.css('opacity', 0);
    //
    //     let opacity = 0;
    //     const interval = setInterval(() => {
    //         console.log("Animation")
    //         opacity += 0.1;
    //
    //         div.css('opacity', opacity);
    //
    //         if (opacity >= 1) {
    //             clearInterval(interval);
    //         }
    //     }, 10);
    //
    // }



}
MyCrmAction.template = "CrmDashboard";

// remember the tag name we put in the first step
registry.category("actions").add("crm_dashboard", MyCrmAction);