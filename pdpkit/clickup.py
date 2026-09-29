"""ClickUp as the product queue.

`batch` takes every task in the Product Research list whose status is CLICKUP_STATUS ("ready to
build"), names the folder after the task, and reads the competitor links from the "Main Competitor"
field plus any product links in the description. When the images are on disk it ticks the "Images
pulled" checkbox and posts one comment on the task, so the team sees it happened from inside ClickUp
and the task is not pulled again (even from another laptop).

Only the personal API token is needed (Settings > Apps > API Token). Every call has a timeout and a
retry with backoff; a rate limit (429) waits and tries again.
"""
from __future__ import annotations

import logging
import time
from pathlib import Path

import requests

from . import config
from .batch import Row, store_urls

log = logging.getLogger("pdpkit.clickup")

API = "https://api.clickup.com/api/v2"


class ClickUpError(RuntimeError):
    pass


class ClickUp:
    def __init__(self, token: str | None = None, session: requests.Session | None = None):
        self.token = (token or config.CLICKUP_TOKEN).strip()
        if not self.token:
            raise ClickUpError("CLICKUP_TOKEN is not set (run SETUP.bat again, or put CLICKUP_TOKEN=pk_... in .env)")
        self.session = session or requests.Session()
        self.session.headers.update({"Authorization": self.token, "Content-Type": "application/json"})

    def _req(self, method: str, path: str, *, params: dict | None = None, json: dict | None = None) -> dict:
        url = f"{API}{path}"
        last = ""
        for attempt in range(4):
            try:
                r = self.session.request(method, url, params=params, json=json, timeout=(10, 45))
            except requests.RequestException as e:
                last = str(e)
                time.sleep(2 ** attempt)
                continue
            if r.status_code == 429 or r.status_code >= 500:
                wait = int(r.headers.get("Retry-After") or 0) or 2 ** attempt
                log.debug("ClickUp %s %s -> %s, retry in %ss", method, path, r.status_code, wait)
                time.sleep(wait)
                last = f"HTTP {r.status_code}"
                continue
            if r.status_code == 401:
                raise ClickUpError("ClickUp rejected the token (401). Get a fresh one: ClickUp > Settings > Apps > API Token")
            if r.status_code >= 400:
                detail = ""
                try:
                    detail = r.json().get("err") or r.json().get("error") or ""
                except ValueError:
                    pass
                raise ClickUpError(f"ClickUp {method} {path}: HTTP {r.status_code} {detail}".strip())
            try:
                return r.json() if r.content else {}
            except ValueError as e:
                raise ClickUpError(f"ClickUp {method} {path}: not JSON") from e
        raise ClickUpError(f"ClickUp {method} {path}: gave up after 4 attempts ({last})")

    # --- reads
    def me(self) -> dict:
        return self._req("GET", "/user").get("user", {})

    def list_info(self, list_id: str) -> dict:
        return self._req("GET", f"/list/{list_id}")

    def fields(self, list_id: str) -> list[dict]:
        return self._req("GET", f"/list/{list_id}/field").get("fields", [])

    def field_id(self, list_id: str, name: str) -> str:
        want = name.strip().lower()
        for f in self.fields(list_id):
            if (f.get("name") or "").strip().lower() == want:
                return f["id"]
        return ""

    def tasks(self, list_id: str, statuses: list[str] | None = None, include_closed: bool = False) -> list[dict]:
        out: list[dict] = []
        page = 0
        while True:
            params: dict = {"page": page, "include_closed": str(include_closed).lower(), "subtasks": "false"}
            if statuses:
                params["statuses[]"] = statuses
            data = self._req("GET", f"/list/{list_id}/task", params=params)
            out.extend(data.get("tasks", []))
            if data.get("last_page", True) or not data.get("tasks"):
                break
            page += 1
        return out

    def task(self, task_id: str) -> dict:
        return self._req("GET", f"/task/{task_id}", params={"include_markdown_description": "true"})

    # --- writes
    def set_field(self, task_id: str, field_id: str, value) -> None:
        self._req("POST", f"/task/{task_id}/field/{field_id}", json={"value": value})

    def comment(self, task_id: str, text: str) -> None:
        self._req("POST", f"/task/{task_id}/comment", json={"comment_text": text, "notify_all": False})


def _field_value(task: dict, name: str):
    want = name.strip().lower()
    if not want:
        return None
    fields = task.get("custom_fields") or []
    for f in fields:
        if (f.get("name") or "").strip().lower() == want:
            return f.get("value")
    # the link field has been renamed once already (Competition URL's -> Main Competitor):
    # fall back to any URL field whose name says competitor / competition
    if "compet" in want:
        for f in fields:
            if f.get("type") == "url" and "compet" in (f.get("name") or "").lower():
                return f.get("value")
    return None


# names the "pull now" column has had, in case it is renamed again (compared with spaces/case removed)
STATUS_ALIASES = ("ready for lp", "ready to lp", "ready for landing page", "ready to build", "lp pending", "pending lp", "pending")


def _norm(s: str) -> str:
    return "".join(ch for ch in (s or "").lower() if ch.isalnum())


def resolve_status(client: ClickUp, list_id: str, wanted: str) -> tuple[str, str]:
    """The list's real status name for `wanted`: exact (ignoring case/spaces), else a known alias.
    Returns (status, note); raises with the list's statuses when nothing fits."""
    statuses = [st.get("status", "") for st in client.list_info(list_id).get("statuses") or []]
    if not statuses:
        return wanted, ""
    by_norm = {_norm(st): st for st in statuses}
    if _norm(wanted) in by_norm:
        return by_norm[_norm(wanted)], ""
    for alias in STATUS_ALIASES:
        if _norm(alias) in by_norm:
            real = by_norm[_norm(alias)]
            return real, f"status '{wanted}' does not exist on the list any more; using '{real}' (set CLICKUP_STATUS to silence this)"
    raise ClickUpError(f"status '{wanted}' is not on the list, and none of the usual names are either. "
                       f"The list has: {', '.join(statuses)}. Set CLICKUP_STATUS in .env to the right one.")


def _truthy(v) -> bool:
    return v is True or str(v).strip().lower() in ("true", "1", "yes")


def product_rows(client: ClickUp, *, list_id: str | None = None, status: str | None = None, url_field: str | None = None,
                 done_field: str | None = None, include_done: bool = False) -> tuple[list[Row], str]:
    """Rows for `batch.process` from the ClickUp list: one per task in `status`, links from the URL
    field + the description. Tasks whose done-checkbox is ticked are left out unless include_done."""
    list_id = list_id or config.CLICKUP_LIST_ID
    status = status or config.CLICKUP_STATUS
    url_field = url_field or config.CLICKUP_URL_FIELD
    done_field = config.CLICKUP_DONE_FIELD if done_field is None else done_field
    rows: list[Row] = []
    no_link: list[str] = []
    done = 0
    status, status_note = resolve_status(client, list_id, status)
    if status_note:
        print(f"    {status_note}", flush=True)
    tasks = client.tasks(list_id, statuses=[status])
    for t in tasks:
        name = (t.get("name") or "").strip()
        if not include_done and _truthy(_field_value(t, done_field)):
            done += 1
            continue
        text = " ".join(x for x in (_field_value(t, url_field) or "", t.get("text_content") or "", t.get("description") or "") if x)
        if not t.get("text_content") and not t.get("description"):
            try:
                full = client.task(t["id"])
                text += " " + (full.get("text_content") or full.get("markdown_description") or "")
            except ClickUpError as e:
                log.debug("description of %s: %s", t.get("id"), e)
        urls = store_urls(text)
        if not urls:
            no_link.append(name or t.get("id", "?"))
            continue
        rows.append(Row(name=name, url=urls[0], source_row=0, extras=urls[1:], task_id=t.get("id", ""), task_url=t.get("url", "")))
    note = f"ClickUp list {list_id}, status '{status}'"
    if done:
        note += f", {done} already pulled"
    if no_link:
        note += ", no product link on: " + ", ".join(no_link[:6]) + (" ..." if len(no_link) > 6 else "")
    return rows, note


def mark_done(client: ClickUp, row: Row, folder: str, images: int, *, list_id: str | None = None,
              done_field: str | None = None, comment: bool | None = None) -> str:
    """Tick the checkbox and leave one comment on the task. Returns a short note for the log;
    never raises (the images are on disk, which is the part that matters)."""
    if not row.task_id:
        return ""
    list_id = list_id or config.CLICKUP_LIST_ID
    done_field = config.CLICKUP_DONE_FIELD if done_field is None else done_field
    comment = config.CLICKUP_COMMENT if comment is None else comment
    notes = []
    if done_field:                       # CLICKUP_DONE_FIELD= (empty) turns the checkbox off entirely
        try:
            fid = client.field_id(list_id, done_field)
            if fid:
                client.set_field(row.task_id, fid, True)
                notes.append(f"'{done_field}' ticked")
            else:
                notes.append(f"(no '{done_field}' checkbox on the list: add one so pulled tasks are skipped on other laptops)")
        except ClickUpError as e:
            notes.append(f"could not tick '{done_field}': {e}")
    if comment:
        try:
            links = "\n".join(f"- {u}" for u in row.urls)
            client.comment(row.task_id, f"Images pulled: {images} file(s) -> {Path(folder).name}\\competitor_imgs\n{links}")
            notes.append("comment posted")
        except ClickUpError as e:
            notes.append(f"could not comment: {e}")
    return "; ".join(notes)


def find_rows(client: ClickUp, query: str, *, list_id: str | None = None, url_field: str | None = None) -> list[Row]:
    """Rows for the cards whose name contains `query` (case-insensitive), or the card with that id or
    URL, in any status. Used by `imageGrabber.py pull "<name>"`."""
    import re
    list_id = list_id or config.CLICKUP_LIST_ID
    url_field = url_field or config.CLICKUP_URL_FIELD
    q = query.strip()
    m = re.search(r"app\.clickup\.com/t/(?:\d+/)?([A-Za-z0-9]+)", q)
    task_id = m.group(1) if m else (q if re.fullmatch(r"[a-z0-9]{6,12}", q) and not " " in q and any(ch.isdigit() for ch in q) else "")
    tasks: list[dict] = []
    if task_id:
        try:
            tasks = [client.task(task_id)]
        except ClickUpError:
            tasks = []
    if not tasks:
        want = _norm(q)
        tasks = [t for t in client.tasks(list_id, include_closed=True) if want in _norm(t.get("name", ""))]
        exact = [t for t in tasks if _norm(t.get("name", "")) == want]
        if exact:
            tasks = exact
    rows: list[Row] = []
    for t in tasks:
        text = " ".join(x for x in (_field_value(t, url_field) or "", t.get("text_content") or "", t.get("description") or "") if x)
        if not t.get("text_content") and not t.get("description"):
            try:
                full = client.task(t["id"])
                text += " " + (full.get("text_content") or full.get("markdown_description") or "")
            except ClickUpError:
                pass
        urls = store_urls(text)
        rows.append(Row(name=(t.get("name") or "").strip(), url=urls[0] if urls else "", source_row=0, extras=urls[1:],
                        task_id=t.get("id", ""), task_url=t.get("url", "")))
    return rows
