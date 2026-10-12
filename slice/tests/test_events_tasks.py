"""FR-031 Phạm vi đọc: Celery (.delay, .apply_async, send_task -> @app.task, @shared_task) và FastAPI BackgroundTasks
(add_task(hàm) -> hàm được truyền vào). Đọc tĩnh trong extract._events."""
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

from l3slice import extract, snapshot  # noqa: E402
from l3slice.common import is_known  # noqa: E402


def events_of(files: dict) -> list[dict]:
    with tempfile.TemporaryDirectory() as t:
        root = Path(t)
        for rel, text in files.items():
            (root / rel).parent.mkdir(parents=True, exist_ok=True)
            (root / rel).write_text(text, encoding="utf-8")
        snap, sources = snapshot.take(root)
        unit = snapshot.inventory(snap)["units"][0]["id"]
        facts = extract.extract(snap, sources, unit)["facts"]
    out = []
    for f in facts:
        if f["kind"] == "event":
            a = f["attributes"]
            ev = next(e for e in f["evidence"] if e["id"] == a["declaration_evidence_id"]["value"])
            out.append({"action": a["action"]["value"], "topic": a["topic"]["value"] if is_known(a["topic"]) else None,
                        "broker": a["broker"]["value"] if is_known(a["broker"]) else None,
                        "namespace": a["namespace"]["value"] if is_known(a["namespace"]) else None,
                        "at": f"{ev['path']}:{ev['start_line']}", "confidence": f["confidence"]})
    return sorted(out, key=lambda x: (x["at"].split(":")[0], int(x["at"].split(":")[1])))


CELERY = {
    "worker/__init__.py": "",
    "worker/app.py": 'from celery import Celery\n\ncelery_app = Celery("w", broker="redis://x")\n',
    "worker/tasks.py": ('from worker.app import celery_app\nfrom celery import shared_task\n\n\n'
                        '@celery_app.task(name="emails.send")\ndef send_email(to):\n    return to\n\n\n'
                        '@celery_app.task\ndef cleanup():\n    pass\n\n\n@shared_task\ndef audit():\n    pass\n'),
    "api.py": ('from worker.tasks import send_email, cleanup\nfrom worker.app import celery_app\n\n\n'
               'def handler():\n    send_email.delay("a")\n    cleanup.apply_async()\n    celery_app.send_task("emails.send", args=[1])\n'
               '    "x".delay()\n'),
}


class Celery(unittest.TestCase):
    def test_tasks_are_receivers_and_calls_are_senders(self):
        ev = events_of(CELERY)
        got = [(e["action"], e["topic"], e["at"]) for e in ev]
        self.assertEqual(got, [("publish", "emails.send", "api.py:6"), ("publish", "worker.tasks.cleanup", "api.py:7"),
                               ("publish", "emails.send", "api.py:8"),
                               ("consume", "emails.send", "worker/tasks.py:5"),
                               ("consume", "worker.tasks.cleanup", "worker/tasks.py:10"),
                               ("consume", "worker.tasks.audit", "worker/tasks.py:15")])

    def test_the_same_app_is_the_same_broker_and_default_names_are_inferred(self):
        ev = {(e["action"], e["at"]): e for e in events_of(CELERY)}
        self.assertEqual(ev[("publish", "api.py:6")]["broker"], ev[("consume", "worker/tasks.py:5")]["broker"])
        self.assertEqual(ev[("publish", "api.py:6")]["namespace"], ev[("consume", "worker/tasks.py:5")]["namespace"])
        self.assertIsNone(ev[("consume", "worker/tasks.py:15")]["broker"])  # shared_task: the app is chosen at run time
        self.assertEqual(ev[("consume", "worker/tasks.py:10")]["confidence"], "inferred")  # Celery's default name
        self.assertEqual(ev[("consume", "worker/tasks.py:5")]["confidence"], "exact")

    def test_celery_is_no_longer_an_unsupported_queue(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            for rel, text in CELERY.items():
                (root / rel).parent.mkdir(parents=True, exist_ok=True)
                (root / rel).write_text(text, encoding="utf-8")
            snap, sources = snapshot.take(root)
            lims = extract.extract(snap, sources, snapshot.inventory(snap)["units"][0]["id"])["limitations"]
        self.assertNotIn("QUEUE_LIBRARY_UNSUPPORTED", [x["code"] for x in lims])


BACKGROUND = {"main.py": ('from fastapi import FastAPI, BackgroundTasks\n\napp = FastAPI()\n\n\n'
                          'def write_log(msg):\n    pass\n\n\nclass Logging:\n    def __init__(self, background_task: BackgroundTasks):\n'
                          '        background_task.add_task(self._send)\n\n    async def _send(self):\n        pass\n\n\n'
                          '@app.post("/x")\ndef x(tasks: BackgroundTasks):\n    tasks.add_task(write_log, "hi")\n'
                          '    other = []\n    other.add_task(write_log)\n')}


class BackgroundTasksEvents(unittest.TestCase):
    def test_add_task_sends_to_the_function_it_passes(self):
        got = [(e["action"], e["topic"], e["at"]) for e in events_of(BACKGROUND)]
        self.assertEqual(got, [("consume", "main.write_log", "main.py:6"), ("publish", "main.Logging._send", "main.py:12"),
                               ("consume", "main.Logging._send", "main.py:14"), ("publish", "main.write_log", "main.py:20")])

    def test_both_ends_share_broker_and_namespace(self):
        ev = events_of(BACKGROUND)
        self.assertEqual({e["broker"] for e in ev}, {"fastapi.BackgroundTasks"})
        self.assertTrue(all(e["namespace"] for e in ev))


class UnsupportedBus(unittest.TestCase):
    """orderflow (chấm held-out 12/10/2026): bus tự viết trên Redis pub/sub bị bỏ sót mà không cảnh báo."""

    def limits(self, files):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            for rel, text in files.items():
                (root / rel).parent.mkdir(parents=True, exist_ok=True)
                (root / rel).write_text(text, encoding="utf-8")
            snap, sources = snapshot.take(root)
            return extract.extract(snap, sources, snapshot.inventory(snap)["units"][0]["id"])["limitations"]

    def test_redis_publish_and_subscribe_are_reported(self):
        bus = ("from redis.asyncio import Redis\n\n\nclass Bus:\n    def __init__(self, c: Redis):\n        self.c = c\n\n"
               "    async def publish(self, topic, msg):\n        await self.c.publish(topic, msg)\n\n"
               "    async def subscribe(self, topic):\n        p = self.c.pubsub()\n        await p.subscribe(topic)\n")
        [lim] = [x for x in self.limits({"bus.py": bus}) if x["code"] == "QUEUE_LIBRARY_UNSUPPORTED"]
        self.assertIn("Redis pub/sub", lim["message"])
        self.assertIn("bus.py:9", lim["message"])

    def test_redis_used_as_a_cache_is_not_reported(self):
        cache = "import redis\n\nr = redis.Redis()\n\n\ndef get(k):\n    return r.get(k)\n"
        self.assertEqual([x for x in self.limits({"cache.py": cache}) if x["code"] == "QUEUE_LIBRARY_UNSUPPORTED"], [])


if __name__ == "__main__":
    unittest.main()
