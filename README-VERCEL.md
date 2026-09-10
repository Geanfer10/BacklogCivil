# BacklogCivil no Vercel

Arquivos para adicionar/substituir no seu repositório **Geanfer10/BacklogCivil**:

- `index.html` (substitui o atual — agora busca os dados via `/api/data` em vez de `data.json`)
- `api/data.js` (função serverless nova — busca o board ao vivo no Monday)

Depois de subir esses arquivos, os antigos `fetch_data.py`, `data.json` e
`.github/workflows/update-data.yml` podem ficar no repositório sem problema
(não atrapalham), ou você pode apagá-los se quiser deixar tudo mais limpo —
eles não são mais usados.

## Passo a passo

1. No repositório `BacklogCivil`, suba/substitua os arquivos `index.html` e
   `api/data.js` (mantendo a pasta `api/`).
2. Acesse [vercel.com](https://vercel.com), faça login com sua conta do GitHub.
3. Clique em **"Add New" → "Project"** e selecione o repositório `BacklogCivil`.
4. Em "Framework Preset", deixe **"Other"**. Clique em **Deploy**.
5. Vá em **Settings → Environment Variables** e crie:
   - Name: `MONDAY_API_TOKEN`
   - Value: seu token de API do Monday
   - Marque Production, Preview e Development
6. Salve, volte em **Deployments**, clique nos "..." do último deploy e escolha
   **Redeploy** (necessário para a variável entrar em vigor).
7. O Vercel vai te dar uma URL, algo como `https://backlog-civil.vercel.app` —
   esse já é o painel completo, atualizado em tempo real a cada acesso.
