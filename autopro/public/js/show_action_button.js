frappe.ui.form.on('Sales Order', {
    refresh: function(frm) {
        // Check if the document is unsaved and has the correct workflow state
        if (frm.is_new() && frm.doc.workflow_state === 'Pending Credit Approval') {
            // Fetch possible workflow transitions for the current workflow state
            frappe.call({
                method: "frappe.client.get_list",
                args: {
                    doctype: "Workflow Transition",
                    filters: {
                        parent: "Sales Order Credit Approval.", //  actual Workflow name
                        current_state: "Pending Credit Approval",
                        allow: frappe.session.user // Ensure the user has permission for the transition
                    },
                    fields: ["action", "next_state"]
                },
                callback: function(r) {
                    if (r.message && r.message.length > 0) {
                        // Add a custom button to save and show workflow actions
                        frm.add_custom_button(__('Save and Apply Workflow'), function() {
                            if (frm.is_dirty()) {
                                // Save the document as Draft
                                frm.save('Draft').then(() => {
                                    // After saving, fetch Workflow Action records
                                    frappe.call({
                                        method: "frappe.clientDNV.get_list",
                                        args: {
                                            doctype: "Workflow Action",
                                            filters: {
                                                reference_doctype: frm.doc.doctype,
                                                reference_name: frm.doc.name,
                                                status: "Open",
                                                user: frappe.session.user
                                            },
                                            fields: ["name", "workflow_action"]
                                        },
                                        callback: function(resp) {
                                            if (resp.message && resp.message.length > 0) {
                                                // Clear existing primary action
                                                frm.page.clear_primary_action();
                                                // Add workflow action buttons
                                                resp.message.forEach(action => {
                                                    frm.add_custom_button(action.workflow_action, function() {
                                                        frappe.confirm(
                                                            __('Are you sure you want to proceed with "{0}"?', [action.workflow_action]),
                                                            function() {
                                                                frappe.call({
                                                                    method: "frappe.model.workflow.apply_workflow",
                                                                    args: {
                                                                        doc: frm.doc,
                                                                        action: action.workflow_action
                                                                    },
                                                                    freeze: true,
                                                                    callback: function(res) {
                                                                        if (!res.exc) {
                                                                            frm.reload_doc();
                                                                        } else {
                                                                            frappe.msgprint(__('Error applying workflow action: {0}', [res.exc]));
                                                                        }
                                                                    },
                                                                    error: function(err) {
                                                                        frappe.msgprint(__('Error: {0}', [err.message]));
                                                                    }
                                                                });
                                                            }
                                                        );
                                                    }, __("Workflow Actions"));
                                                });
                                                // Set Workflow Actions as primary button group
                                                frm.page.set_inner_btn_group_as_primary(__("Workflow Actions"));
                                            } else {
                                                frappe.msgprint(__('No workflow actions available for this document.'));
                                            }
                                        },
                                        error: function(err) {
                                            frappe.msgprint(__('Error fetching workflow actions: {0}', [err.message]));
                                        }
                                    });
                                }).catch((err) => {
                                    frappe.msgprint(__('Error saving document: {0}', [err.message]));
                                });
                            }
                        }, __("Actions"));
                    } else {
                        frappe.msgprint(__('No workflow transitions defined for "Pending Credit Approval".'));
                    }
                },
                error: function(err) {
                    frappe.msgprint(__('Error fetching workflow transitions: {0}', [err.message]));
                }
            });
        }
    },
    onload: function(frm) {
        // Ensure workflow_state is set to Pending Credit Approval for new documents
        if (frm.is_new() && !frm.doc.workflow_state) {
            frm.set_value('workflow_state', 'Pending Credit Approval');
        }
    }
});