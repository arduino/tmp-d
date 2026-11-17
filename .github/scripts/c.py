# SPDX-FileCopyrightText: Copyright (C) Arduino s.r.l. and/or its affiliated companies
#
# SPDX-License-Identifier: MPL-2.0

from __future__ import annotations

import os
import re
import sys
import uuid
from pathlib import Path

D = Path("d")
O = "o"
RE = re.compile(r"^[a-z][a-z0-9_]{0,39}$")


class E(Exception):
    pass


def fields(path: str) -> dict[str, str]:
    out: dict[str, str] = {}
    key = None
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.startswith("### "):
            key = line[4:].strip().lower()
            out[key] = ""
        elif key is not None:
            out[key] += line + "\n"
    return {k: ("" if v.strip() == "_No response_" else v.strip()) for k, v in out.items()}


def name(value: str) -> str:
    if not RE.match(value):
        raise E(f"`{value}`: `[a-z][a-z0-9_]*`")
    return value


def members(k: str) -> list[str]:
    path = D / k / O
    if not path.is_file():
        return []
    return [line.split()[0].lstrip("@") for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def has(k: str, user: str) -> bool:
    return user.lower() in (m.lower() for m in members(k))


def done(**values: str) -> int:
    lines = []
    for key, value in values.items():
        mark = f"EOF_{uuid.uuid4().hex}"
        lines.append(f"{key}<<{mark}\n{value}\n{mark}\n")
    target = os.environ.get("GITHUB_OUTPUT")
    if target:
        with open(target, "a", encoding="utf-8") as out:
            out.writelines(lines)
    else:
        print("".join(lines), end="")
    return 0


def main(fn) -> None:
    body, user, issue = sys.argv[1:4]
    try:
        sys.exit(done(ok="true", **fn(fields(body), user, issue)))
    except E as err:
        sys.exit(done(ok="false", e=str(err)))
