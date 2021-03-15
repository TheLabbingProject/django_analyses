"""
Definition of the :class:`QuerySetRunner` class.
"""
import logging
from typing import Any, Dict, List, Tuple

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Model, QuerySet
from django_analyses.models.analysis import Analysis
from django_analyses.models.analysis_version import AnalysisVersion
from django_analyses.models.input.definitions.input_definition import (
    InputDefinition,
)
from django_analyses.models.pipeline.node import Node
from django_analyses.runner import messages
from django_analyses.tasks import execute_node
from django_analyses.utils.progressbar import create_progressbar

_LOGGER = logging.getLogger("analysis_exection")


class QuerySetRunner:
    """
    Base class for batch queryset processing.

    Example
    -------
    For a general usage example, see the :ref:`queryset-processing` section in
    the documentation.
    """

    #: QuerySet model.
    MODEL: Model = None

    #
    # Analysis Information and Configuration
    #
    ANALYSIS_TITLE: str = ""
    """
    Required :class:`~django_analyses.models.analysis.Analysis` instance title.
    """
    ANALYSIS_VERSION_TITLE: str = ""
    """
    Required :class:`~django_analyses.models.analysis.AnalysisVersion` instance
    title.
    """
    ANALYSIS_CONFIGURATION: dict = None
    """
    Common input specification dictionary as it is expected to be defined in
    the required :class:`~django_analyses.models.pipeline.node.Node`'s
    :attr:`~django_analyses.models.pipeline.node.Node.configuration` field. If
    none is provided, defaults to :attr:`_NO_CONFIGURATION`.
    """
    INPUT_KEY: str = ""
    """
    The associated :class:`~django_analyses.models.analysis.AnalysisVersion`
    instance's
    :class:`~django_analyses.models.input.definitions.input_definition.InputDefinition`
    which will be used to query pending runs and execute them.
    """

    #
    # Messages
    #
    BATCH_RUN_START: str = messages.BATCH_RUN_START
    DEFAULT_QUERYSET_QUERY: str = messages.DEFAULT_QUERYSET_QUERY
    DEFAULT_QUERYSET_REPORT: str = messages.DEFAULT_QUERYSET_REPORT
    EXECUTION_STARTED: str = messages.EXECUTION_STARTED
    FILTER_QUERYSET_START: str = messages.FILTER_QUERYSET_START
    INPUT_GENERATION: str = messages.INPUT_GENERATION
    INPUT_GENERATION_FINISHED: str = messages.INPUT_GENERATION_FINISHED
    INPUT_QUERY_START: str = messages.INPUT_QUERY_START
    INPUT_QUERY_END: str = messages.INPUT_QUERY_END
    NONE_PENDING: str = messages.NONE_PENDING
    NONE_PENDING_IN_QUERYSET: str = messages.NONE_PENDING_IN_QUERYSET
    NO_CANDIDATES: str = messages.NO_CANDIDATES
    PENDING_FOUND: str = messages.PENDING_FOUND
    PENDING_QUERY_START: str = messages.PENDING_QUERY_START
    PREPROCESSING_FAILURE: str = messages.PREPROCESSING_FAILURE
    PREPROCESSING_FAILURE_REPORT: str = messages.PREPROCESSING_FAILURE_REPORT

    #
    # Miscellaneous
    #
    INPUT_GENERATION_PROGRESSBAR_KWARGS: dict = {
        "unit": "instance",
        "desc": "Preparing inputs",
    }
    """
    A dictionary used for tqdm_ progressbar customization.

    .. _tqdm:
       https://github.com/tqdm/tqdm
    """

    _search: bool = False
    """
    Keeps track of whether a queryset was provided (False) or this is a full
    dataset search.
    """

    _input_set: QuerySet = None
    """
    Keep a cached version of the input set to prevent duplicate queries.
    """

    _NO_CONFIGURATION = {}
    """
    Empty configuration dictionary to copy if no :attr:`ANALYSIS_CONFIGURATION`
    is specified.
    """

    def filter_queryset(
        self, queryset: QuerySet, log_level: int = logging.INFO
    ) -> QuerySet:
        """
        Applies any custom filtering to the a given data model's queryset.

        Parameters
        ----------
        queryset : QuerySet
            A collection of the data model's instances
        log_level : int, optional
            Logging level to use, by default 20 (INFO)

        Returns
        -------
        QuerySet
            Fitered queryset
        """
        self.log_filter_start(log_level)
        return queryset

    def log_filter_start(self, log_level: int = logging.INFO) -> None:
        """
        Logs the beginning of queryset filtering prior to execution.

        Parameters
        ----------
        log_level : int, optional
            Logging level to use, by default 20 (INFO)
        """
        prefix = "" if self._search else "\n"
        message = prefix + self.FILTER_QUERYSET_START
        _LOGGER.log(log_level, message)

    def get_default_queryset(self, log_level: int = logging.INFO) -> QuerySet:
        """
        Returns the default data queryset for batch execution.

        Parameters
        ----------
        log_level : int, optional
            Logging level to use, by default 20 (INFO)

        Returns
        -------
        QuerySet
            Default batch execution data queryset
        """
        self.log_default_query_start(log_level=log_level)
        queryset = self.MODEL.objects.all()
        queryset = self.filter_queryset(queryset)
        self.log_default_query_end(queryset=queryset, log_level=log_level)
        return queryset

    def log_default_query_start(self, log_level: int = logging.INFO) -> None:
        """
        Log start of default execution queryset query.

        Parameters
        ----------
        log_level : int, optional
            Logging level to use, by default 20 (INFO)
        """
        start_message = self.DEFAULT_QUERYSET_QUERY
        _LOGGER.log(log_level, start_message)

    def log_default_query_end(
        self, queryset: QuerySet, log_level: int = logging.INFO
    ) -> None:
        """
        Log end of default execution queryset query.

        Parameters
        ----------
        queryset : QuerySet
            Detected execution candidates
        log_level : int, optional
            Logging level to use, by default 20 (INFO)
        """
        end_message = self.DEFAULT_QUERYSET_REPORT.format(
            n_candidates=queryset.count()
        )
        _LOGGER.log(log_level, end_message)

    def query_analysis(self) -> Analysis:
        """
        Returns the analysis to be executed.

        Returns
        -------
        Analysis
            Executed analysis
        """
        return Analysis.objects.get(title=self.ANALYSIS_TITLE)

    def query_analysis_version(self) -> AnalysisVersion:
        """
        Returns the analysis version to be executed.

        Returns
        -------
        AnalysisVersion
            Executed analysis version
        """
        return AnalysisVersion.objects.get(
            analysis=self.analysis, title=self.ANALYSIS_VERSION_TITLE
        )

    def create_configuration(self) -> dict:
        """
        Returns the configuration dictionary for the execution node.

        Returns
        -------
        dict
            Node configuration
        """
        configuration = (
            self._NO_CONFIGURATION
            if self.ANALYSIS_CONFIGURATION is None
            else self.ANALYSIS_CONFIGURATION
        )
        return configuration.copy()

    def get_or_create_node(self) -> Node:
        """
        Get or create the required execution node according to the specified
        analysis configuration.

        Returns
        -------
        Node
            Execution node
        """
        node, created = Node.objects.get_or_create(
            analysis_version=self.analysis_version,
            configuration=self.configuration,
        )
        return node

    def query_input_definition(self) -> InputDefinition:
        """
        Returns the input definition which corresponds to the queryset
        instances.

        Returns
        -------
        InputDefinition
            Instance input definition
        """
        return self.analysis_version.input_definitions.get(key=self.INPUT_KEY)

    def query_input_set(self, log_level: int = logging.DEBUG) -> QuerySet:
        """
        Returns a queryset of existing
        :class:`~django_analyses.models.input.input.Input` instances
        of the execution node.

        Parameters
        ----------
        log_level : int, optional
            Logging level to use, by default 20 (INFO)

        Returns
        -------
        QuerySet
            Existing inputs
        """
        # Log start.
        start_message = self.INPUT_QUERY_START
        _LOGGER.log(log_level, start_message)

        # Query.
        runs = self.node.run_set.all()
        inputs = self.input_definition.input_set.filter(run__in=runs)

        # Log end.
        end_message = self.INPUT_QUERY_END.format(n_existing=runs.count())
        _LOGGER.log(log_level, end_message)

        return inputs

    def get_instance_representation(self, instance: Model) -> Any:
        """
        Returns the representation of a single instance from the queryset as an
        :class:`~django_analyses.models.input.input.Input` instance's
        :attr:`~django_analyses.models.input.input.Input.value`.

        Parameters
        ----------
        instance : Model
            Instance to be represented as input value

        Returns
        -------
        Any
            Input value
        """
        return instance

    def has_run(self, instance: Model) -> bool:
        """
        Check whether the provided *instance* has an existing run in the
        databaes or not.

        Parameters
        ----------
        instance : Model
            Data instance to check

        Returns
        -------
        bool
            Whether the data instance has an existing run or not
        """
        value = self.get_instance_representation(instance)
        try:
            self.input_set.get(value=value)
        except ObjectDoesNotExist:
            return False
        else:
            return True

    def query_progress(
        self, queryset: QuerySet = None, log_level: int = logging.INFO,
    ) -> Tuple[QuerySet, QuerySet]:
        """
        Splits *queryset* to instances with and without existing runs.

        Parameters
        ----------
        queryset : QuerySet, optional
            Queryset to split by run status, by default None
        log_level : int, optional
            Logging level to use, by default 20 (INFO)

        Returns
        -------
        Tuple[QuerySet, QuerySet]
            Existing, Pending
        """
        # Log start.
        start_message = self.PENDING_QUERY_START
        _LOGGER.log(log_level, start_message)

        # Split to existing and pending.
        existing_ids = [
            instance.id for instance in queryset if self.has_run(instance)
        ]
        # A list comprehension is used here (rather than a query) because the
        # queryset can be a slice, in which case Django will raise an
        # AssertionError.
        pending_ids = [
            instance.id
            for instance in queryset
            if instance.id not in existing_ids
        ]
        # self.MODEL should be used rather than the queryset for the same
        # reason mentioned above.
        existing = self.MODEL.objects.filter(id__in=existing_ids)
        pending = self.MODEL.objects.filter(id__in=pending_ids)

        # Log end.
        if pending:
            self.log_pending(existing, pending)
        else:
            self.log_none_pending(queryset)

        return existing, pending

    def create_input_specification(self, instance: Model) -> dict:
        """
        Returns an input specification dictionary with the given data
        *instance* as input.

        Parameters
        ----------
        instance : Model
            Data instance to be proocessed

        Returns
        -------
        dict
            Input specification dictionary
        """
        try:
            return {self.INPUT_KEY: self.get_instance_representation(instance)}
        # Report and skip instances raising an exception.
        except RuntimeError:
            model_name = self.MODEL.__name__
            message = self.PREPROCESSING_FAILURE.format(
                model_name=model_name, instance_id=instance.id
            )
            _LOGGER.warning(message)

    def create_inputs(
        self, queryset: QuerySet, progressbar: bool = True
    ) -> List[Dict[str, List[str]]]:
        """
        Returns a list of dictionary input specifications.

        Parameters
        ----------
        instances : QuerySet
            Batch of instances to run the analysis over
        progressbar : bool, optional
            Whether to display a progressbar, by default True

        Returns
        -------
        List[Dict[str, List[str]]]
            Input specifications
        """
        _LOGGER.info(self.INPUT_GENERATION)
        # Generate input specifications.
        iterable = create_progressbar(
            queryset,
            disable=not progressbar,
            **self.INPUT_GENERATION_PROGRESSBAR_KWARGS
        )
        inputs = [
            self.create_input_specification(instance) for instance in iterable
        ]
        # Report instances that could not be preprocessed.
        n_invalid = inputs.count(None)
        if n_invalid:
            model_name = self.MODEL.__name__
            message = self.PREPROCESSING_FAILURE_REPORT.format(
                n_invalid=n_invalid, n_total=len(inputs), model_name=model_name
            )
            _LOGGER.warning(message)
        # Return `None`-filtered input specifications.
        inputs = [
            specification
            for specification in inputs
            if specification is not None
        ]
        end_message = self.INPUT_GENERATION_FINISHED.format(
            n_inputs=len(inputs)
        )
        _LOGGER.info(end_message)
        return inputs

    def run(
        self,
        queryset: QuerySet = None,
        max_total: int = None,
        prep_progressbar: bool = True,
        log_level: int = logging.INFO,
        dry: bool = False,
    ):
        """
        Execute this class's :attr:`node` in batch over all data instances in
        *queryset*. If none provided, queries a default execution queryset.

        Parameters
        ----------
        queryset : QuerySet, optional
            Queryset to run, by default None
        max_total : int, optional
            Maximal total number of runs, by default None
        prep_progressbar : bool, optional
            Whether to display a progressbar for input generation, by default
            True
        log_level : int, optional
            Logging level to use, by default 20 (INFO)
        dry : bool, optional
            Whether this is a dry run (no execution) or not, by default False

        See Also
        --------
        :func:`get_default_queryset`
        """
        # Log start.
        start_message = self.BATCH_RUN_START.format(
            analysis_version=self.analysis_version
        )
        _LOGGER.log(log_level, start_message)

        # Modify/generate queryset.
        self._search = queryset is None
        queryset = (
            self.get_default_queryset(log_level=log_level)
            if self._search
            else self.filter_queryset(queryset)
        )
        existing, pending = self.query_progress(queryset, log_level=log_level)

        # Generate input specifications and execute.
        if pending:
            inputs = self.create_inputs(pending, prep_progressbar)
            inputs = inputs[:max_total]
            if inputs:
                if not dry:
                    execute_node.delay(node_id=self.node.id, inputs=inputs)
                self.log_execution_start(n_instances=len(inputs))

    def log_execution_start(
        self, n_instances: int, log_level: int = logging.INFO
    ) -> None:
        """
        Log the start of a batch execution over some queryset.

        Parameters
        ----------
        n_instances : int
            Number of instances in the queryset
        log_level : int, optional
            Logging level to use, by default 20 (INFO)
        """
        model_name = self.MODEL.__name__
        start_message = self.EXECUTION_STARTED.format(
            analysis_version=self.analysis_version,
            n_instances=n_instances,
            model_name=model_name,
        )
        _LOGGER.log(log_level, start_message)

    def log_none_pending(
        self, queryset: QuerySet, log_level: int = logging.INFO
    ) -> None:
        """
        Log an empty queryset of pending instances.

        Parameters
        ----------
        queryset : QuerySet
            Provided or generated execution queryset
        log_level : int, optional
            Logging level to use, by default 20 (INFO)
        """
        model_name = self.MODEL.__name__

        # In cases where to data queryset was provided by the user:
        # * Handle no pending scans seem to be found in the entire database.
        if self._search and queryset:
            message = self.NONE_PENDING.format(model_name=model_name)
        # * Handle no execution candidates were found in the entire database.
        elif self._search:
            message = self.NO_CANDIDATES.format(model_name=model_name)

        # In cases where a queryset was provided and no pending scans were
        # found:
        else:
            message = self.NONE_PENDING_IN_QUERYSET.format(
                model_name=model_name, n_instances=queryset.count(),
            )

        _LOGGER.log(log_level, message)

    def log_pending(
        self,
        existing: QuerySet,
        pending: QuerySet,
        log_level: int = logging.INFO,
    ) -> None:
        """
        Log the number of pending  vs. existing instances.

        Parameters
        ----------
        pending : QuerySet
            Instances with existing runs
        pending : QuerySet
            Instances pending execution
        log_level : int, optional
            Logging level to use, by default 20 (INFO)
        """
        message = self.PENDING_FOUND.format(n_pending=pending.count())
        _LOGGER.log(log_level, message)

    @property
    def analysis(self) -> Analysis:
        """
        Returns the required analysis.

        Returns
        -------
        Analysis
            Analysis to be executed

        See Also
        --------
        :func:`query_analysis`
        """
        return self.query_analysis()

    @property
    def analysis_version(self) -> AnalysisVersion:
        """
        Returns the required analysis version.

        Returns
        -------
        AnalysisVersion
            Analysis version to be executed

        See Also
        --------
        :func:`query_analysis_version`
        """
        return self.query_analysis_version()

    @property
    def node(self) -> Node:
        """
        Returns the required execution node.

        Returns
        -------
        Node
            Node to be executed

        See Also
        --------
        :func:`get_or_create_node`
        """
        return self.get_or_create_node()

    @property
    def input_definition(self) -> InputDefinition:
        """
        Returns the data instance's matching input definition.

        Returns
        -------
        InputDefinition
            Data instance input definition

        See Also
        --------
        :func:`query_input_definition`
        """
        return self.query_input_definition()

    @property
    def input_set(self) -> QuerySet:
        """
        Returns a queryset of existing
        :class:`~django_analyses.models.input.input.Input` instances
        for the executed node.

        Returns
        -------
        QuerySet
            Existing inputs

        See Also
        --------
        :func:`query_input_set`
        """
        if self._input_set is None:
            self._input_set = self.query_input_set()
        return self._input_set

    @property
    def configuration(self) -> dict:
        """
        Returns the configuration dictionary for the execution node.

        Returns
        -------
        dict
            Node configuration

        See Also
        --------
        :func:`create_configuration`
        """
        return self.create_configuration()
