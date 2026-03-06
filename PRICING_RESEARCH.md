# LLM Provider Pricing Research

**Date:** March 2026
**Model:** Gemini 2.5 Flash

## Pricing Comparison

| Provider | Input (per 1M tokens) | Output (per 1M tokens) | Notes |
|---|---|---|---|
| **OpenRouter** (`google/gemini-2.5-flash`) | $0.30 | $2.50 | Via Google AI Studio provider |
| **Google AI Direct** (`gemini-2.5-flash`) | $0.30 | $2.50 | Direct Gemini API |

## Key Findings

1. **Pricing is identical** — Both OpenRouter (via Google AI Studio provider) and Google AI direct charge the same rates: $0.30/M input, $2.50/M output.

2. **Google AI Free Tier** — Google provides free access to Gemini 2.5 Flash with rate limits (5-15 RPM depending on the model). This is useful for development/testing but not suitable for production workloads.

3. **Cost Optimization** (Google AI Direct only):
   - **Batch processing**: 50% discount for async/non-urgent workloads
   - **Context caching**: Cache reads cost 10% of base input price

4. **Alternative models**:
   - `gemini-2.5-flash-lite`: $0.10/M input, $0.40/M output (cheaper but less capable)
   - `gemini-2.5-pro`: $1.25/M input, $10.00/M output (more capable but ~4x more expensive)

## Recommendation

Since pricing is the same, the choice comes down to operational factors:

- **Keep OpenRouter as default** — simpler setup, single API key for multiple models, OpenAI-compatible API format
- **Add Google AI as alternative** — useful for context caching (10% input cost on cache hits), batch processing (50% discount), and the free tier for development

The provider abstraction layer should support both, configurable via `LLM_PROVIDER` env var.

## Sources

- [OpenRouter — Gemini 2.5 Flash](https://openrouter.ai/google/gemini-2.5-flash)
- [Google AI Gemini API Pricing](https://ai.google.dev/gemini-api/docs/pricing)
