---
title: Used Karpathy’s LLM Wiki to Turn Claude Code into a Self-Evolving System
source: https://x.com/intheworldofai/status/2041632641716514947
author:
  - "[[@intheworldofai]]"
published: 2026-04-08
created: 2026-04-11
description: Most of us use Claude Code as a powerful pair programmer.0:14We paste context, ask for features or fixes, and get decent code back.But the n...
tags:
  - 📂Project/LLMWiki
image: https://abs.twimg.com/rweb/ssr/default/v2/og/image.png
---

![画像](https://pbs.twimg.com/media/HFVUlmiXQAAJ7Go?format=jpg&name=large)

Most of us use Claude Code as a powerful pair programmer.

<video preload="none" tabindex="-1" playsinline="" aria-label="埋め込み動画" poster="https://pbs.twimg.com/amplify_video_thumb/2041631212553564162/img/EIg5u3vnDU2PlRX-.jpg" style="width: 100%; height: 100%; position: absolute; background-color: black; top: 0%; left: 0%; transform: rotate(0deg) scale(1.005);" eagle-collectable="true"><source type="video/mp4" src="blob:https://x.com/9dc983aa-f006-4f40-9e95-1cd62372e743"></video>

0:14

We paste context, ask for features or fixes, and get decent code back.

But the next session? It often forgets key decisions, repeats patterns you already rejected, or lacks awareness of your existing components and business rules.

This is **Context Amnesia** - and it kills momentum on larger projects.

Andrej Karpathy recently shared a better pattern in his viral post and accompanying **LLM Wiki** gist.

![画像](https://pbs.twimg.com/media/HFVTsbhXcAAsvM2?format=jpg&name=large)

Gist format of LLM WIKI by Andrej Karpathy

Instead of treating the LLM as a stateless code generator, use it to **build and maintain a persistent, self-updating knowledge base** - a living wiki of interconnected Markdown files.

Raw sources go in → the LLM compiles, summarizes, links, and maintains everything → your AI becomes dramatically smarter over time.

I took this exact idea and applied it to my **frontend + CRM project**.

I fed Claude Code my React/TypeScript codebase, Shadcn/ui components, CRM requirements, API specs, and past decisions.

What happened next was eye-opening: it built a **fully updating dashboard**, pulled in the right Shadcn packages, maintained consistency with my design system, and continuously updated its own wiki with new architecture insights, component relationships, and rationale.

![画像](https://pbs.twimg.com/media/HFVVCzAW0AAf6EW?format=jpg&name=large)

**Here’s the complete walkthrough - including exactly how I set it up.**

The Core Idea: From Throwaway Answers to a Compounding Wiki

Traditional prompting or basic RAG throws raw documents at the model every time. Knowledge doesn’t accumulate.

Karpathy’s LLM Wiki changes that:

- You maintain a raw/ folder with source materials (code files, docs, notes, images, etc.).
- The LLM **incrementally compiles** these into a clean wiki/ directory of structured Markdown files: summaries, entity pages, concept articles, backlinks, and indexes.
- The wiki is persistent and becomes the primary context for future work.
- The LLM also maintains the wiki: it flags contradictions, suggests new connections, updates pages when new information arrives, and even files your own outputs (like generated code explanations) back into the system.

Result: Your AI develops real, long-term expertise in your project instead of starting fresh every time.

What Happened in My Project - I pointed Claude Code at my frontend repo and CRM-related sources.

Following the LLM Wiki pattern, I asked it to ingest everything and build a living knowledge base. It:

- Discovered and documented all existing Shadcn components
- Created interlinked pages for data models, user flows, and architecture decisions
- When I asked for a **fully updating dashboard**, it referenced the wiki for existing patterns, chose appropriate Shadcn packages, ensured consistency, and then updated the wiki with the new implementation details, component relationships, and rationale
- Over multiple sessions, outputs kept getting smarter - it started proactively suggesting improvements based on earlier decisions and catching potential inconsistencies

It felt like working with a senior engineer who had deeply internalized the entire project and was actively evolving its understanding.

Step-by-Step Setup Guide (Copy-Paste Ready)

Here’s exactly how to replicate this (takes ~5–15 minutes to start, then compounds):

1. **Create the Folder Structure** Pick a dedicated directory for your LLM Wiki (I recommend keeping it separate from your main code repo to keep things clean):

```plaintext
my-llm-wiki/
├── raw/          # Drop all source materials here (code files, PDFs, meeting notes, exported sessions, web clips, images, etc.)
├── wiki/         # The compiled, structured knowledge base (LLM-maintained)
│   ├── index.md
│   ├── concepts/
│   ├── entities/
│   ├── components/     # e.g., for Shadcn or React components
│   ├── decisions/
│   └── summaries/
└── schema.md     # Your "rules of the wiki" (like CLAUDE.md) — critical for consistency
```

1. **Start with Karpathy’s Idea File** Go to the gist: [https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)Copy the entire content. Paste it into a new Claude Code session as your starting prompt. Tell Claude: “Build me a complete LLM Wiki system based on this idea file. I use Obsidian for viewing. Create the folder structure if needed, define a good schema.md, and give me clear step-by-step instructions on how to ingest sources and have you maintain the wiki.”
2. **Define Your Schema (schema.md)** This is the “constitution” for how the LLM should behave. Include: - Folder conventions - Naming rules for pages - How to handle backlinks and citations - When and how to update existing pages - Style guidelines (e.g., always include references to raw sources) - Specifics for your domain (e.g., “For frontend components, document props, Shadcn dependencies, and usage examples”) Let Claude help draft and evolve this file over time.
3. **Ingest Your Sources**Drop files into the raw/ folder (code, docs, screenshots, exported chat sessions, etc.). Then prompt Claude (in the project context): “Ingest the new sources from raw/ and compile/update the wiki. Create or update relevant pages with summaries, backlinks, and connections to existing knowledge. Then show me a summary of changes.” Start with one or a few sources at a time so you can review and guide it. Once the pattern is established, you can batch more.
4. **Work + Evolve the System** For coding tasks, add this recurring instruction: “First consult the wiki/ for relevant context and patterns. After completing the task, update the wiki with new decisions, component details, and any learnings.” Example prompt for your dashboard: “Using the wiki as context, build a fully updating dashboard for the CRM. Use appropriate Shadcn packages, maintain consistency with existing components, and then update the wiki with the new architecture and relationships.”
5. **View & Navigate in Obsidian** Open the entire my-llm-wiki/ folder as a vault in Obsidian. You now have a beautiful, graph-viewable knowledge base where the LLM does most of the writing and maintenance.
6. **Maintenance & Linting (The Self-Evolving Part)** Periodically run: “Run a health check on the wiki: find contradictions, orphan pages, missing links, or opportunities for new connections. Suggest improvements and make updates.” This is where the system becomes truly self-evolving - the LLM actively improves its own knowledge base.

**Optional Enhancements**

- Combine with the earlier **Claude + Obsidian Memory Stack** (CLAUDE.md + MCP) for even stronger session memory.
- Add tools/scripts for auto-exporting Claude sessions into raw/.
- Use Obsidian plugins (Marp for slides, Dataview, etc.) to visualize outputs.
- For larger wikis, the LLM can maintain index files and summaries so queries stay efficient.

**The Payoff**

After just a few sessions, Claude stopped feeling like a fresh intern and started acting like a domain expert who remembered every prior decision.

The dashboard wasn’t generic - it was deeply consistent with my project’s patterns, and the wiki now serves as living documentation that makes future changes faster and less error-prone.

This is the shift Karpathy highlighted: moving from “manipulating code” to “manipulating knowledge” that compounds.

In 2026, the strongest AI coding setups won’t just have big context windows - they’ll have rich, self-maintained knowledge bases that make the AI genuinely smarter about your work every day.

Watch the full setup video where I walk through the live process (prompts, folder structure, ingesting sources, building the dashboard, and wiki updates):

![画像](https://pbs.twimg.com/media/HFVWAZbWoAAfmV7?format=jpg&name=large)

→ [https://youtu.be/9iWTRMjbBvo](https://youtu.be/9iWTRMjbBvo)

What do you think? Have you tried building an LLM Wiki yet?

Drop your experiences, questions, or tweaks below - especially if you’re applying this to frontend, CRM, or other domains.

[#ClaudeCode](https://x.com/search?q=%23ClaudeCode&src=hashtag_click) [#LLMWiki](https://x.com/search?q=%23LLMWiki&src=hashtag_click) [#Karpathy](https://x.com/search?q=%23Karpathy&src=hashtag_click) [#SelfEvolvingAI](https://x.com/search?q=%23SelfEvolvingAI&src=hashtag_click) [#Obsidian](https://x.com/search?q=%23Obsidian&src=hashtag_click) [#AI](https://x.com/search?q=%23AI&src=hashtag_click) [#DevTools](https://x.com/search?q=%23DevTools&src=hashtag_click)