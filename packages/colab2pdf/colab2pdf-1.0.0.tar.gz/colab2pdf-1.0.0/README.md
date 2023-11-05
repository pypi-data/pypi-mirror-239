# Colab2PDF

Convert your Colab notebook to a PDF. One-minute install. No configuration required.

## Showcase Your Work: Beautiful. Simple. Clean.

<p float="left">
  <img src="example1.png" width="33%" />
  <img src="example2.png" width="33%" />
</p>

## Just Copy, Paste, and Run [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1zqrIYC0iQ_CZkRqGXgZggrwjtt_4BmpL?usp=sharing)

```python
# @title Convert to PDF and Download {display-mode:"form"}
# Colab2PDF v1.0.0 by Drengskapur (https://github.com/drengskapur/colab2pdf)
# This code is licensed under the GNU General Public License v3 (GPLv3)
def colab2pdf():
    import datetime, json, os, pathlib, urllib, warnings, IPython, nbformat, requests, werkzeug, yaml, google
    INCLUDE_OUTPUT = True # @param {type:"boolean"}
    LINE_NUMBERS = False # @param {type:"boolean"}
    HIGHLIGHT_STYLE = "arrow" # @param ["arrow", "atom-one", "ayu", "breeze", "breezedark", "dracula", "espresso", "github", "gruvbox", "haddock", "kate", "monochrome", "monokai", "nord", "oblivion", "printing", "pygments", "radical", "solarized", "tango", "vim-dark", "zenburn"]
    VERBOSE = False # Set to True to debug
    QUIET = '--quiet' if not VERBOSE else ''
    TEMP_DIR = pathlib.Path("/content/temp") / datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE = TEMP_DIR / "config.yml"
    URL = f"http://{os.environ['COLAB_JUPYTER_IP']}:{os.environ['KMP_TARGET_PORT']}/api/sessions"
    NB_NAME = pathlib.Path(werkzeug.utils.secure_filename(urllib.parse.unquote(requests.get(URL).json()[0]["name"])))
    TEMP_NB = TEMP_DIR / NB_NAME.with_suffix(".ipynb")
    NB_PDF = TEMP_DIR / NB_NAME.with_suffix(".pdf")
    MARGINS = "top: 1in, bottom: 1in, left: 1in, right: 1in"
    MT, MB, ML, MR = MARGINS.split(', ')
    CONFIG = {
        'execute': {'include': INCLUDE_OUTPUT},
        'code-line-numbers': LINE_NUMBERS,
        'highlight-style': HIGHLIGHT_STYLE,
        'margin-top': MT.split(': ')[1], 'margin-bottom': MB.split(': ')[1], 'margin-left': ML.split(': ')[1], 'margin-right': MR.split(': ')[1],
        'latex-auto-install': True,
        'include-in-header': [{"text": r"\usepackage{fvextra}"}, {"text": r"\DefineVerbatimEnvironment{Highlighting}{Verbatim}{breaksymbolleft={},showspaces=false,showtabs=false,breaklines,breakanywhere,commandchars=\\\{\}}"}],
        'include-before-body': [{"text": r"\DefineVerbatimEnvironment{verbatim}{Verbatim}{breaksymbolleft={},showspaces=false,showtabs=false,breaklines}"}]
    }
    with CONFIG_FILE.open("w") as patch: yaml.dump(CONFIG, patch)
    RAW_NB = google.colab._message.blocking_request("get_ipynb", timeout_sec=30)
    warnings.filterwarnings('ignore', category=nbformat.validator.MissingIDFieldWarning)
    FILTERED = [cell for cell in nbformat.reads(json.dumps(RAW_NB["ipynb"]), as_version=4).cells if "--Colab2PDF" not in cell.source]
    if not FILTERED: FILTERED.append(nbformat.v4.new_code_cell("#"))
    NOTEBOOK = nbformat.v4.new_notebook(cells=FILTERED)
    with TEMP_NB.open("w") as temp_file: nbformat.write(NOTEBOOK, temp_file)
    if not pathlib.Path("/usr/local/bin/quarto").exists():
        !wget '{QUIET}' "https://quarto.org/download/latest/quarto-linux-amd64.deb" --output-document="{TEMP_DIR}/quarto-linux-amd64.deb"
        !dpkg --install "{TEMP_DIR}/quarto-linux-amd64.deb"
        !quarto install tinytex --update-path
        IPython.display.clear_output(wait=True)
    !quarto render '{TEMP_NB}' --metadata-file='{CONFIG_FILE}' --to pdf '{QUIET}'
    google.colab.files.download(NB_PDF)

colab2pdf()
```
