from django.conf import settings
from django_analyses.models.analysis_version import AnalysisVersion
from django_analyses.utils import messages


def get_visualizers() -> dict:
    return getattr(settings, "ANALYSIS_VISUALIZERS", {})


def get_visualizer(
    analysis_version: AnalysisVersion, provider: str = None
) -> callable:
    visualizers = get_visualizers()
    analysis_title = analysis_version.analysis.title
    analysis_visualizers = visualizers.get(analysis_title, {})
    analysis_version_title = analysis_version.title
    analysis_version_visualizers = analysis_visualizers.get(
        analysis_version_title, {}
    )
    if analysis_version_visualizers:
        provider_dict = isinstance(analysis_version_visualizers, dict)
        if provider_dict and provider:
            try:
                return analysis_version_visualizers[provider]
            except KeyError:
                message = messages.UNREGISTERED_VISUALIZATION_PROVIDER.format(
                    provider=provider, analysis_version=analysis_version,
                )
                raise NotImplementedError(message)
        elif provider_dict:
            providers = list(analysis_version_visualizers.keys())
            message = messages.MISSING_VISUALIZATION_PROVIDER.format(
                analysis_version=analysis_version, providers=providers,
            )
        elif isinstance(analysis_version_visualizers, callable):
            return analysis_version_visualizers
    message = messages.VISUALIZER_NOT_IMPLEMENTED.format(
        analysis_version=analysis_version
    )
    raise NotImplementedError(message)
