import click
import erpnext
import frappe
from frappe.utils.change_log import get_app_branch
from packaging import version

import india_compliance

IC_VERSION = version.parse(india_compliance.__version__)

VERSIONS_TO_COMPARE = [
    {
        "app_name": "Frappe",
        "current_version": version.parse(frappe.__version__),
        "required_versions": {
            "version-14": "14.57.0",
            # Frappe #43160 (fetch_from on Autocomplete fields)
            "version-15": "15.121.1",
            # Local bench pin: this bench runs Frappe 16.31.0 on purpose
            # (see version-16-ewaybill branch); do not re-add a version-16
            # requirement above 16.31.0 without upgrading Frappe first.
        },
    },
    {
        "app_name": "ERPNext",
        "current_version": version.parse(erpnext.__version__),
        "required_versions": {
            "version-14": "14.70.7",
            # ERPNext #55758
            "version-15": "15.113.0",
            "version-16": "16.24.0",
        },
    },
]


def execute():
    for app in VERSIONS_TO_COMPARE:
        app_name = app["app_name"]
        app_version = app["current_version"]

        if IC_VERSION.major != app_version.major:
            show_error_and_exit(
                f"Incompatible {app_name} Version: \n"
                f"{app_name} version {app_version} not compatible with India Compliance {IC_VERSION}\n"
                f"Please switch to version {IC_VERSION.major} of {app_name} to use the current version of"
                " India Compliance.\n"
                "Alternatively, you may need to change the version of India Compliance App to"
                f" version {app_version.major} to match your {app_name} version.\n"
            )

        if IC_VERSION.major == 17:
            continue

        app_branch = get_app_branch(app_name.lower())
        required_versions = app["required_versions"]

        if app_branch not in required_versions:
            continue

        required_version = version.parse(required_versions[app_branch])

        if app_version < required_version:
            show_error_and_exit(
                f"Incompatible {app_name} Version: \n"
                f"{app_name} version {app_version} not compatible with India Compliance {IC_VERSION}\n"
                f"Please upgrade {app_name} to version {required_version} or above to use the current version of"
                " India Compliance.\n"
                f"Alternatively, you may need to downgrade the version of India Compliance App to {app_version}"
                f" to match your {app_name} version.\n"
            )


def show_error_and_exit(error_message):
    click.secho(error_message, fg="red")
    raise SystemExit(1)
