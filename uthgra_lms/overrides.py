import frappe
from frappe import _


def show_signup():
	"""Return our signup template (LMS form + a required WhatsApp field).

	Wired via the `signup_form_template` hook. Frappe reads
	get_hooks("signup_form_template")[-1], so the last-installed app wins —
	this app must be installed after `lms`.
	"""
	return "uthgra_lms/templates/signup-form.html"


@frappe.whitelist(allow_guest=True)
def sign_up(email, full_name, verify_terms, user_category=None, whatsapp=None):
	"""Wrap lms.lms.user.sign_up to require and persist a WhatsApp number.

	Registered through `override_whitelisted_methods`, so the LMS signup form's
	call to `lms.lms.user.sign_up` transparently routes here. Account creation is
	delegated to the original handler (roles, verification email, country, …); we
	only add the WhatsApp validation and persist it on the new User.
	"""
	whatsapp = (whatsapp or "").strip()
	if not whatsapp:
		frappe.throw(_("El número de WhatsApp es obligatorio."))

	# Direct import returns the ORIGINAL function (not this override) — no recursion.
	from lms.lms.user import sign_up as lms_sign_up

	result = lms_sign_up(email, full_name, verify_terms, user_category)

	# Persist WhatsApp only for a freshly created account (LMS returns 1 or 2).
	status = result[0] if isinstance(result, (list, tuple)) else None
	if status in (1, 2):
		user_name = frappe.db.get_value("User", {"email": email}, "name")
		if user_name:
			frappe.db.set_value("User", user_name, "whatsapp", whatsapp)
			frappe.db.commit()

	return result
