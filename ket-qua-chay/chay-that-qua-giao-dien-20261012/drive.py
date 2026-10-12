import json
import sys
import time
import urllib.request

BASE = "http://127.0.0.1:8001"


def call(path, body=None):
    r = urllib.request.Request(BASE + path, json.dumps(body).encode() if body else None,
                               {"Content-Type": "application/json", "X-L3GEN-Client": "web-v1", "Origin": BASE})
    return json.loads(urllib.request.urlopen(r, timeout=30).read())


cfg = call("/api/config")
run = call("/api/runs", {"source": cfg["defaults"]["source"], "membership": cfg["defaults"]["membership"],
                         "mode": sys.argv[1] if len(sys.argv) > 1 else "oneshot", "notice_version": cfg["notice_version"]})
print(run["run_id"], flush=True)
while True:
    v = call("/api/runs/" + run["run_id"])
    if v["status"] != "running":
        break
    time.sleep(3)
print(v["status"], v["message"])
r = v.get("result")
if r:
    a = r["agent"]
    print(a["status"], a.get("reason"), a.get("mode"), a.get("turns"))
    print("requests:", [(q.get("input"), q.get("output"), round(q.get("cost_usd") or 0, 4)) for q in a.get("requests", [])])
    print([x["path"] + ":" + x["status"] for x in r["artifacts"]])
    print([l["code"] for l in r["limitations"]])
    print("dir:", v.get("output_directory"))
