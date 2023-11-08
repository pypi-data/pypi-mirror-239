# Copyright (c) HashiCorp, Inc.
# SPDX-License-Identifier: MPL-2.0

"""Provides Datadog related exceptions."""


class DatadogException(Exception):
    """A generic Datadog exception.

    All exceptions should inherit from this to allow for hierarchical handling.
    """
