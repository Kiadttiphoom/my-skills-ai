#!/usr/bin/env python3
"""IDE resolution and source opening helpers for the local log collector."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import shutil
import subprocess
from typing import Any

LOCATION_PATTERN = re.compile(r'^(?P<path>.+?):(?P<line>\d+)(?::(?P<column>\d+))?$')


@dataclass(frozen=True)
class IdeSpec:
    id: str
    label: str
    kind: str
    cli_candidates: tuple[str, ...]
    app_candidates: tuple[str, ...]


IDE_SPECS: tuple[IdeSpec, ...] = (
    IdeSpec('cursor', 'Cursor', 'vscode-family', ('cursor',), ('Cursor.app',)),
    IdeSpec('vscode', 'VS Code', 'vscode-family', ('code',), ('Visual Studio Code.app',)),
    IdeSpec('windsurf', 'Windsurf', 'vscode-family', ('windsurf',), ('Windsurf.app',)),
    IdeSpec('zed', 'Zed', 'zed', ('zed', 'zeditor'), ('Zed.app',)),
    IdeSpec('webstorm', 'WebStorm', 'jetbrains', ('webstorm',), ('WebStorm.app',)),
    IdeSpec('phpstorm', 'PhpStorm', 'jetbrains', ('phpstorm',), ('PhpStorm.app',)),
    IdeSpec('idea', 'IntelliJ IDEA', 'jetbrains', ('idea',), ('IntelliJ IDEA.app',)),
    IdeSpec('sublime', 'Sublime Text', 'sublime', ('subl',), ('Sublime Text.app',)),
    IdeSpec('textmate', 'TextMate', 'textmate', ('mate',), ('TextMate.app',)),
)

APP_SEARCH_DIRS = (
    Path('/Applications'),
    Path.home() / 'Applications',
)


def _normalize_text(value: Any) -> str:
    return value.strip() if isinstance(value, str) else ''


def get_ide_spec(ide_id: str) -> IdeSpec | None:
    normalized = ide_id.strip().lower()
    for spec in IDE_SPECS:
        if spec.id == normalized:
            return spec
    return None


def _find_cli(spec: IdeSpec) -> str:
    for candidate in spec.cli_candidates:
        resolved = shutil.which(candidate)
        if resolved:
            return resolved
    return ''


def _find_app(spec: IdeSpec) -> str:
    for directory in APP_SEARCH_DIRS:
        for app_name in spec.app_candidates:
            app_path = directory / app_name
            if app_path.exists():
                return str(app_path)
    return ''


def list_ide_options(selected_ide: str = '') -> list[dict[str, Any]]:
    options: list[dict[str, Any]] = []
    known_ids = set()
    for spec in IDE_SPECS:
        cli_path = _find_cli(spec)
        app_path = _find_app(spec)
        options.append(
            {
                'id': spec.id,
                'label': spec.label,
                'available': bool(cli_path or app_path),
                'launcher': 'cli' if cli_path else ('app' if app_path else ''),
            },
        )
        known_ids.add(spec.id)

    selected = _normalize_text(selected_ide).lower()
    if selected and selected not in known_ids:
        options.append(
            {
                'id': selected,
                'label': f'Unsupported ({selected})',
                'available': False,
                'launcher': '',
            },
        )

    return options


def get_ide_option(ide_id: str, ide_options: list[dict[str, Any]]) -> dict[str, Any] | None:
    normalized = _normalize_text(ide_id).lower()
    if not normalized:
        return None
    for option in ide_options:
        if option['id'] == normalized:
            return option
    return None


def resolve_selected_ide(
    *,
    stored_selected_ide: str,
    default_ide: str,
    ide_options: list[dict[str, Any]],
) -> tuple[str, str]:
    stored_selected = _normalize_text(stored_selected_ide).lower()
    if stored_selected:
        return stored_selected, 'config'

    configured_default = _normalize_text(default_ide).lower()
    default_option = get_ide_option(configured_default, ide_options)
    if default_option and default_option['available']:
        return configured_default, 'default'

    for option in ide_options:
        if option['available']:
            return option['id'], 'auto'

    if configured_default:
        return configured_default, 'default'

    return '', 'none'


def parse_location(value: str) -> dict[str, Any]:
    location = _normalize_text(value)
    if not location:
        return {'pathText': '', 'line': None, 'column': None, 'parseError': 'location_missing'}

    match = LOCATION_PATTERN.match(location)
    if not match:
        return {'pathText': location, 'line': None, 'column': None, 'parseError': 'invalid_location'}

    return {
        'pathText': match.group('path'),
        'line': int(match.group('line')),
        'column': int(match.group('column')) if match.group('column') else None,
        'parseError': '',
    }


def resolve_location(value: str, workspace_root: Path) -> dict[str, Any]:
    parsed = parse_location(value)
    path_text = parsed['pathText']
    line = parsed['line']
    column = parsed['column']
    workspace_root = workspace_root.resolve(strict=False)

    if not path_text:
        return {
            'location': value,
            'pathText': '',
            'line': line,
            'column': column,
            'parseError': parsed['parseError'] or 'location_missing',
            'resolvedPath': '',
            'displayPath': value,
            'exists': False,
            'openable': False,
        }

    candidate_path = Path(path_text).expanduser()
    absolute_path_forbidden = candidate_path.is_absolute()
    if not candidate_path.is_absolute():
        candidate_path = workspace_root / candidate_path
    resolved_path = candidate_path.resolve(strict=False)
    exists = resolved_path.exists()
    within_workspace = False

    try:
        resolved_path.relative_to(workspace_root)
        within_workspace = True
    except ValueError:
        within_workspace = False

    if within_workspace:
        display_path = str(resolved_path.relative_to(workspace_root))
    else:
        display_path = str(resolved_path)

    parse_error = parsed['parseError']
    if not parse_error and absolute_path_forbidden:
        parse_error = 'absolute_path_forbidden'
    elif not parse_error and not within_workspace:
        parse_error = 'location_outside_workspace'

    return {
        'location': value,
        'pathText': path_text,
        'line': line,
        'column': column,
        'parseError': parse_error,
        'resolvedPath': str(resolved_path),
        'displayPath': display_path,
        'exists': exists,
        'withinWorkspace': within_workspace,
        'openable': within_workspace and exists and line is not None and not parse_error,
    }


def enrich_location_records(
    raw_locations: list[dict[str, Any]],
    *,
    workspace_root: Path,
) -> list[dict[str, Any]]:
    return [
        {
            **record,
            **resolve_location(record.get('location', ''), workspace_root),
        }
        for record in raw_locations
    ]


def _goto_target(path: str, line: int, column: int | None) -> str:
    target = f'{path}:{line}'
    if column is not None:
        target = f'{target}:{column}'
    return target


def _build_command(spec: IdeSpec, resolved_location: dict[str, Any]) -> list[str]:
    cli_path = _find_cli(spec)
    app_path = _find_app(spec)
    resolved_path = resolved_location['resolvedPath']
    line = resolved_location['line']
    column = resolved_location['column']

    if not resolved_path or line is None:
        raise ValueError('location_missing_line')

    goto_target = _goto_target(resolved_path, line, column)

    if spec.kind == 'vscode-family':
        if cli_path:
            return [cli_path, '--goto', goto_target]
        if app_path:
            return ['open', '-a', app_path, '--args', '--goto', goto_target]
    elif spec.kind == 'zed':
        if cli_path:
            return [cli_path, goto_target]
        if app_path:
            return ['open', '-a', app_path, '--args', goto_target]
    elif spec.kind == 'jetbrains':
        command: list[str]
        if cli_path:
            command = [cli_path]
        elif app_path:
            command = ['open', '-a', app_path, '--args']
        else:
            command = []
        if command:
            command.extend(['--line', str(line)])
            if column is not None:
                command.extend(['--column', str(column)])
            command.append(resolved_path)
            return command
    elif spec.kind == 'sublime':
        if cli_path:
            return [cli_path, goto_target]
    elif spec.kind == 'textmate':
        if cli_path:
            line_target = str(line) if column is None else f'{line}:{column}'
            return [cli_path, '-l', line_target, resolved_path]

    raise ValueError('launcher_unavailable')


def open_location_in_ide(ide_id: str, resolved_location: dict[str, Any]) -> dict[str, Any]:
    spec = get_ide_spec(ide_id)
    if spec is None:
        raise ValueError('unsupported_ide')
    if not resolved_location.get('openable'):
        raise ValueError(resolved_location.get('parseError') or 'location_unavailable')

    command = _build_command(spec, resolved_location)
    process = subprocess.Popen(
        command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
        start_new_session=True,
    )
    try:
        _, stderr = process.communicate(timeout=1)
    except subprocess.TimeoutExpired:
        return {
            'ide': spec.id,
            'label': spec.label,
            'launchStatus': 'requested',
            'confirmed': False,
            'command': command,
            'resolvedPath': resolved_location['resolvedPath'],
            'line': resolved_location['line'],
            'column': resolved_location['column'],
        }

    if process.returncode != 0:
        message = (stderr or '').strip() or 'launcher_failed'
        raise RuntimeError(message)

    return {
        'ide': spec.id,
        'label': spec.label,
        'launchStatus': 'confirmed',
        'confirmed': True,
        'command': command,
        'resolvedPath': resolved_location['resolvedPath'],
        'line': resolved_location['line'],
        'column': resolved_location['column'],
    }
