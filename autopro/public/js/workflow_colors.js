// Custom status colors beyond default styles
const STATUS_COLORS = {
  "Draft": "#FFC107",      // Amber
  "Pending Credit Approval": "#17A2B8", // Teal
  "Approved": "#007BFF",   // Blue
  "Packing": "#6C757D",    // Gray
  "Delivery Pending": "#FD7E14", // Orange
  "Delivered": "#28A745",  // Green
  "Completed": "#6F42C1"   // Purple
};

// Apply to list view
frappe.listview_settings['Sales Order'] = {
  onload: function(listview) {
    apply_status_colors();
  }
};

// Form view integration
frappe.ui.form.on('Sales Order', {
  refresh: function(frm) {
    colorize_status(frm);
  }
});

function colorize_status(frm) {
  const status = frm.doc.status;
  const $status = $(frm.fields_dict.status.wrapper);
  
  $status.css({
    'background-color': STATUS_COLORS[status] || '#EEE',
    'color': '#FFF',
    'padding': '2px 10px',
    'border-radius': '4px',
    'font-weight': 'bold'
  });
}

function apply_status_colors() {
  $('[data-fieldname="status"]').each(function() {
    const status = $(this).text().trim();
    $(this).css({
      'background-color': STATUS_COLORS[status] || '#EEE',
      'color': '#FFF',
      'padding': '2px 8px',
      'border-radius': '4px'
    });
  });
}