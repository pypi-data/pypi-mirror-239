import unittest

from cwstorm.serializers import default, storm

from cwstorm.dsl.job import Job
from cwstorm.dsl.dag_node import DagNode
from cwstorm.dsl.task import Task
from cwstorm.dsl.cmd import Cmd


class StormTest(unittest.TestCase):
    def setUp(self):
        DagNode.reset()
        self.job = Job()

    def test_serialize_comment(self):
        self.job.comment("foo")
        serialized = storm.serialize(self.job)
        self.assertEqual(serialized["comment"], "foo")

    def test_serialize_job_with_children(self):
        self.job.add(Task())
        serialized = storm.serialize(self.job)
        self.assertEqual(serialized["tasks"][0]["name"], "Task_00000")

    def test_serialize_job_with_children_and_commands(self):
        self.job.cleanup(Cmd().argv("echo", "done"))
        task = Task().commands(Cmd().argv("echo", "progress"))
        self.job.add(task)
        serialized = storm.serialize(self.job)
        self.assertEqual(serialized["tasks"][0]["name"], "Task_00000")
        self.assertEqual(
            serialized["tasks"][0]["commands"][0]["argv"], ["echo", "progress"]
        )
        self.assertEqual(serialized["cleanup"]["argv"], ["echo", "done"])

    def test_serialize_job_with_references(self):
        render1 = Task().commands(Cmd().argv("render1"))
        render2 = Task().commands(Cmd().argv("render2"))

        self.job.add(render1)
        self.job.add(render2)
        export_1_2 = Task().commands(Cmd().argv("export_1_2"))
        render1.add(export_1_2)
        render2.add(export_1_2)
        serialized = storm.serialize(self.job)

        self.assertEqual(serialized["tasks"][0]["tasks"][0]["name"], "Task_00002")
        self.assertEqual(serialized["tasks"][1]["tasks"][0]["name"], "Task_00002")
        self.assertFalse(serialized["tasks"][0]["tasks"][0]["reference"])
        self.assertTrue(serialized["tasks"][1]["tasks"][0]["reference"])

    def test_serialize_job_with_dicts(self):
        self.job.env({"foo": "bar"})
        serialized = storm.serialize(self.job)
        self.assertEqual(serialized["env"], {"foo": "bar"})


class CytoscapeTest(unittest.TestCase):
    def setUp(self):
        DagNode.reset()
        self.job = Job()

    def test_serialize_comment(self):
        self.job.comment("foo")
        serialized = default.serialize(self.job)
        self.assertEqual(serialized["nodes"][0]["data"]["id"], "Job_00000")

    def test_serialize_job_with_children(self):
        self.job.add(Task())
        serialized = default.serialize(self.job)

        self.assertEqual(len(serialized["nodes"]), 2)
        self.assertEqual(len(serialized["edges"]), 1)

    def test_serialize_job_with_references(self):
        render1 = Task().commands(Cmd().argv("render1"))
        render2 = Task().commands(Cmd().argv("render2"))

        self.job.add(render1)
        self.job.add(render2)
        export_1_2 = Task().commands(Cmd().argv("export_1_2"))
        render1.add(export_1_2)
        render2.add(export_1_2)

        serialized = default.serialize(self.job)
        nodes = serialized["nodes"]
        edges = serialized["edges"]

        self.assertEqual(len(nodes), 4)
        self.assertEqual(len(edges), 4)


#        ┌─────┐
#        │ job │
#        └──┬──┘
#           │
#     ┌─────┴───────┐
# ┌───┴───┐     ┌───┴───┐
# │ frame1│     │ frame2│
# └───┬───┘     └───┬───┘
#     └──────┬──────┘
#            │
#        ┌───┴───┐
#        │  ass  │
#        └───┬───┘
