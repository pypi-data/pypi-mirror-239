"""Sets up the package."""
import os
import re
from pathlib import Path

from setuptools import find_namespace_packages, setup

ROOT = Path(__file__).parent


def get_string_from_file_by_variable_name(obj_name: str, file_path: Path) -> str:
    """Get a string from the source code of a file by its variable name.

    Args:
        obj_name: Variable name of the string defined in the file.
        file_path: Path to the file.

    Returns:
        Variable name's value.
    """
    file_text = file_path.read_text(encoding="utf-8")
    return re.search(rf'{obj_name}\s*=\s*[\'"]([^\'"]*)[\'"]', file_text).group(1)


name = "scihence"
version = get_string_from_file_by_variable_name(
    "__version__", Path("src") / name / "__init__.py"
)
job = os.getenv("CI_JOB_ID")
if job and not (os.getenv("CI_COMMIT_BRANCH") == os.getenv("CI_DEFAULT_BRANCH")):
    version += f"+job{job}"

package_data = {
    name: [
        "visualize/fonts/**",
        "visualize/mplstyles/*",
    ],
}
for package, data_list in package_data.items():
    for data in data_list:
        assert (Path("src") / package).glob(data)

install_requires = [
    "matplotlib>=3.5.0,<4",
    "mlflow>=2.1.1,<3",
    "numpy>=1.23.0,<2",
    "pandas>=2.0.0,<3",
    "Pillow>=10.0.0,<11",
    "plotly>=5.0.0,<8",
    "seaborn>=0.12.0,<1",
    "xgboost>=1.7.0,<2",
]

extras_require = {
    "build": [
        "build",
        "tox",
    ],
    "check": [
        "pre-commit",
        "tox",
    ],
    "docs": [
        "furo",
        "pre-commit",
        "sphinx",
        "tox",
    ],
    "lint": [
        "ruff",
        "tox",
    ],
    "pub": [
        "twine",
    ],
    "test": [
        "junit2html",
        "pytest",
        "pytest-cov",
        "tox",
    ],
}
extras_require["dev"] = sum(extras_require.values(), [])

setup(
    name=name,
    author="Henry Broomfield",
    description="Henry's tools in Python.",
    long_description=(ROOT / "README.md").read_text(),
    long_description_content_type="text/markdown",
    packages=find_namespace_packages(where="src"),
    package_dir={name: f"src/{name}"},
    include_package_data=True,
    package_data=package_data,
    install_requires=install_requires,
    python_requires=">=3.11.0,<3.12",
    extras_require=extras_require,
    url="https://gitlab.com/HennersBro98/scihence",
    license=(ROOT / "LICENSE").read_text(),
    version=version,
)
