app_name = "autopro"
app_title = "Autozone Pro Ltd Customization"
app_publisher = "Autozone Pro Ltd"
app_description = "All Customizations"
app_email = "othienobenedict8@gmail.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "autopro",
# 		"logo": "/assets/autopro/logo.png",
# 		"title": "Autozone Pro Ltd Customization",
# 		"route": "/autopro",
# 		"has_permission": "autopro.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/autopro/css/autopro.css"
# app_include_js = "/assets/autopro/js/autopro.js"

# include js, css files in header of web template
# web_include_css = "/assets/autopro/css/autopro.css"
# web_include_js = "/assets/autopro/js/autopro.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "autopro/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# 
doctype_js = {
    "Sales Person" : [
        "public/js/100_percent_contribution.js"
    ],
    "Payment Entry": [
        "public/js/check_duplicate_mobile_money.js",
        "public/js/check_reference_no.js",
        "public/js/payment_entry_default_ref_no.js",
    ],
    "Sales Order Item":[
        # "public/js/current_stock_quantity.js",
        "public/js/default_discount_account.js"
    ],
    "Sales Order":[
        "public/js/customer_search.js",
        "public/js/default_discount_account.js",
        "public/js/increase_the_sales_search.js",
        "public/js/outstanding.js",
        "public/js/sales_person_name_on_list.js",
        "public/js/show_sales_person.js",
        "public/js/status_display.js",
        "public/js/total_discount.js",
        "public/js/workflow_colors.js",
        "public/js/100_percent_contribution.js",
        "public/js/default_qty_for _P25.js",
        "public/js/default_warehouse.js",
        "public/js/discount_percentage.js",
        "public/js/current_stock_quantity.js",
        "public/js/show_action_button.js",
        "public/js/cancelled_show.js",
        "public/js/update_delivery_note.js",
        "public/js/track_courier_details.js",
        "public/js/create_delivery_note.js",
        "public/js/create_pick_list.js",
        "public/js/create_packing_slip.js",
        "public/js/hide_sales_order_buttons.js",

    ],
    "Sales Invoice Item":[
        "public/js/default_discount_account.js"
    ],
    "Item Price":[
        "public/js/default_discount_account.js",
        "public/js/display_quantity_available.js"
    ],
    "Sales Invoice":[
        "public/js/hide_invoice_cancel_for_store.js",
        "public/js/default_discount_account.js",
    ],
    "Journal Entry":[
        "public/js/journal_entry_ref_no.js"
    ],
    "Pick List":[
       "public/js/create_pick_list.js",
    #    "public/js/create_delivery_note_from_pick_list.js"
        
    ],
    "GL Entry":[
        'public/js/general_leger_checkbox.js'
    ],
    "Packing Slip":[
        'public/js/packing_slip.js'
    ],
    "Delivery Note":[
        'public/js/get_gate_and_office_pass.js',
        'public/js/create_delivery_note.js'
    ],
    "Customer":[
        'public/js/customer_whatsapp.js'
    ]
    }
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "autopro/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "autopro.utils.jinja_methods",
# 	"filters": "autopro.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "autopro.install.before_install"
# after_install = "autopro.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "autopro.uninstall.before_uninstall"
# after_uninstall = "autopro.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "autopro.utils.before_app_install"
# after_app_install = "autopro.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "autopro.utils.before_app_uninstall"
# after_app_uninstall = "autopro.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "autopro.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events
workflow_methods = {
    "create_pick_list_from_sales_order": "autopro.autopro.doctype.sales_order_custom.sales_order_custom.create_pick_list_on_workflow"
}


doc_events = {
    # "Packing Slip": {
    #     "validate": "autopro.custom_scripts.packing_slip.validate_packing_slip"
    # },
	# "Packing Slip":{
    #     "before_insert": "autopro.custom_scripts.packing_slip_from_dn.populate_rate_amount"
    # }
    "Delivery Note": {
        "before_submit": "autopro.custom_scripts.check_packing_slip.check_packing_slip",
        "on_submit": "autopro.custom_scripts.update_dn_status.on_submit"
    },       

    "Sales Order": {
        "before_workflow_action": "autopro.custom_scripts.submit_delivery_note_workflow.restrict_next_state_if_dn_not_submitted"
    },
    "Sales Order":{
        "before_workflow_action": "autopro.custom_scripts.halt_sales_order.check_courier_details"
    }
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"autopro.tasks.all"
# 	],
# 	"daily": [
# 		"autopro.tasks.daily"
# 	],
# 	"hourly": [
# 		"autopro.tasks.hourly"
# 	],
# 	"weekly": [
# 		"autopro.tasks.weekly"
# 	],
# 	"monthly": [
# 		"autopro.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "autopro.install.before_tests"

# Overriding Methods
# ------------------------------
######## Create webhook for frappe wahtsapp integration live chat and so on
override_whitelisted_methods = {
    "autopro.custom_scripts.api.webhook_test.receive_webhook": "autopro.custom_scripts.api.webhook_test.receive_webhook"
}

# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "autopro.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["autopro.utils.before_request"]
# after_request = ["autopro.utils.after_request"]

# Job Events
# ----------
# before_job = ["autopro.utils.before_job"]
# after_job = ["autopro.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"autopro.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

fixtures = [
    "Workflow",
    "Workflow State",
    "Workflow Action Master"
]


