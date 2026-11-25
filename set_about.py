#!/usr/bin/env python3
"""Set About (description/homepage/topics) for 4orky/roast-your-fridge.

Same credential flow as ghpat.py (dynamic_credentials surrogate for
custom.github-pat); ghpat.py's set-about is hardcoded to token-radar-01,
so this bounty uses its own values here.
"""
import json
import sys
import urllib.error
import urllib.request

sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
from dynamic_credentials import add_surrogate_to_request, read_json_response

CRED = "custom.github-pat"
HOSTS = ["api.github.com"]
API = "https://api.github.com"


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args):
        raise RuntimeError("redirect refused, verify the endpoint")


def call(method, path, body=None):
    url = API + path
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    if data is not None:
        req.add_header("Content-Type", "application/json")
    add_surrogate_to_request(req, CRED, allowed_hosts=HOSTS)
    try:
        with urllib.request.build_opener(NoRedirect()).open(req, timeout=120) as resp:
            return resp.status, read_json_response(resp)
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode("utf-8", errors="replace")}


DESC = ("One funny single-line roast of a fridge. Built by an AI agent "
        "for make.fun's \"One Line, One Laugh: Roast Your Fridge\" "
        "bounty, $3 prize pool.")
assert len(DESC) <= 245, len(DESC)

s, b = call("PATCH", "/repos/4orky/roast-your-fridge", {
    "description": DESC,
    "homepage": "https://make.fun/c/u-suzy-one-line-one-laugh-roast-your-fridge-f1063521",
})
print(json.dumps({"patch_status": s, "description": b.get("description"),
                  "homepage": b.get("homepage"),
                  "error": b.get("error", b.get("message"))}))
assert s == 200
s, b = call("PUT", "/repos/4orky/roast-your-fridge/topics", {
    "names": ["makefun", "ai-agents", "bounties", "growth"],
})
print(json.dumps({"topics_status": s, "names": b.get("names"),
                  "error": b.get("error", b.get("message"))}))
assert s == 200
print("ABOUT OK")
