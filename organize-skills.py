import pathlib, re, json, hashlib, subprocess, os

ROOT = pathlib.Path(__file__).resolve().parent
BASE = ROOT / 'shared' / 'skills'
OUT = ROOT / 'skill-organization-audit'
OUT.mkdir(exist_ok=True)
dirs = sorted((p for p in BASE.iterdir() if p.is_dir()), key=lambda p:p.name.casefold())
def git(*args):
    return subprocess.run(['git', *args], cwd=ROOT, capture_output=True, text=True, encoding='utf-8', errors='replace')
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def snapshot(p):
    return {str(f.relative_to(p)).replace('\\','/'):digest(f) for f in p.rglob('*') if f.is_file()}
if '--finish' in __import__('sys').argv:
    rows=json.loads((OUT/'inventory-before.json').read_text(encoding='utf-8'))
    source=pathlib.Path(__file__).read_text(encoding='utf-8')
    exec(source[source.rindex('# Update concrete paths in repository overview;'):])
    raise SystemExit()
before_status = git('status','--short').stdout
(OUT/'git-status-before.txt').write_text(before_status, encoding='utf-8')
explicit = {
 'analyzing-dotnet-performance':'dotnet-analyzing-performance', 'optimizing-ef-core-queries':'dotnet-efcore-query-optimization',
 'configuring-opentelemetry-dotnet':'dotnet-opentelemetry', 'nextjs':'nextjs-core','nestjs':'nestjs-core',
 'next-cache-components':'nextjs-cache-components','next-forge':'nextjs-forge','next-upgrade':'nextjs-upgrade','turbopack':'nextjs-turbopack',
 'arch-render':'architecture-render','architecture':'architecture-core','archlang':'architecture-archlang','revit-bim':'architecture-revit-bim',
 'skills-architects':'architecture-architect-skills','sketch':'editor-sketch','banner-design':'design-banner',
 'iot-dev':'iot-development','workbench-mqtt':'mqtt-workbench','sql-server-design':'sqlserver-design','postgresql-design':'postgres-design',
 'supabase':'supabase-core','github':'github-core','gmail':'gmail-core','gh-address-comments':'github-address-comments','gh-fix-ci':'github-fix-ci',
 'documents':'document-core','spreadsheets':'spreadsheet-core','presentations':'presentation-core','pdf':'pdf-core','slides':'presentation-slides',
 'excel-live-control':'spreadsheet-excel-live-control','shopee_affiliate_product_research_skill':'shopee-affiliate-product-research',
 'json-render':'ai-json-render','eve':'agent-eve','skill-creator':'agent-skill-creator','template-creator':'agent-artifact-template-creator',
 'control-in-app-browser':'browser-control-in-app','mobile-app-ui-design':'uiux-mobile-app-design','ui-styling':'uiux-styling','ui-ux-pro-max':'uiux-pro-max',
 'design':'design-core','brand':'design-brand','impeccable':'uiux-impeccable','hatch-pet':'graphics-hatch-pet','visualize':'graphics-visualize',
 'web-quality-skills':'web-seo','scroll-world':'web-scroll-world','sites-building':'web-sites-building','sites-hosting':'web-sites-hosting',
 'linear':'general-linear','yeet':'github-publish-changes','monitoring-expert':'devops-monitoring-expert',
 'cycle-counting':'commerce-cycle-counting','inventory-optimization':'commerce-inventory-optimization','replenishment-strategy':'commerce-replenishment-strategy',
 'swr':'react-swr','shadcn':'react-shadcn','auth':'nextjs-auth','cms':'web-cms','email':'web-email','payments':'commerce-payments',
 'sign-in-with-vercel':'vercel-sign-in','turborepo':'vercel-turborepo',
}
dotnet = '''aspnet-core author-component binlog-failure-analysis binlog-generation build-parallelism build-perf-baseline build-perf-diagnostics check-bin-obj-clash clr-activation-debugging collect-user-input configure-auth convert-blazor-server-to-webapp convert-to-cpm coordinate-components copy-to-output-directory coverage-analysis crap-score create-blazor-project create-datadriven-aspnetcore csharp-scripts detect-static-dependencies directory-build-organization dump-collect eval-performance exp-mock-usage-analysis exp-simd-vectorization exp-test-maintainability extension-points fetch-and-send-data filter-syntax generate-testability-wrappers including-generated-files incremental-build item-management microbenchmarking migrate-dotnet10-to-dotnet11 migrate-dotnet8-to-dotnet9 migrate-dotnet9-to-dotnet10 migrate-mstest-v1v2-to-v3 migrate-mstest-v3-to-v4 migrate-nullable-references migrate-static-to-wrapper migrate-vstest-to-mtp migrate-xunit-to-mstest migrate-xunit-to-xunit-v3 minimal-api-file-upload msbuild-antipatterns msbuild-modernization msbuild-server mtp-hot-reload nuget-trusted-publishing plan-ui-change platform-detection property-patterns resolve-project-references run-tests setup-local-sdk support-prerendering system-text-json-net11 target-authoring technology-selection template-authoring template-comparison template-discovery template-instantiation template-smart-defaults template-validation thread-abort-migration use-js-interop writing-mstest-tests'''.split()
testing = 'assertion-quality code-testing-agent code-testing-extensions find-untested-sources grade-tests test-analysis-extensions test-anti-patterns test-gap-analysis test-smell-detection test-tagging verification'.split()
system = 'api-design back-of-the-envelope blob-store caching consistency-coordination content-delivery data-storage distributed-logging distributed-search dns load-balancing messaging-streaming observability requirements-scoping resilience-failure scaling-evolution sequencer service-decomposition sharded-counters system-design task-scheduling'.split()
vercel = 'bootstrap cdn-caching chat-sdk cron-jobs deployments-cicd env-vars geist geistdocs investigation-mode knowledge-update marketplace micro microfrontends ncc routing-middleware runtime-cache satori workflow'.split()
for names, prefix in [(dotnet,'dotnet'),(testing,'testing'),(system,'systemdesign'),(vercel,'vercel')]:
    for n in names: explicit[n] = prefix+'-'+n
rows=[]
path_dependencies={}
existing={p.name for p in dirs}
for f in BASE.rglob('*'):
    if not f.is_file() or f.suffix.lower() not in ('.md','.py','.ps1','.js','.mjs','.cjs','.json','.toml','.yaml','.yml','.sh'): continue
    try: content=f.read_text(encoding='utf-8-sig')
    except (UnicodeError,OSError): continue
    for m in re.finditer(r'(?:skills[/\\])([A-Za-z0-9_.-]+)(?=[/\\\s\x22\x27`]|$)',content):
        if m.group(1) in existing:
            path_dependencies.setdefault(m.group(1),[]).append(str(f.relative_to(BASE)))
    for m in re.finditer(r'(?<![\w/])((?:\.\./)+[A-Za-z0-9_./-]+)',content):
        target=(f.parent/m.group(1)).resolve()
        if target.exists() and target.is_relative_to(BASE) and target!=BASE:
            owner=target.relative_to(BASE).parts[0]
            source=f.relative_to(BASE).parts[0]
            if owner!=source: path_dependencies.setdefault(owner,[]).append(str(f.relative_to(BASE)))
for p in dirs:
    skill=p/'SKILL.md'
    text=skill.read_text(encoding='utf-8-sig') if skill.exists() else ''
    fm=re.match(r'^---\s*\n(.*?)\n---',text,re.S)
    front=fm.group(1) if fm else ''
    desc=re.search(r'^description:\s*(.*?)(?=\n[^\s]|\Z)',front,re.M|re.S)
    purpose=re.sub(r'\s+',' ',desc.group(1) if desc else '')
    name=re.search(r'^name:\s*(.*)$',front,re.M)
    new=explicit.get(p.name,p.name)
    manual=[]
    if new!=p.name and p.name in path_dependencies:
        manual.append('Existing concrete path dependency in '+path_dependencies[p.name][0])
    if not skill.exists() and p.name not in ('.system','skills-architects'):
        manual.append('No top-level SKILL.md; existing container preserved')
    if new!=p.name:
        # Preserve skill contents: a rename must not invalidate installed self-path commands.
        selfref=re.compile(r'(?:skills[/\\]|skills\\\\)'+re.escape(p.name)+r'(?=[/\\\s\x22\x27`]|$)')
        for f in p.rglob('*'):
            if f.is_file() and f.suffix.lower() in ('.md','.py','.ps1','.js','.mjs','.cjs','.json','.toml','.yaml','.yml','.sh'):
                try: s=f.read_text(encoding='utf-8-sig')
                except (UnicodeError,OSError): continue
                if selfref.search(s): manual.append('Hard-coded installed self path in '+str(f.relative_to(p))); break
    if manual: new=p.name
    prefix=new.split('-')[0]
    cat={'dotnet':'.NET','nextjs':'Next.js','react':'React','nestjs':'NestJS','flutter':'Flutter','android':'Mobile','apple':'Mobile','maui':'Mobile','vercel':'Vercel','supabase':'Supabase','database':'Database','postgres':'Database','sqlserver':'Database','testing':'Testing','security':'Security','architecture':'Architecture','systemdesign':'Architecture','sketchup':'SketchUp','editor':'Editor','design':'Design/UIUX','uiux':'Design/UIUX','iot':'IoT','esp32':'IoT','mqtt':'IoT','ai':'AI/Agents','agent':'AI/Agents','document':'Documents','spreadsheet':'Documents','presentation':'Documents','pdf':'Documents','commerce':'Commerce','shopee':'Commerce'}.get(prefix,'Other')
    if p.name in ('design','brand','impeccable','ui-ux-pro-max'): cat='Design/UIUX'
    rows.append(dict(old=p.name,new=new,category=cat,action='KEEP' if new==p.name else 'RENAME',manual=manual,name=name.group(1) if name else None,purpose=purpose,metadata=[f.name for f in p.iterdir() if f.is_file()],files=snapshot(p)))
dest=[r['new'].casefold() for r in rows]
assert len(dest)==len(set(dest)), 'Case-insensitive destination collision'
for p in dirs:
    for f in [p,*p.rglob('*')]:
        assert not f.is_symlink() and not f.is_junction(), f'Link/junction requires review: {f}'
for r in rows:
    if r['action']=='RENAME': assert not (BASE/r['new']).exists(),r['new']
(OUT/'inventory-before.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
lines=['# Skill Rename Map','','All entries remain direct children of `shared/skills`. Skill identities and file contents are preserved.','', '| Old | New | Category | Reason |','|---|---|---|---|']
for r in rows:
    reason='; '.join(r['manual']) or ('Protected namespace' if r['old']=='.system' or r['old'].startswith('artifact-template-') else r['purpose'][:220] or 'Existing building-architecture skill collection')
    lines.append(f"| {r['old']} | {r['new']} {'(KEEP)' if r['action']=='KEEP' else ''} | {r['category']} | {reason.replace('|','/')} |")
lines+=['','## Needs Manual Review','']
for r in rows:
    if r['manual']: lines.append('- `'+r['old']+'`: '+'; '.join(r['manual']))
lines+=['','## Compatibility','', 'No repository-wide discovery rule was found requiring frontmatter name to equal directory name. Existing names and references to skill identities remain unchanged. Plugin copies under codex and gemini retain their own paths. Existing nested containers are not flattened.','']
(ROOT/'skill-rename-map.md').write_text('\n'.join(lines),encoding='utf-8')
# Search the entire repository for every original renamed name before execution.
patterns=OUT/'old-names.txt'
patterns.write_text('\n'.join(r['old'] for r in rows if r['action']=='RENAME')+'\n',encoding='utf-8')
scan=subprocess.run(['rg','-n','-F','-f',str(patterns),'--hidden','-g','!.git/**','-g','!skill-organization-audit/**','-g','!skill-rename-map.md','-g','!organize-skills.py','.'],cwd=ROOT,capture_output=True,text=True,encoding='utf-8',errors='replace')
assert scan.returncode in (0,1),scan.stderr
(OUT/'references-before.txt').write_text(scan.stdout,encoding='utf-8')
print(json.dumps({'directories':len(rows),'root_skills':sum(r['name'] is not None for r in rows),'renames':sum(r['action']=='RENAME' for r in rows),'manual':[r['old'] for r in rows if r['manual']],'reference_lines':len(scan.stdout.splitlines())},ensure_ascii=False))
if '--execute' not in __import__('sys').argv: raise SystemExit()
for r in rows:
    if r['action']=='KEEP': continue
    old='shared/skills/'+r['old']; new='shared/skills/'+r['new']
    tracked=git('ls-files','--',old).stdout.strip()
    if tracked:
        result=git('mv','--',old,new)
        if result.returncode: raise RuntimeError(result.stderr)
    else: (BASE/r['old']).rename(BASE/r['new'])
# Update concrete paths in repository overview; identity-only references stay intact.
readme=ROOT/'README.md'
data=readme.read_bytes()
for r in rows:
    if r['action']=='RENAME':
        for sep in ('/','\\'):
            old=('shared'+sep+'skills'+sep+r['old']).encode()
            replacement=('shared'+sep+'skills'+sep+r['new']).encode()
            data=re.sub(re.escape(old)+rb'(?=[/\\\s`"\)\]]|$)',lambda m:replacement,data)
if data!=readme.read_bytes(): readme.write_bytes(data)
errors=[]
assert len(list(p for p in BASE.iterdir() if p.is_dir()))==len(rows)
for r in rows:
    actual=snapshot(BASE/r['new'])
    if actual!=r['files']: errors.append('Content/file mismatch: '+r['new'])
assert not errors,errors
after=git('status','--short').stdout
(OUT/'git-status-after.txt').write_text(after,encoding='utf-8')
cats=['.NET','Next.js','React','NestJS','Flutter','Mobile','Vercel','Supabase','Database','Testing','Security','Architecture','SketchUp','Editor','Design/UIUX','IoT','AI/Agents','Documents','Commerce','Other']
report=['# Skill Organization Verification','',f'Total skills: {sum(r["name"] is not None for r in rows)}',f'Total top-level directories: {len(rows)}',f'Renamed: {sum(r["action"]=="RENAME" for r in rows)}',f'Kept: {sum(r["action"]=="KEEP" for r in rows)}',f'Manual review: {sum(bool(r["manual"]) for r in rows)}','Errors: 0','','File paths within every directory and SHA-256 hashes are identical before and after. `.system` and all artifact-template directories are unchanged. No new nested category directories or links were created. No repository-wide validation command was found; bundled validators target individual skills/plugins and are not the repository discovery specification.','']
for cat in cats:
    report+=['## '+cat,'']
    for r in rows:
        if r['category']==cat: report.append('- `'+r['old']+'`'+(' → `'+r['new']+'`' if r['action']=='RENAME' else ' — KEEP')+(' — Needs Manual Review' if r['manual'] else ''))
    if not any(r['category']==cat for r in rows):report.append('- None')
    report.append('')
report+=['## Git status','','```text',after.rstrip(),'```','']
(ROOT/'skill-organization-report.md').write_text('\n'.join(report),encoding='utf-8')
print('Verification passed: all files and contents preserved.')
