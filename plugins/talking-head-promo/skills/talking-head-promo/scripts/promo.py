"""Unified local workflow. Stdlib only; no credentials in projects or logs."""
import argparse, hashlib, json, os, pathlib, shutil, subprocess, sys, time, threading
import urllib.request, urllib.error, uuid
import math

HERE = pathlib.Path(__file__).resolve().parent

def onboarding():
    emit('onboarding', '首次配置 ElevenLabs API Key，即可开始自动生成口播字幕',
         links={'register':'https://elevenlabs.io/app',
                'api_key':'https://elevenlabs.io/app/developers/api-keys',
                'free_plan':'https://elevenlabs.io/pricing',
                'api_pricing':'https://elevenlabs.io/pricing/api'},
         steps=['创建或编辑密钥时开启“限制密钥”，不要为方便关闭权限限制。',
                '“语音转文本 / Speech to Text”选择“访问 / Access”；“用户 / User”也选择“访问 / Access”，用于读取账户额度。',
                '其他端点保持“无权限”；建议开启“泄露后自动禁用”，设置适当有效期，并点击“创建密钥”或“保存更改”。',
                '账户额度保护另外检查免费账户和关闭超额计费；密钥权限设置不等于关闭计费。保存密钥不保证解决 401 认证错误。',
                '在自己的终端运行 setup，按隐藏提示输入密钥；不要发送到聊天。',
                '配置一次后提交口播与参考视频，由 Codex 编排后续流程。'],
         quota_note='官网 Free 套餐标注每月 10,000 积分。按通用价格页约 330 积分/分钟仅作算术估算，约 30 分钟；不是 API 免费时长保证。网页转写页另列免费 UI 12 分钟，API 采用美元计价，具体额度与扣费以账号为准。',
         billing_note='插件不会购买套餐或充值，也不会修改账户计费设置。已开通的付费或超额计费仍可能发生；使用前查看自己的账户设置。修改动画、复用已完成字幕不会再次调用转写。',
         pricing_checked='2026-09-18')

def emit(stage, message, **extra):
    print(json.dumps(dict(stage=stage, message=message, **extra), ensure_ascii=False), flush=True)

def save(file, data):
    tmp = file.with_suffix(file.suffix + '.tmp')
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    tmp.replace(file)

def load(file):
    return json.loads(file.read_text(encoding='utf-8-sig'))

def run(args, cwd=None):
    subprocess.run(args, cwd=cwd, check=True)

def doctor():
    found = {x: shutil.which(x) for x in ['node','ffmpeg','ffprobe','npx']}
    missing = [x for x,v in found.items() if not v]
    if found['node']:
        r=subprocess.run([found['node'],'-p','process.versions.node.split(".")[0]'],capture_output=True,text=True)
        if r.returncode or int(r.stdout.strip() or 0)<22: missing.append('node>=22')
    guidance=['Node.js 22+ 提供 node/npx；FFmpeg 提供 ffmpeg/ffprobe。',
              'Node.js 官方下载：https://nodejs.org/en/download',
              'FFmpeg 官方下载：https://ffmpeg.org/download.html',
              'Windows 可在用户确认后执行：winget install OpenJS.NodeJS.LTS；winget install Gyan.FFmpeg',
              'HyperFrames 不需要手动下载；首次渲染会通过 npx 下载固定版本并显示真实进度。',
              '安装后重新打开终端，再运行 doctor 验证。',
              'Talk-Flow-Studio 只检测并引导；不会未经用户确认自动安装系统软件。']
    emit('dependencies', '依赖检查完成；缺少项会给出官方下载地址和可复制命令', found=found, missing=missing, guidance=guidance)
    return not missing

def secret_path():
    return pathlib.Path(os.environ.get('LOCALAPPDATA', str(pathlib.Path.home()))) / 'TalkingHeadPromo' / 'elevenlabs.dpapi'

def setup():
    onboarding()
    if os.name != 'nt':
        raise RuntimeError('此平台请通过安全的环境管理器设置 ELEVENLABS_API_KEY；不保存明文配置。')
    target = secret_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    # Read-Host SecureString is converted to current-user DPAPI ciphertext only.
    script = "$k=Read-Host 'ElevenLabs API Key (hidden)' -AsSecureString; $k | ConvertFrom-SecureString | Set-Content -LiteralPath $env:PROMO_SECRET_FILE; Write-Host 'Saved encrypted credential'"
    env = dict(os.environ, PROMO_SECRET_FILE=str(target))
    subprocess.run(['powershell','-NoProfile','-Command',script], env=env, check=True)
    emit('credential', '密钥已按当前 Windows 用户加密保存，未写入插件或工程')

def key():
    value = os.environ.get('ELEVENLABS_API_KEY')
    if value: return value.strip()
    file = secret_path()
    if os.name == 'nt' and file.exists():
        script = "$s=Get-Content -Raw -LiteralPath $env:PROMO_SECRET_FILE | ConvertTo-SecureString; $p=[Runtime.InteropServices.Marshal]::SecureStringToBSTR($s); try {[Runtime.InteropServices.Marshal]::PtrToStringBSTR($p)} finally {[Runtime.InteropServices.Marshal]::ZeroFreeBSTR($p)}"
        r = subprocess.run(['powershell','-NoProfile','-Command',script], env=dict(os.environ,PROMO_SECRET_FILE=str(file)), capture_output=True, text=True)
        if r.returncode: raise RuntimeError('本机密钥无法解密，请重新 setup')
        return r.stdout.strip()
    onboarding()
    raise RuntimeError('缺少密钥：按上方注册链接创建后，在自己的终端运行 promo.py setup，或设置 ELEVENLABS_API_KEY。不要把密钥发到聊天。')

def captions(words, max_chars=24, max_seconds=4):
    cues=[]; group=[]
    def flush():
        if group:
            cues.append(dict(start=group[0]['start'],end=group[-1]['end'],text=''.join(w['text'] for w in group).strip()))
            group.clear()
    previous=0
    for w in words:
        if w.get('type') not in ('word','spacing'): continue
        a,b=w.get('start'),w.get('end')
        if not isinstance(a,(int,float)) or not isinstance(b,(int,float)) or a<previous or b<a:
            raise RuntimeError('转写时间点无效，不能伪造字幕时间')
        previous=b
        text=w.get('text','')
        if not isinstance(text,str): raise RuntimeError('转写文本无效')
        if group and (a-group[-1]['end']>.65 or b-group[0]['start']>max_seconds or len(''.join(x['text'] for x in group))+len(text)>max_chars): flush()
        if text.strip() or group: group.append(dict(start=a,end=b,text=text))
        if text.rstrip().endswith(('.', '!', '?', '。','！','？','；')): flush()
    flush()
    return [c for c in cues if c['text'] and c['end']>c['start']]

def stamp(t):
    ms=round(t*1000); h,ms=divmod(ms,3600000); m,ms=divmod(ms,60000); s,ms=divmod(ms,1000)
    return f'{h:02}:{m:02}:{s:02},{ms:03}'

def outputs(work, data):
    cues=captions(data.get('words',[]))
    if not cues: raise RuntimeError('没有有效逐词时间点，无法生成同步字幕')
    save(work/'captions.json',cues)
    (work/'subtitles.srt').write_text('\n\n'.join(f"{i+1}\n{stamp(c['start'])} --> {stamp(c['end'])}\n{c['text']}" for i,c in enumerate(cues))+'\n',encoding='utf-8')
    return cues

def request_transcript(audio, credential, model):
    boundary='promo-'+uuid.uuid4().hex; parts=[]
    for name,value in dict(model_id=model,timestamps_granularity='word',tag_audio_events='false',diarize='false').items():
        parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{name}"\r\n\r\n{value}\r\n'.encode())
    parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="speech.flac"\r\nContent-Type: audio/flac\r\n\r\n'.encode()+audio.read_bytes()+b'\r\n')
    parts.append(f'--{boundary}--\r\n'.encode())
    req=urllib.request.Request('https://api.elevenlabs.io/v1/speech-to-text',data=b''.join(parts),headers={'xi-api-key':credential,'Content-Type':'multipart/form-data; boundary='+boundary})
    try:
        with urllib.request.urlopen(req,timeout=600) as r: return json.load(r)
    except urllib.error.HTTPError as e:
        hint={401:'密钥无效',403:'缺少 Speech-to-Text 权限',429:'额度或速率限制'}.get(e.code,'服务错误')
        raise RuntimeError(f'ElevenLabs HTTP {e.code}: {hint}；未自动重试') from None
    except (OSError,TimeoutError):
        raise RuntimeError('网络请求结果不确定，可能已计费。检查服务记录后，明确允许重试；不会自动重发。') from None

def quota_decision(subscription, seconds):
    if not isinstance(subscription,dict): raise RuntimeError('额度保护：无法读取额度，停止上传')
    # Strict free-only mode, no silent opt-out or paid-tier fallback.
    if subscription.get('tier')!='free': raise RuntimeError('额度保护：无法确认是免费账户，停止上传')
    if type(subscription.get('max_credit_limit_extension')) is not int or subscription['max_credit_limit_extension']!=0:
        raise RuntimeError('额度保护：超额计费未明确关闭。请在 ElevenLabs 关闭 usage-based billing 后重试')
    used,limit=subscription.get('character_count'),subscription.get('character_limit')
    if type(used) is not int or type(limit) is not int or used<0 or limit<0:
        raise RuntimeError('额度保护：额度数据不完整，停止上传')
    if not math.isfinite(seconds) or seconds<=0: raise RuntimeError('额度保护：音频时长不明确，停止上传')
    remaining=max(0,limit-used)
    # Safety reserve, NOT a provider price or guaranteed API entitlement.
    reserve=math.ceil(seconds/60)*1000+1500
    if remaining<reserve: raise RuntimeError(f'额度保护：剩余 {remaining} 积分不足安全预留 {reserve}，已停止；不会发送转写请求')
    return dict(remaining=remaining,safety_reserve=reserve)

def check_quota(credential, source):
    emit('quota','检查免费额度与超额计费设置；检查失败就停止')
    req=urllib.request.Request('https://api.elevenlabs.io/v1/user/subscription',headers={'xi-api-key':credential})
    try:
        with urllib.request.urlopen(req,timeout=30) as r: subscription=json.load(r)
    except (OSError,ValueError):
        raise RuntimeError('额度保护：无法查询账户。请给密钥开启账户/订阅只读权限；未发送转写请求') from None
    probe=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',str(source)],capture_output=True,text=True)
    if probe.returncode: raise RuntimeError('额度保护：无法核实音频时长，停止上传')
    try: seconds=float(probe.stdout.strip())
    except ValueError: raise RuntimeError('额度保护：时长无效，停止上传') from None
    result=quota_decision(subscription,seconds)
    emit('quota','免费账户安全预检查通过；不代表提供商的计费保证',**result)
    return result

def prepare(args):
    if not doctor(): raise RuntimeError('依赖缺失，按提示安装后再次运行')
    source=pathlib.Path(args.video).resolve()
    if not source.is_file(): raise RuntimeError('口播文件不存在')
    work=pathlib.Path(args.project).resolve(); work.mkdir(parents=True,exist_ok=True)
    digest=hashlib.sha256()
    with source.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''): digest.update(chunk)
    signature=digest.hexdigest()
    statefile=work/'workflow.json'
    state=load(statefile) if statefile.exists() else {}
    if state and (state.get('source_sha256')!=signature or state.get('model')!=args.model): raise RuntimeError('来源或模型改变，请使用新工程目录，避免串字幕')
    if not state:
        state=dict(source_sha256=signature,model=args.model,stage='created');save(statefile,state)
    raw=work/'transcript.json'
    if raw.exists():
        outputs(work,load(raw));emit('transcription','复用已有转写，不会再次收费');return
    if state['stage'] in ('uploading','uncertain','failed') and not args.retry_upload:
        raise RuntimeError('上次请求未完成。确认可重复计费后用 --retry-upload 重试；已完成步骤保留。')
    credential=key()
    if not args.allow_upload: raise RuntimeError('转写需要将音频上传 ElevenLabs 并可能收费；用户同意后添加 --allow-upload')
    check_quota(credential,source)
    audio=work/'speech.flac'
    if not audio.exists():
        emit('extract','提取口播音频')
        temporary=work/('speech-'+uuid.uuid4().hex+'.flac')
        run(['ffmpeg','-v','error','-i',str(source),'-vn','-ac','1','-ar','16000','-c:a','flac',str(temporary)])
        temporary.replace(audio)
    state['stage']='uploading';save(statefile,state)
    stop=threading.Event(); started=time.monotonic()
    def heartbeat():
        while not stop.wait(10): emit('transcribing','正在转写；实际时间取决于片长、网络与服务负载',elapsed_seconds=round(time.monotonic()-started),estimated_seconds=None)
    threading.Thread(target=heartbeat,daemon=True).start()
    emit('transcribing','上传并转写中；不显示虚假的百分比，最长请求等待 10 分钟')
    try:
        data=request_transcript(audio,credential,args.model);save(raw,data)
        cues=outputs(work,data);state['stage']='transcribed';save(statefile,state)
        emit('ready','转写完成，请 Codex 按参考设计分镜，再执行 finish',captions=len(cues),srt=str(work/'subtitles.srt'))
    except Exception:
        state['stage']='uncertain';save(statefile,state);raise
    finally: stop.set()

def finish(args):
    if not doctor(): raise RuntimeError('依赖缺失，请按提示安装后恢复')
    work=pathlib.Path(args.project).resolve();p=load(work/'plan.json')
    p['captions']=load(work/'captions.json');save(work/'plan-captioned.json',p)
    output=work/'composition'
    emit('build','合并字幕与设计分镜')
    if not output.exists(): run(['node',str(HERE/'studio.mjs'),'build',str(work/'plan-captioned.json'),str(output)])
    elif load(output/'plan.json')!=p: raise RuntimeError('已有构图与最新分镜不一致，请使用新版本工程，不覆盖已编辑内容')
    if args.render:
        npx=shutil.which('npx.cmd') if os.name=='nt' else shutil.which('npx')
        emit('check','检查布局与时间轴');run([npx,'--yes','hyperframes@0.8.46','check'],cwd=output)
        video=output/'renders'/'video.mp4'
        if not video.exists():
            emit('render','渲染中，下面显示渲染器的真实进度');run([npx,'--yes','hyperframes@0.8.46','render','--quality','looks','--output','renders/video.mp4'],cwd=output)
        run(['node',str(HERE/'studio.mjs'),'verify',str(video),str(work/'plan-captioned.json')])
        emit('complete','成片参数核验完成；仍需试听和画面复核',video=str(video))
    else: emit('preview','字幕已进入可编辑工程',project=str(output))

def main():
    p=argparse.ArgumentParser();sub=p.add_subparsers(dest='command',required=True)
    sub.add_parser('doctor');sub.add_parser('setup');sub.add_parser('onboarding')
    q=sub.add_parser('prepare');q.add_argument('--video',required=True);q.add_argument('--project',required=True);q.add_argument('--model',default='scribe_v2');q.add_argument('--allow-upload',action='store_true');q.add_argument('--retry-upload',action='store_true')
    q=sub.add_parser('finish');q.add_argument('--project',required=True);q.add_argument('--render',action='store_true')
    args=p.parse_args()
    try:
        if args.command=='doctor': return 0 if doctor() else 1
        if args.command=='onboarding': onboarding()
        if args.command=='setup': setup()
        if args.command in ('prepare','finish'):
            work=pathlib.Path(args.project).resolve();work.mkdir(parents=True,exist_ok=True)
            lock=work/'.workflow.lock'
            try: fd=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY)
            except FileExistsError: raise RuntimeError('工程正在运行或存在中断锁。确认没有制作进程后移除 .workflow.lock 再恢复，避免重复收费。')
            os.close(fd)
            try:
                if args.command=='prepare': prepare(args)
                else: finish(args)
            finally: lock.unlink(missing_ok=True)
        return 0
    except Exception as e: emit('error',str(e));return 1

if __name__=='__main__': sys.exit(main())

