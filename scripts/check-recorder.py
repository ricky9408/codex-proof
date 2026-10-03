import json,subprocess,sys,tempfile
from pathlib import Path
runner=Path(__file__).resolve().parent.parent/'plugins/codex-proof/skills/prove-bug/scripts/proof.py'
with tempfile.TemporaryDirectory() as folder:
 def run(*args):return subprocess.run([sys.executable,str(runner),*args],capture_output=True,text=True)
 before=run('run','--out',folder,'--phase','before','--',sys.executable,'-c','print("actual failure output"); raise SystemExit(7)')
 assert before.returncode==7
 assert Path(folder,'before.stdout.txt').read_text()=='actual failure output\n'
 after=run('run','--out',folder,'--phase','after','--',sys.executable,'-c','print("actual passing output")')
 assert after.returncode==0
 report=run('report','--out',folder,'--bug','Recorder integration fixture','--limits','Recorder test only')
 assert report.returncode==0
 assert json.loads(Path(folder,'proof.json').read_text())['observed_fail_then_pass']
 timeout=run('run','--out',folder,'--phase','before','--timeout','1','--',sys.executable,'-c','import time;time.sleep(2)')
 assert timeout.returncode==124
 report=run('report','--out',folder,'--bug','Timeout fixture','--limits','Recorder test only')
 assert report.returncode==1
 assert not json.loads(Path(folder,'proof.json').read_text())['observed_fail_then_pass']
 error=run('run','--out',folder,'--phase','before','--','/nonexistent/codex-proof-executable')
 assert error.returncode==124
 assert json.loads(Path(folder,'before.json').read_text())['status']=='execution-error'
print('PASS: actual exit code/output preserved; real fail/pass paired; timeout and launch error rejected as reproduction.')
