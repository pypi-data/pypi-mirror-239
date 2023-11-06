import unittest

from cwstorm.dsl.job import Job
from cwstorm.dsl.dag_node import DagNode
from cwstorm.dsl.task import Task
from cwstorm.dsl.cmd import Cmd
from unittest.mock import patch
from datetime import datetime


class SmokeTest(unittest.TestCase):
    def setUp(self):
        DagNode.reset()
        self.node = Job()

    def test_env_attribute(self):
        self.node.env({"foo": "bar"})
        self.assertEqual(self.node.env(), {"foo": "bar"})

    def test_comment_attribute(self):
        self.node.comment("foo")
        self.assertEqual(self.node.comment(), "foo")

    def test_account_id_must_be_16_digits(self):
        self.assertRaises(ValueError, self.node.account_id, "foo")
        self.assertRaises(ValueError, self.node.account_id, "12345678901234567")

