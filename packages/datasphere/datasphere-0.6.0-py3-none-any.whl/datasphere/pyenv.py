from dataclasses import dataclass
import importlib
import logging
import os
from packaging.requirements import Requirement
from pathlib import Path
import sys
from typing import Dict, Any

from envzy import AutoExplorer, ModulePathsList, PackagesDict

from datasphere.config import PythonEnv as PythonEnvConfig
import yaml

logger = logging.getLogger(__name__)


@dataclass
class PythonEnv:
    version: str
    local_modules_paths: ModulePathsList
    pypi_packages: PackagesDict

    @property
    def conda_yaml(self) -> str:
        dependencies = [f'python=={self.version}', 'pip']

        libraries = [f'{name}{version}' for name, version in self.pypi_packages.items()]
        if libraries:
            dependencies.append({'pip': libraries})

        return yaml.dump({'name': 'default', 'dependencies': dependencies}, sort_keys=False)


def define_py_env(main_script_path: str, py_env_cfg: PythonEnvConfig) -> PythonEnv:
    # User may not add cwd to PYTHONPATH, in case of running execution through `datasphere`, not `python -m`.
    # Since path to python script can be only relative, this should always work.
    sys.path.append(os.getcwd())
    namespace = _get_module_namespace(main_script_path)

    explorer = AutoExplorer()
    py_env = PythonEnv(
        version='.'.join(str(x) for x in explorer.target_python),
        local_modules_paths=explorer.get_local_module_paths(namespace),
        pypi_packages={
            name: f'=={version}' for name, version in
            explorer.get_pypi_packages(namespace).items()
        },
    )

    logger.debug('auto-defined python env: %s', py_env)

    if py_env_cfg.version:
        logger.debug('using python version from config')
        py_env.version = py_env_cfg.version
    if py_env_cfg.requirements:
        logger.debug('using requirements from config')
        py_env.pypi_packages = _parse_requirements(py_env_cfg.requirements)

    return py_env


def _get_module_namespace(path: str) -> Dict[str, Any]:
    module_spec = importlib.util.spec_from_file_location('module', path)
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    return vars(module)


def _parse_requirements(f: Path) -> PackagesDict:
    lines = [line.strip() for line in f.read_text().strip().split('\n')]
    result = {}
    for line in lines:
        req = Requirement(line)
        assert req.marker is None, f'requirement markers are not supported ({line})'
        assert req.url is None, f'requirement url is not supported ({line})'
        extras = f'[{",".join(sorted(req.extras))}]' if req.extras else ''
        result[req.name + extras] = str(req.specifier)
    return result
