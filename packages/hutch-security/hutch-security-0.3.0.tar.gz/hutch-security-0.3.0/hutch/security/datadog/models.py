# Copyright (c) HashiCorp, Inc.
# SPDX-License-Identifier: MPL-2.0

"""Provides Datadog related models for data mapping."""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Extra


class EventSearchEntity(BaseModel, extra=Extra.allow):
    """Map event search log entries into native data types."""

    pass


class EventSearchPage(BaseModel, extra=Extra.forbid):
    """Map event search page information into native data types."""

    after: str


class EventSearchMeta(BaseModel, extra=Extra.forbid):
    """Map event search metadata into native data types."""

    page: Optional[EventSearchPage] = None
    status: str
    elapsed: int
    request_id: str


class EventSearchResult(BaseModel, extra=Extra.forbid):
    """Maps event search result into native data types."""

    data: Optional[List[EventSearchEntity]]
    meta: Optional[EventSearchMeta] = None
    links: Optional[Dict[str, Any]]
