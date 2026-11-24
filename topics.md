# Knowledge base index

The interviewer uses this file to choose topics and to know which source file to open before judging an answer.
Paths are relative to `knowledge/`. Timestamps like `[04:30]` point into the transcript files.

**Levels**
- **L1 (basic):** define the term, explain it in your own words.
- **L2 (mechanism):** explain how or why it works, compare two related concepts.
- **L3 (applied / business):** apply it to a business case, pick between options, name the trade-off or risk.

The "must-know points" below are a checklist distilled from the sources. They are not a replacement for them: **always open the listed file before grading an answer.**

---

## A. Foundations: what LLMs are

### A1. AI vs machine learning vs deep learning vs generative AI
- Source: `transcripts/02-ai-machine-learning-and-generative-ai.md`; `coursera/02-what-we-mean-by-ai.md`
- Must-know:
  - AI = simulating human-like intelligence (learn, infer, reason); early work = expert systems (Lisp, Prolog), 1980s–90s.
  - Machine learning = learns patterns from data instead of being explicitly programmed; good at prediction and spotting outliers (e.g. cybersecurity); popular in the 2010s.
  - Deep learning = ML with multi-layer neural networks; hard to explain why it gives a result.
  - Generative AI = built on foundation models (e.g. LLMs); generates new content (text, audio, video, deepfakes). Music analogy: new songs from existing notes.
  - Course view: most AI in the world is NOT generative (spam filters, recommendations, fraud detection = classifying/ranking). Generative AI = transformer-based models producing new content one token at a time.
- Levels: L1 define each layer; L2 nest them and give an example of each; L3 is a given business tool generative or classification AI?

### A2. How LLMs work
- Source: `transcripts/01-how-llms-work.md`; `coursera/04-next-token-prediction.md`, `coursera/05-next-token-prediction-try-it-out.md`; Karpathy `transcripts/00-foundations-karpathy.md` (pretraining, tokens, inference: approx. first hour)
- Must-know:
  - LLM = a foundation model for text (and code), pre-trained on huge amounts of unlabeled data with self-supervised learning.
  - LLM = data + architecture (transformer neural network) + training.
  - Training: predict the next word, compare to the real one, adjust parameters to reduce the error, repeat. Parameters = values the model adjusts while learning (GPT-3: 175 billion, 45 TB of data).
  - Fine-tuning on a smaller specific dataset makes it good at a specific task.
  - Course: "a vastly sophisticated autocomplete, not a search engine"; the same mechanism gives fluency AND hallucination.
  - Sampling: the model outputs a probability distribution over next tokens; picking from it = sampling. Temperature (low = focused, high = random/creative), top-k (keep the k most likely), top-p (keep the smallest set whose probabilities add up to p). Markov chain (1906) vs LLM: same sampling, but the LLM computes the distribution with a forward pass through billions of parameters over the whole context.
  - Business uses (IBM): customer-service chatbots, content creation, code generation/review.
- Levels: L1 what is an LLM / a parameter; L2 why the same answer can differ between runs (sampling); L3 which settings for a compliance summary vs a marketing slogan.

### A3. Transformers and attention
- Source: `transcripts/03-transformers.md`; `transcripts/04-context-windows.md` (self-attention)
- Must-know:
  - GPT = Generative Pre-trained Transformer; transformers turn one sequence into another (e.g. translation).
  - Encoder (works on the input) + decoder (generates the output).
  - Attention mechanism gives each word context from the other words; unlike RNNs, transformers do not have to process words in order → parallel processing → much faster training.
  - Semi-supervised: unsupervised pre-training on unlabeled data, then supervised fine-tuning.
  - Uses: translation, summarisation, writing documents, even chess and image processing.
- Levels: L1 what does GPT stand for; L2 why attention beat RNNs; L3 why does parallel training matter for scaling.

### A4. Tokens and context windows (working memory)
- Source: `transcripts/04-context-windows.md`; `coursera/08-working-memory.md`; `transcripts/16-memory.md` (working memory)
- Must-know:
  - Context window = the model's working memory; measured in tokens. A token can be a character, part of a word, a word or a short phrase (≈1.5 tokens per English word). Tokenizer converts text to tokens.
  - Everything in the window counts: user prompts, model replies, the (hidden) system prompt, attached documents and code, RAG results.
  - When a conversation is longer than the window, earlier parts are no longer seen → the model guesses → hallucinations.
  - Bigger is not simply better: compute grows quadratically (2× tokens ≈ 4× compute); "lost in the middle" (best recall at the beginning and end); a bigger attack surface for jailbreaks.
  - Course: the window is a **cliff, not a gradient**; silent truncation; the model does not learn from your corrections; no memory across sessions unless a memory feature exists. Fixes: front-load important material, chunk long work, re-supply context, memory/projects/compaction.
- Levels: L1 what is a token / a context window; L2 why put key info at the start; L3 a 300-page contract: what can go wrong and what do you do.

### A5. How AI gets its character (pretraining → fine-tuning)
- Source: `coursera/03-how-ai-gets-its-character.md`; Karpathy (post-training, SFT, RLHF: approx. 1:00:00 onward and 2:48:00 onward)
- Must-know:
  - Pretraining → a document completer that has no concept of helping you.
  - Fine-tuning on human judgments → an assistant (treats input as a request, answers, declines harmful asks; helpful, honest, harmless).
  - Fingerprints of fine-tuning: **sycophancy**, **verbosity**, **over-caution**, **loose confidence calibration**.
  - Karpathy: base model = "internet document simulator"; the assistant comes from post-training on conversation data written by human labellers; RLHF uses a reward model trained on human preferences.
- Levels: L1 what are the two training stages; L2 why is an assistant sycophantic; L3 how to get honest feedback on a business plan from an AI.

### A6. The four properties framework (Anthropic Academy)
- Source: `coursera/01-intro.md`, `02`, `04`, `06`, `08`, `10`, `12`, `13`
- Must-know:
  - Four properties: **Next Token Prediction** (where answers come from), **Knowledge** (what it knows), **Working Memory** (what it attends to), **Steerability** (how much you control it).
  - Each property is a continuum from capability to limitation; the same mechanism produces both. Calibrated trust = locate your task on the continuum.
  - Link to the 4D AI Fluency Framework (human competencies): Delegation, Description, Discernment, Diligence. NTP ↔ Discernment, Knowledge ↔ Delegation, Working Memory and Steerability ↔ Description.
  - Most real failures are **two properties colliding**: NTP + Knowledge = hallucinated specifics; Working Memory + Steerability = long-conversation drift. Fixes: verify specifics, re-supply context, offload to code execution, invite pushback.
- Levels: L1 name the four properties; L2 explain one capability/limitation pair; L3 diagnose a failure scenario and name the fix.

---

## B. Reliability and limits

### B1. Hallucinations
- Source: `transcripts/05-hallucinations.md`; `coursera/04-next-token-prediction.md`; Karpathy (hallucinations, approx. 1:20:00–1:30:00)
- Must-know:
  - Hallucination = output that deviates from facts or contextual logic; "plausible-sounding nonsense".
  - Types (IBM): sentence contradiction, prompt contradiction, factual contradiction, nonsensical/irrelevant.
  - Causes: data quality (noise, errors, bias, gaps), generation method (beam search, sampling; trade-offs fluency vs diversity, accuracy vs novelty), input context (unclear, contradictory or missing).
  - Mitigations: clear specific prompts, lower temperature, multi-shot (few-shot) prompting with examples; RAG and tools.
  - Course: fabrication concentrates in **specifics** (names, dates, statistics, citations, URLs, quotes); mitigations: citations, uncertainty signalling, constrained generation, generator-verifier loops.
  - Karpathy: models imitate the confident style of training answers; fix = train the model to say "I don't know", and give it tools (web search) to refresh working memory.
- Levels: L1 define a hallucination; L2 why do LLMs hallucinate; L3 an AI-written audit memo cites three regulations: what do you check.

### B2. Knowledge and its limits
- Source: `coursera/06-knowledge.md`, `coursera/07-knowledge-try-it-out.md`
- Must-know:
  - Knowledge comes only from training data and is frozen at the **knowledge cutoff**.
  - Capability zone: frequent, consistent, within-training topics. Limitation zone: rare, post-cutoff, niche, local, contested.
  - Failures: staleness, uneven coverage, inherited bias (what counts as "normal"), source amnesia (can't say where it learned something).
  - Fixes: web search, retrieval (RAG/MCP), tools.
- Levels: L1 what is a knowledge cutoff; L2 why niche topics fail more; L3 asking about a 2026 Danish tax rule: what do you do.

### B3. Steerability
- Source: `coursera/10-steerability.md`, `coursera/11-steerability-try-it-out.md`
- Must-know:
  - The model follows instructions by continuing a pattern (fine-tuning taught instruction-following), not by understanding.
  - Tight control: short, concrete, verifiable instructions (format, length, role). Loose: long reasoning chains, abstract asks, precise arithmetic.
  - Failures: **reasoning drift** (small errors compound), **letter-over-spirit** (instruction followed, intent missed), brittle arithmetic.
  - Fixes: state the goal, not just the format; checkpoints; system prompts, code execution, visible reasoning, structured outputs.
- Levels: L1 what is steerability; L2 letter vs spirit example; L3 a 6-step budget calculation: how to make it reliable.

### B4. Probabilistic vs deterministic (AI agents vs business rules)
- Source: `transcripts/06-probabilistic-versus-deterministic-outcomes.md`
- Must-know:
  - Business rule (rules engine) = explicit IF-conditions-THEN-action written by a person; **deterministic** (same input → same output). Example: refund if the order is < 30 days old AND not a final sale.
  - AI agent = goal + context + tools; works out the steps itself; **probabilistic** (samples from a distribution; the same request can get different answers).
  - Rules: well-defined logic, structured inputs, regulated work (the rule IS the explanation → audits), unit-testable, no inference cost.
  - Agents: messy/unstructured inputs, unanticipated cases, judgment (e.g. reason for a return), can call tools (vision model, order history).
  - Best practice = **hybrid**: rules first (cheap, fast) → escalate unclear cases to the agent → deterministic guardrails (e.g. threshold) → human in the loop for high stakes.
- Levels: L1 define deterministic vs probabilistic; L2 why rules are better for audits; L3 design an invoice-approval flow.

### B5. Prompt injection and AI security
- Source: `transcripts/19-prompt-injection.md`
- Must-know:
  - Prompt injection = crafting input that overrides the system's instructions; "social engineering a computer". Example: car-dealership chatbot agreeing to sell an SUV for $1.
  - #1 on the OWASP Top 10 for LLMs.
  - Jailbreak (e.g. "DAN", role play) gets around guardrails.
  - Why possible: in LLMs, instructions and input are not cleanly separated (unlike traditional programs).
  - **Direct** (attacker types it) vs **indirect** (poisoned data in documents/web pages/RAG sources picked up by an innocent user's request).
  - Consequences: malware, misinformation, data leakage, remote takeover.
  - Defences (no single fix, arms race): curate training data, least privilege, human in the loop for important actions, input filters, RLHF, model-scanning tools, ML detection and response, vetting API calls.
- Levels: L1 define prompt injection; L2 direct vs indirect; L3 an AI assistant reads supplier emails and can pay invoices: risks and controls.

---

## C. Representing and retrieving knowledge

### C1. Embeddings
- Source: `transcripts/07-embeddings.md`; `coursera/07-knowledge-try-it-out.md`
- Must-know:
  - Embeddings = words/text as numeric vectors; similar meanings are close together; distance and direction encode similarity.
  - Needed because ML algorithms need numbers, not raw text.
  - Uses: text classification (spam), named entity recognition, word similarity/analogy (king–queen, man–woman), Q&A, clustering, recommendations.
  - Frequency-based (TF-IDF: frequent in this document, rare in the corpus) vs prediction-based (word2vec 2013: CBOW predicts the word from its context, skip-gram predicts the context from the word; GloVe 2014: co-occurrence statistics).
  - Transformers use **contextual** embeddings ("bank" of a river vs bank for money).
  - Course: meaning as a place; real models ~1,000 dimensions (1,024 in the example); dimensions are not human-readable; similarity search finds the nearest k items; cosine similarity (direction, −1 to 1) instead of straight-line distance; this beats keyword search ("car" vs "automobile").
- Levels: L1 what is an embedding; L2 static vs contextual embeddings; L3 why keyword search fails on an internal policy library.

### C2. Vector databases
- Source: `transcripts/08-vector-databases.md`
- Must-know:
  - Evolution: SQL (structured tables) → NoSQL (documents) → graph (nodes/relationships) → vector databases (for AI).
  - Stores vectors/embeddings of any data (text, images, audio) for similarity search.
  - Uses: chatbots/NLP semantics, image/voice recognition, similarity search and recommendations.
  - Benefits: flexibility (unstructured data), scalability (millions/billions of vectors), speed (low-latency indexed queries).
  - Polyglot architecture: use several database types together.
- Levels: L1 what does a vector DB store; L2 how it differs from SQL; L3 when a company needs one.

### C3. Retrieval-augmented generation (RAG)
- Source: `transcripts/09-retrieval-augmented-generation-rag.md`; `transcripts/10-prompt-versus-context-engineering.md`
- Must-know:
  - Two LLM problems: **no source** and **out of date** (moons example: Jupiter vs Saturn).
  - RAG = before generating, retrieve relevant content from a content store (open internet or closed documents) and add it to the prompt. Prompt = instruction + retrieved content + user question.
  - Benefits: update the data store instead of retraining; answers grounded in primary sources with evidence; fewer hallucinations and less data leakage; can say "I don't know".
  - Risk: a weak retriever → answerable questions get no answer. Work on both retriever and generator.
  - Context-engineering video: RAG returns only the relevant sections; hybrid search (semantic + keyword).
- Levels: L1 what does RAG stand for / do; L2 RAG vs fine-tuning; L3 HR policy chatbot design and what can go wrong.

---

## D. From prompts to agents

### D1. Prompt engineering vs context engineering
- Source: `transcripts/10-prompt-versus-context-engineering.md`; `coursera/08-working-memory.md`
- Must-know:
  - Prompt engineering = crafting the input text (instructions, examples, formatting cues).
  - Context engineering = the broader discipline of programmatically assembling everything the LLM sees at inference: prompts, retrieved documents, memory, tools, state.
  - Agent Graeme example: Paris, Kentucky vs Paris, France (missing context/tool use); the €900 Ritz (missing travel policy).
  - Prompt techniques: role assignment, few-shot examples, chain-of-thought ("think step by step"), constraint setting.
  - Context components: memory (short-term summarisation, long-term vector DB), state management (multi-step progress), RAG (relevant sections, hybrid search), tools (with good descriptions), dynamic prompts (~80% dynamic content, 20% static instructions).
  - "Prompt engineering gives you better questions; context engineering gives you better systems."
- Levels: L1 define both; L2 why a perfect prompt can still fail; L3 which context does an expense-report agent need.

### D2. Tool calling
- Source: `transcripts/11-tool-calling.md`
- Must-know:
  - Tool calling connects an LLM to real-time data and actions (APIs, databases, code interpreters).
  - Flow: the app sends messages + tool definitions → the LLM **recommends** a tool call → the app executes it → the result goes back to the LLM → next tool or final answer. The LLM itself does not execute.
  - Tool definition = name + description (when/how to use) + input parameters.
  - Example: weather in Miami → weather API → 71 degrees.
  - Risk: the LLM can hallucinate or produce incorrect tool calls. Embedded tool calling = a library/framework holds the definitions and executes and retries the calls.
- Levels: L1 what is tool calling; L2 who executes the tool and why it matters; L3 a currency-conversion tool for a finance chatbot.

### D3. MCP vs APIs
- Source: `transcripts/12-mcp-and-apis.md`
- Must-know:
  - MCP = Model Context Protocol, open standard from Anthropic (late 2024); "USB-C port for AI applications".
  - Architecture: MCP host runs MCP clients; each client opens a JSON-RPC 2.0 session to an MCP server; servers expose capabilities.
  - Primitives: **tools** (actions, e.g. get_weather), **resources** (read-only data), **prompt templates**.
  - **Dynamic discovery** (tools/list, resources/list, prompts/list): agents can find new capabilities at runtime without redeploying code.
  - API = rules for requesting a service; abstraction layer; REST over HTTP (GET, POST, PUT, DELETE), JSON responses.
  - Similarities: both client-server, both abstraction layers, both simplify integration.
  - Differences: MCP is purpose-built for LLMs vs APIs are general purpose; dynamic discovery; a standardised interface (5 MCP servers = same calls; 5 APIs = 5 adapters).
  - MCP servers often **wrap** existing APIs (e.g. the GitHub MCP server): layers in the stack, not rivals.
- Levels: L1 what is MCP / an API; L2 why dynamic discovery matters; L3 connecting an agent to CRM + email + ERP.

### D4. AI agents and compound AI systems
- Source: `transcripts/13-ai-agents.md`
- Must-know:
  - Shift from monolithic models to **compound AI systems** (model + programmatic components: databases, verifiers, tools). Example: vacation-days question needs database access.
  - RAG is a compound system with **programmatic control logic** (a fixed path), so it fails off-topic (weather).
  - Agent = an LLM in charge of the control logic. Three capabilities: **reason** (plan), **act** (tools), **memory** (inner logs, conversation history).
  - ReAct = reason + act loop: plan → act (tool) → observe → iterate → answer. Sunscreen example.
  - Sliding scale of autonomy: narrow, well-defined problems → programmatic is more efficient; complex, varied tasks → agentic. Human in the loop.
- Levels: L1 what is an AI agent; L2 compound system vs agent; L3 should a payroll query bot be agentic?

### D5. Agents in business workflows
- Source: `transcripts/14-business-workflows.md`
- Must-know:
  - Real-world agent problems: span multiple systems, involve policies/approvals/rules, must fit existing workflows, human in the loop.
  - Successful agents = **coordination layers**, not standalone decision-makers.
  - Patterns: (1) multi-step orchestration across systems (employee onboarding); (2) policy-governed action execution (IT support: auto-execute low-risk, escalate high-risk); (3) exception handling in defined processes (invoice processing: happy path vs missing/mismatched data); (4) triage and routing at volume (customer service).
  - Successful agents are narrowly scoped, orchestrate systems, apply rules, keep humans in the loop, designed for integration not isolation.
- Levels: L1 why do demos fail in production; L2 name two patterns; L3 design an agent for invoice processing.

### D6. Agent skills (SKILL.md)
- Source: `transcripts/15-agent-skills.md`
- Must-know:
  - Skills give agents **procedural knowledge** (how work gets done), e.g. a 47-step compliance-report workflow.
  - Format: a folder with SKILL.md; YAML front matter with mandatory **name** and **description** (the description is the trigger condition); a markdown body with instructions; optional `scripts/`, `references/`, `assets/`.
  - **Progressive disclosure**: tier 1 name + description loaded at startup; tier 2 full body when the task matches; tier 3 resources only when needed.
  - Comparison: MCP = what the agent can reach (tools); RAG = factual reference knowledge; fine-tuning = baked into weights, permanent but expensive; skills = procedural, version-controlled, portable.
  - Open standard (agentskills.io, Apache 2.0), adopted by Claude Code, OpenAI Codex, etc.
  - Memory analogy: semantic ↔ RAG, episodic ↔ conversation logs, procedural ↔ skills.
  - Security: skills can run scripts → review before installing (prompt injection, tool poisoning, malware).
- Levels: L1 what is a skill; L2 progressive disclosure and why; L3 skill vs RAG vs fine-tuning for a month-end closing process.

### D7. Agent memory
- Source: `transcripts/16-memory.md`
- Must-know:
  - CoALA framework (Princeton, Cognitive Architectures for Language Agents): four memory types.
  - **Working** = the context window (like RAM: fast, volatile, limited; lost in the middle).
  - **Semantic** = facts, rules, conventions (vector DBs, knowledge graphs, or simply markdown files like CLAUDE.md loaded each session).
  - **Procedural** = how to do things (agent skills, SKILL.md, progressive disclosure).
  - **Episodic** = past interactions distilled into useful notes; the hardest (what to forget is an engineering problem).
  - Not every agent needs all four: thermostat → working only; password-reset bot → working + procedural; coding agent → all four.
  - Memory separates a chatbot from an agent.
- Levels: L1 name the four types; L2 semantic vs episodic; L3 which memory does a customer-support agent need.

### D8. Reasoning models (LRMs)
- Source: `transcripts/17-reasoning-models.md`; Karpathy (thinking models / RL, approx. 2:07:00–2:48:00)
- Must-know:
  - LRMs "think before they talk": plan, weigh options, check, then answer (internal chain of thought).
  - Built on a pre-trained LLM + reasoning-focused fine-tuning (logic puzzles, multi-step maths, coding with chain-of-thought answers) + reinforcement learning (RLHF or **process reward models** that judge each step) + optionally **distillation** (a teacher model's reasoning traces train a smaller model).
  - **Inference-time (test-time) compute**: more thinking for harder questions; multiple chains, voting, tree search with backtracking, tool calls.
  - Trade-off: better accuracy on complex tasks, less prompt engineering, vs higher cost (compute, VRAM, energy) and latency. A simple caption → a regular LLM is fine.
  - The top benchmark scorers tend to be reasoning models.
- Levels: L1 LLM vs LRM; L2 what is test-time compute; L3 when is a reasoning model worth the cost in a business.

---

## E. Systems, evaluation and trust

### E1. The AI stack (complete AI systems)
- Source: `transcripts/18-complete-ai-systems.md`
- Must-know:
  - Five layers: **infrastructure** (GPUs; on-premise, cloud, local), **models** (open vs proprietary, size LLM vs SLM, specialisation; >2 million on Hugging Face), **data** (sources, pipelines, vector DBs, RAG to go past the knowledge cutoff), **orchestration** (plan, execute with tool calls, review/critique loops; MCP), **application** (interfaces/modalities, revisions and citations, integrations).
  - Choices across the stack affect quality, speed, cost and safety. Example: a drug-discovery research assistant.
- Levels: L1 name the layers; L2 why the model alone is not enough; L3 design the stack for an accounting assistant.

### E2. Benchmarks
- Source: `transcripts/20-benchmarks.md`
- Must-know:
  - Benchmark = standardised framework: a task, a metric, a score (0–100); compares models, guides fine-tuning.
  - Three steps: prepare sample data → test (zero-shot, few-shot or fine-tuned) → score.
  - Metrics: accuracy, recall, perplexity (often combined).
  - Track-team analogy (200/400/800 m).
  - Limitations: miss edge cases; can be too specific → overfitting; finite lifespan (saturated benchmarks must be replaced).
- Levels: L1 what is a benchmark; L2 why a high score may not transfer; L3 choosing a model for customer emails.

### E3. LLM-as-a-judge (evaluating outputs)
- Source: `transcripts/21-evaluating-ai-outputs.md`
- Must-know:
  - Why: manual labelling is slow; traditional metrics (BLEU, ROUGE) need a reference and only count word overlap.
  - Two reference-free strategies: **direct assessment** (rubric) and **pairwise comparison** (A or B, then ranking). User study (EvalAssist): ~half prefer direct, ~quarter pairwise, rest combined.
  - Benefits: scale, flexibility (refine criteria), nuance (subjective qualities).
  - Biases: **positional**, **verbosity**, **self-enhancement**. Mitigation: swap positions and check consistency; stay vigilant.
- Levels: L1 what is LLM-as-a-judge; L2 name the biases; L3 evaluating 5,000 chatbot replies.

### E4. Explainable AI (XAI)
- Source: `transcripts/22-explainability.md`
- Must-know:
  - Black box: even creators can't explain a specific result (fraud-detection example: $100 coffee flagged).
  - XAI = methods that let humans understand how a model reached its result → trust.
  - Three methods: **prediction accuracy** (LIME, Local Interpretable Model-agnostic Explanations), **traceability** (DeepLIFT, compares neuron activations to a reference) — both technical; **decision understanding** (human factor: educate teams, dashboards with main factors and minimum change needed for a different outcome).
  - Also: troubleshooting, monitoring fairness, quality and **drift** (performance degrades as production data differs from training data).
  - Uses: finance, healthcare, criminal justice; regulatory compliance; lets affected people challenge decisions.
- Levels: L1 what is XAI; L2 what is model drift; L3 explaining a rejected loan to a customer and a regulator.

### E5. Synthetic data
- Source: `transcripts/23-synthetic-data.md`
- Must-know:
  - Artificially generated data that replicates the properties of real data (from existing datasets or algorithms/models).
  - Why: real data is scarce or sensitive (financial records, medical histories).
  - Benefits: cheap, easy, perfectly labelled, high volume; train models then transfer to real data; test fraud detection, autonomous vehicles; can reduce bias. Gartner: 70% less real data needed by 2025.
  - Challenge: can't capture all real-world variety or unexpected events (Leicester City 2015).
  - Generation: manipulate existing data (noise, transforms), GANs, statistical generators.
- Levels: L1 what is synthetic data; L2 when it fails; L3 a bank training a fraud model: should it use synthetic data?

### E6. Selecting the right AI use case
- Source: `transcripts/24-selecting-business-applications.md`
- Must-know:
  - GenAI is not always the right play (wrong choice = missed opportunity, lost money, brand damage).
  - Examples: financial forecasting → traditional models at a fraction of the cost; optimisation → established patterns.
  - "Tech to problem and problem to tech": find the right tech for a problem, and find use cases for existing investments → total cost of ownership and ROI.
  - Four considerations: **needs**, **capabilities**, **integration** (with the existing IT stack), **skills**.
  - Look for repeatable patterns, consider the data architecture, adapt as reality changes.
- Levels: L1 is GenAI always the answer; L2 the four considerations; L3 recommend an approach for demand forecasting vs drafting supplier emails.

---

## F. Karpathy deep dive (`transcripts/00-foundations-karpathy.md`, ~3.5 h)

Use for deeper or follow-up questions. Section times are approximate; search the file for keywords.

| Topic | Approx. time | Key ideas |
| --- | --- | --- |
| Pretraining data | 0:00–0:08 | Filtered internet text (FineWeb, ~44 TB), deduplication, quality filters |
| Tokenization | 0:08–0:15 | Text → bytes → byte-pair encoding → ~100k token vocabulary |
| Neural network training | 0:15–0:26 | Predict the next token, adjust parameters to reduce the loss |
| Inference | 0:26–0:31 | Sample one token at a time; stochastic outputs |
| Base model | 0:31–0:59 | GPT-2, Llama 3; an "internet document simulator"; knowledge stored in parameters like a vague recollection; regurgitation |
| Post-training (SFT) | 0:59–1:20 | Conversation datasets written by human labellers; the assistant imitates them; chat templates |
| Hallucinations, tools, memory | 1:20–1:42 | Why models make things up; "I don't know" training; web search; knowledge in parameters = vague recollection vs context window = working memory |
| Knowledge of self | 1:42–1:47 | The model has no persistent self; its identity comes from training data and system prompts |
| Models need tokens to think | 1:47–2:01 | Computation per token is limited; spread reasoning over many tokens; use code for maths |
| Tokenization limits | 2:01–2:05 | Spelling and counting problems because models see tokens, not letters |
| Jagged intelligence | 2:05–2:07 | Brilliant at some tasks, fails at simple ones (e.g. 9.11 vs 9.9) |
| Reinforcement learning | 2:07–2:42 | Practice problems, trial and error; thinking models (e.g. DeepSeek-R1) learn chains of thought |
| AlphaGo analogy | 2:42–2:48 | RL can go beyond imitating humans |
| RLHF | 2:48–3:09 | Reward model trained on human preferences for unverifiable tasks; can be gamed, so it is limited |
| Future and resources | 3:09–3:31 | Multimodality, agents, test-time training; LM Arena; how to keep up |
