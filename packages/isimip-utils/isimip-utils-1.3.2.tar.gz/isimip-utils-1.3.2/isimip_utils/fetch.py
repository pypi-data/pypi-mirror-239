import json
import logging
import os
import re
from pathlib import Path
from urllib.parse import urlparse

import requests

from isimip_utils.exceptions import NotFound

logger = logging.getLogger(__name__)


def fetch_definitions(bases, path):
    path_components = Path(path).parts
    for i in range(len(path_components), 0, -1):
        definitions_path = Path('definitions').joinpath(os.sep.join(path_components[:i+1])).with_suffix('.json')
        definitions_json = fetch_json(bases, definitions_path, extend_base='output')

        if definitions_json:
            logger.debug('definitions_path = %s', definitions_path)
            logger.debug('definitions_json = %s', definitions_json)

            definitions = {}
            for definition_name, definition in definitions_json.items():
                # convert the definitions to dicts if they are lists
                if isinstance(definition, list):
                    definitions[definition_name] = {
                        row['specifier']: row for row in definition
                    }
                else:
                    definitions[definition_name] = definition

            logger.debug('definitions = %s', definitions)
            return definitions

    raise NotFound(f'no definitions found for {path}')


def fetch_pattern(bases, path):
    path_components = Path(path).parts
    for i in range(len(path_components), 0, -1):
        pattern_path = Path('pattern').joinpath(os.sep.join(path_components[:i+1]) + '.json')
        pattern_json = fetch_json(bases, pattern_path, extend_base='output')

        if pattern_json:
            logger.debug('pattern_path = %s', pattern_path)
            logger.debug('pattern_json = %s', pattern_json)

            if not all([
                isinstance(pattern_json['path'], str),
                isinstance(pattern_json['file'], str),
                isinstance(pattern_json['dataset'], str),
                isinstance(pattern_json['suffix'], list)
            ]):
                break

            pattern = {
                'path': re.compile(pattern_json['path']),
                'file': re.compile(pattern_json['file']),
                'dataset': re.compile(pattern_json['dataset']),
                'suffix': pattern_json['suffix'],
                'specifiers': pattern_json.get('specifiers', []),
                'specifiers_map': pattern_json.get('specifiers_map', {})
            }

            logger.debug('pattern = %s', pattern)

            return pattern

    raise NotFound(f'no pattern found for {path}')


def fetch_schema(bases, path):
    path_components = Path(path).parts
    for i in range(len(path_components), 0, -1):
        schema_path = Path('schema').joinpath(os.sep.join(path_components[:i+1])).with_suffix('.json')
        schema_json = fetch_json(bases, schema_path, extend_base='output')

        if schema_json:
            logger.debug('schema_path = %s', schema_path)
            logger.debug('schema_json = %s', schema_json)
            return schema_json

    raise NotFound(f'no schema found for {path}')


def fetch_tree(bases, path):
    path_components = Path(path).parts
    for i in range(len(path_components), 0, -1):
        tree_path = Path('tree').joinpath(os.sep.join(path_components[:i+1])).with_suffix('.json')
        tree_json = fetch_json(bases, tree_path, extend_base='output')

        if tree_json:
            logger.debug('tree_path = %s', tree_path)
            logger.debug('tree_json = %s', tree_json)
            return tree_json

    raise NotFound(f'no tree found for {path}')


def fetch_resource(location):
    return fetch_json([location])


def fetch_json(bases, path=None, extend_base=None):
    for base in bases:
        if urlparse(base).scheme:
            if path is not None:
                json_url = base.rstrip('/') + '/' + path.as_posix()
            else:
                json_url = base.rstrip('/')

            logger.debug('json_url = %s', json_url)

            try:
                response = requests.get(json_url)
            except requests.exceptions.ConnectionError:
                return None

            if response.status_code == 200:
                return response.json()

        else:
            json_path = Path(base).expanduser()
            if extend_base is not None:
                json_path /= extend_base
            if path is not None:
                json_path /= path

            logger.debug('json_path = %s', json_path)

            if json_path.exists():
                return json.loads(open(json_path).read())


def fetch_file(bases, path=None, extend_base=None):
    for base in bases:
        if urlparse(base).scheme:
            if path is not None:
                file_url = base.rstrip('/') + '/' + path.as_posix()
            else:
                file_url = base.rstrip('/')

            logger.debug('file_url = %s', file_url)

            try:
                response = requests.get(file_url)
            except requests.exceptions.ConnectionError:
                return None

            if response.status_code == 200:
                return response.content

        else:
            file_path = Path(base).expanduser()
            if extend_base is not None:
                file_path /= extend_base
            if path is not None:
                file_path /= path

            logger.debug('file_path = %s', file_path)

            if file_path.exists():
                return file_path.read()
