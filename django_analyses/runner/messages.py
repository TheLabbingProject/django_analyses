"""
Default logs and messages for the
:class:`~django_analyses.runner.queryset_runner.QuerySetRunner` class.
"""


class bcolors:
    """
    ANSI escape sequences used for text formatting.

    References
    ----------
    * https://stackoverflow.com/a/287944/4416932
    """

    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


#: Batch run start messsage.
BATCH_RUN_START = f"{bcolors.UNDERLINE}{bcolors.HEADER}{bcolors.BOLD}{{analysis_version}}{bcolors.ENDC}{bcolors.UNDERLINE}{bcolors.HEADER}: Batch Execution{bcolors.ENDC}"

#: Report querying default execution queryset.
DEFAULT_QUERYSET_QUERY = f"\n🔎 {bcolors.OKBLUE}Default execution queryset generation:\n{bcolors.ENDC}Querying execution candidates..."

#: Report default queryset query result.
DEFAULT_QUERYSET_REPORT = "{n_candidates} execution candidates found."

#: Report the successful creation of an asynchronous execution task.
EXECUTION_STARTED = f"\n{bcolors.OKGREEN}🚀Successfully started {{analysis_version}} execution over {{n_instances}} {{model_name}} instances🚀{bcolors.ENDC}"

#: Filter queryset start.
FILTER_QUERYSET_START = "Filtering queryset..."

#: Reporting starting to generate input specifications for analysis execution.
INPUT_GENERATION = (
    f"\n🔀 {bcolors.OKBLUE}Generating input specifications:{bcolors.ENDC}"
)

INPUT_GENERATION_FINISHED = "{n_inputs} input specifications prepared."

#: Report querying existing input instances.
INPUT_QUERY_START = "Querying existing runs..."

#: Report number of existing input instances.
INPUT_QUERY_END = "{n_existing} runs found."

#: No pending instances were detected in the database.
NONE_PENDING = f"{bcolors.OKGREEN}Congratulations! No pending {{model_name}} instances were detected in the database 👏{bcolors.ENDC}"

#: No pending instances were detected in the provided queryset.
NONE_PENDING_IN_QUERYSET = f"{bcolors.OKGREEN}All {{n_instances}} provided {{model_name}} instances have been processed already 👑{bcolors.ENDC}"

#: No candidates in execution queryset.
NO_CANDIDATES = f"{bcolors.WARNING}No execution candidates detected in {{model_name}} queryset!{bcolors.ENDC}"

#: Report pending instances.
PENDING_FOUND = "{n_pending} instances pending execution."

#: Report starting a queryset existing/pending split.
PENDING_QUERY_START = f"\n⚖  {bcolors.OKBLUE}Checking execution status for the input queryset:\n{bcolors.ENDC}Filtering existing runs..."

#: General input preprocessing failure message.
PREPROCESSING_FAILURE = f"{bcolors.WARNING}Failed to preprocess {{model_name}} #{{instance_id}}!{bcolors.ENDC}"

#: Report number of preprocessing failures encountered.
PREPROCESSING_FAILURE_REPORT = f"{bcolors.WARNING}{bcolors.BOLD}{{n_invalid}} of {{n_total}} {{model_name}} instances failed to be preprocessed for input generation.{bcolors.ENDC}"

# flake8: noqa: E501
