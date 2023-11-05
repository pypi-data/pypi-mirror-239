import argparse
import os
import sys

import isort
from gitbetter import Git
from pathier import Pathier

from hassle import hassle_utilities
from hassle.generate_tests import generate_test_files
from hassle.run_tests import run_tests

root = Pathier(__file__).parent


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "package",
        type=str,
        default=".",
        nargs="?",
        help=""" The name of the package or project to use,
        assuming it's a subfolder of your current working directory.
        Can also be a full path to the package. If nothing is given,
        the current working directory will be used.""",
    )

    parser.add_argument(
        "-b", "--build", action="store_true", help=""" Build the package. """
    )

    parser.add_argument(
        "-t",
        "--tag_version",
        action="store_true",
        help=""" Add a git tag corresponding to the version in pyproject.toml. """,
    )

    parser.add_argument(
        "-i",
        "--install",
        action="store_true",
        help=""" Install the package from source. """,
    )

    parser.add_argument(
        "-iv",
        "--increment_version",
        type=str,
        default=None,
        choices=["major", "minor", "patch"],
        help=""" Increment version in pyproject.toml.
        Can be one of "major", "minor", or "patch". """,
    )

    parser.add_argument(
        "-p",
        "--publish",
        action="store_true",
        help=""" Publish package to PyPi.
        Note: You must have configured twine 
        and registered a PyPi account/generated an API
        key to use this option.""",
    )

    parser.add_argument(
        "-rt",
        "--run_tests",
        action="store_true",
        help=""" Run tests for the package. """,
    )

    parser.add_argument(
        "-gt",
        "--generate_tests",
        action="store_true",
        help=""" Generate tests for the package. """,
    )

    parser.add_argument(
        "-uc",
        "--update_changelog",
        action="store_true",
        help=""" Update changelog file. """,
    )

    parser.add_argument(
        "-od",
        "--overwrite_dependencies",
        action="store_true",
        help=""" When building a package, packagelister will be used
        to update the dependencies list in pyproject.toml.
        The default behavior is to append any new dependencies to
        the current list so as not to erase any manually added dependencies
        that packagelister may not detect. If you don't have any manually 
        added dependencies and want to remove any dependencies that your
        project no longer uses, pass this flag.""",
    )

    parser.add_argument(
        "-ca",
        "--commit_all",
        type=str,
        default=None,
        help=""" Git stage and commit all tracked files with this supplied commit message.
        If 'build' is passed, all commits will have message: 'chore: build v{current_version}""",
    )

    parser.add_argument(
        "-s",
        "--sync",
        action="store_true",
        help=""" Pull from github, then push current commit to repo. """,
    )

    parser.add_argument(
        "-dv",
        "--dependency_versions",
        action="store_true",
        help=""" Include version specifiers for dependencies in
        pyproject.toml.""",
    )

    parser.add_argument(
        "-up",
        "--update",
        type=str,
        default=None,
        choices=["major", "minor", "patch"],
        help=""" Expects one argument: "major", "minor", or "patch".
        Passing "-up minor" is equivalent to passing "--build --tag_version --increment_version minor --update_changelog --commit_all build --sync".
        To publish the updated package, the -p/--publish switch needs to be added to the cli input.
        To install the updated package, the -i/--install switch also needs to be added.""",
    )

    parser.add_argument(
        "-st",
        "--skip_tests",
        action="store_true",
        help=""" Don't run tests when using the -b/--build command. """,
    )

    parser.add_argument(
        "-ip",
        "--is_published",
        action="store_true",
        help=""" Check that the version number in `pyproject.toml` and `pypi.org/project/{project_name}` agree. """,
    )

    args = parser.parse_args()

    args.package = Pathier(args.package).resolve()

    if args.update:
        args.build = True
        args.tag_version = True
        args.increment_version = args.update
        args.update_changelog = True
        args.commit_all = "build"
        args.sync = True

    if args.increment_version and args.increment_version not in [
        "major",
        "minor",
        "patch",
    ]:
        raise ValueError(
            f"Invalid option for -iv/--increment_version: {args.increment_version}"
        )

    if args.commit_all == "":
        raise ValueError("Commit message for args.commit_all cannot be empty.")

    if args.publish and not hassle_utilities.on_primary_branch():
        print(
            "WARNING: You are trying to publish a project that does not appear to be on its main branch."
        )
        choice = input("Continue? (y/n) ")
        if choice != "y":
            print("Quitting hassle.")
            sys.exit()

    return args


def build(
    package_dir: Pathier,
    skip_tests: bool = False,
    overwrite_dependencies: bool = False,
    increment_version: str | None = None,
):
    """Perform the build process.

    Steps:
    * Run tests (unless `skip_tests` is `True`)
    * Raise error and abandon build if tests fail
    * Format source code with `Black`
    * Sort source code imports with `isort`
    * Update project dependencies in `pyproject.toml`
    * Increment version in `pyproject.toml` if `increment_version` supplied
    * Generate docs
    * Delete previous `dist` folder contents
    * Invoke build module"""
    if not skip_tests and not run_tests(package_dir):
        raise RuntimeError(
            f"ERROR: {package_dir.stem} failed testing.\nAbandoning build."
        )
    hassle_utilities.format_files(package_dir)
    [isort.file(path) for path in package_dir.rglob("*.py")]
    hassle_utilities.update_dependencies(
        package_dir / "pyproject.toml", overwrite_dependencies
    )
    if increment_version:
        hassle_utilities.increment_version(
            package_dir / "pyproject.toml", increment_version
        )
    # Vermin isn't taking into account the minimum version of dependencies.
    # Removing from now and defaulting to >=3.10
    # hassle_utilities.update_minimum_python_version(pyproject_path)
    hassle_utilities.generate_docs(package_dir)
    (package_dir / "dist").delete()
    os.system(f"{sys.executable} -m build {package_dir}")


def main(args: argparse.Namespace = None):
    if not args:
        args = get_args()

    pyproject_path = args.package / "pyproject.toml"
    args.package.mkcwd()

    git = Git()

    if not pyproject_path.exists():
        raise FileNotFoundError(f"Could not locate pyproject.toml for {args.package}")

    if args.generate_tests:
        generate_test_files(args.package)

    if args.run_tests:
        run_tests(args.package)

    if args.build:
        build(
            args.package,
            args.skip_tests,
            args.overwrite_dependencies,
            args.increment_version,
        )

    if args.increment_version and not args.build:
        hassle_utilities.increment_version(pyproject_path, args.increment_version)

    if args.commit_all:
        if args.commit_all == "build":
            version = pyproject_path.loads()["project"]["version"]
            args.commit_all = f"chore: build v{version}"
        git.add_all()
        git.commit(f'-m "{args.commit_all}"')

    if args.tag_version:
        hassle_utilities.tag_version(args.package)

    if args.update_changelog:
        hassle_utilities.update_changelog(pyproject_path)
        if args.tag_version:
            with git.capturing_output():
                tags = git.tag("--sort=-committerdate").stdout
                most_recent_tag = tags[: tags.find("\n")]
                git.tag(f"-d {most_recent_tag}")
        input("Press enter to continue after manually adjusting the changelog...")
        with git.capturing_output():
            status = git.status().stdout
            if -1 < status.find("Untracked files") < status.find("CHANGELOG.md"):
                git.add_files([(args.package / "CHANGELOG.md")])
        git.commit_files([args.package / "CHANGELOG.md"], "chore: update changelog")
        if args.tag_version:
            with git.capturing_output():
                git.tag(most_recent_tag)

    if args.publish:
        os.system(f"twine upload {args.package / 'dist' / '*'}")

    if args.install:
        os.system(
            f"{sys.executable} -m pip install {args.package} --no-deps --upgrade --no-cache-dir"
        )

    if args.sync:
        git.pull(f"origin {git.current_branch} --tags")
        git.push(f"origin {git.current_branch} --tags")

    if args.is_published:
        is_published = hassle_utilities.latest_version_is_published(
            args.package / "pyproject.toml"
        )
        if is_published:
            print("The most recent version of this package has been published.")
        else:
            print("The most recent version of this package has not been published.")


if __name__ == "__main__":
    main(get_args())
