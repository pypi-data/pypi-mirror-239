from __future__ import unicode_literals
from click import ClickException


class MdDocsException(ClickException):
    """Base exceptions for all MdDocs Exceptions"""


class ConfigurationError(MdDocsException):
    """Error in configuration"""
