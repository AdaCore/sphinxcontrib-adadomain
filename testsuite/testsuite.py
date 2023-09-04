#! /usr/bin/env python3

import glob
import os
import os.path as P
from shutil import copytree
import sys
import subprocess

from e3.testsuite import Testsuite
from e3.testsuite.driver.diff import DiffTestDriver
from e3.fs import sync_tree

TESTSUITE_DIR = P.abspath(P.join(P.dirname(P.abspath(__file__))))

CONF_PY_TEMPLATE = """
project = 'test_project'
copyright = '2023, Test author'
author = 'Test author'
extensions = ['sphinxcontrib.adadomain']
"""

INDEX_RST_TEMPLATE = """
Test doc
========

Contents:

.. toctree::
   :numbered:
   :maxdepth: 3

   {}

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""


class GendocDriver(DiffTestDriver):
    """
    Driver to test doc generation.

    This driver will run sphinx-build with the XML backend, and use XML output
    as a baseline.

    While this is far from ideal, it's the best output we found. It's certainly
    better than to compare against HTML output because it contains less
    non-semantic information.
    """

    @property
    def copy_test_directory(self) -> bool:
        return False

    def set_up(self) -> None:
        self.derived_env = dict(os.environ)
        if self.env.options.python_prefix:
            self.derived_env["PATH"] = (
                P.join(self.env.options.python_prefix, "bin")
                + P.pathsep
                + self.derived_env["PATH"]
            )

        # Generate rst if needed
        if self.env.options.regenerate_rst:
            self.shell(
                [
                    "python",
                    "-m",
                    "laldoc.generate_rst",
                    "-P",
                    self.test_env.get("project_file", "prj/prj.gpr"),
                    "-O",
                    ".",
                ],
                cwd=self.test_env["test_dir"],
                env=self.derived_env,
                analyze_output=False,
            )

        sync_tree(
            self.test_env["test_dir"],
            self.test_env["working_dir"],
            delete=True,
        )

        super().set_up()

    def run(self) -> None:
        doc_template_dir = P.join(TESTSUITE_DIR, "doc_template")

        # Create conf.py file
        with open(P.join(self.test_env["working_dir"], "conf.py"), "w") as f:
            f.write(CONF_PY_TEMPLATE)

        rst_files = glob.glob(P.join(self.test_env["working_dir"], "*.rst"))

        with open(P.join(self.test_env["working_dir"], "index.rst"), "w") as f:
            f.write(INDEX_RST_TEMPLATE.format(
                "    \n".join([P.basename(r) for r in rst_files])
            ))

        self.shell(
            ["sphinx-build", ".", "out"] + rst_files + ["-q", "-b", "xml"],
            env=self.derived_env,
        )

        if self.env.options.generate_html:
            self.shell(
                ["sphinx-build", ".", "html"]
                + rst_files + ["-q", "-b", "html"]
            )

        for xmlf in glob.glob(
            P.join(self.test_env["working_dir"], "out", "*.xml")
        ):
            # Skip index.xml
            if not P.basename(xmlf) == "index.xml":
                with open(xmlf) as f:
                    self.output += f"### {P.basename(xmlf)}:\n\n"
                    lines = f.readlines()
                    # Get rid of the "<document source>" tag, because it
                    # contains the full path to the test.
                    for line in lines:
                        if not "<document source=" in line:
                            self.output += line
                    self.output += "\n"


class AdaDomainTest(Testsuite):
    """
    Testsuite for sphinxcontrib-adadomain
    """
    tests_subdir = "tests"
    test_driver_map = {"gen-doc": GendocDriver}
    default_driver = "gen-doc"

    def add_options(self, parser):
        parser.add_argument(
            "--regenerate-rst", action="store_true",
            help="Run laldoc's generate_rst prior to running the tests."
        )
        parser.add_argument(
            "--rewrite", "-r", action="store_true",
            help="Rewrite test baselines according to current output."
        )
        parser.add_argument(
            "--generate-html", "-H", action="store_true",
            help="Also generate the html version of the doc. Useful to check"
            " that the output is correct."
        )
        parser.add_argument(
            "--no-mypy", action="store_true",
            help="Do not run mypy after successful testsuite runs."
        )
        parser.add_argument(
            "--python-prefix",
            help="Installation prefix for the Python distribution that"
            " provides Sphinx, sphinxcontrib-adadomain and laldoc. If"
            " omitted, assume they are available in the environment.",
        )

    def set_up(self):
        self.env.rewrite_baselines = self.env.options.rewrite


if __name__ == "__main__":
    t = AdaDomainTest()
    ret_1 = t.testsuite_main()
    if ret_1:
        sys.exit(ret_1)
    if not t.env.options.no_mypy:
        print("Running mypy")
        subprocess.check_call(["mypy"], cwd=P.join(TESTSUITE_DIR, ".."))
