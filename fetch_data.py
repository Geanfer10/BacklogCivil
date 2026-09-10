#!/usr/bin/env python3
"""
Busca os itens do board "Backlog de Atividades - Construção Civil" no Monday.com
e gera o arquivo data.json consumido pelo painel HTML (index.html).

Requer a variável de ambiente MONDAY_API_TOKEN (secret do GitHub Actions).
"""

import json
import os
import sys
import urllib.request

BOARD_ID = "18430512760"

COLUMN_IDS = {
    "data_solicitacao": "date_mm72jn36",
    "data_execucao": "date_mm72vm92",
    "ordem_servico": "text_mm72dhsw",
    "status": "color_mm72t2m8",
    "prioridade": "color_mm729h5r",
    "solicitante": "text_mm722d2b",
}

GROUP_ORDER = ["topics", "group_mm72zwqs", "group_mm72f941", "group_mm72xfpz"]

QUERY = """
query ($boardId: [ID!]) {
  boards(ids: $boardId) {
    groups {
      id
      title
    }
    items_page(limit: 500) {
      items {
        id
        name
        group {
          id
          title
        }
        column_values(ids: [
          "date_mm72jn36", "date_mm72vm92", "text_mm72dhsw",
          "color_mm72t2m8", "color_mm729h5r", "text_mm722d2b"
        ]) {
          id
          text
        }
      }
    }
  }
}
"""


def gql(token, query, variables):
    req = urllib.request.Request(
        "https://api.monday.com/v2",
        data=json.dumps({"query": query, "variables": variables}).encode("utf-8"),
        headers={
            "Authorization": token,
            "Content-Type": "application/json",
            "API-Version": "2024-10",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = json.loads(resp.read().decode("utf-8"))
    if "errors" in body:
        raise RuntimeError(body["errors"])
    return body["data"]


def main():
    token = os.environ.get("MONDAY_API_TOKEN")
    if not token:
        print("ERRO: variável de ambiente MONDAY_API_TOKEN não definida", file=sys.stderr)
        sys.exit(1)

    data = gql(token, QUERY, {"boardId": [BOARD_ID]})
    board = data["boards"][0]

    groups_meta = {g["id"]: g["title"] for g in board["groups"]}

    items_by_group = {gid: [] for gid in GROUP_ORDER}

    for item in board["items_page"]["items"]:
        col_map = {cv["id"]: (cv["text"] or "") for cv in item["column_values"]}
        group_id = item["group"]["id"]
        record = {
            "id": item["id"],
            "atividade": item["name"],
            "data_solicitacao": col_map.get(COLUMN_IDS["data_solicitacao"], ""),
            "data_execucao": col_map.get(COLUMN_IDS["data_execucao"], ""),
            "ordem_servico": col_map.get(COLUMN_IDS["ordem_servico"], ""),
            "status": col_map.get(COLUMN_IDS["status"], ""),
            "prioridade": col_map.get(COLUMN_IDS["prioridade"], ""),
            "solicitante": col_map.get(COLUMN_IDS["solicitante"], ""),
        }
        items_by_group.setdefault(group_id, []).append(record)

    output = {
        "generated_at": __import__("datetime").datetime.utcnow().isoformat() + "Z",
        "groups": [
            {
                "id": gid,
                "title": groups_meta.get(gid, gid),
                "items": items_by_group.get(gid, []),
            }
            for gid in GROUP_ORDER
        ],
    }

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"data.json gerado com sucesso ({sum(len(g['items']) for g in output['groups'])} itens)")


if __name__ == "__main__":
    main()
