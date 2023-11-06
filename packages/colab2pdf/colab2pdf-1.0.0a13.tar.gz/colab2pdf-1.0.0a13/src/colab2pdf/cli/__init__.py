# SPDX-FileCopyrightText: 2023-present Drengskapur <service@drengskapur.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
import argparse
import datetime
import json
import os
import pathlib
import subprocess
import textwrap
import urllib
import warnings
from typing import Dict, Union

import google
import nbformat
import requests
import werkzeug
import yaml

from colab2pdf.__about__ import __version__

warnings.filterwarnings('ignore', category=nbformat.validator.MissingIDFieldWarning)


def _create_temp_dir() -> pathlib.Path:
    """
    Create a temporary directory for storing intermediate files.

    Returns:
        pathlib.Path: The path of the created temporary directory.
    """
    base_temp_dir = pathlib.Path("/content/temp")
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    temp_dir = base_temp_dir / timestamp

    temp_dir.mkdir(parents=True, exist_ok=True)
    return temp_dir


def _get_notebook_name() -> pathlib.Path:
    """
    Get the name of the currently running Colab notebook.

    Returns:
        pathlib.Path: The sanitized name of the notebook.
    """
    ip = os.environ['COLAB_JUPYTER_IP']
    port = os.environ['KMP_TARGET_PORT']
    base_url = f"http://{ip}:{port}"

    endpoint = "/api/sessions"
    url = base_url + endpoint

    response = requests.get(url)
    data = response.json()

    unquoted_notebook_name = urllib.parse.unquote(data[0]["name"])
    sanitized_notebook_name = werkzeug.utils.secure_filename(unquoted_notebook_name)

    return pathlib.Path(sanitized_notebook_name)


def _create_config(config_path: pathlib.Path, options: Dict[str, Union[str, bool]]):
    """
    Create a config file based on given options.

    Args:
        config (pathlib.Path): Path to write the config file.
        options (Dict[str, Union[str, bool]]): User-provided options for PDF generation.
    """
    config = {
        'execute': {
            'include': options.get('show-output', True),
        },
        'code-line-numbers': options.get('line-numbers', False),
        'highlight-style': options.get('highlight-style', "arrow"),
        'margin-top': options.get('margin-top', "1in"),
        'margin-bottom': options.get('margin-bottom', "1in"),
        'margin-left': options.get('margin-left', "1in"),
        'margin-right': options.get('margin-right', "1in"),
        'latex-auto-install': options.get('latex-auto-install', True),
        'include-in-header': [
            {"text": r"\usepackage{fvextra}"},
            {"text": r"\DefineVerbatimEnvironment{Highlighting}{Verbatim}{breaksymbolleft={},showspaces=false,showtabs=false,breaklines,breakanywhere,commandchars=\\\{\}}"}
        ],
        'include-before-body': [
            {
                "text": r"\DefineVerbatimEnvironment{verbatim}{Verbatim}{breaksymbolleft={},showspaces=false,showtabs=false,breaklines}"
            }
        ],
    }

    with config_path.open("w") as file:
        yaml.dump(config, file)


def _get_notebook() -> nbformat.NotebookNode:
    """
    Get the current Colab notebook

    Returns:
        nbformat.NotebookNode: The Colab notebook.
    """
    request_response = google.colab._message.blocking_request("get_ipynb", timeout_sec=30)
    ipynb_content = request_response["ipynb"]
    nb_content_json = json.dumps(ipynb_content)

    parsed_notebook = nbformat.reads(nb_content_json, as_version=4)
    all_cells = parsed_notebook.cells

    # we don't want the !colab2pdf command to show in the PDF
    filtered_cells = [cell for cell in all_cells if "!colab2pdf" not in cell.source]

    new_notebook = nbformat.v4.new_notebook()
    new_notebook.cells = filtered_cells if filtered_cells else [nbformat.v4.new_code_cell("#")]

    return new_notebook


def _run_cmd(cmd: str):
    """
    Run a shell command and print its output.

    Args:
        cmd (str): The command to run.
    """
    cmd_list = cmd.split()
    result = subprocess.run(cmd_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if "--quiet" not in cmd:
        print(result.stdout.decode(), result.stderr.decode())


def _install_quarto(temp_dir: pathlib.Path, quiet: str):
    """
    Install Quarto and TinyTeX if not already installed.

    Args:
        temp_dir (pathlib.Path): The temporary directory for storing downloaded files.
        quiet (str): '--quiet' to minimize console output, otherwise ''.
    """
    download_url = "https://quarto.org/download/latest/quarto-linux-amd64.deb"
    quarto_path = pathlib.Path("/usr/local/bin/quarto")

    if not quarto_path.exists():
        _run_cmd(f"wget {download_url} -O {temp_dir}/quarto-linux-amd64.deb {quiet}")
        _run_cmd(f"dpkg -i {temp_dir}/quarto-linux-amd64.deb")
        _run_cmd(f"quarto install tinytex --update-path {quiet}")


def download(options: Dict[str, Union[str, bool]]):
    """
    Download a Colab notebook as a PDF.

    Args:
        options (Dict[str, Union[str, bool]]): User-provided options for configuring PDF generation.
    """
    quiet = "--quiet" if options.get('quiet', False) else ''
    temp_dir = _create_temp_dir()

    notebook_name = _get_notebook_name()
    notebook = temp_dir / notebook_name.with_suffix(".ipynb")

    config = temp_dir / "config.yml"
    _create_config(config, options)

    with notebook.open("w") as file:
        nbformat.write(_get_notebook(), file)

    _install_quarto(temp_dir, quiet)
    _run_cmd(f"quarto render {notebook} --metadata-file {config} --to pdf {quiet}")

    google.colab.files.download(temp_dir / notebook_name.with_suffix(".pdf"))


def run():
    """
    Parse command-line arguments and run the appropriate function.
    """
    parser = argparse.ArgumentParser(
        description=textwrap.dedent(
            """\
            Colab2PDF: Convert Your Colab Notebook to a PDF.
            One-Minute Install. Zero Configuration.
            License: GPL-3.0-or-later
            Source: https://github.com/drengskapur/colab2pdf
            """
        ),
        prog="colab2pdf",
        formatter_class=argparse.RawTextHelpFormatter,
        add_help=True,
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"colab2pdf {__version__}",
        help="Show the version number and exit.",
    )

    subparsers = parser.add_subparsers(dest="command", help="Commands available in colab2pdf.")
    download_parser = subparsers.add_parser(
        "download",
        help="Convert a Google Colab notebook to PDF and download the resulting file.",
        description="Convert a Google Colab notebook to PDF and download the resulting file.",
    )

    highlight_choices = [
        "arrow",
        "atom-one",
        "ayu",
        "breeze",
        "breezedark",
        "dracula",
        "espresso",
        "github",
        "gruvbox",
        "haddock",
        "kate",
        "monochrome",
        "monokai",
        "nord",
        "oblivion",
        "printing",
        "pygments",
        "radical",
        "solarized",
        "tango",
        "vim-dark",
        "zenburn",
    ]

    download_parser.add_argument(
        "--highlight",
        default="arrow",
        choices=highlight_choices,
        help="Specify the highlight style for code in the PDF.\n"
        f"Choices: {', '.join(highlight_choices)}\n"
        "Default: arrow",
    )

    download_parser.add_argument(
        "--top-margin",
        default="1in",
        help="Specify the top margin of the PDF. Default: 1in",
    )

    download_parser.add_argument(
        "--bottom-margin",
        default="1in",
        help="Specify the bottom margin of the PDF. Default: 1in",
    )

    download_parser.add_argument(
        "--left-margin",
        default="1in",
        help="Specify the left margin of the PDF. Default: 1in",
    )

    download_parser.add_argument(
        "--right-margin",
        default="1in",
        help="Specify the right margin of the PDF. Default: 1in",
    )

    download_parser.add_argument(
        "--show-output",
        action="store_true",
        default=True,
        help="Include code output in the PDF. Default: True",
    )

    download_parser.add_argument(
        "--line-numbers",
        action="store_true",
        default=False,
        help="Include line numbers in code cells. Default: False",
    )

    download_parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        default=True,
        help="Minimize console output. Default: True",
    )

    args = parser.parse_args()

    if args.command is None:
        args.command = 'download'

    options = {
        'highlight': getattr(args, 'highlight', 'arrow'),
        'top-margin': getattr(args, 'top_margin', '1in'),
        'bottom-margin': getattr(args, 'bottom_margin', '1in'),
        'left-margin': getattr(args, 'left_margin', '1in'),
        'right-margin': getattr(args, 'right_margin', '1in'),
        'show-output': getattr(args, 'show_output', True),
        'line-numbers': getattr(args, 'line_numbers', False),
        'quiet': getattr(args, 'quiet', True),
    }

    if args.command == 'download':
        download(options)


if __name__ == "__main__":
    run()
