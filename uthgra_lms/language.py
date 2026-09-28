"""Serve guests in the site language instead of the browser language.

For a Guest, `frappe.translate.get_language` picks the language from the
`preferred_language` cookie, then the browser's Accept-Language header, and
only then System Settings. A visitor whose browser is in English therefore
gets /login and the signup form in English even though the site is Spanish.

This `before_request` hook runs after Frappe has set `frappe.local.lang` and
replaces the browser-header choice with the System Settings language. Explicit
choices (`?_lang=` and the `preferred_language` cookie) and logged-in users
are left untouched.
"""

import frappe
from frappe.translate import get_preferred_language_cookie


def use_site_language_for_guests() -> None:
	# OPTIONS (CORS preflight) requests never get a session.
	session = getattr(frappe.local, "session", None)
	if not session or session.user != "Guest":
		return

	if frappe.form_dict.get("_lang") or get_preferred_language_cookie():
		return

	site_language = frappe.get_system_settings("language")
	if site_language:
		frappe.local.lang = site_language
