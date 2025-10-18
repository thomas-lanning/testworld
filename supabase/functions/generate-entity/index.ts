import { serve } from "https://deno.land/std@0.168.0/http/server.ts";

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
};

serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response(null, { headers: corsHeaders });
  }

  try {
    const { companyData } = await req.json();

    console.log('Generating entity profile via Ollama for:', companyData?.substring?.(0, 100));

    const systemPrompt = `You are an expert business analyst. Analyze the provided company information and create a detailed personality profile. Extract and synthesize exactly the following fields:
- name: Company name (string)
- who_they_are: 2-3 sentence description of the company's identity and core business (string)
- goals: Primary business objectives and strategic aims (string, not an array)
- risk_appetite: How the company approaches risk - use one of: conservative, moderate, aggressive (string)
- market_position: Their position in the market - use one of: leader, challenger, niche player, emerging (string)
- leadership_style: Management and decision-making approach (string)

Return ONLY a valid JSON object with these exact keys and ALL VALUES MUST BE STRINGS (not arrays or objects). Do not include code fences, backticks, or any preamble.`;

    const userPrompt = `Analyze this company data and create a personality profile:\n\n${companyData}`;

    // Configurable Ollama endpoint (local by default) and optional API key for Ollama Cloud
    const OLLAMA_API_URL = Deno.env.get("OLLAMA_API_URL") || "http://localhost:11434";
    const OLLAMA_API_KEY = Deno.env.get("OLLAMA_API_KEY");
    const OLLAMA_MODEL = Deno.env.get("OLLAMA_MODEL") || "llama3.1";

    const baseUrl = OLLAMA_API_URL.replace(/\/$/, "");
    const isCloud = /(api\.ollama\.ai|openai|anthropic|groq|xai|azure)/i.test(baseUrl);
    const endpoint = isCloud ? `${baseUrl}/v1/chat/completions` : `${baseUrl}/api/chat`;

    const headers: Record<string, string> = { "Content-Type": "application/json" };
    if (OLLAMA_API_KEY) {
      headers["Authorization"] = `Bearer ${OLLAMA_API_KEY}`;
    }

    const requestBody = isCloud
      ? {
          model: OLLAMA_MODEL,
          messages: [
            { role: "system", content: systemPrompt },
            { role: "user", content: userPrompt }
          ],
          stream: false,
        }
      : {
          model: OLLAMA_MODEL,
          messages: [
            { role: "system", content: systemPrompt },
            { role: "user", content: userPrompt }
          ],
          stream: false,
        };

    const response = await fetch(endpoint, {
      method: "POST",
      headers,
      body: JSON.stringify(requestBody),
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error("Ollama error:", response.status, errorText);
      return new Response(
        JSON.stringify({ error: `Ollama error: ${response.status}` }),
        { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    const data = await response.json();

    // Handle response parsing for local vs. cloud
    const contentRaw = isCloud
      ? (data?.choices?.[0]?.message?.content ?? "")
      : (data?.message?.content ?? data?.messages?.[data?.messages?.length - 1]?.content ?? "");

    const content = String(contentRaw).replace(/```json\s*/g, '').replace(/```\s*/g, '').trim();

    let entityProfile;
    try {
      entityProfile = JSON.parse(content);
    } catch (e) {
      console.error("Failed to parse Ollama JSON, returning fallback shape. Raw:", content);
      entityProfile = {
        name: "Unknown Company",
        who_they_are: "No description provided.",
        goals: "Unknown",
        risk_appetite: "moderate",
        market_position: "niche player",
        leadership_style: "data-driven",
      };
    }

    return new Response(
      JSON.stringify({ profile: entityProfile }),
      { headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  } catch (error) {
    console.error("Error generating entity:", error);
    return new Response(
      JSON.stringify({ error: error instanceof Error ? error.message : "Unknown error" }),
      { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  }
});