frappe.ui.form.on('Packing List', {
    refresh: function(frm) {
        set_item_filter(frm);
        show_fill_button(frm);
        update_remaining_qty(frm);
    },
    sales_invoice: function(frm) {
        if (frm.doc.sales_invoice) {
            load_invoice_items(frm);
        } else {
            frm.clear_table('table_ttya');
            frm.clear_table('table_hqkk');
            frm.clear_table('custom_box_summary');
            frm.refresh_fields();
        }
        set_item_filter(frm);
        show_fill_button(frm);
    },
    table_hqkk_add: function(frm) { set_item_filter(frm); },
    table_hqkk_remove: function(frm) { update_remaining_qty(frm); }
});

/* -------------------------------------------------------------
   FILTER PACKING TABLE TO ONLY SHOW INVOICE ITEMS
   ------------------------------------------------------------- */
function set_item_filter(frm) {
    const items = (frm.doc.table_ttya || []).map(r => r.item).filter(Boolean);
    frm.fields_dict.table_hqkk.grid.get_field('item').get_query = function () {
        return { filters: [['name', 'in', items.length ? items : ['-']]] };
    };
}

/* -------------------------------------------------------------
   LOAD INVOICE ITEMS
   ------------------------------------------------------------- */
function load_invoice_items(frm) {
    if (!frm.doc.sales_invoice) return;

    frappe.call({
        method: 'frappe.client.get',
        args: { doctype: 'Sales Invoice', name: frm.doc.sales_invoice },
        callback: function (r) {
            const inv = r.message;
            if (!inv?.items?.length) {
                frappe.msgprint(__('No items in the selected invoice.'));
                return;
            }

            frm.clear_table('table_ttya');
            inv.items.forEach(itm => {
                const row = frm.add_child('table_ttya');
                row.item = itm.item_code;
                row.item_name = itm.item_name;
                row.qty = itm.qty;
                row.uom = itm.uom;
                row.remaining_qty = itm.qty;   // initial remaining = full qty
            });

            frm.refresh_field('table_ttya');
            update_remaining_qty(frm);
            show_fill_button(frm);
        }
    });
}

/* -------------------------------------------------------------
   UPDATE REMAINING QTY – **source of truth**
   ------------------------------------------------------------- */
function update_remaining_qty(frm) {
    if (!frm.doc.table_ttya) return;

    // 1. reset to original qty
    frm.doc.table_ttya.forEach(inv => inv.remaining_qty = inv.qty);

    // 2. subtract everything that is already packed
    (frm.doc.table_hqkk || []).forEach(pack => {
        const inv = frm.doc.table_ttya.find(r => r.item === pack.item);
        if (inv) {
            inv.remaining_qty -= (pack.quantity || 0);
            if (inv.remaining_qty < 0) inv.remaining_qty = 0;
        }
    });

    frm.refresh_field('table_ttya');
}

/* -------------------------------------------------------------
   SHOW “Fill Box Items” BUTTON
   ------------------------------------------------------------- */
function show_fill_button(frm) {
    frm.remove_custom_button(__('Fill Box Items'));
    if (frm.doc.sales_invoice && frm.doc.docstatus === 0 && frm.doc.table_ttya?.length) {
        frm.add_custom_button(__('Fill Box Items'), () => open_box_dialog(frm), __('Actions'));
    }
}

/* -------------------------------------------------------------
   DIALOG – PACK ITEMS INTO A BOX
   ------------------------------------------------------------- */
function open_box_dialog(frm) {
    const d = new frappe.ui.Dialog({
        title: __('Pack Items into Box'),
        fields: [
            {
                fieldname: 'box_number',
                fieldtype: 'Int',
                label: __('Box Number'),
                reqd: 1,
                default: get_next_box_number(frm)
            },
            { fieldname: 'box_weight', fieldtype: 'Float', label: __('Box Weight (kg)'), reqd: 1, default: 0 },
            {
                fieldname: 'items',
                fieldtype: 'Table',
                label: __('Items to Pack'),
                cannot_add_rows: true,
                in_place_edit: true,
                data: [],
                fields: [
                    { fieldname: 'select', fieldtype: 'Check', label: 'Select', in_list_view: 1, width: 60 },
                    { fieldname: 'item', fieldtype: 'Link', options: 'Item', label: 'Item', read_only: 1, in_list_view: 1 },
                    { fieldname: 'item_name', fieldtype: 'Data', label: 'Name', read_only: 1, in_list_view: 1 },
                    { fieldname: 'remaining_qty', fieldtype: 'Float', label: 'Remaining', read_only: 1, in_list_view: 1 },
                    { fieldname: 'quantity', fieldtype: 'Float', label: 'Pack Qty', default: 0, in_list_view: 1 }
                ]
            }
        ],
        primary_action_label: __('Add to Box'),
        primary_action: function () {
            const vals = d.get_values();
            if (!vals) return;

            if (save_box(frm, vals, d)) {
                // move to next box
                const next = vals.box_number + 1;
                d.set_value('box_number', next);
                d.set_value('box_weight', 0);

                // **REBUILD DIALOG FROM SCRATCH**
                rebuild_dialog_items(frm, d);

                frappe.show_alert({
                    message: __('Box {0} saved! Ready for Box {1}', [vals.box_number, next]),
                    indicator: 'green'
                });
            }
        }
    });

    // auto‑load weight when user types an existing box number
    d.fields_dict.box_number.df.onchange = function () {
        const bn = d.get_value('box_number');
        const box = (frm.doc.custom_box_summary || []).find(b => b.box_number == bn);
        d.set_value('box_weight', box ? box.weight_kg : 0);
    };

    rebuild_dialog_items(frm, d);
    d.show();
}

/* -------------------------------------------------------------
   NEXT BOX NUMBER
   ------------------------------------------------------------- */
function get_next_box_number(frm) {
    const used = (frm.doc.table_hqkk || []).map(r => r.box_number).filter(Boolean);
    return used.length ? Math.max(...used) + 1 : 1;
}

/* -------------------------------------------------------------
   REBUILD DIALOG – ONLY SHOW ITEMS WITH remaining_qty > 0
   ------------------------------------------------------------- */
function rebuild_dialog_items(frm, dialog) {
    // Build **fresh** rows – ignore anything that was in the dialog before
    const fresh = (frm.doc.table_ttya || [])
        .filter(row => row.remaining_qty > 0)          // <-- HIDE ZERO
        .map(row => ({
            select: 0,                                 // always start unchecked
            item: row.item,
            item_name: row.item_name,
            remaining_qty: row.remaining_qty,
            quantity: 0                                 // always start with 0
        }));

    const tbl = dialog.fields_dict.items;
    tbl.df.data = fresh;
    tbl.grid.refresh();

    // Force repaint (Frappe sometimes needs two refreshes)
    setTimeout(() => tbl.grid.refresh(), 0);
}

/* -------------------------------------------------------------
   SAVE BOX – add items, update weight, recalc remaining_qty
   ------------------------------------------------------------- */
function save_box(frm, vals, dialog) {
    const box = vals.box_number;
    const weight = vals.box_weight || 0;
    const selected = (vals.items || []).filter(r => r.select && r.quantity > 0);

    if (!selected.length) {
        frappe.msgprint({ title: __('No Items'), message: __('Select at least one item with quantity > 0.'), indicator: 'red' });
        return false;
    }

    // ---------- VALIDATE ----------
    for (let itm of selected) {
        const invRow = frm.doc.table_ttya.find(r => r.item === itm.item);
        if (!invRow || itm.quantity > invRow.remaining_qty) {
            frappe.msgprint({
                title: __('Insufficient Quantity'),
                message: __('Only {0} remaining for <b>{1}</b>', [invRow?.remaining_qty || 0, invRow?.item_name || itm.item]),
                indicator: 'orange'
            });
            return false;
        }
    }

    // ---------- ADD TO PACKING TABLE ----------
    selected.forEach(itm => {
        const row = frm.add_child('table_hqkk');
        row.box_number = box;
        row.item = itm.item;
        row.item_name = itm.item_name;
        row.quantity = itm.quantity;
        row.box_weight = weight;
        const invRow = frm.doc.table_ttya.find(r => r.item === itm.item);
        if (invRow) row.uom = invRow.uom;
    });

    // ---------- UPDATE BOX SUMMARY (no duplicates) ----------
    const existing = (frm.doc.custom_box_summary || []).find(b => b.box_number == box);
    if (existing) {
        existing.weight_kg = weight;
    } else {
        const b = frm.add_child('custom_box_summary');
        b.box_number = box;
        b.weight_kg = weight;
    }

    // ---------- REFRESH FORM ----------
    frm.refresh_field('table_hqkk');
    frm.refresh_field('custom_box_summary');

    // **THIS IS THE ONLY PLACE remaining_qty IS CALCULATED**
    update_remaining_qty(frm);

    return true;
}