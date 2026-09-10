# Backlog de Construção Civil — Painel

Painel HTML estático que exibe o board "Backlog de Atividades - Construção Civil"
do Monday.com (id 18430512760), no mesmo padrão visual do painel de Manutenção.

## Como publicar (GitHub Pages)

1. Crie um repositório novo no GitHub (ex: `BacklogConstrucao`), público ou privado
   (privado também funciona com GitHub Pages em contas pagas; em contas gratuitas
   o Pages exige repositório público).
2. Suba estes arquivos para a raiz do repositório, mantendo a pasta `.github/workflows/`:
   - `index.html`
   - `fetch_data.py`
   - `data.json`
   - `.github/workflows/update-data.yml`
3. Em **Settings → Secrets and variables → Actions → New repository secret**,
   crie o secret `MONDAY_API_TOKEN` com o seu token de API do Monday.com
   (Avatar → Administração → API, ou Perfil → Developers → My access tokens).
4. Em **Settings → Pages**, configure "Deploy from a branch", branch `main`,
   pasta `/ (root)`.
5. Em **Actions**, rode manualmente o workflow "Atualizar dados do backlog"
   uma primeira vez (botão "Run workflow") para gerar o `data.json` com dados reais.
6. O painel ficará disponível em:
   `https://<seu-usuario>.github.io/<nome-do-repositorio>/`

## Atualização automática

O workflow roda a cada 5 minutos (`*/5 * * * *`), busca os dados do board no
Monday.com e faz commit do `data.json` atualizado. O GitHub não garante execução
exata no minuto — pode haver alguns minutos de atraso, principalmente em
repositórios gratuitos.

## Estrutura de dados (data.json)

Cada item traz: atividade (nome), data de solicitação, data de execução,
ordem de serviço, status, prioridade e solicitante (texto livre).
