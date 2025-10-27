frappe.ui.form.on('Delivery Note', {
    // Trigger on workflow action or a custom button
    mark_in_transit: function(frm) {

        // Only show if workflow state is Dispatched
        if(frm.doc.workflow_state !== "Dispatched") return;

        let d = new frappe.ui.Dialog({
            title: 'Generate Gate Passes',
            fields: [
                {
                    label: 'Office Gate Pass',
                    fieldname: 'office_gate_pass',
                    fieldtype: 'Data',
                    reqd: 1
                },
                {
                    label: 'Store Gate Pass',
                    fieldname: 'store_gate_pass',
                    fieldtype: 'Data',
                    reqd: 1
                }
            ],
            primary_action_label: 'Generate',
            primary_action: function(values) {
                // Call server method to generate gate passes
                frappe.call({
                    method: "autopro.custom_scripts.get_gate_and_office_pass.generate_gate_passes",
                    args: {
                        delivery_note_name: frm.doc.name,
                        office_gate_pass: values.office_gate_pass,
                        store_gate_pass: values.store_gate_pass
                    },
                    callback: function(r) {
                        if(r.message){
                            frm.set_value('office_gate_pass', r.message.office_gate_pass);
                            frm.set_value('store_gate_pass', r.message.store_gate_pass);
                            frm.set_value('workflow_state', 'In Transit');
                            frm.save();
                            frappe.msgprint('Gate Passes Generated and Delivery Note marked as In Transit');
                        }
                    }
                });

                d.hide();
            }
        });

        d.show();
    }
});
