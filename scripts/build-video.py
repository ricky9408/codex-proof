from pathlib import Path
import subprocess,json
root=Path(__file__).resolve().parent.parent
segments=[('intro-slide.png',3),('before.webm',3),('before.png',3),('tests-slide.png',4),('after.webm',3),('after.png',3),('end-slide.png',3)]
paths=[]
for i,(name,seconds) in enumerate(segments):
 source=root/'evidence'/name;out=root/'evidence'/f'demo-segment-{i}.mp4'
 args=['ffmpeg','-y','-loglevel','error']
 if source.suffix=='.png':args+=['-loop','1']
 vf='scale=1280:720,fps=30,format=yuv420p' if source.suffix=='.png' else 'scale=1280:800,crop=1280:712:0:0,pad=1280:720:0:0:color=0xf6f8fc,fps=30,format=yuv420p'
 args+=['-i',str(source),'-t',str(seconds),'-vf',vf,'-an','-c:v','libx264','-preset','fast','-crf','20',str(out)]
 subprocess.run(args,check=True);paths.append(out)
concat=root/'evidence/demo-concat.txt';concat.write_text('\n'.join("file '"+p.name+"'" for p in paths)+'\n')
output=root/'codex-proof-demo.mp4';subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',str(concat),'-c','copy','-movflags','+faststart',str(output)],check=True)
info=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration,size:stream=codec_name,width,height,pix_fmt','-of','json',str(output)],capture_output=True,text=True,check=True)
(root/'evidence/video-metadata.json').write_text(info.stdout);print(info.stdout)
for p in paths:p.unlink()
concat.unlink()
