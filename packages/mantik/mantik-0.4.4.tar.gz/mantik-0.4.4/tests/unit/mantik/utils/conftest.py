import pathlib

import pytest

import mantik.unicore as unicore

FILE_DIR = pathlib.Path(__file__).parent


@pytest.fixture(scope="function")
def example_config() -> unicore.config.core.Config:
    return unicore.config.core.Config(
        api_url="test-url",
        user="user",
        password="password",
        project="test-project",
        environment=unicore.config.environment.Environment(
            execution=unicore.config.executable.Apptainer(
                path=pathlib.Path("mantik-test.sif"),
            )
        ),
        resources=unicore.config.resources.Resources(queue="batch"),
        exclude=["*.sif"],
    )


@pytest.fixture()
def example_project_path() -> pathlib.Path:
    return FILE_DIR / "../../../resources/test-project"
