# Refresh the GitHub About panel for 4orky/roast-your-fridge.
# Runs two calls: PATCH the description plus homepage, then PUT the topic list.
# Credentials come from the registered custom.github-pat connection through
# the dynamic_credentials surrogate helper, exactly like ghpat.py does it.
# Nothing secret is ever printed; only HTTP statuses and public fields go out.
import json as _json
import sys as _sys
import urllib.error as _errors
import urllib.request as _net
_sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
from dynamic_credentials import add_surrogate_to_request as _sign, read_json_response as _parse
_PROVIDER = "custom.github-pat"
_TRUSTED = ["api.github.com"]
_ROOT = "https://api.github.com"
_SLUG = "4orky/roast-your-fridge"
_BOUNTY_URL = "https://make.fun/c/u-suzy-one-line-one-laugh-roast-your-fridge-f1063521"
_BLURB = "One-line fridge roast, built by an AI agent for make.fun: One Line, One Laugh: Roast Your Fridge ($3 prize)."
if len(_BLURB) > 350:
    raise SystemExit("blurb exceeds the GitHub description limit")
class _RefuseRedirect(_net.HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, msg, headers, newurl):
        raise ValueError("redirect blocked, refusing to follow " + str(newurl))
def _request(verb, route, payload):
    endpoint = _ROOT + route
    encoded = _json.dumps(payload).encode() if payload is not None else None
    outgoing = _net.Request(endpoint, data=encoded, method=verb)
    outgoing.add_header("X-GitHub-Api-Version", "2022-11-28")
    outgoing.add_header("Accept", "application/vnd.github+json")
    if encoded:
        outgoing.add_header("Content-Type", "application/json")
    _sign(outgoing, _PROVIDER, allowed_hosts=_TRUSTED)
    def _send():
        try:
            opener = _net.build_opener(_RefuseRedirect())
            with opener.open(outgoing, timeout=120) as incoming:
                return incoming.status, _parse(incoming)
        except _errors.HTTPError as failure:
            detail = failure.read().decode("utf-8", errors="replace")
            return failure.code, {"failure": detail}
    return _send()
_JOBS = [("PATCH", "/repos/" + _SLUG, {"description": _BLURB, "homepage": _BOUNTY_URL}), ("PUT", "/repos/" + _SLUG + "/topics", {"names": "makefun ai-agents bounties growth".split()})]
for _verb, _route, _payload in _JOBS:
    _code, _body = _request(_verb, _route, _payload)
    print(_json.dumps({"verb": _verb, "http_status": _code, "body": _body}))
    if _code != 200:
        raise SystemExit("GitHub About update failed on " + _verb)
_code, _body = _request("GET", "/repos/" + _SLUG, None)
print(_json.dumps({"verb": "GET", "http_status": _code, "description": _body.get("description"), "homepage": _body.get("homepage"), "topics": _body.get("topics")}))
if _code != 200 or _body.get("description") != _BLURB or _body.get("homepage") != _BOUNTY_URL or sorted(_body.get("topics") or []) != sorted("makefun ai-agents bounties growth".split()):
    raise SystemExit("GitHub About verification mismatch after update")
print("ABOUT REFRESHED")
