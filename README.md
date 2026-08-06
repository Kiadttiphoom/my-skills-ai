# 🤖 My Skills AI

Professional centralized repository for AI Coding Assistant configurations, shared skills, rules, and plugins (Codex & Gemini Antigravity).

---

## 📚 Quick Index / Categories

กดที่หมวดหมู่เพื่อกระโดดไปยังรายละเอียดของแต่ละกลุ่ม:

* [🗄️ Database Design](#1-database-design)
* [⚡ .NET Architecture & Performance](#2-net-architecture--performance)
* [🧪 Testing & Code Quality](#3-testing--code-quality)
* [📦 MSBuild & Dependency Management](#4-msbuild--dependency-management)
* [🚀 Upgrades & Migrations](#5-upgrades--migrations)
* [🌐 Frontend & Cloud (Vercel / Next.js)](#6-frontend--cloud-vercel--nextjs)
* [🤖 AI & Agent Frameworks](#7-ai--agent-frameworks)
* [📄 Artifact Templates & Documents](#8-artifact-templates--documents)

---

## 🔍 Quick Search Table (ตารางค้นหาด่วน)

| ถ้าจะทำ / เทคโนโลยีที่ใช้ | ใช้ Skill นี้ |
| :--- | :--- |
| **SQL Server (T-SQL)** | `sql-server-design` |
| **PostgreSQL** | `postgresql-design` |
| **Enterprise Database Architecture (DDD / Normalization)** | `database-design` |
| **EF Core Optimization (N+1 / Tracking / Compiled)** | `optimizing-ef-core-queries` |
| **Supabase (Database / Auth / Realtime / RLS)** | `supabase`, `supabase-postgres-best-practices` |
| **ASP.NET Core Web API / Blazor / MVC** | `aspnet-core`, `dotnet-webapi` |
| **.NET Performance Analysis & Anti-patterns** | `analyzing-dotnet-performance` |
| **Benchmark (.NET BenchmarkDotNet)** | `microbenchmarking` |
| **Unit Testing & Test Generation (Polyglot)** | `code-testing-agent` |
| **Run .NET Tests (VSTest / MTP)** | `run-tests` |
| **MSTest Authoring & Modernization** | `writing-mstest-tests` |
| **Central Package Management (CPM)** | `convert-to-cpm` |
| **MSBuild Infrastructure & Props/Targets** | `directory-build-organization` |
| **.NET Upgrade (8 ➔ 9 ➔ 10 ➔ 11)** | `migrate-dotnet8-to-dotnet9`, `migrate-dotnet9-to-dotnet10`, `migrate-dotnet10-to-dotnet11` |
| **Next.js (App Router / PPR / Caching)** | `nextjs`, `next-upgrade`, `next-cache-components` |
| **React UI Components & Best Practices** | `shadcn`, `react-best-practices`, `geist` |
| **Vercel CLI / Deployment / Functions** | `vercel-cli`, `vercel-functions`, `deployments-cicd` |
| **AI SDK & AI Gateways** | `ai-sdk`, `ai-gateway`, `ai-elements` |

---

## 📌 Repository Architecture (Shared Skills Structure)

คลังนี้ใช้โครงสร้างแบบ **Shared Repository** เพื่อให้ AI ทุกตัว (Codex และ Gemini) ใช้งานชุดความรู้เดียวกัน ป้องกันการแก้ไขซ้ำซ้อน:

```text
my-skills-ai/
├── 🤝 shared/           # 🌟 ศูนย์กลางความรู้ร่วม (Single Source of Truth)
│   ├── 📜 rules/        # กฎเหล็กในการเขียนโค้ด (csharp-style.md, aspnet-core-auto.md, default.rules)
│   └── 🧠 skills/       # ชุดความรู้และคู่มือเทคโนโลยีทั้งหมด 195+ Skills
│
├── 🤖 codex/            # การตั้งค่าเฉพาะทางของ Codex App
│   ├── 📄 AGENTS.md     # System Prompts หลักของ Codex
│   ├── ⚙️ config.toml   # ไฟล์ตั้งค่าระบบ (MCP Servers, Theme, Plugins)
│   ├── 🐶 pets/         # Mascot & Avatar (Buddy)
│   └── 🧩 plugins/      # ปลั๊กอินเฉพาะทาง (19 Plugins)
│
└── ♊ gemini/           # การตั้งค่าเฉพาะทางของ Gemini Antigravity
```

---

## 🛠️ Category Details

<a id="1-database-design"></a>
### 🗄️ 1. Database Design
* **`database-design`**: ออกแบบ Enterprise Database Architecture, Data Modeling (DDD), Normalization & Partitioning
* **`sql-server-design`**: ออกแบบ MS SQL Server (T-SQL), Temporal Tables, Filtered Indexes, Columnstore, RLS
* **`postgresql-design`**: ออกแบบ PostgreSQL, JSONB Indexing (GIN), UUIDv7, BRIN Indexing, RLS
* **`optimizing-ef-core-queries`**: ปรับแต่ง EF Core Queries, แก้ปัญหา N+1, Tracking Modes, Compiled Queries
* **`supabase` / `supabase-postgres-best-practices`**: การใช้งาน Supabase, Database, Auth, Realtime & RLS

<a id="2-net-architecture--performance"></a>
### ⚡ 2. .NET Architecture & Performance
* **`aspnet-core` / `dotnet-webapi`**: สกิลพัฒนาและจัดโครงสร้าง ASP.NET Core Web API, Minimal APIs, Blazor, SignalR
* **`analyzing-dotnet-performance`**: สแกนหา Performance Anti-patterns กว่า 50 รูปแบบใน .NET (Async, Memory, LINQ, Regex)
* **`microbenchmarking`**: ออกแบบและรัน Benchmark ด้วย BenchmarkDotNet (BDN)
* **`build-perf-diagnostics` / `build-perf-baseline`**: วินิจฉัยและแก้ปัญหา MSBuild ทำงานช้าด้วย Binary Logs (binlog)
* **`dotnet-aot-compat`**: แก้ไขปัญหาและปรับแต่งโค้ดให้รองรับ Native AOT และ Trimming

<a id="3-testing--code-quality"></a>
### 🧪 3. Testing & Code Quality
* **`code-testing-agent`**: จุดเริ่มต้นหลักสำหรับสร้าง/เขียน Unit Tests ครอบคลุมหลายภาษา (C#, Python, TS, Go ฯลฯ)
* **`run-tests`**: ตรวจสอบและรันคำสั่ง `dotnet test` ที่ถูกต้องตาม Test Runner (VSTest / MTP)
* **`test-anti-patterns`**: สแกนหาจุดบกพร่องในชุดการทดสอบ (Swallowed Exceptions, Flaky Tests, Shared State)
* **`writing-mstest-tests`**: เขียนและ modernization ชุดทดสอบด้วย MSTest 3.x/4.x APIs
* **`assertion-quality` / `test-gap-analysis`**: ประเมินความลึกของการทดสอบและหาช่องโหว่โค้ดที่ยังไม่มี Test ครอบคลุม

<a id="4-msbuild--dependency-management"></a>
### 📦 4. MSBuild & Dependency Management
* **`directory-build-organization`**: จัดการโครงสร้าง MSBuild ด้วย `Directory.Build.props` / `Directory.Build.targets`
* **`convert-to-cpm`**: แปลงระบบจัดการ Package เป็น NuGet Central Package Management (CPM) ด้วย `Directory.Packages.props`
* **`msbuild-antipatterns` / `msbuild-modernization`**: ตรวจจับข้อผิดพลาดในไฟล์ `.csproj` และแปลงเป็น SDK-Style

<a id="5-upgrades--migrations"></a>
### 🚀 5. Upgrades & Migrations
* **`migrate-dotnet8-to-dotnet9` / `migrate-dotnet9-to-dotnet10` / `migrate-dotnet10-to-dotnet11`**: ย้ายเวอร์ชัน .NET และแก้ Breaking Changes
* **`migrate-nullable-references`**: เปิดใช้งานและแก้ไข Nullable Reference Types (NRT)
* **`migrate-vstest-to-mtp`**: ย้ายการรัน Test จาก VSTest ไปยัง Microsoft.Testing.Platform (MTP)

<a id="6-frontend--cloud-vercel--nextjs"></a>
### 🌐 6. Frontend & Cloud (Vercel / Next.js)
* **`nextjs` / `next-upgrade` / `next-cache-components`**: การพัฒนาและปรับแต่ง Next.js App Router & Cache
* **`shadcn` / `geist` / `react-best-practices`**: การใช้งาน Component UI และ Best Practices ของ React
* **`vercel-cli` / `vercel-functions` / `deployments-cicd`**: การตั้งค่า Deployment, Serverless Functions บน Vercel

<a id="7-ai--agent-frameworks"></a>
### 🤖 7. AI & Agent Frameworks
* **`ai-sdk` / `ai-gateway` / `ai-elements`**: การพัฒนาแอปด้วย Vercel AI SDK, Unified Gateway & UI Components
* **`chat-sdk` / `json-render`**: การทำ Multi-platform Chat Bots และ AI Dynamic UI Rendering

<a id="8-artifact-templates--documents"></a>
### 📄 8. Artifact Templates & Documents
* **`documents` / `pdf` / `presentations` / `spreadsheets`**: สกิลการสร้างและประมวลผลไฟล์เอกสาร Word, PDF, Slides, Excel
* **`artifact-template-*`**: แม่แบบเอกสารมาตรฐาน เช่น System Design, Design Report, Project Kickoff ฯลฯ

---

## 🚀 How to Sync / Use on a New Machine

เมื่อนำไปใช้กับเครื่องใหม่ ให้ดึงไฟล์จากโฟลเดอร์ `shared/` ไปใช้งาน:

### 1. นำไปใส่ Codex App:
```powershell
# Copy Shared Skills & Rules
Copy-Item -Path ".\shared\skills\*" -Destination "$env:USERPROFILE\.codex\skills\" -Recurse -Force
Copy-Item -Path ".\shared\rules\*" -Destination "$env:USERPROFILE\.codex\rules\" -Recurse -Force

# Copy Codex Specific Configs, Plugins & Mascot
Copy-Item -Path ".\codex\plugins\*" -Destination "$env:USERPROFILE\.codex\plugins\" -Recurse -Force
Copy-Item -Path ".\codex\AGENTS.md", ".\codex\config.toml" -Destination "$env:USERPROFILE\.codex\" -Force
Copy-Item -Path ".\codex\pets\*" -Destination "$env:USERPROFILE\.codex\pets\" -Recurse -Force
```

### 2. นำไปใส่ Gemini Antigravity:
```powershell
# Copy Shared Skills & Rules
Copy-Item -Path ".\shared\skills\*" -Destination "$env:USERPROFILE\.gemini\config\skills\" -Recurse -Force
Copy-Item -Path ".\shared\rules\*" -Destination "$env:USERPROFILE\.gemini\config\rules\" -Recurse -Force
```

---

*Updated: August 2026*
