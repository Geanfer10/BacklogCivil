// api/board-construcao.js
// Busca os dados do board "Backlog de Atividades - Construção Civil" (id 18430512760)
// diretamente no Monday.com a cada requisição. Sem cache — sempre em tempo real.

const BOARD_ID = "18430512760";

const GROUP_ORDER = ["topics", "group_mm72zwqs", "group_mm72f941", "group_mm72xfpz"];

const QUERY = `
query ($boardId: [ID!]) {
  boards(ids: $boardId) {
    groups { id title }
    items_page(limit: 500) {
      items {
        id
        name
        group { id title }
        column_values(ids: [
          "date_mm72jn36", "date_mm72vm92", "text_mm72dhsw",
          "color_mm72t2m8", "color_mm729h5r", "text_mm722d2b"
        ]) {
          id
          text
        }
        assets { id public_url }
      }
    }
  }
}`;

export default async function handler(req, res) {
  try {
    const token = process.env.MONDAY_API_TOKEN;
    if (!token) {
      res.status(500).json({ error: "MONDAY_API_TOKEN não configurado no Vercel" });
      return;
    }

    const mondayRes = await fetch("https://api.monday.com/v2", {
      method: "POST",
      headers: {
        Authorization: token,
        "Content-Type": "application/json",
        "API-Version": "2024-10",
      },
      body: JSON.stringify({ query: QUERY, variables: { boardId: [BOARD_ID] } }),
    });

    const body = await mondayRes.json();
    if (body.errors) {
      res.status(502).json({ error: "Erro na API do Monday", details: body.errors });
      return;
    }

    const board = body.data.boards[0];
    const groupsMeta = Object.fromEntries(board.groups.map(g => [g.id, g.title]));
    const itemsByGroup = Object.fromEntries(GROUP_ORDER.map(id => [id, []]));

    for (const item of board.items_page.items) {
      const colMap = Object.fromEntries(item.column_values.map(cv => [cv.id, cv.text || ""]));
      const fotos = (item.assets || []).map(a => a.public_url).filter(Boolean);
      const record = {
        id: item.id,
        atividade: item.name,
        data_solicitacao: colMap["date_mm72jn36"] || "",
        data_execucao: colMap["date_mm72vm92"] || "",
        ordem_servico: colMap["text_mm72dhsw"] || "",
        status: colMap["color_mm72t2m8"] || "",
        prioridade: colMap["color_mm729h5r"] || "",
        solicitante: colMap["text_mm722d2b"] || "",
        fotos,
      };
      const groupId = item.group.id;
      if (!itemsByGroup[groupId]) itemsByGroup[groupId] = [];
      itemsByGroup[groupId].push(record);
    }

    const payload = {
      generated_at: new Date().toISOString(),
      groups: GROUP_ORDER.map(id => ({
        id,
        title: groupsMeta[id] || id,
        items: itemsByGroup[id] || [],
      })),
    };

    res.setHeader("Cache-Control", "no-store");
    res.status(200).json(payload);
  } catch (err) {
    res.status(500).json({ error: "Erro interno", details: String(err) });
  }
}
