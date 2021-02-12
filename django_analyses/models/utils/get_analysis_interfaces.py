"""
Utility functions for analysis version interfaces retrieval.
"""
from django.conf import settings

NO_INTERFACES = (
    "Failed to find ANALYSIS_INTERFACES dictionary in project settings!"
)
MISSING_INTERFACE = "No interface detected for {analysis_version}!"


def get_analysis_interfaces() -> dict:
    try:
        return settings.ANALYSIS_INTERFACES
    except AttributeError:
        raise RuntimeError(NO_INTERFACES)


def get_analysis_version_interface(analysis_version) -> type:
    analysis_title = analysis_version.analysis.title
    try:
        interfaces = get_analysis_interfaces()
        return interfaces[analysis_title][analysis_version.title]
    except KeyError:
        message = MISSING_INTERFACE.format(analysis_version=analysis_version)
        raise NotImplementedError(message)
