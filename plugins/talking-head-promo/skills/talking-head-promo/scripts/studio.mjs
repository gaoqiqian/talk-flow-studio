import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';

const here=path.dirname(fileURLToPath(import.meta.url));
const patterns=new Set(['title','process','grid','split','quote','chat','proof','stat','outro']);
const finite=x=>typeof x==='number'&&Number.isFinite(x);
const read=file=>JSON.parse(fs.readFileSync(file,'utf8').replace(/^\uFEFF/,''));
const relative=p=>typeof p==='string'&&p.length>0&&!path.isAbsolute(p)&&!/[\\]/.test(p)&&!p.split('/').includes('..')&&!/^[a-z]+:/i.test(p);
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));

export function validatePlan(p){
  const errors=[],warnings=[];
  if(!p||typeof p!=='object')return{ok:false,errors:['plan must be an object'],warnings};
  if(!finite(p.duration)||p.duration<=0)errors.push('duration must be positive seconds');
  if(![24,30,60].includes(p.fps))errors.push('fps must be 24, 30 or 60');
  if(p.width!==1280||p.height!==720)errors.push('starter supports 1280x720; adapt the layout before choosing another canvas');
  if(p.source!==undefined&&!relative(p.source))errors.push('source must be a project-relative file using forward slashes');
  if(p.speakerOffsetX!==undefined&&(!finite(p.speakerOffsetX)||Math.abs(p.speakerOffsetX)>320))errors.push('speakerOffsetX must be a finite pixel offset between -320 and 320');
  if(p.source&&p.speakerOffsetX===undefined)warnings.push('speaker framing is unconfirmed: inspect source and exported face clearance; centered footage may be obscured');
  if(p.theme!==undefined&&(p.theme===null||typeof p.theme!=='object'||Array.isArray(p.theme)))errors.push('theme must be an object');
  if(p.theme&&typeof p.theme==='object')for(const [key,value] of Object.entries(p.theme)){
    if(!['ink','paper','accent'].includes(key)||!/^#[0-9a-f]{6}$/i.test(value))errors.push('theme accepts ink/paper/accent hex colors only');
  }
  const scenes=Array.isArray(p.scenes)?p.scenes:[];
  if(!scenes.length)errors.push('scenes must be a non-empty array');
  const ids=new Set();let previousEnd=0;
  scenes.forEach((s,i)=>{
    const prefix='scene '+i+': ';
    if(!s||typeof s!=='object'){errors.push(prefix+'must be an object');return;}
    if(typeof s.id!=='string'||!/^[a-z][a-z0-9-]*$/.test(s.id)||ids.has(s.id))errors.push(prefix+'id must be a unique lowercase slug');
    ids.add(s.id);
    if(!patterns.has(s.pattern))errors.push(prefix+'unknown pattern');
    if(!finite(s.start)||!finite(s.end)||s.start<0||s.end<=s.start||s.end>p.duration)errors.push(prefix+'invalid final-timeline window');
    if(s.start<previousEnd)errors.push(prefix+'scenes must be chronological and non-overlapping');
    previousEnd=s.end;
    if(typeof s.title!=='string'||!s.title.trim())errors.push(prefix+'title is required');
    if(s.title?.length>54)warnings.push(prefix+'title may need copy reduction or a custom layout');
    if(typeof s.body==='string'&&s.body.length>130)warnings.push(prefix+'body is dense; simplify or split');
    if(s.end-s.start>12)warnings.push(prefix+'long hold: plan a progressive build or deliberate presenter pause');
    if(s.items!==undefined&&!Array.isArray(s.items))errors.push(prefix+'items must be an array');
    const items=Array.isArray(s.items)?s.items:[];
    if(items.length>8)errors.push(prefix+'starter allows at most eight items');
    if(s.pattern==='split'&&items.length!==2)errors.push(prefix+'split needs exactly two items');
    if(s.pattern==='proof'&&!relative(s.asset))errors.push(prefix+'proof needs a project-relative asset');
    if(s.pattern==='chat'&&!s.illustration)errors.push(prefix+'starter chat is illustrative; set illustration=true or use actual evidence');
    let last=s.start;
    items.forEach((item,j)=>{
      if(typeof item?.text!=='string'||!item.text.trim())errors.push(prefix+'item '+j+' text required');
      if(!finite(item?.at)||item.at<s.start||item.at>s.end-.35||item.at<last)errors.push(prefix+'item '+j+' cue must be chronological and inside the beat with settle time');
      last=item?.at;
      if(item?.text?.length>64)warnings.push(prefix+'item '+j+' may be difficult to read');
    });
    if(scenes[i-1]?.pattern===s.pattern&&scenes[i-2]?.pattern===s.pattern)warnings.push(prefix+'three identical visual forms; review variety');
  });
  let captionEnd=0;
  if(p.captions!==undefined&&!Array.isArray(p.captions))errors.push('captions must be an array');
  for(const [i,c] of (Array.isArray(p.captions)?p.captions:[]).entries()){
    if(!c||typeof c!=='object'){errors.push('caption '+i+': must be an object');continue;}
    if(!finite(c.start)||!finite(c.end)||c.start<captionEnd||c.end<=c.start||c.end>p.duration||typeof c.text!=='string'||!c.text.trim())errors.push('caption '+i+': invalid window or text');
    captionEnd=c.end;
    if(c.text?.length>64)warnings.push('caption '+i+': split long copy into readable cues');
  }
  return{ok:errors.length===0,errors,warnings};
}

export function mapTranscript(transcript,cuts){
  if(!Array.isArray(transcript)||!Array.isArray(cuts)||!cuts.length)throw Error('transcript and cuts must be arrays; cuts cannot be empty');
  let final=0,previousSourceEnd=0;
  const windows=cuts.map((cut,i)=>{
    const {sourceStart,sourceEnd}=cut;
    if(!finite(sourceStart)||!finite(sourceEnd)||sourceStart<0||sourceEnd<=sourceStart||sourceStart<previousSourceEnd)throw Error('cut '+i+' must be positive, chronological and non-overlapping');
    previousSourceEnd=sourceEnd;
    const w={...cut,finalStart:final};final+=sourceEnd-sourceStart;return w;
  });
  const segments=[];
  transcript.forEach((segment,i)=>{
    if(!finite(segment.start)||!finite(segment.end)||segment.end<=segment.start||typeof segment.text!=='string')throw Error('invalid transcript segment '+i);
    for(const w of windows){
      const a=Math.max(segment.start,w.sourceStart),b=Math.min(segment.end,w.sourceEnd);
      if(a<b)segments.push({...segment,start:w.finalStart+a-w.sourceStart,end:w.finalStart+b-w.sourceStart,sourceStart:a,sourceEnd:b,needsTextReview:a!==segment.start||b!==segment.end});
    }
  });
  return{duration:final,windows,segments};
}

function renderScene(s,i){
  const items=(s.items??[]).map((item,j)=>'<div class="item item-'+j+'"><b>'+String(j+1).padStart(2,'0')+'</b><span>'+esc(item.text)+'</span></div>').join('');
  const evidence=s.pattern==='proof'?'<figure><img src="'+esc(s.asset)+'" alt="'+esc(s.assetLabel??'Product evidence')+'"><figcaption>'+esc(s.assetLabel??'Real screenshot supplied for this project')+'</figcaption></figure>':'';
  const illustration=s.illustration?'<div class="disclosure">Illustrative example</div>':'';
  return '<section class="clip scene pattern-'+s.pattern+'" id="scene-'+s.id+'" data-start="'+s.start+'" data-duration="'+(s.end-s.start)+'" data-track-index="'+(i+2)+'"><div class="panel"><div class="eyebrow">'+esc(s.kicker??String(i+1).padStart(2,'0')+' / '+s.pattern.toUpperCase())+'</div><h1>'+esc(s.title)+'</h1>'+(s.body?'<p class="body">'+esc(s.body)+'</p>':'')+'<div class="items">'+items+'</div>'+evidence+illustration+'</div></section>';
}

export function buildProject(planFile,out){
  const p=read(planFile),audit=validatePlan(p);
  if(!audit.ok)throw Error(audit.errors.join('\n'));
  const output=path.resolve(out),base=path.dirname(path.resolve(planFile));
  if(fs.existsSync(output)&&fs.readdirSync(output).length)throw Error('output must be a new or empty directory; never overwrite an existing project');
  const files=[...(p.source?[p.source]:[]),...p.scenes.filter(s=>s.asset).map(s=>s.asset)];
  for(const name of files){if(!relative(name))throw Error('unsafe asset path');if(!fs.statSync(path.resolve(base,name)).isFile())throw Error('asset is not a file: '+name);}
  fs.mkdirSync(output,{recursive:true});
  for(const name of new Set(files)){
    const dest=path.join(output,name);fs.mkdirSync(path.dirname(dest),{recursive:true});fs.copyFileSync(path.resolve(base,name),dest);
  }
  const template=fs.readFileSync(path.join(here,'../assets/starter.html'),'utf8');
  const captions=(p.captions??[]).map((c,i)=>'<div class="clip caption-clip" id="caption-'+i+'" data-start="'+c.start+'" data-duration="'+(c.end-c.start)+'" data-track-index="30"><div class="caption">'+esc(c.text)+'</div></div>').join('');
  const media=p.source?'<video id="speaker-video" src="'+esc(p.source)+'" muted playsinline data-start="0" data-duration="'+p.duration+'" data-track-index="0"></video><audio id="speaker-audio" src="'+esc(p.source)+'" data-start="0" data-duration="'+p.duration+'" data-track-index="1"></audio>':'<div class="presenter-demo"><span>PRESENTER AREA</span><p>Illustrative demo · replace with your video</p></div>';
  const slots={DURATION:String(p.duration),FPS:String(p.fps),MEDIA:media,SCENES:p.scenes.map(renderScene).join('')+captions,RUNTIME:fs.readFileSync(path.join(here,'../assets/runtime.js'),'utf8')};
  const framing='<style>#speaker-video{transform:translateX('+String(p.speakerOffsetX??0)+'px)}</style>';
  const html=template.replace(/__([A-Z]+)__/g,(_,key)=>slots[key]??'').replace('</head>',framing+'</head>');
  fs.writeFileSync(path.join(output,'index.html'),html);
  fs.mkdirSync(path.join(output,'motion'),{recursive:true});
  fs.copyFileSync(path.join(here,'../assets/runtime.js'),path.join(output,'motion/runtime.js'));
  fs.copyFileSync(path.join(here,'../assets/style.css'),path.join(output,'motion/style.css'));
  const safeJson=JSON.stringify(p).replace(/</g,'\\u003c').replace(/\u2028/g,'\\u2028').replace(/\u2029/g,'\\u2029');
  fs.writeFileSync(path.join(output,'motion/plan.js'),'window.PromoPlan='+safeJson+';\n');
  fs.writeFileSync(path.join(output,'plan.json'),JSON.stringify(p,null,2)+'\n');
  fs.writeFileSync(path.join(output,'package.json'),JSON.stringify({name:'creator-video',private:true,scripts:{check:'npx --yes hyperframes@0.8.46 check',preview:'npx --yes hyperframes@0.8.46 preview',render:'npx --yes hyperframes@0.8.46 render --quality looks --output renders/video.mp4'}},null,2)+'\n');
  return{output,...audit};
}

export function probeMedia(file){
  const result=spawnSync('ffprobe',['-v','error','-show_streams','-show_format','-of','json',file],{encoding:'utf8',windowsHide:true,maxBuffer:8*1024*1024});
  if(result.error)throw Error('ffprobe unavailable: '+result.error.message);
  if(result.status!==0)throw Error(result.stderr.trim()||'ffprobe failed');
  const data=JSON.parse(result.stdout),video=data.streams.find(s=>s.codec_type==='video'),audio=data.streams.find(s=>s.codec_type==='audio');
  const rate=video?.avg_frame_rate?.split('/').map(Number),fps=rate?.[1]?rate[0]/rate[1]:null;
  return{duration:Number(data.format.duration),bytes:Number(data.format.size),width:video?.width,height:video?.height,fps,videoCodec:video?.codec_name,audioCodec:audio?.codec_name??null};
}

export function verifyMedia(meta,p){
  const errors=[];
  if(!meta.videoCodec)errors.push('missing video stream');
  if(!meta.audioCodec&&p.source)errors.push('missing voice/audio stream');
  if(meta.width!==p.width||meta.height!==p.height)errors.push('dimensions differ from plan');
  if(!finite(meta.fps)||Math.abs(meta.fps-p.fps)>.02)errors.push('fps differs from plan');
  if(!finite(meta.duration)||Math.abs(meta.duration-p.duration)>1/p.fps+.05)errors.push('duration differs from plan by more than one frame plus encoder rounding');
  return{ok:!errors.length,errors,media:meta};
}

if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){
  try{
    const [command,...args]=process.argv.slice(2);let result;
    if(command==='check')result=validatePlan(read(args[0]));
    else if(command==='map')result=mapTranscript(read(args[0]),read(args[1]));
    else if(command==='build')result=buildProject(args[0],args[1]);
    else if(command==='probe')result=probeMedia(args[0]);
    else if(command==='verify')result=verifyMedia(probeMedia(args[0]),read(args[1]));
    else throw Error('Usage: node studio.mjs check PLAN | map TRANSCRIPT CUTS | build PLAN NEW_DIR | probe VIDEO | verify VIDEO PLAN');
    process.stdout.write(JSON.stringify(result,null,2)+'\n');
    if(result.ok===false)process.exitCode=1;
  }catch(error){process.stderr.write(error.message+'\n');process.exitCode=1;}
}
