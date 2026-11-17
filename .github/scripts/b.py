# SPDX-FileCopyrightText: Copyright (C) Arduino s.r.l. and/or its affiliated companies
#
# SPDX-License-Identifier: MPL-2.0

from __future__ import annotations

import shutil

from c import D, E, has, main, name


def run(f: dict[str, str], user: str, issue: str) -> dict[str, str]:
    kv = f.get("id", "")
    if kv.count(":") != 1:
        raise E(f"`{kv}`: `k:v`")
    k, v = (name(x) for x in kv.split(":"))
    if not (D / k / v).is_dir():
        raise E(f"`{k}:{v}` not found")
    if not has(k, user):
        raise E(f"`{k}`: not allowed")
    shutil.rmtree(D / k / v)
    return {"branch": f"b/{issue}-{k}-{v}", "files": str(D / k / v), "title": f"- {k}:{v}"}


main(run)
