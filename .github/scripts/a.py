# SPDX-FileCopyrightText: Copyright (C) Arduino s.r.l. and/or its affiliated companies
#
# SPDX-License-Identifier: MPL-2.0

from __future__ import annotations

from c import D, E, O, has, main, members, name


def run(f: dict[str, str], user: str, issue: str) -> dict[str, str]:
    k = name(f.get("k", ""))
    v = name(f.get("v", ""))
    files = []
    if members(k):
        if not has(k, user):
            raise E(f"`{k}`: " + ", ".join(f"@{m}" for m in members(k)))
    elif (D / k).is_dir() and any(p.is_dir() for p in (D / k).iterdir()):
        raise E(f"`{k}`: no `{O}`")
    else:
        (D / k).mkdir(parents=True, exist_ok=True)
        (D / k / O).write_text(f"{user}\n", encoding="utf-8")
        files.append(D / k / O)
    if (D / k / v).exists():
        raise E(f"`{k}:{v}` exists")
    (D / k / v).mkdir(parents=True)
    (D / k / v / "m.yaml").write_text(f"id: {k}:{v}\nby: {user}\nn: {issue}\n", encoding="utf-8")
    files.append(D / k / v / "m.yaml")
    return {"branch": f"a/{issue}-{k}-{v}", "files": " ".join(map(str, files)), "title": f"{k}:{v}"}


main(run)
