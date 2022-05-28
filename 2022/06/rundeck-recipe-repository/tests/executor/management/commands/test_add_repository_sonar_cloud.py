import unittest

from io import StringIO

import pytest

from django.core.management import CommandError
from django.core.management import call_command


class TestAddRepositorySonarCloud:
    def test_should_raise_error_given_missing_arguments(self):
        with pytest.raises(CommandError) as error:
            # Act
            call_command("add_repository_sonar_cloud")
        # Assert
        expected_message = "Error: the following arguments are required: --repository-name, --github-access-token, --sonar-cloud-access-token, --installation-id"
        assert str(error.value) == expected_message

    @unittest.skip("This is supposed to be executed manually")
    def test_should_add_repository(self):
        # Arrange
        repository_name = "raveofphonetics/test-2"
        github_access_token = "YOUR_github_access_token"
        sonar_cloud_access_token = "YOUR_sonar_cloud_access_token"
        installation_id = "26030682"
        out = StringIO()
        # Act
        call_command(
            "add_repository_sonar_cloud",
            "--repository-name",
            repository_name,
            "--github-access-token",
            github_access_token,
            "--sonar-cloud-access-token",
            sonar_cloud_access_token,
            "--installation-id",
            installation_id,
            stdout=out,
        )
        # Assert
        expected_project_key = "_".join(repository_name.split("/"))
        assert (
            out.getvalue() == f"Retrieving repository ID given the parameter: {repository_name}\n"
            f"Adding the repository {repository_name} to installation ID 26030682\n"
            "It's okay on Github!\n"
            f"Adding project {expected_project_key} on SonarCloud\n"
            f"Project {expected_project_key} already exists on Sonar Cloud\n"
            "Done!\n"
        )
