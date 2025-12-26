# YedidAI: A Hebrew RAG-based Assistant for Social Rights


The full project report is available in LaTeX at [`Final_Report.pdf`](./Final_Report.pdf).

This system is aimed at producing concise, actionable guidance in Hebrew, while surfacing relevant legal/administrative references.

We named the project "YedidAI" (Hebrew: "AI ידיד" or "ידידיי"), "yedid" = friend, "yedidai" = my friends, deliberately: it conveys "your AI friend" and reflects our goal to be a compassionate, helpful assistant for people in need.

## Abstract

We present YedidAI, a prototypical retrieval-augmented generation (RAG) system designed to assist Hebrew-speaking users in understanding and exercising social and legal rights in Israel. The pipeline integrates a dense semantic search index (SentenceTransformers) over curated rights pages with a conversational front-end driven by large language models (Anthropic / OpenAI). The project was motivated by the confusion and information gaps following the October 7th war in Israel: many evacuees, injured soldiers and civilians, families of hostages, and bereaved families were unsure of their entitlements or how to locate relevant guidance on the KolZchut (https://www.kolzchut.org.il/he/%D7%A2%D7%9E%D7%95%D7%93_%D7%A8%D7%90%D7%A9%D7%99) website. YedidAI aims to provide a conversational interface where users can describe their situation in free text, receive clarifying questions, and obtain personalized rights and links to authoritative pages.

## Introduction

Accessing authoritative, personalized information about rights and entitlements can be challenging. This work was motivated by the confusion at the beginning of the October 7th war in Israel, when many people who deserved rights and assistance (evacuees, injured soldiers and civilians, families of hostages, bereaved families, and others) were either unaware of their entitlements or unable to find the relevant information on the KOLZchut website.

YedidAI addresses this gap by combining information retrieved from a structured corpus of Israeli rights pages with an empathetic, social-worker-style conversational agent. 
Our goal was to create a chatbot that allows users to tell their story in free language, asks clarifying follow-up questions to uncover missing or forgotten details, and returns the likely entitlements along with links to authoritative pages for next steps.
The system is aimed at producing concise, actionable guidance in Hebrew, while surfacing relevant legal/administrative references.

## Related Work

YedidAI follows the RAG design pattern (retrieval + generation) used in recent work that improved grounding and factuality in knowledge-intensive tasks. We also adopt domain-specific prompt/system prompt designs inspired by legal and public-advice systems.

## Dataset

The project uses a curated JSON corpus (derived from public rights pages / XML dumps) covering domains such as disability benefits, pensions, parking permits for disabled people, and employment rights. Documents include structured fields ("title", "eligibility_section", "full_text"). Embeddings are serialized (data/embedded_data.json) for efficient retrieval.

## Methodology

- **Retrieval:** Embed passages using `paraphrase-multilingual-MiniLM-L12-v2` (SentenceTransformers) and perform cosine-similarity retrieval to obtain top-k relevant passages.
- **Generation / Conversational Flow:** A chat component manages dialogue (system prompt mimics an empathetic social worker in Hebrew). After building a short user profile, the system retrieves supporting passages and prompts an LLM (Anthropic or OpenAI) to produce succinct, actionable guidance in Hebrew.
- **Safety & Policy:** System prompts enforce brevity, empathy, and factual grounding; the system avoids offering professional legal advice and includes a safety/escalation plan.

## Implementation Details

Key files:

- `src/rag.py` — semantic search engine (embed, save/load, semantic_search)
- `src/chatbot.py` — conversational loop and prompts
- `src/anthropic_wrapper.py`, `src/openai_tools.py` — LLM wrappers and system prompts
- `src/app.py` — Gradio interface and orchestration

Environment variables (API keys, chosen model) drive the system behavior.

## Experiments and Results

Current evaluation is qualitative:

- Retrieval returns semantically relevant passages for typical queries.
- LLMs produce empathetic, actionable responses when provided with retrieved context and clear prompts.
- Observed issues include hallucination when retrieval fails to surface key evidence, inconsistent citations, and occasional verbosity.

We recommend quantitative evaluation (precision@k for retrieval, automatic overlap metrics for grounding) and human evaluation for helpfulness and clarity.

## Conclusions and Future Work

YedidAI shows initial promise as a RAG-based assistant for rights-related queries in Hebrew. Next steps:

1. Quantitative and human evaluation and creation of an evaluation dataset.
2. Add provenance tokens and explicit citations for all claims.
3. Implement safety and escalation flows (when to advise professional consultation).
4. Improve indexing, passage-level retrieval, and caching to reduce latency.

## Acknowledgements

Thanks to contributors and to public sources of rights information used to compile the dataset.