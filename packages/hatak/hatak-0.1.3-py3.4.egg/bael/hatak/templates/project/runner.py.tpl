from hatak.tests.runner import TestRunner

from .fixtures import Fixtures
from {{settings["package:name"]}}.application.init import main


def run():
    TestRunner(main, Fixtures)()
