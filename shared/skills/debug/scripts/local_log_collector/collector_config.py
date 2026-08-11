#!/usr/bin/env python3
"""Config helpers for the local log collector."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

CONFIG_DIR = Path.home() / '.junerdd'
CONFIG_FILE = CONFIG_DIR / 'config.json'
COLLECTOR_SECTION_PATH = ('debug', 'collector')
SELECTED_IDE_PATH = (*COLLECTOR_SECTION_PATH, 'ide', 'selected')


class ConfigError(RuntimeError):
    """Raised when ~/.junerdd/config.json cannot be read safely."""


def load_root_config() -> dict[str, Any]:
    if not CONFIG_FILE.exists():
        return {}

    try:
        payload = json.loads(CONFIG_FILE.read_text(encoding='utf-8'))
    except OSError as exc:
        raise ConfigError(f'config_read_failed: {exc}') from exc
    except json.JSONDecodeError as exc:
        raise ConfigError(f'config_invalid_json: {CONFIG_FILE}') from exc

    if not isinstance(payload, dict):
        raise ConfigError(f'config_root_must_be_object: {CONFIG_FILE}')
    return payload


def write_root_config(payload: dict[str, Any]) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    temp_path = CONFIG_FILE.with_suffix(f'{CONFIG_FILE.suffix}.tmp')
    temp_path.write_text(json.dumps(payload, ensure_ascii=True, indent=2), encoding='utf-8')
    os.replace(temp_path, CONFIG_FILE)


def _deep_copy_dict(value: dict[str, Any]) -> dict[str, Any]:
    copied: dict[str, Any] = {}
    for key, item in value.items():
        if isinstance(item, dict):
            copied[key] = _deep_copy_dict(item)
        else:
            copied[key] = item
    return copied


def _ensure_nested_dict(payload: dict[str, Any], path: tuple[str, ...]) -> dict[str, Any]:
    current = payload
    for index, key in enumerate(path):
        next_value = current.get(key)
        if next_value is None:
            next_value = {}
            current[key] = next_value
        elif not isinstance(next_value, dict):
            dotted_path = '.'.join(path[: index + 1])
            raise ConfigError(f'config_path_must_be_object: {dotted_path}')
        current = next_value
    return current


def _prune_empty_branch(payload: dict[str, Any], path: tuple[str, ...]) -> None:
    if not path:
        return

    parent_path = path[:-1]
    key = path[-1]
    current: Any = payload
    parents: list[tuple[dict[str, Any], str]] = []
    for branch_key in parent_path:
        if not isinstance(current, dict):
            return
        parents.append((current, branch_key))
        current = current.get(branch_key)

    if not isinstance(current, dict):
        return
    current.pop(key, None)

    for parent, branch_key in reversed(parents):
        branch = parent.get(branch_key)
        if isinstance(branch, dict) and not branch:
            parent.pop(branch_key, None)
            continue
        break


def update_collector_selected_ide(selected_ide: str) -> dict[str, Any]:
    normalized = selected_ide.strip().lower()
    current = load_root_config()
    updated = _deep_copy_dict(current)

    if normalized:
        ide_config = _ensure_nested_dict(updated, SELECTED_IDE_PATH[:-1])
        ide_config[SELECTED_IDE_PATH[-1]] = normalized
    else:
        _prune_empty_branch(updated, SELECTED_IDE_PATH)

    write_root_config(updated)
    return updated


def _get_nested_dict(payload: dict[str, Any], path: tuple[str, ...]) -> dict[str, Any]:
    current: Any = payload
    for key in path:
        if not isinstance(current, dict):
            return {}
        current = current.get(key)
    return _deep_copy_dict(current) if isinstance(current, dict) else {}


def get_collector_config(payload: dict[str, Any]) -> dict[str, Any]:
    return _get_nested_dict(payload, COLLECTOR_SECTION_PATH)


def get_stored_selected_ide(payload: dict[str, Any]) -> str:
    collector_config = get_collector_config(payload)
    ide_config = collector_config.get('ide')
    if not isinstance(ide_config, dict):
        return ''
    selected = ide_config.get('selected')
    return selected.strip() if isinstance(selected, str) else ''


def build_config_response(
    root_config: dict[str, Any],
    *,
    selected_ide: str,
    selected_ide_available: bool,
    selected_source: str,
    ide_options: list[dict[str, Any]],
    config_error: str = '',
) -> dict[str, Any]:
    return {
        'ok': True,
        'configFile': str(CONFIG_FILE),
        'configError': config_error,
        'collectorConfig': get_collector_config(root_config),
        'ide': {
            'selected': selected_ide,
            'selectedAvailable': selected_ide_available,
            'selectedSource': selected_source,
            'options': ide_options,
        },
    }
