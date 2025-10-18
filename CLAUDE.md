# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a React + TypeScript application for creating AI-generated company entity profiles and visualizing business relationships through an interactive network graph. The app uses Vite for development, Supabase for backend services (Postgres, Edge Functions), and Ollama for local AI generation. All tooling is designed to run 100% locally without external API dependencies.

## Development Commands

### Web Application
```bash
npm i                    # Install dependencies
npm run dev              # Start dev server at http://localhost:8080
npm run build            # Production build
npm run build:dev        # Development mode build
npm run preview          # Preview production build
npm run lint             # Run ESLint
```

### Supabase Local Stack
```bash
supabase start                           # Start local Postgres, API, Studio, Edge Functions
supabase db reset --no-backup --force   # Reset database and apply migrations
supabase functions serve --env-file .env.local --no-verify-jwt  # Start edge functions dev server
supabase stop                            # Stop all services
```

Supabase Studio runs at http://localhost:54323 for database management.

### Ollama (AI Generation)
```bash
ollama serve &          # Start Ollama service
ollama pull llama3.1    # Download the LLaMA 3.1 model
```

## Architecture

### Frontend Stack
- **Framework**: React 18 + TypeScript
- **Bundler**: Vite 5 with SWC plugin for fast refresh
- **UI Components**: shadcn/ui (Radix UI primitives + Tailwind CSS)
- **State Management**: React useState/useEffect with TanStack React Query for server state
- **Routing**: React Router v6
- **Styling**: Tailwind CSS with custom theme via CSS variables

### Backend Architecture
- **Database**: Supabase Postgres with three main tables:
  - `companies`: AI-generated entity profiles with personality traits (name, who_they_are, goals, risk_appetite, market_position, leadership_style)
  - `relationships`: Directed connections between companies with labels and strength (0-1 scale)
  - `projects`: Saved simulation states containing company/relationship IDs and layout data
- **Edge Functions**: Deno-based functions in `supabase/functions/` directory
  - `generate-entity`: Calls Ollama API to analyze company data and generate structured personality profiles
- **Storage**: `company-uploads` bucket for file uploads (though currently unused)
- **RLS Policies**: All tables have public access policies (no authentication yet - Phase 1)

### Key Application Flow
1. User uploads company data via file/text/URL in `UploadSection`
2. Data sent to `generate-entity` Edge Function
3. Edge Function calls Ollama (llama3.1 model) with structured prompt
4. AI returns JSON profile parsed and saved to `companies` table
5. Company node appears in `NetworkVisualization` canvas
6. Users drag between nodes to create relationships via `RelationshipCreator` dialog
7. Projects can be saved/loaded via `ProjectManager` to persist entire simulation state

### Component Organization
```
src/
├── components/
│   ├── simulation/          # Core simulation features
│   │   ├── NetworkVisualization.tsx    # SVG canvas with draggable nodes/edges
│   │   ├── CompanyNode.tsx            # Individual draggable node UI
│   │   ├── UploadSection.tsx          # Multi-tab data input (file/text/URL)
│   │   ├── RelationshipCreator.tsx    # Dialog for defining edge properties
│   │   └── ProjectManager.tsx         # Save/load simulation state
│   ├── ui/                  # shadcn/ui components (buttons, cards, dialogs, etc.)
│   └── NetworkBackground.tsx
├── pages/
│   ├── Home.tsx            # Landing page
│   ├── Simulation.tsx      # Main simulation orchestrator
│   └── NotFound.tsx
├── integrations/supabase/
│   ├── client.ts           # Supabase client instance
│   └── types.ts            # Auto-generated DB types
└── lib/utils.ts            # Tailwind merge utilities
```

### Path Alias
The project uses `@/` as an alias for `src/` directory. All imports use this convention (e.g., `@/components/ui/button`).

## Configuration Files

### Environment Variables
Create `.env.local` at project root:
```
VITE_SUPABASE_URL=http://localhost:54321
VITE_SUPABASE_PUBLISHABLE_KEY=<anon-key-from-supabase-start>
```

For edge functions, create `supabase/functions/generate-entity/.env`:
```
OLLAMA_API_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1
OLLAMA_API_KEY=              # Optional, for Ollama Cloud or other providers
```

### TypeScript Configuration
- Relaxed mode: `noImplicitAny: false`, `strictNullChecks: false`
- Type safety is minimal; expect `any` casts, especially around Supabase queries

## Important Implementation Details

### Ollama Edge Function
The `generate-entity` function supports both local Ollama and cloud-based providers:
- Local: `http://localhost:11434/api/chat` (Ollama format)
- Cloud: `/v1/chat/completions` endpoint (OpenAI-compatible format)

Detection is pattern-based on `OLLAMA_API_URL`. The function returns a strict JSON schema for company profiles and includes fallback parsing if the model returns malformed JSON.

### Network Visualization
- Uses raw SVG for relationship rendering with quadratic Bezier curves
- Nodes are absolutely positioned `div` elements with drag-and-drop
- Relationship strength maps to line width and opacity
- Arrow markers defined in SVG `<defs>` and referenced via `markerEnd`
- Temporary drag connections shown with dashed lines during relationship creation

### Database Schema Notes
- Relationship `strength` is DECIMAL(3,2) constrained 0-1
- Projects store `company_ids` and `relationship_ids` as UUID arrays
- `layout_data` is JSONB for storing node positions and other metadata
- All IDs use UUIDs generated by Postgres `gen_random_uuid()`

## Testing & Quality

This project currently has:
- No test suite
- ESLint configured but with minimal rules
- No CI/CD pipeline
- No E2E tests

When adding tests in the future, consider using Vitest (already Vite-compatible).

## Python API Client

A Python client library is available in `python_api/` for programmatic data population:

### Quick Usage
```bash
cd python_api
pip install -r requirements.txt
python testworld_client.py  # Test connection
python example_usage.py      # Run examples
```

### Common Operations
```python
from testworld_client import TestworldClient

client = TestworldClient()

# Create company with AI
company = client.create_company_from_ai("Company description...")

# Create relationship
client.create_relationship(
    source_company_id=company1['id'],
    target_company_id=company2['id'],
    label="Partner",
    strength=0.8
)

# Query data
companies = client.get_companies()
```

### Use Cases
- **Web scraping**: Automatically populate from Wikipedia, APIs, etc.
- **Bulk imports**: Load from CSV, JSON, databases
- **Network generation**: Create simulated company networks
- **Data migration**: Transfer data from other sources

See `python_api/README.md` for complete documentation.

## Known Constraints

- No authentication system (all data publicly accessible via RLS policies)
- Ollama must be running locally before edge functions work
- File uploads only support `.txt` files (PDFs require parsing library)
- TypeScript strict mode is disabled, leading to potential runtime errors
- Network visualization does not support zoom/pan (fixed viewport)
