#!/usr/bin/env python3
"""Local evidence recorder. Executes an explicit argv; never uses a shell."""
import argparse, hashlib, json, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path

def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='action',required=True)
    run=sub.add_parser('run');run.add_argument('--out',required=True);run.add_argument('--phase',choices=['before','after'],required=True);run.add_argument('--cwd',default='.');run.add_argument('--source',action='append',default=[]);run.add_argument('--timeout',type=int,default=120);run.add_argument('command',nargs=argparse.REMAINDER)
    report=sub.add_parser('report');report.add_argument('--out',required=True);report.add_argument('--bug',required=True);report.add_argument('--limits',required=True);report.add_argument('--artifact',action='append',default=[])
    args=parser.parse_args();out=Path(args.out).resolve();out.mkdir(parents=True,exist_ok=True)
    if args.action=='run':
        command=args.command[1:] if args.command[:1]==['--'] else args.command
        if not command:parser.error('explicit command after -- is required')
        cwd=Path(args.cwd).resolve(); started=datetime.now(timezone.utc).isoformat()
        sources=[]
        for source in args.source:
            p=(cwd/source).resolve();sources.append({'path':source,'sha256':digest(p)})
        try:
            result=subprocess.run(command,cwd=cwd,capture_output=True,timeout=args.timeout)
            stdout,stderr,code=result.stdout,result.stderr,result.returncode;status='completed'
        except subprocess.TimeoutExpired as e:
            stdout,stderr,code=e.stdout or b'',e.stderr or b'',None;status='timeout'
        except OSError as e:
            stdout,stderr,code=b'',str(e).encode(),None;status='execution-error'
        (out/f'{args.phase}.stdout.txt').write_bytes(stdout);(out/f'{args.phase}.stderr.txt').write_bytes(stderr)
        record={'phase':args.phase,'command':command,'cwd':str(cwd),'started_at':started,'finished_at':datetime.now(timezone.utc).isoformat(),'exit_code':code,'status':status,'sources':sources,'stdout_sha256':hashlib.sha256(stdout).hexdigest(),'stderr_sha256':hashlib.sha256(stderr).hexdigest()}
        (out/f'{args.phase}.json').write_text(json.dumps(record,indent=2)+'\n')
        sys.stdout.buffer.write(stdout);sys.stderr.buffer.write(stderr)
        return code if code is not None and 0<=code<=255 else 124
    records=[json.loads((out/f'{phase}.json').read_text()) for phase in ('before','after')]
    artifacts=[]
    for name in args.artifact:
        p=(out/name).resolve()
        if not p.is_relative_to(out):parser.error('artifacts must remain inside evidence directory')
        artifacts.append({'path':name,'sha256':digest(p),'bytes':p.stat().st_size})
    before,after=records
    paired=before['status']=='completed' and before['exit_code'] not in (None,0) and after['status']=='completed' and after['exit_code']==0
    report={'bug':args.bug,'limits':args.limits,'observed_fail_then_pass':paired,'warning':'Exit codes alone do not establish a meaningful regression. Review assertions and raw logs. Screenshots are observations, not a general correctness guarantee.','runs':records,'artifacts':artifacts}
    (out/'proof.json').write_text(json.dumps(report,indent=2)+'\n')
    lines=['# Codex Proof evidence',args.bug,'','| Phase | Exit | Status |','|---|---:|---|']+[f"| {r['phase']} | {r['exit_code']} | {r['status']} |" for r in records]
    lines+=['','## Evidence limits',args.limits,'',report['warning'],'','## Artifacts']+[f"- `{a['path']}` — SHA-256 `{a['sha256']}`" for a in artifacts]
    (out/'PROOF.md').write_text('\n'.join(lines)+'\n');print(json.dumps({'observed_fail_then_pass':paired,'report':str(out/'PROOF.md')}));return 0 if paired else 1
if __name__=='__main__':sys.exit(main())
