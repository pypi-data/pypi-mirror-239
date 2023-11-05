import argparse
import os
import sys
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from gitbetter import Git
from pathier import Pathier

import hassle.hassle_config as hassle_config
from hassle.generate_tests import generate_test_files

root = Pathier(__file__).parent


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "name",
        type=str,
        help=""" Name of the package to create in the current working directory. """,
    )

    parser.add_argument(
        "-s",
        "--source_files",
        nargs="*",
        type=str,
        default=[],
        help=""" List of additional source files to create in addition to the default
        __init__.py and {name}.py files.""",
    )

    parser.add_argument(
        "-d",
        "--description",
        type=str,
        default="",
        help=""" The package description to be added to the pyproject.toml file. """,
    )

    parser.add_argument(
        "-dp",
        "--dependencies",
        nargs="*",
        type=str,
        default=[],
        help=""" List of dependencies to add to pyproject.toml.
        Note: hassle.py will automatically scan your project for 3rd party
        imports and update pyproject.toml. This switch is largely useful
        for adding dependencies your project might need, but doesn't
        directly import in any source files,
        like an os.system() call that invokes a 3rd party cli.""",
    )

    parser.add_argument(
        "-k",
        "--keywords",
        nargs="*",
        type=str,
        default=[],
        help=""" List of keywords to be added to the keywords field in pyproject.toml. """,
    )

    parser.add_argument(
        "-as",
        "--add_script",
        action="store_true",
        help=""" Add section to pyproject.toml declaring the package 
        should be installed with command line scripts added. 
        The default is '{name} = "{name}.{name}:main".
        You will need to manually change this field.""",
    )

    parser.add_argument(
        "-nl",
        "--no_license",
        action="store_true",
        help=""" By default, projects are created with an MIT license.
        Set this flag to avoid adding a license if you want to configure licensing
        at another time.""",
    )

    parser.add_argument(
        "-os",
        "--operating_system",
        type=str,
        default=None,
        nargs="*",
        help=""" List of operating systems this package will be compatible with.
        The default is OS Independent.
        This only affects the 'classifiers' field of pyproject.toml .""",
    )

    parser.add_argument(
        "-np",
        "--not_package",
        action="store_true",
        help=""" Put source files in top level directory and delete tests folder. """,
    )

    args = parser.parse_args()
    args.source_files.extend(["__init__.py", f"{args.name}.py"])

    return args


def get_answer(question: str) -> bool:
    """Repeatedly ask the user a yes/no question until a 'y' or a 'n' is received."""
    ans = ""
    question = question.strip()
    if "?" not in question:
        question += "?"
    question += " (y/n): "
    while ans not in ["y", "yes", "no", "n"]:
        ans = input(question).strip().lower()
        if ans in ["y", "yes"]:
            return True
        elif ans in ["n", "no"]:
            return False
        else:
            print("Invalid answer.")


def check_pypi_for_name(package_name: str) -> bool:
    """Check if a package with package_name already exists on `pypi.org`.
    Returns `True` if package name exists.
    Only checks the first page of results."""
    url = f"https://pypi.org/search/?q={package_name.lower()}"
    response = requests.get(url)
    if response.status_code != 200:
        raise RuntimeError(
            f"Error: pypi.org returned status code: {response.status_code}"
        )
    soup = BeautifulSoup(response.text, "html.parser")
    pypi_packages = [
        span.text.lower()
        for span in soup.find_all("span", class_="package-snippet__name")
    ]
    return package_name in pypi_packages


def check_pypi_for_name_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("name", type=str)
    args = parser.parse_args()
    if check_pypi_for_name(args.name):
        print(f"{args.name} is already taken.")
    else:
        print(f"{args.name} is available.")


def create_pyproject_file(targetdir: Pathier, args: argparse.Namespace):
    """Create `pyproject.toml` in `./{project_name}` from args, pyproject_template, and hassle_config."""
    pyproject = (root / "pyproject_template.toml").loads()
    if not hassle_config.config_exists():
        hassle_config.warn()
        if not get_answer("Continue creating new package with blank config?"):
            raise Exception("Aborting new package creation")
        else:
            print("Creating blank hassle_config.toml...")
            hassle_config.create_config()
    config = hassle_config.load_config()
    pyproject["project"]["name"] = args.name
    pyproject["project"]["authors"] = config["authors"]
    pyproject["project"]["description"] = args.description
    pyproject["project"]["dependencies"] = args.dependencies
    pyproject["project"]["keywords"] = args.keywords
    if args.operating_system:
        pyproject["project"]["classifiers"][2] = "Operating System :: " + " ".join(
            args.operating_system
        )
    if args.no_license:
        pyproject["project"]["classifiers"].pop(1)
    for field in config["project_urls"]:
        pyproject["project"]["urls"][field] = config["project_urls"][field].replace(
            "$name", args.name
        )
    if args.add_script:
        pyproject["project"]["scripts"][args.name] = f"{args.name}.{args.name}:main"
    if args.not_package:
        for item in ["build-system", "tool", "project.scripts"]:
            if item in pyproject:
                pyproject.pop(item)
    (targetdir / "pyproject.toml").dumps(pyproject)


def create_source_files(srcdir: Pathier, filelist: list[str]):
    """Generate empty source files in `./{package_name}/src/{package_name}/`"""
    srcdir.mkdir(parents=True, exist_ok=True)
    for file in filelist:
        (srcdir / file).touch()
    init = srcdir / "__init__.py"
    if init.exists():
        init.append('__version__ = "0.0.0"')


def create_readme(targetdir: Pathier, args: argparse.Namespace):
    """Create `README.md` in `./{package_name}` from readme_template and args."""
    readme = (root / "README_template.md").read_text()
    readme = readme.replace("$name", args.name).replace(
        "$description", args.description
    )
    (targetdir / "README.md").write_text(readme)


def create_license(targetdir: Pathier):
    """Add MIT license file to `./{package_name}`."""
    license_template = (root / "license_template.txt").read_text()
    license_template = license_template.replace("$year", str(datetime.now().year))
    (targetdir / "LICENSE.txt").write_text(license_template)


def create_gitignore(targetdir: Pathier):
    """Add `.gitignore` to `./{package_name}`"""
    (root / ".gitignore_template").copy(targetdir / ".gitignore", True)


def create_vscode_settings(targetdir: Pathier):
    """Add `settings.json` to `./.vscode`"""
    vsdir = targetdir / ".vscode"
    vsdir.mkdir(parents=True, exist_ok=True)
    (root / ".vscode_template").copy(vsdir / "settings.json", True)


def main(args: argparse.Namespace = None):
    if not args:
        args = get_args()
    if not args.not_package:
        try:
            if check_pypi_for_name(args.name):
                print(f"{args.name} already exists on pypi.org")
                if not get_answer("Continue anyway?"):
                    sys.exit(0)
        except Exception as e:
            print(e)
            print(
                f"Couldn't verify that {args.name} doesn't already exist on pypi.org ."
            )
            if not get_answer("Continue anyway?"):
                sys.exit(0)
    try:
        targetdir: Pathier = Pathier.cwd() / args.name
        try:
            targetdir.mkdir(parents=True, exist_ok=False)
        except:
            print(f"{targetdir} already exists.")
            if not get_answer("Overwrite?"):
                sys.exit(0)
        create_pyproject_file(targetdir, args)
        create_source_files(
            targetdir if args.not_package else (targetdir / "src" / args.name),
            args.source_files[1:] if args.not_package else args.source_files,
        )
        create_readme(targetdir, args)
        if not args.not_package:
            generate_test_files(targetdir)
            create_vscode_settings(targetdir)
        create_gitignore(targetdir)
        if not args.no_license:
            create_license(targetdir)
        os.chdir(targetdir)
        git = Git()
        git.new_repo()

    except Exception as e:
        if not "Aborting new package creation" in str(e):
            print(e)
        if get_answer("Delete created files?"):
            targetdir.delete()


if __name__ == "__main__":
    main(get_args())
