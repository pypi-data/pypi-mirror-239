from __future__ import annotations

import abc
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from request_mapper.types import IncomingMappedData, RequestMapperDecorator


class RequestMapperIntegration(abc.ABC):
    """Base class for integrations."""

    @abc.abstractmethod
    def set_up(self, request_mapper_decorator: RequestMapperDecorator) -> None:
        """Initialize the integration. Map views, error handlers and perform tasks as necessary."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_query_as_dict(self) -> IncomingMappedData:
        """Return the current request query data as a mapping."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_request_body_as_dict(self) -> IncomingMappedData:
        """Return the current request body as a mapping."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_form_data_as_dict(self) -> IncomingMappedData:
        """Return current request's form data as a mapping."""
        raise NotImplementedError
