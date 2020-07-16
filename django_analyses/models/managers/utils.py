from django_analyses.models.managers import messages


def get_analysis_version_string_id(definition: dict) -> str:
    try:
        return definition["analysis_version"]
    except KeyError:
        message = messages.NODE_DEFINITION_MISSING_ANALYSIS_VERSION.format(
            definition=definition
        )
        raise KeyError(message)
