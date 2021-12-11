from typing import Dict, Union

from django.conf import settings

OUTPUT_PARSERS_SETTING_KEY: str = "ANALYSIS_OUTPUT_PARSERS"
DEFAULT_OUTPUT_PARSERS = {}


def get_output_parsers() -> Dict[str, Union[Dict[str, object], object]]:
    """
    Returns output parsers defined in the project's settings, or the default
    MRI output parsers if none are set.

    Returns
    -------
    Dict[str, Union[Dict[str, object], object]]
        A dictionary mapping analysis titles to either an object that is meant
        to be initialized with a run path, or a dictionary of version titles
        and such objects
    """
    return getattr(
        settings, OUTPUT_PARSERS_SETTING_KEY, DEFAULT_OUTPUT_PARSERS
    )


def get_output_parser(
    analysis_title: str, analysis_version_title: str = None
) -> Union[object, Dict[str, object]]:
    """
    Get the run output parser for a particular analysis version, the general
    output parser of an analysis, or a dictionary mapping analysis versions to
    output parser objects (if *analysis_version_title* is None).

    Parameters
    ----------
    analysis_title : str
        Analysis instance title
    analysis_version_title : str, optional
        Analysis version title, by default None

    Returns
    -------
    Union[object, Dict[str, object]]
        Analysis or analysis version parser, or a dictionary of analysis
        versions and the corresponding parsers
    """
    output_parsers = get_output_parsers()
    try:
        analysis_parsers = output_parsers[analysis_title]
    except KeyError:
        pass
    else:
        if (
            isinstance(analysis_parsers, dict)
            and analysis_version_title is not None
        ):
            try:
                return analysis_parsers[analysis_version_title]
            except KeyError:
                pass
        return analysis_parsers
