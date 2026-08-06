# 🤖 My Skills AI

Centralized repository for AI Coding Assistant configurations, custom skills, rules, and plugins (Codex & Gemini Antigravity).

---

## 📌 Repository Overview

คลังเก็บข้อมูลสำหรับสำรองและซิงค์ (Backup & Sync) สมองและชุดความรู้ของ AI Assistants ที่ใช้งานข้ามเครื่อง:

```text
my-skills-ai/
├── 🤖 codex/            # การตั้งค่า สกิล และปลั๊กอินสำหรับ Codex App
│   ├── 📄 AGENTS.md     # System Prompts หลัก
│   ├── ⚙️ config.toml   # ไฟล์ตั้งค่าระบบ (MCP, Theme, Plugins Enabled)
│   ├── 🐶 pets/         # Mascot & Avatar (Buddy)
│   ├── 🧩 plugins/      # ปลั๊กอินเสริม (19 Plugins)
│   ├── 📜 rules/        # กฎเหล็กในการเขียนโค้ด (3 Rules)
│   └── 🧠 skills/       # ชุดความรู้และเทคนิคเฉพาะทาง (195 Skills)
│
└── ♊ gemini/           # การตั้งค่าและสกิลสำหรับ Gemini Antigravity
    ├── 📜 rules/        # กฎเหล็กในการเขียนโค้ด (3 Rules)
    └── 🧠 skills/       # ชุดความรู้และเทคนิคเฉพาะทาง (195 Skills)
```

---

## 🛠️ สรุปหมวดหมู่ Skills & Tools (Skill Categorization)

ความรู้ทั้งหมด 195 สกิล ถูกจัดหมวดหมู่ตามหน้าที่การใช้งาน ดังนี้:

### 1. 🗄️ Database & Schema Design
* **`database-design`**: ออกแบบ Enterprise Database Architecture, Data Modeling (DDD), Normalization & Partitioning
* **`sql-server-design`**: ออกแบบ MS SQL Server (T-SQL), Temporal Tables, Filtered Indexes, Columnstore, RLS
* **`postgresql-design`**: ออกแบบ PostgreSQL, JSONB Indexing (GIN), UUIDv7, BRIN Indexing, RLS
* **`optimizing-ef-core-queries`**: ปรับแต่ง EF Core Queries, แก้ปัญหา N+1, Tracking Modes, Compiled Queries
* **`supabase` / `supabase-postgres-best-practices`**: การใช้งาน Supabase, Database, Auth, Realtime & RLS

### 2. ⚡ .NET Architecture & Performance Optimization
* **`aspnet-core` / `dotnet-webapi`**: สกิลพัฒนาและจัดโครงสร้าง ASP.NET Core Web API, Minimal APIs, Blazor, SignalR
* **`analyzing-dotnet-performance`**: สแกนหา Performance Anti-patterns กว่า 50 รูปแบบใน .NET (Async, Memory, LINQ, Regex)
* **`microbenchmarking`**: ออกแบบและรัน Benchmark ด้วย BenchmarkDotNet (BDN)
* **`build-perf-diagnostics` / `build-perf-baseline`**: วินิจฉัยและแก้ปัญหา MSBuild ทำงานช้าด้วย Binary Logs (binlog)
* **`dotnet-aot-compat`**: แก้ไขปัญหาและปรับแต่งโค้ดให้รองรับ Native AOT และ Trimming

### 3. 🧪 Testing & Code Quality Audit
* **`code-testing-agent`**: จุดเริ่มต้นหลักสำหรับสร้าง/เขียน Unit Tests ครอบคลุมหลายภาษา (C#, Python, TS, Go ฯลฯ)
* **`run-tests`**: ตรวจสอบและรันคำสั่ง `dotnet test` ที่ถูกต้องตาม Test Runner (VSTest / MTP)
* **`test-anti-patterns`**: สแกนหาจุดบกพร่องในชุดการทดสอบ (Swallowed Exceptions, Flaky Tests, Shared State)
* **`writing-mstest-tests`**: เขียนและ modernization ชุดทดสอบด้วย MSTest 3.x/4.x APIs
* **`assertion-quality` / `test-gap-analysis`**: ประเมินความลึกของการทดสอบและหาช่องโหว่โค้ดที่ยังไม่มี Test ครอบคลุม

### 4. 📦 MSBuild & Dependency Management
* **`directory-build-organization`**: จัดการโครงสร้าง MSBuild ด้วย `Directory.Build.props` / `Directory.Build.targets`
* **`convert-to-cpm`**: แปลงระบบจัดการ Package เป็น NuGet Central Package Management (CPM) ด้วย `Directory.Packages.props`
* **`msbuild-antipatterns` / `msbuild-modernization`**: ตรวจจับข้อผิดพลาดในไฟล์ `.csproj` และแปลงเป็น SDK-Style

### 5. 🚀 Upgrades & Migrations
* **`migrate-dotnet8-to-dotnet9` / `migrate-dotnet9-to-dotnet10` / `migrate-dotnet10-to-dotnet11`**: ย้ายเวอร์ชัน .NET และแก้ Breaking Changes
* **`migrate-nullable-references`**: เปิดใช้งานและแก้ไข Nullable Reference Types (NRT)
* **`migrate-vstest-to-mtp`**: ย้ายการรัน Test จาก VSTest ไปยัง Microsoft.Testing.Platform (MTP)

### 6. 🌐 Frontend & Cloud Services (Vercel / Next.js)
* **`nextjs` / `next-upgrade` / `next-cache-components`**: การพัฒนาและปรับแต่ง Next.js App Router & Cache
* **`shadcn` / `geist` / `react-best-practices`**: การใช้งาน Component UI และ Best Practices ของ React
* **`vercel-cli` / `vercel-functions` / `deployments-cicd`**: การตั้งค่า Deployment, Serverless Functions บน Vercel

---

## 🚀 How to Sync / Use on a New Machine

เมื่อต้องการนำไปใช้กับเครื่องใหม่ สามารถคัดลอกไฟล์จาก Repo นี้ไปยังโฟลเดอร์ระบบของ AI ได้ดังนี้:

### 1. นำไปใส่ Codex App:
```powershell
# Copy Skills, Plugins & Rules
Copy-Item -Path ".\codex\skills\*" -Destination "$env:USERPROFILE\.codex\skills\" -Recurse -Force
Copy-Item -Path ".\codex\plugins\*" -Destination "$env:USERPROFILE\.codex\plugins\" -Recurse -Force
Copy-Item -Path ".\codex\rules\*" -Destination "$env:USERPROFILE\.codex\rules\" -Recurse -Force

# Copy Configs & Mascot
Copy-Item -Path ".\codex\AGENTS.md", ".\codex\config.toml" -Destination "$env:USERPROFILE\.codex\" -Force
Copy-Item -Path ".\codex\pets\*" -Destination "$env:USERPROFILE\.codex\pets\" -Recurse -Force
```

### 2. นำไปใส่ Gemini Antigravity:
```powershell
# Copy Skills & Rules
Copy-Item -Path ".\gemini\skills\*" -Destination "$env:USERPROFILE\.gemini\config\skills\" -Recurse -Force
Copy-Item -Path ".\gemini\rules\*" -Destination "$env:USERPROFILE\.gemini\config\rules\" -Recurse -Force
```

---

*Updated: August 2026*
