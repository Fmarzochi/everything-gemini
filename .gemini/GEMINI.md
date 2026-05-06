# Everything Gemini for Gemini CLI

**CRITICAL MANDATE:** You are operating with the Everything Gemini (ECC) system by Felipe Marzochi. Before starting any task, you MUST consult the `skills/` and `agents/` directories. These folders contain the collective intelligence and battle-tested workflows that define your operating standards.

## Overview

Everything Gemini (ECC) is a cross-harness coding system with 36 specialized agents, 142 skills, and 68 commands.

Gemini support is currently focused on a strong project-local instruction layer via `.gemini/GEMINI.md`, plus the shared MCP catalog and package-manager setup assets shipped by the installer.

## Core Workflow

1. Plan before editing large features.
2. Prefer test-first changes for bug fixes and new functionality.
3. Review for security before shipping.
4. Keep changes self-contained, readable, and easy to revert.

## Coding Standards

- Prefer immutable updates over in-place mutation.
- Keep functions small and files focused.
- Validate user input at boundaries.
- Never hardcode secrets.
- Fail loudly with clear error messages instead of silently swallowing problems.

## Security Checklist

Before any commit:

- No hardcoded API keys, passwords, or tokens
- All external input validated
- Parameterized queries for database writes
- Sanitized HTML output where applicable
- Authz/authn checked for sensitive paths
- Error messages scrubbed of sensitive internals

## Delivery Standards

- Use conventional commits: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `perf`, `ci`
- Run targeted verification for touched areas before shipping
- Prefer contained local implementations over adding new third-party runtime dependencies

## ECC Areas To Reuse

- `AGENTS.md` for repo-wide operating rules
- `skills/` for deep workflow guidance. Use the skills in this folder to inform your strategy and execution.
- `agents/` for specialized persona guidance. Invoke these agents when you need deep expertise in a specific area.
- `commands/` for slash-command patterns worth adapting into prompts/macros
- `mcp-configs/` for shared connector baselines

## Communication & Feedback

- Use `update_topic` frequently to keep the user informed of your current focus, progress, and any blockers. This ensures transparency and allows for course correction if needed.

## Available Skills Catalog

To use a skill, use the `activate_skill` tool with the name provided below.

- **rust-testing**: Rust testing patterns including unit tests, integration tests, async testing, property-based testing, mocking, and coverage. Follows TDD methodology.
- **swift-actor-persistence**: Thread-safe data persistence in Swift using actors — in-memory cache with file-backed storage, eliminating data races by design.
- **continuous-learning-v2**: Instinct-based learning system that observes sessions via hooks, creates atomic instincts with confidence scoring, and evolves them into skills/commands/agents. v2.1 adds project-scoped instincts to prevent cross-project contamination.
- **configure-ecc**: Interactive installer for Everything Gemini — guides users through selecting and installing skills and rules to user-level or project-level directories, verifies paths, and optionally optimizes installed files.
- **pytorch-patterns**: PyTorch deep learning patterns and best practices for building robust, efficient, and reproducible training pipelines, model architectures, and data loading.
- **customer-billing-ops**: Operate customer billing workflows such as subscriptions, refunds, churn triage, billing-portal recovery, and plan analysis using connected billing tools like Stripe. Use when the user needs to help a customer, inspect subscription state, or manage revenue-impacting billing operations.
- **frontend-patterns**: Frontend development patterns for React, Next.js, state management, performance optimization, and UI best practices.
- **connections-optimizer**: Reorganize the user's X and LinkedIn network with review-first pruning, add/follow recommendations, and channel-specific warm outreach drafted in the user's real voice. Use when the user wants to clean up following lists, grow toward current priorities, or rebalance a social graph around higher-signal relationships.
- **videodb**: See, Understand, Act on video and audio. See- ingest from local files, URLs, RTSP/live feeds, or live record desktop; return realtime context and playable stream links. Understand- extract frames, build visual/semantic/temporal indexes, and search moments with timestamps and auto-clips. Act- transcode and normalize (codec, fps, resolution, aspect ratio), perform timeline edits (subtitles, text/image overlays, branding, audio overlays, dubbing, translation), generate media assets (image, audio, video), and create real time alerts for events from live streams or desktop capture.
- **logistics-exception-management**: >
- **laravel-verification**: "Verification loop for Laravel projects: env checks, linting, static analysis, tests with coverage, security scans, and deployment readiness."
- **flutter-dart-code-review**: Library-agnostic Flutter/Dart code review checklist covering widget best practices, state management patterns (BLoC, Riverpod, Provider, GetX, MobX, Signals), Dart idioms, performance, accessibility, security, and clean architecture.
- **postgres-patterns**: PostgreSQL database patterns for query optimization, schema design, indexing, and security. Based on Supabase best practices.
- **healthcare-cdss-patterns**: Clinical Decision Support System (CDSS) development patterns. Drug interaction checking, dose validation, clinical scoring (NEWS2, qSOFA), alert severity classification, and integration into EMR workflows.
- **browser-qa**: Use this skill to automate visual testing and UI interaction verification using browser automation after deploying features.
- **kotlin-ktor-patterns**: Ktor server patterns including routing DSL, plugins, authentication, Koin DI, kotlinx.serialization, WebSockets, and testApplication testing.
- **api-design**: REST API design patterns including resource naming, status codes, pagination, filtering, error responses, versioning, and rate limiting for production APIs.
- **continuous-learning**: Automatically extract reusable patterns from Gemini CLI sessions and save them as learned skills for future use.
- **nextjs-turbopack**: Next.js 16+ and Turbopack — incremental bundling, FS caching, dev speed, and when to use Turbopack vs webpack.
- **kotlin-exposed-patterns**: JetBrains Exposed ORM patterns including DSL queries, DAO pattern, transactions, HikariCP connection pooling, Flyway migrations, and repository pattern.
- **energy-procurement**: >
- **laravel-plugin-discovery**: Discover and evaluate Laravel packages via LaraPlugins.io MCP. Use when the user wants to find plugins, check package health, or assess Laravel/PHP compatibility.
- **springboot-patterns**: Spring Boot architecture patterns, REST API design, layered services, data access, caching, async processing, and logging. Use for Java Spring Boot backend work.
- **skill-comply**: Visualize whether skills, rules, and agent definitions are actually followed — auto-generates scenarios at 3 prompt strictness levels, runs agents, classifies behavioral sequences, and reports compliance rates with full tool call timelines
- **autonomous-agent-harness**: Transform Gemini CLI into a fully autonomous agent system with persistent memory, scheduled operations, computer use, and task queuing. Replaces standalone agent frameworks (Hermes, AutoGPT) by leveraging Gemini CLI's native crons, dispatch, MCP tools, and memory. Use when the user wants continuous autonomous operation, scheduled tasks, or a self-directing agent loop.
- **csharp-testing**: C# and .NET testing patterns with xUnit, FluentAssertions, mocking, integration tests, and test organization best practices.
- **python-patterns**: Pythonic idioms, PEP 8 standards, type hints, and best practices for building robust, efficient, and maintainable Python applications.
- **nanoclaw-repl**: Operate and extend NanoClaw v2, ECC's zero-dependency session-aware REPL built on gemini -p.
- **terminal-ops**: Evidence-first repo execution workflow for ECC. Use when the user wants a command run, a repo checked, a CI failure debugged, or a narrow fix pushed with exact proof of what was executed and verified.
- **verification-loop**: "A comprehensive verification system for Gemini CLI sessions."
- **golang-patterns**: Idiomatic Go patterns, best practices, and conventions for building robust, efficient, and maintainable Go applications.
- **research-ops**: Evidence-first current-state research workflow for ECC. Use when the user wants fresh facts, comparisons, enrichment, or a recommendation built from current public evidence and any supplied local context.
- **ui-demo**: Record polished UI demo videos using Playwright. Use when the user asks to create a demo, walkthrough, screen recording, or tutorial video of a web application. Produces WebM videos with visible cursor, natural pacing, and professional feel.
- **compose-multiplatform-patterns**: Compose Multiplatform and Jetpack Compose patterns for KMP projects — state management, navigation, theming, performance, and platform-specific UI.
- **coding-standards**: Baseline cross-project coding conventions for naming, readability, immutability, and code-quality review. Use detailed frontend or backend skills for framework-specific patterns.
- **evm-token-decimals**: Prevent silent decimal mismatch bugs across EVM chains. Covers runtime decimal lookup, chain-aware caching, bridged-token precision drift, and safe normalization for bots, dashboards, and DeFi tools.
- **design-system**: Use this skill to generate or audit design systems, check visual consistency, and review PRs that touch styling.
- **hookify-rules**: This skill should be used when the user asks to create a hookify rule, write a hook rule, configure hookify, add a hookify rule, or needs guidance on hookify rule syntax and patterns.
- **java-coding-standards**: "Java coding standards for Spring Boot services: naming, immutability, Optional usage, streams, exceptions, generics, and project layout."
- **nuxt4-patterns**: Nuxt 4 app patterns for hydration safety, performance, route rules, lazy loading, and SSR-safe data fetching with useFetch and useAsyncData.
- **ai-regression-testing**: Regression testing strategies for AI-assisted development. Sandbox-mode API testing without database dependencies, automated bug-check workflows, and patterns to catch AI blind spots where the same model writes and reviews code.
- **content-engine**: Create platform-native content systems for X, LinkedIn, TikTok, YouTube, newsletters, and repurposed multi-platform campaigns. Use when the user wants social posts, threads, scripts, content calendars, or one source asset adapted cleanly across platforms.
- **benchmark**: Use this skill to measure performance baselines, detect regressions before/after PRs, and compare stack alternatives.
- **article-writing**: Write articles, guides, blog posts, tutorials, newsletter issues, and other long-form content in a distinctive voice derived from supplied examples or brand guidance. Use when the user wants polished written content longer than a paragraph, especially when voice consistency, structure, and credibility matter.
- **agent-eval**: Head-to-head comparison of coding agents (Gemini CLI, Aider, Codex, etc.) on custom tasks with pass rate, cost, time, and consistency metrics
- **bun-runtime**: Bun as runtime, package manager, bundler, and test runner. When to choose Bun vs Node, migration notes, and Vercel support.
- **laravel-security**: Laravel security best practices for authn/authz, validation, CSRF, mass assignment, file uploads, secrets, rate limiting, and secure deployment.
- **agent-payment-x402**: Add x402 payment execution to AI agents — per-task budgets, spending controls, and non-custodial wallets via MCP tools. Use when agents need to pay for APIs, services, or other agents.
- **google-workspace-ops**: Operate across Google Drive, Docs, Sheets, and Slides as one workflow surface for plans, trackers, decks, and shared documents. Use when the user needs to find, summarize, edit, migrate, or clean up Google Workspace assets without dropping to raw tool calls.
- **returns-reverse-logistics**: >
- **eval-harness**: Formal evaluation framework for Gemini CLI sessions implementing eval-driven development (EDD) principles
- **jpa-patterns**: JPA/Hibernate patterns for entity design, relationships, query optimization, transactions, auditing, indexing, pagination, and pooling in Spring Boot.
- **ai-first-engineering**: Engineering operating model for teams where AI agents generate a large share of implementation output.
- **laravel-tdd**: Test-driven development for Laravel with PHPUnit and Pest, factories, database testing, fakes, and coverage targets.
- **hipaa-compliance**: HIPAA-specific entrypoint for healthcare privacy and security work. Use when a task is explicitly framed around HIPAA, PHI handling, covered entities, BAAs, breach posture, or US healthcare compliance requirements.
- **gan-style-harness**: "GAN-inspired Generator-Evaluator agent harness for building high-quality applications autonomously. Based on Google's March 2026 harness design paper."
- **prompt-optimizer**: >-
- **continuous-agent-loop**: Patterns for continuous autonomous agent loops with quality gates, evals, and recovery controls.
- **hexagonal-architecture**: Design, implement, and refactor Ports & Adapters systems with clear domain boundaries, dependency inversion, and testable use-case orchestration across TypeScript, Java, Kotlin, and Go services.
- **email-ops**: Evidence-first mailbox triage, drafting, send verification, and sent-mail-safe follow-up workflow for ECC. Use when the user wants to organize email, draft or send through the real mail surface, or prove what landed in Sent.
- **healthcare-emr-patterns**: EMR/EHR development patterns for healthcare applications. Clinical safety, encounter workflows, prescription generation, clinical decision support integration, and accessibility-first UI for medical data entry.
- **ralphinho-rfc-pipeline**: RFC-driven multi-agent DAG execution pattern with quality gates, merge queues, and work unit orchestration.
- **fal-ai-media**: Unified media generation via fal.ai MCP — image, video, and audio. Covers text-to-image (Nano Banana), text/image-to-video (Seedance, Kling, Veo 3), text-to-speech (CSM-1B), and video-to-audio (ThinkSound). Use when the user wants to generate images, videos, or audio with AI.
- **lead-intelligence**: AI-native lead intelligence and outreach pipeline. Replaces Apollo, Clay, and ZoomInfo with agent-powered signal scoring, mutual ranking, warm path discovery, source-derived voice modeling, and channel-specific outreach across email, LinkedIn, and X. Use when the user wants to find, qualify, and reach high-value contacts.
- **data-scraper-agent**: Build a fully automated AI-powered data collection agent for any public source — job boards, prices, news, GitHub, sports, anything. Scrapes on a schedule, enriches data with a free LLM (Gemini Flash), stores results in Notion/Sheets/Supabase, and learns from user feedback. Runs 100% free on GitHub Actions. Use when the user wants to monitor, collect, or track any public data automatically.
- **repo-scan**: Cross-stack source code asset audit — classifies every file, detects embedded third-party libraries, and delivers actionable four-level verdicts per module with interactive HTML reports.
- **iterative-retrieval**: Pattern for progressively refining context retrieval to solve the subagent context problem
- **architecture-decision-records**: Capture architectural decisions made during Gemini CLI sessions as structured ADRs. Auto-detects decision moments, records context, alternatives considered, and rationale. Maintains an ADR log so future developers understand why the codebase is shaped the way it is.
- **enterprise-agent-ops**: Operate long-lived agent workloads with observability, security boundaries, and lifecycle management.
- **database-migrations**: Database migration best practices for schema changes, data migrations, rollbacks, and zero-downtime deployments across PostgreSQL, MySQL, and common ORMs (Prisma, Drizzle, Kysely, Django, TypeORM, golang-migrate).
- **cpp-testing**: Use only when writing/updating/fixing C++ tests, configuring GoogleTest/CTest, diagnosing failing or flaky tests, or adding coverage/sanitizers.
- **codebase-onboarding**: Analyze an unfamiliar codebase and generate a structured onboarding guide with architecture map, key entry points, conventions, and a starter GEMINI.md. Use when joining a new project or setting up Gemini CLI for the first time in a repo.
- **quality-nonconformance**: >
- **accessibility**: Design, implement, and audit inclusive digital products using WCAG 2.2 Level AA
- **healthcare-eval-harness**: Patient safety evaluation harness for healthcare application deployments. Automated test suites for CDSS accuracy, PHI exposure, clinical workflow integrity, and integration compliance. Blocks deployments on safety failures.
- **cpp-coding-standards**: C++ coding standards based on the C++ Core Guidelines (isocpp.github.io). Use when writing, reviewing, or refactoring C++ code to enforce modern, safe, and idiomatic practices.
- **video-editing**: AI-assisted video editing workflows for cutting, structuring, and augmenting real footage. Covers the full pipeline from raw capture through FFmpeg, Remotion, ElevenLabs, fal.ai, and final polish in Descript or CapCut. Use when the user wants to edit video, cut footage, create vlogs, or build video content.
- **tdd-workflow**: Use this skill when writing new features, fixing bugs, or refactoring code. Enforces test-driven development with 80%+ coverage including unit, integration, and E2E tests.
- **santa-method**: "Multi-agent adversarial verification with convergence loop. Two independent review agents must both pass before output ships."
- **crosspost**: Multi-platform content distribution across X, LinkedIn, Threads, and Bluesky. Adapts content per platform using content-engine patterns. Never posts identical content cross-platform. Use when the user wants to distribute content across social platforms.
- **defi-amm-security**: Security checklist for Solidity AMM contracts, liquidity pools, and swap flows. Covers reentrancy, CEI ordering, donation or inflation attacks, oracle manipulation, slippage, admin controls, and integer math.
- **seo**: Audit, plan, and implement SEO improvements across technical SEO, on-page optimization, structured data, Core Web Vitals, and content strategy. Use when the user wants better search visibility, SEO remediation, schema markup, sitemap/robots work, or keyword mapping.
- **code-tour**: Create CodeTour `.tour` files — persona-targeted, step-by-step walkthroughs with real file and line anchors. Use for onboarding tours, architecture walkthroughs, PR tours, RCA tours, and structured "explain how this works" requests.
- **carrier-relationship-management**: >
- **backend-patterns**: Backend architecture patterns, API design, database optimization, and server-side best practices for Node.js, Express, and Next.js API routes.
- **workspace-surface-audit**: Audit the active repo, MCP servers, plugins, connectors, env surfaces, and harness setup, then recommend the highest-value ECC-native skills, hooks, agents, and operator workflows. Use when the user wants help setting up Gemini CLI or understanding what capabilities are actually available in their environment.
- **production-scheduling**: >
- **kotlin-testing**: Kotlin testing patterns with Kotest, MockK, coroutine testing, property-based testing, and Kover coverage. Follows TDD methodology with idiomatic Kotlin practices.
- **agent-introspection-debugging**: Structured self-debugging workflow for AI agent failures using capture, diagnosis, contained recovery, and introspection reports.
- **docker-patterns**: Docker and Docker Compose patterns for local development, container security, networking, volume strategies, and multi-service orchestration.
- **token-budget-advisor**: >-
- **x-api**: X/Twitter API integration for posting tweets, threads, reading timelines, search, and analytics. Covers OAuth auth patterns, rate limits, and platform-native content posting. Use when the user wants to interact with X programmatically.
- **django-verification**: "Verification loop for Django projects: migrations, linting, tests with coverage, security scans, and deployment readiness checks before release or PR."
- **gemini-devfleet**: Orchestrate multi-agent coding tasks via Gemini DevFleet — plan projects, dispatch parallel agents in isolated worktrees, monitor progress, and read structured reports.
- **search-first**: Research-before-coding workflow. Search for existing tools, libraries, and patterns before writing custom code. Invokes the researcher agent.
- **nestjs-patterns**: NestJS architecture patterns for modules, controllers, providers, DTO validation, guards, interceptors, config, and production-grade TypeScript backends.
- **project-flow-ops**: Operate execution flow across GitHub and Linear by triaging issues and pull requests, linking active work, and keeping GitHub public-facing while Linear remains the internal execution layer. Use when the user wants backlog control, PR triage, or GitHub-to-Linear coordination.
- **ecc-tools-cost-audit**: Evidence-first ECC Tools burn and billing audit workflow. Use when investigating runaway PR creation, quota bypass, premium-model leakage, duplicate jobs, or GitHub App cost spikes in the ECC Tools repo.
- **swift-concurrency-6-2**: Swift 6.2 Approachable Concurrency — single-threaded by default, @concurrent for explicit background offloading, isolated conformances for main actor types.
- **manim-video**: Build reusable Manim explainers for technical concepts, graphs, system diagrams, and product walkthroughs, then hand off to the wider ECC video stack if needed. Use when the user wants a clean animated explainer rather than a generic talking-head script.
- **autonomous-loops**: "Patterns and architectures for autonomous Gemini CLI loops — from simple sequential pipelines to RFC-driven multi-agent DAG systems."
- **product-capability**: Translate PRD intent, roadmap asks, or product discussions into an implementation-ready capability plan that exposes constraints, invariants, interfaces, and unresolved decisions before multi-service work starts. Use when the user needs an ECC-native PRD-to-SRS lane instead of vague planning prose.
- **dart-flutter-patterns**: Production-ready Dart and Flutter patterns covering null safety, immutable state, async composition, widget architecture, popular state management frameworks (BLoC, Riverpod, Provider), GoRouter navigation, Dio networking, Freezed code generation, and clean architecture.
- **openclaw-persona-forge**: |-
- **hermes-imports**: Convert local Hermes operator workflows into sanitized ECC skills and release-pack artifacts. Use when preparing a Hermes workflow for public ECC reuse without leaking private workspace state, credentials, or local-only paths.
- **agent-harness-construction**: Design and optimize AI agent action spaces, tool definitions, and observation formatting for higher completion rates.
- **strategic-compact**: Suggests manual context compaction at logical intervals to preserve context through task phases rather than arbitrary auto-compaction.
- **springboot-tdd**: Test-driven development for Spring Boot using JUnit 5, Mockito, MockMvc, Testcontainers, and JaCoCo. Use when adding features, fixing bugs, or refactoring.
- **api-connector-builder**: Build a new API connector or provider by matching the target repo's existing integration pattern exactly. Use when adding one more integration without inventing a second architecture.
- **click-path-audit**: "Trace every user-facing button/touchpoint through its full state change sequence to find bugs where functions individually work but cancel each other out, produce wrong final state, or leave the UI in an inconsistent state. Use when: systematic debugging found no bugs but users report broken buttons, or after any major refactor touching shared state stores."
- **council**: Convene a four-voice council for ambiguous decisions, tradeoffs, and go/no-go calls. Use when multiple valid paths exist and you need structured disagreement before choosing.
- **ck**: Persistent per-project memory for Gemini CLI. Auto-loads project context on session start, tracks sessions with git activity, and writes to native memory. Commands run deterministic Node.js scripts — behavior is consistent across model versions.
- **dashboard-builder**: Build monitoring dashboards that answer real operator questions for Grafana, SigNoz, and similar platforms. Use when turning metrics into a working dashboard instead of a vanity board.
- **context-budget**: Audits Gemini CLI context window consumption across agents, skills, MCP servers, and rules. Identifies bloat, redundant components, and produces prioritized token-savings recommendations.
- **perl-patterns**: Modern Perl 5.36+ idioms, best practices, and conventions for building robust, maintainable Perl applications.
- **customs-trade-compliance**: >
- **laravel-patterns**: Laravel architecture patterns, routing/controllers, Eloquent ORM, service layers, queues, events, caching, and API resources for production apps.
- **remotion-video-creation**: Best practices for Remotion - Video creation in React. 29 domain-specific rules covering 3D, animations, audio, captions, charts, transitions, and more.
- **team-builder**: Interactive agent picker for composing and dispatching parallel teams
- **visa-doc-translate**: Translate visa application documents (images) to English and create a bilingual PDF with original and translation
- **perl-security**: Comprehensive Perl security covering taint mode, input validation, safe process execution, DBI parameterized queries, web security (XSS/SQLi/CSRF), and perlcritic security policies.
- **agentic-engineering**: Operate as an agentic engineer using eval-first execution, decomposition, and cost-aware model routing.
- **deployment-patterns**: Deployment workflows, CI/CD pipeline patterns, Docker containerization, health checks, rollback strategies, and production readiness checklists for web applications.
- **perl-testing**: Perl testing patterns using Test2::V0, Test::More, prove runner, mocking, coverage with Devel::Cover, and TDD methodology.
- **springboot-verification**: "Verification loop for Spring Boot projects: build, static analysis, tests with coverage, security scans, and diff review before release or PR."
- **deep-research**: Multi-source deep research using firecrawl and exa MCPs. Searches the web, synthesizes findings, and delivers cited reports with source attribution. Use when the user wants thorough research on any topic with evidence and citations.
- **django-patterns**: Django architecture patterns, REST API design with DRF, ORM best practices, caching, signals, middleware, and production-grade Django apps.
- **regex-vs-llm-structured-text**: Decision framework for choosing between regex and LLM when parsing structured text — start with regex, add LLM only for low-confidence edge cases.
- **product-lens**: Use this skill to validate the "why" before building, run product diagnostics, and pressure-test product direction before the request becomes an implementation contract.
- **frontend-slides**: Create stunning, animation-rich HTML presentations from scratch or by converting PowerPoint files. Use when the user wants to build a presentation, convert a PPT/PPTX to web, or create slides for a talk/pitch. Helps non-designers discover their aesthetic through visual exploration rather than abstract choices.
- **kotlin-patterns**: Idiomatic Kotlin patterns, best practices, and conventions for building robust, efficient, and maintainable Kotlin applications with coroutines, null safety, and DSL builders.
- **security-bounty-hunter**: Hunt for exploitable, bounty-worthy security issues in repositories. Focuses on remotely reachable vulnerabilities that qualify for real reports instead of noisy local-only findings.
- **django-tdd**: Django testing strategies with pytest-django, TDD methodology, factory_boy, mocking, coverage, and testing Django REST Framework APIs.
- **rust-patterns**: Idiomatic Rust patterns, ownership, error handling, traits, concurrency, and best practices for building safe, performant applications.
- **agent-sort**: Build an evidence-backed ECC install plan for a specific repo by sorting skills, commands, rules, hooks, and extras into DAILY vs LIBRARY buckets using parallel repo-aware review passes. Use when ECC should be trimmed to what a project actually needs instead of loading the full bundle.
- **cost-aware-llm-pipeline**: Cost optimization patterns for LLM API usage — model routing by task complexity, budget tracking, retry logic, and prompt caching.
- **foundation-models-on-device**: Apple FoundationModels framework for on-device LLM — text generation, guided generation with @Generable, tool calling, and snapshot streaming in iOS 26+.
- **swift-protocol-di-testing**: Protocol-based dependency injection for testable Swift code — mock file system, network, and external APIs using focused protocols and Swift Testing.
- **content-hash-cache-pattern**: Cache expensive file processing results using SHA-256 content hashes — path-independent, auto-invalidating, with service layer separation.
- **documentation-lookup**: Use up-to-date library and framework docs via Context7 MCP instead of training data. Activates for setup questions, API references, code examples, or when the user names a framework (e.g. React, Next.js, Prisma).
- **springboot-security**: Spring Security best practices for authn/authz, validation, CSRF, secrets, headers, rate limiting, and dependency security in Java Spring Boot services.
- **finance-billing-ops**: Evidence-first revenue, pricing, refunds, team-billing, and billing-model truth workflow for ECC. Use when the user wants a sales snapshot, pricing comparison, duplicate-charge diagnosis, or code-backed billing reality instead of generic payments advice.
- **market-research**: Conduct market research, competitive analysis, investor due diligence, and industry intelligence with source attribution and decision-oriented summaries. Use when the user wants market sizing, competitor comparisons, fund research, technology scans, or research that informs business decisions.
- **jira-integration**: Use this skill when retrieving Jira tickets, analyzing requirements, updating ticket status, adding comments, or transitioning issues. Provides Jira API patterns via MCP or direct REST calls.
- **knowledge-ops**: Knowledge base management, ingestion, sync, and retrieval across multiple storage layers (local files, MCP memory, vector stores, Git repos). Use when the user wants to save, organize, sync, deduplicate, or search across their knowledge systems.
- **skill-stocktake**: "Use when auditing Gemini skills and commands for quality. Supports Quick Scan (changed skills only) and Full Stocktake modes with sequential subagent batch evaluation."
- **android-clean-architecture**: Clean Architecture patterns for Android and Kotlin Multiplatform projects — module structure, dependency rules, UseCases, Repositories, and data layer patterns.
- **nodejs-keccak256**: Prevent Ethereum hashing bugs in JavaScript and TypeScript. Node's sha3-256 is NIST SHA3, not Ethereum Keccak-256, and silently breaks selectors, signatures, storage slots, and address derivation.
- **golang-testing**: Go testing patterns including table-driven tests, subtests, benchmarks, fuzzing, and test coverage. Follows TDD methodology with idiomatic Go practices.
- **unified-notifications-ops**: Operate notifications as one ECC-native workflow across GitHub, Linear, desktop alerts, hooks, and connected communication surfaces. Use when the real problem is alert routing, deduplication, escalation, or inbox collapse.
- **e2e-testing**: Playwright E2E testing patterns, Page Object Model, configuration, CI/CD integration, artifact management, and flaky test strategies.
- **mcp-server-patterns**: Build MCP servers with Node/TypeScript SDK — tools, resources, prompts, Zod validation, stdio vs Streamable HTTP. Use Context7 or official MCP docs for latest API.
- **git-workflow**: Git workflow patterns including branching strategies, commit conventions, merge vs rebase, conflict resolution, and collaborative development best practices for teams of all sizes.
- **python-testing**: Python testing strategies using pytest, TDD methodology, fixtures, mocking, parametrization, and coverage requirements.
- **brand-voice**: Build a source-derived writing style profile from real posts, essays, launch notes, docs, or site copy, then reuse that profile across content, outreach, and social workflows. Use when the user wants voice consistency without generic AI writing tropes.
- **dmux-workflows**: Multi-agent orchestration using dmux (tmux pane manager for AI agents). Patterns for parallel agent workflows across Gemini CLI, Codex, OpenCode, and other harnesses. Use when running multiple agent sessions in parallel or coordinating multi-agent development workflows.
- **clickhouse-io**: ClickHouse database patterns, query optimization, analytics, and data engineering best practices for high-performance analytical workloads.
- **github-ops**: GitHub repository operations, automation, and management. Issue triage, PR management, CI/CD operations, release management, and security monitoring using the gh CLI. Use when the user wants to manage GitHub issues, PRs, CI status, releases, contributors, stale items, or any GitHub operational task beyond simple git commands.
- **llm-trading-agent-security**: Security patterns for autonomous trading agents with wallet or transaction authority. Covers prompt injection, spend limits, pre-send simulation, circuit breakers, MEV protection, and key handling.
- **liquid-glass-design**: iOS 26 Liquid Glass design system — dynamic glass material with blur, reflection, and interactive morphing for SwiftUI, UIKit, and WidgetKit.
- **canary-watch**: Use this skill to monitor a deployed URL for regressions after deploys, merges, or dependency upgrades.
- **kotlin-coroutines-flows**: Kotlin Coroutines and Flow patterns for Android and KMP — structured concurrency, Flow operators, StateFlow, error handling, and testing.
- **plankton-code-quality**: "Write-time code quality enforcement using Plankton — auto-formatting, linting, and Gemini-powered fixes on every file edit via hooks."
- **investor-materials**: Create and update pitch decks, one-pagers, investor memos, accelerator applications, financial models, and fundraising materials. Use when the user needs investor-facing documents, projections, use-of-funds tables, milestone plans, or materials that must stay internally consistent across multiple fundraising assets.
- **gateguard**: Fact-forcing gate that blocks Edit/Write/Bash (including MultiEdit) and demands concrete investigation (importers, data schemas, user instruction) before allowing the action. Measurably improves output quality by +2.25 points vs ungated agents.
- **inventory-demand-planning**: >
- **automation-audit-ops**: Evidence-first automation inventory and overlap audit workflow for ECC. Use when the user wants to know which jobs, hooks, connectors, MCP servers, or wrappers are live, broken, redundant, or missing before fixing anything.
- **django-security**: Django security best practices, authentication, authorization, CSRF protection, SQL injection prevention, XSS prevention, and secure deployment configurations.
- **messages-ops**: Evidence-first live messaging workflow for ECC. Use when the user wants to read texts or DMs, recover a recent one-time code, inspect a thread before replying, or prove which message source was actually checked.
- **blueprint**: >-
- **investor-outreach**: Draft cold emails, warm intro blurbs, follow-ups, update emails, and investor communications for fundraising. Use when the user wants outreach to angels, VCs, strategic investors, or accelerators and needs concise, personalized, investor-facing messaging.
- **security-scan**: Scan your Gemini CLI configuration (.gemini/ directory) for security vulnerabilities, misconfigurations, and injection risks using AgentShield. Checks GEMINI.md, settings.json, MCP servers, hooks, and agent definitions.
- **swiftui-patterns**: SwiftUI architecture patterns, state management with @Observable, view composition, navigation, performance optimization, and modern iOS/macOS UI best practices.
- **nutrient-document-processing**: Process, convert, OCR, extract, redact, sign, and fill documents using the Nutrient DWS API. Works with PDFs, DOCX, XLSX, PPTX, HTML, and images.
- **social-graph-ranker**: Weighted social-graph ranking for warm intro discovery, bridge scoring, and network gap analysis across X and LinkedIn. Use when the user wants the reusable graph-ranking engine itself, not the broader outreach or network-maintenance workflow layered on top of it.
- **security-review**: Use this skill when adding authentication, handling user input, working with secrets, creating API endpoints, or implementing payment/sensitive features. Provides comprehensive security checklist and patterns.
- **healthcare-phi-compliance**: Protected Health Information (PHI) and Personally Identifiable Information (PII) compliance patterns for healthcare applications. Covers data classification, access control, audit trails, encryption, and common leak vectors.
- **opensource-pipeline**: "Open-source pipeline: fork, sanitize, and package private projects for safe public release. Chains 3 agents (forker, sanitizer, packager). Triggers: '/opensource', 'open source this', 'make this public', 'prepare for open source'."
- **safety-guard**: Use this skill to prevent destructive operations when working on production systems or running agents autonomously.
- **rules-distill**: "Scan skills to extract cross-cutting principles and distill them into rules — append, revise, or create new rule files"
- **dotnet-patterns**: Idiomatic C# and .NET patterns, conventions, dependency injection, async/await, and best practices for building robust, maintainable .NET applications.
- **exa-search**: Neural search via Exa MCP for web, code, and company research. Use when the user needs web search, code examples, company intel, people lookup, or AI-powered deep research with Exa's neural search engine.
