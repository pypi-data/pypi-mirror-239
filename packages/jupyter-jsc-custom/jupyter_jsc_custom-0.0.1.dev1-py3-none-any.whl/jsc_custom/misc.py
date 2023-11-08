import json
import os

import yaml
from jupyterhub.app import app_log

from .log_utils import update_extra_handlers

_custom_config_cache = {}
_custom_config_last_update = 0
_custom_config_file = os.environ.get("CUSTOM_CONFIG_PATH")

_logging_cache = {}


def get_custom_config():
    global _custom_config_cache
    global _custom_config_last_update
    global _logging_cache

    # Only update custom_config, if it has changed on disk
    try:
        last_change = os.path.getmtime(_custom_config_file)
        if last_change > _custom_config_last_update:
            app_log.debug("Load custom config file.")
            with open(_custom_config_file, "r") as f:
                ret = yaml.full_load(f)
            _custom_config_last_update = last_change
            _custom_config_cache = ret

            if _custom_config_cache.get("logging", {}) != _logging_cache:
                _logging_cache = _custom_config_cache.get("logging", {})
                app_log.debug("Update Logger")
                update_extra_handlers(_logging_cache)

    except:
        app_log.exception("Could not load custom config file")
    else:
        return _custom_config_cache


_reservations_cache = {}
_reservations_last_update = 0
_reservations_file = os.environ.get("RESERVATIONS_FILE")


def get_reservations():
    global _reservations_cache
    global _reservations_last_update
    try:
        # Only update reservations, if it has changed on disk
        last_change = os.path.getmtime(_reservations_file)
        if last_change > _reservations_last_update:
            app_log.debug("Load reservation file")
            with open(_reservations_file, "r") as f:
                ret = json.load(f)
            _reservations_last_update = last_change
            _reservations_cache = ret
    except:
        app_log.exception("Could not load reservation file")
    finally:
        return _reservations_cache


_incidents_cache = {}
_incidents_last_update = 0
_incidents_file = os.environ.get("INCIDENTS_FILE")


def get_incidents():
    global _incidents_cache
    global _incidents_last_update
    try:
        last_change = os.path.getmtime(_incidents_file)
        if last_change > _incidents_last_update:
            app_log.debug("Load incidents file")
            with open(_incidents_file, "r") as f:
                ret = json.load(f)
            _incidents_last_update = last_change
            _incidents_cache = ret
    except:
        app_log.exception("Could not load incidents file")
    return _incidents_cache


async def create_ns(user):
    ns = dict(user=user)
    if user:
        auth_state = await user.get_auth_state()
        if "refresh_token" in auth_state.keys():
            del auth_state["refresh_token"]
        ns["auth_state"] = auth_state
    return ns
