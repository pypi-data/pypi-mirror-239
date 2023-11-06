# SPDX-FileCopyrightText: 2023-present Drengskapur <service@drengskapur.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
if __name__ == "__main__":
    try:
        import google.colab
    except:
        raise RuntimeError("This script must be run in Google Colaboratory.")
    import sys
    from colab2pdf.cli import run

    sys.exit(run())
