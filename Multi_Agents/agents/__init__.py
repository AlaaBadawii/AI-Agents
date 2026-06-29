"""Agents package with automatic module registration."""

import importlib
import pkgutil


def _load_agent_modules():
	for module_info in pkgutil.iter_modules(__path__):
		if module_info.name.startswith("_") or module_info.name == "orchestrator":
			continue
		importlib.import_module(f"{__name__}.{module_info.name}")


_load_agent_modules()
