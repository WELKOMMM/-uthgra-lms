# uthgra_lms

Custom Frappe app with UTHGRA's customizations for **Frappe LMS**. Installed on
top of stock `frappe/lms` (never fork it), following the documented Frappe
extension pattern (custom app + hooks + fixtures).

## What it does

- Adds a **required WhatsApp number** to the LMS sign-up.
  - `whatsapp` Custom Field on `User` (shipped as a fixture).
  - Replaces the LMS signup form via the `signup_form_template` hook (adds the
    WhatsApp field; Frappe uses the last-installed app's template).
  - Persists it by wrapping `lms.lms.user.sign_up` via
    `override_whitelisted_methods` — no LMS code is modified.

WhatsApp is required **at registration** (form validation + server-side check),
not at the doctype level, so admin/system user saves are never broken.

## Install (via the deploy `apps.json`)

Add this app **after** `lms` so its hooks win:

```json
[
  { "url": "https://github.com/frappe/payments", "branch": "version-16" },
  { "url": "https://github.com/frappe/lms", "branch": "v2.63.0" },
  { "url": "https://github.com/WELKOMMM/-uthgra-lms", "branch": "main" }
]
```

Then redeploy (bump `CACHE_BUST` to force a rebuild). First boot installs the app,
imports the Custom Field, and applies the hooks.

## Install (manual bench, for testing)

```bash
bench get-app uthgra_lms https://github.com/WELKOMMM/-uthgra-lms
bench --site <site> install-app uthgra_lms
bench --site <site> migrate
bench build && bench clear-cache
```

## Verify

Open `/login#signup` — the form must show the **WhatsApp** field and reject an
empty value. After signup, `User.whatsapp` holds the number
(Desk → User, or `bench --site <site> execute "frappe.db.get_value('User', '<email>', 'whatsapp')"`).
