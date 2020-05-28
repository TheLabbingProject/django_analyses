Integration Customization
=========================


The :class:`~django_analyses.models.analysis_version.AnalysisVersion` model offers
three special fields that may be used to customize an instance's integration with
its interface:

* :attr:`~django_analyses.models.analysis_version.AnalysisVersion.run_method_key`:
  :obj:`str` determining the name of the interface's method that will be called when
  executing. By default this will be set to *"run"*.

* :attr:`~django_analyses.models.analysis_version.AnalysisVersion.fixed_run_method_kwargs`:
  :obj:`dict` of fixed keyword arguments to pass to the interface's :meth:`run` method
  when called. By default this will be set to :attr:`{}`.

* :attr:`~django_analyses.models.analysis_version.AnalysisVersion.nested_results_attribute`:
  :obj:`str` specifying a nested attribute or method to be called on a returned object to
  retrieve a :obj:`dict` of the results. By default this will be set to :obj:`None`.
