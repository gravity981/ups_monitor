# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

`ups_monitor` is a Home Assistant custom integration for monitoring a UPS (Uninterruptible Power Supply) device connected to a Home Assistant server. It is distributed via HACS (Home Assistant Community Store).

## Architecture

The integration follows the standard HA custom component layout under `custom_components/ups_monitor/`:

- `manifest.json` — integration metadata required by HA (domain, version, iot_class, etc.)
- `__init__.py` — entry point; implements `async_setup_entry` / `async_unload_entry`
- `config_flow.py` — UI-driven config flow (`ConfigFlow`, version 1)
- `const.py` — shared constants (currently just `DOMAIN`)
- `strings.json` / `translations/en.json` — UI string definitions for the config flow

`hacs.json` at the repo root makes the repository indexable by HACS.

The integration uses `iot_class: local_polling`, meaning it periodically polls the UPS device rather than receiving push updates.
