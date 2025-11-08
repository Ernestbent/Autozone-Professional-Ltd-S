# apps/autopro/autopro/custom_scripts/api/webhook_test.py
import frappe

@frappe.whitelist(allow_guest=True)
def receive():
    # Read VERIFY_TOKEN from site config (set via bench set-config)
    expected_token = frappe.local.conf.get("VERIFY_TOKEN", "vibecode")

    # === VERIFICATION (GET) ===
    if frappe.request.method == "GET":
        mode = frappe.form_dict.get("hub.mode")
        token = frappe.form_dict.get("hub.verify_token")
        challenge = frappe.form_dict.get("hub.challenge")

        if mode == "subscribe" and token == expected_token:
            frappe.response["message"] = challenge  # Plain text
            return
        return "Invalid token", 403

    # === INCOMING MESSAGE (POST) ===
    if frappe.request.method == "POST":
        payload = frappe.local.request.get_json(silent=True) or {}
        frappe.log_error("WhatsApp Webhook", frappe.as_json(payload, indent=2))
        return {"status": "OK"}, 200

    return "Invalid method", 405