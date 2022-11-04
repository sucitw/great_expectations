from __future__ import annotations

import logging
import pathlib
from pprint import pformat as pf
from typing import TYPE_CHECKING, ClassVar, Dict, Optional, Union

from pydantic import DirectoryPath, validate_arguments

from great_expectations.zep.config import GxConfig
from great_expectations.zep.sources import _SourceFactories

if TYPE_CHECKING:
    from great_expectations.zep.interfaces import Datasource

LOGGER = logging.getLogger(__name__)


class DataContext:
    """
    NOTE: this is just a scaffold for exploring and iterating on our ZEP prototype
    this will be formalized and tested prior to release.

    Use `great_expectations.get_context()` for a real DataContext.
    """

    _context: ClassVar[Optional[DataContext]] = None

    _datasources: Dict[str, Datasource]
    root_directory: Union[DirectoryPath, str, None]

    @classmethod
    def get_context(
        cls, context_root_dir: Optional[DirectoryPath] = None
    ) -> DataContext:
        if not cls._context:
            cls._context = DataContext(context_root_dir=context_root_dir)

        assert cls._context
        if cls._context.root_directory:
            # load config and add/instantiate Datasources & Assets
            config_path = pathlib.Path(cls._context.root_directory) / "config.yaml"
            loaded_config = GxConfig.parse_yaml(config_path)
            for ds_name, datasource in loaded_config.datasources.items():
                LOGGER.info(f"Loaded '{ds_name}' from config")
                cls._context._attach_datasource_to_context(datasource)
                # TODO: add assets?

        return cls._context

    @validate_arguments
    def __init__(self, context_root_dir: Optional[DirectoryPath] = None) -> None:
        self.root_directory = context_root_dir
        self._sources: _SourceFactories = _SourceFactories(self)
        self._datasources: Dict[str, Datasource] = {}
        LOGGER.info(f"4a. Available Factories - {self._sources.factories}")
        LOGGER.info(f"4b. `type_lookup` mapping ->\n{pf(self._sources.type_lookup)}")

    @property
    def sources(self) -> _SourceFactories:
        return self._sources

    def _attach_datasource_to_context(self, datasource: Datasource) -> None:
        self._datasources[datasource.name] = datasource

    def get_datasource(self, datasource_name: str) -> Datasource:
        # NOTE: this same method exists on AbstractDataContext
        # TODO (kilo59): implement as __getitem__ ?
        return self._datasources[datasource_name]


def get_context(context_root_dir: Optional[DirectoryPath] = None) -> DataContext:
    """ZEP get_context placeholder function."""
    LOGGER.info(f"3. Getting context {context_root_dir or ''}")
    context = DataContext.get_context(context_root_dir=context_root_dir)
    return context