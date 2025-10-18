# Testworld - Local Development

This project runs fully locally using Vite (React + TS), Supabase (Docker via CLI), and Ollama for AI generation.

## Prerequisites
- Node.js 18+ and npm
- Docker Desktop
- Supabase CLI (`brew install supabase/tap/supabase` or see docs)
- Ollama installed and running (`brew install ollama`)

## Install & Run Web App
```sh
npm i
npm run dev
```

## Run Supabase locally
Initialize and start the local stack (Postgres, API, Studio, Edge Runtime):
```sh
# From the project root where the supabase/ directory exists
supabase start

# Apply existing migrations (if not automatically applied)
supabase db reset --no-backup --force

# In a separate terminal, link the project locally (optional)
# supabase link --project-ref <local>
```

- Supabase Studio: http://localhost:54323
- API URL and anon key are provided by `supabase start` output.

Create a `.env.local` file for the Vite app with your local Supabase creds:
```sh
# Vite reads import.meta.env.*
VITE_SUPABASE_URL=http://localhost:54321
VITE_SUPABASE_PUBLISHABLE_KEY=anon-key-from-supabase-start
```

## Edge Functions
To run and test the edge function locally:
```sh
# Start edge functions dev server
supabase functions serve --env-file .env.local --no-verify-jwt

# In the app, we invoke: supabase.functions.invoke('generate-entity', ...)
# The SDK will call the local functions endpoint when VITE_SUPABASE_URL points to localhost.
```

## Ollama for AI
Install and start Ollama, then pull a chat model:
```sh
ollama serve &
ollama pull llama3.1
```
The edge function `supabase/functions/generate-entity/index.ts` calls `http://localhost:11434/api/chat` with model `llama3.1`.

## Development Notes
- We removed Lovable tooling and external AI calls. All AI goes through Ollama locally.
- Update OpenGraph/Twitter images in `index.html` as needed (currently `/public/placeholder.svg`).

## Build & Preview
```sh
npm run build
npm run preview
```
