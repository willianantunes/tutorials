import requests

from django.core.management import CommandError
from django.core.management.base import BaseCommand
from github import Github
from sonarqube import SonarCloudClient
from sonarqube.utils.exceptions import ValidationError


class Command(BaseCommand):
    help = "Add repository on Sonar Cloud"

    def add_arguments(self, parser):
        parser.add_argument(
            "--repository-name",
            required=True,
            type=str,
            help="The target repository",
        )
        parser.add_argument(
            "--github-access-token",
            type=str,
            required=True,
            help="The access token to call GitHub API",
        )
        parser.add_argument(
            "--sonar-cloud-access-token",
            type=str,
            required=True,
            help="The access token to call GitHub API",
        )
        parser.add_argument(
            "--installation-id",
            type=int,
            required=True,
            help="The installation ID of the SonarCloud App in your organization",
        )

    def handle(self, *args, **options):
        self.repository_name = options["repository_name"]
        self.github_access_token = options["github_access_token"]
        self.sonar_cloud_access_token = options["sonar_cloud_access_token"]
        self.installation_id = options["installation_id"]

        self.stdout.write(f"Retrieving repository ID given the parameter: {self.repository_name}")
        # PAT required scopes: repo, write:org, read:org
        github_api = Github(self.github_access_token)
        repository = github_api.get_repo(self.repository_name)
        repository_id = repository.id

        # This is not available in GitHub Python Library
        self.stdout.write(f"Adding the repository {self.repository_name} to installation ID {self.installation_id}")
        headers = {"Authorization": f"token {self.github_access_token}", "Accept": "application/vnd.github.v3+json"}
        url = f"https://api.github.com/user/installations/{self.installation_id}/repositories/{repository_id}"
        result = requests.put(url, headers=headers)

        status_code = result.status_code
        if status_code not in [204, 304]:
            error_message = result.json()["message"]
            raise CommandError(f"Something went wrong! Message given status code {status_code}: {error_message}")
        self.stdout.write("It's okay on Github!")

        organization_key = repository.organization.login
        repository_name = repository.name
        project_key = f"{organization_key}_{repository_name}"
        self.stdout.write(f"Adding project {project_key} on SonarCloud")
        sonar = SonarCloudClient("https://sonarcloud.io/", token=self.sonar_cloud_access_token)
        try:
            sonar.projects.create_project(
                project=project_key,
                name=repository_name,
                organization=organization_key,
            )
        except ValidationError as e:
            treatable_error = "could not create project, key already exists"
            if treatable_error not in str(e).lower():
                raise e
            else:
                self.stdout.write(f"Project {project_key} already exists on Sonar Cloud")
        self.stdout.write("Done!")
