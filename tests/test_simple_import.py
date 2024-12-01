from pathlib import Path

from pyrepa import analyze_project


def test_analyze_project():
    expected_dependencies = {
        ("tests.sample_project.main.main", "secondary.helper"),
    }

    path = Path("tests/sample_project")
    dependencies = analyze_project(path)
    assert len(dependencies) == len(expected_dependencies)
    assert set(dependencies) == expected_dependencies
