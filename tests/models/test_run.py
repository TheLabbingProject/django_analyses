from django.conf import settings
from django.test import TestCase
from pathlib import Path
from tests.factories.input.types.string_input import StringInputFactory
from tests.factories.run import RunFactory


class RunTestCase(TestCase):
    """
    Tests for the :class:`~django_analyses.models.run.Run` model.

    """

    def setUp(self):
        """
        Adds the created instances to the tests' contexts.
        For more information see unittest's :meth:`~unittest.TestCase.setUp` method.

        """

        self.run = RunFactory()
        self.string_input = StringInputFactory(run=self.run)
        # TODO: Create factories for input and output types and call them
        # here so that run has some to test with.

    ########
    # Meta #
    ########

    ###########
    # Methods #
    ###########

    def test_string(self):
        expected = (
            f"#{self.run.id} {self.run.analysis_version} run from {self.run.created}"
        )
        value = str(self.run)
        self.assertEqual(value, expected)

    ##############
    # Properties #
    ##############

    def test_input_defaults(self):
        value = self.run.input_defaults
        expected = self.run.analysis_version.input_specification.default_configuration
        self.assertDictEqual(value, expected)

    def test_input_configuration(self):
        value = self.run.input_configuration
        expected = self.run.input_defaults.copy()
        expected.update(self.run.raw_input_configuration)
        self.assertDictEqual(value, expected)

    def test_input_set(self):
        value = self.run.input_set
        expected = self.run.base_input_set.select_subclasses()
        self.assertQuerysetEqual(value, expected, transform=lambda x: x)
        # The 'transform' kwargs was added because of the problem explained here:
        # https://stackoverflow.com/a/49129560/4416932

    def test_output_set(self):
        value = self.run.output_set
        expected = self.run.base_output_set.select_subclasses()
        self.assertQuerysetEqual(value, expected, transform=lambda x: x)
        # The 'transform' kwargs was added because of the problem explained here:
        # https://stackoverflow.com/a/49129560/4416932

    def test_output_configuration(self):
        value = self.run.output_configuration
        expected = {output.key: output.value for output in self.run.output_set}
        self.assertDictEqual(value, expected)

    def test_raw_input_configuration(self):
        self.string_input.definition.is_output_path = True
        self.string_input.definition.save()
        self.string_input.value = Path(settings.MEDIA_ROOT) / "name.ext"
        self.string_input.save()
        value = self.run.raw_input_configuration
        expected = {self.string_input.key: "name.ext"}
        self.assertDictEqual(value, expected)
