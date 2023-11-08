# Copyright (c) HashiCorp, Inc.
# SPDX-License-Identifier: MPL-2.0

"""Provides a Datadog log events API client."""

import datetime

import requests

from hutch.security.datadog.constants import API_ENDPOINT
from hutch.security.datadog.exceptions import DatadogException
from hutch.security.datadog.models import EventSearchResult


class Client:
    """Implements a basic Datadog log events API client."""

    def __init__(self, api_key: str, app_key: str):
        """Initialise a Datadog query client.

        :param api_key: The Datadog API key to authenticate with.
        :param app_key: The Datadog application key to authenticate with.
        """
        self.base_url = f"{API_ENDPOINT}/logs/events"
        self.headers = {
            "Content-Type": "application/json",
            "DD-API-KEY": api_key,
            "DD-APPLICATION-KEY": app_key,
        }

    def _search(
        self,
        start: datetime.datetime,
        end: datetime.datetime,
        query: str,
        cursor: str = None,
        limit: int = 1000,
    ) -> EventSearchResult:
        """Performs a Datadog log events search, returning the results.

        If a pagination token (cursor) is provided, it will be included in the request.

        :param start: A datetime object expressing the start of the search window.
        :param end: A datetime object expressing the end of the search window.
        :param query: The query to use when searching Datadog.
        :param cursor: An optional cursor to use to request the next page of results.
        :param limit: An optional limit for the number of results to return per page.
        """
        # Construct pagination data.
        page = {"limit": limit}
        if cursor:
            page["cursor"] = cursor

        try:
            response = requests.post(
                f"{self.base_url}/search",
                headers=self.headers,
                json={
                    "filter": {
                        "from": start.isoformat(timespec="seconds"),
                        "to": end.isoformat(timespec="seconds"),
                        "query": query,
                    },
                    "page": page,
                },
                timeout=60,
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as err:
            raise DatadogException(err)

        data = response.json()
        return EventSearchResult(
            links=data.get("links"),
            meta=data.get("meta"),
            data=data.get("data"),
        )

    def search(
        self,
        start: datetime.datetime,
        end: datetime.datetime,
        query: str,
    ) -> EventSearchResult:
        """Performs a Datadog search, returning all possible results using a generator.

        :param start: A datetime object expressing the start of the search window.
        :param end: A datetime object expressing the end of the search window.
        :param query: The query to use when searching Datadog.
        """
        result = self._search(start, end, query)

        # Yield all data as it is returned.
        while hasattr(result.meta.page, "after") and result.meta.page.after:
            yield result

            result = self._search(
                start=start,
                end=end,
                query=query,
                cursor=result.meta.page.after,
            )

        # Handle the final page.
        yield result
