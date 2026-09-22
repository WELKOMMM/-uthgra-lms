app_name = "uthgra_lms"
app_title = "Uthgra Lms"
app_publisher = "UTHGRA"
app_description = "UTHGRA customizations for Frappe LMS (WhatsApp required at signup)"
app_email = "admin@welkomia.com"
app_license = "mit"

# Installed on top of `lms`; must load after it so our hooks win.
required_apps = ["lms"]

# Ship the `whatsapp` Custom Field on User with the app (imported on install/migrate).
fixtures = [
    {"dt": "Custom Field", "filters": [["name", "in", ["User-whatsapp"]]]},
]

# Replace the LMS signup form with ours (adds the WhatsApp field).
# Frappe uses get_hooks("signup_form_template")[-1], so the last-installed app wins.
signup_form_template = "uthgra_lms.overrides.show_signup"

# Transparently extend the LMS signup handler to persist the WhatsApp number.
override_whitelisted_methods = {
    "lms.lms.user.sign_up": "uthgra_lms.overrides.sign_up",
}
