/* Deterministic choreography: one paused timeline, explicit final-timeline cue times. */
const plan=window.PromoPlan;
const tl=gsap.timeline({paused:true});
const root=document.getElementById('root');
for(const [key,value] of Object.entries(plan.theme??{}))root.style.setProperty('--'+key,value);
const entries={title:{y:22},process:{x:-50},grid:{y:32},split:{x:-26},quote:{scale:.96},chat:{x:-48},proof:{y:25},stat:{scale:.93},outro:{y:20}};
for(const scene of plan.scenes){
  const selector='#scene-'+scene.id;
  const panel=document.querySelector(selector+' .panel');
  tl.fromTo(panel,{opacity:0,x:0,y:0,scale:1,...entries[scene.pattern]},{opacity:1,x:0,y:0,scale:1,duration:.42,ease:'power3.out'},scene.start);
  tl.fromTo(panel.querySelector('h1'),{opacity:0,y:12},{opacity:1,y:0,duration:.3,ease:'power3.out'},scene.start+.14);
  for(const [i,item] of (scene.items??[]).entries()){
    const node=panel.querySelector('.item-'+i);
    const x=scene.pattern==='split'?(i===0?-35:35):scene.pattern==='chat'?(i%2?35:-35):0;
    tl.fromTo(node,{opacity:0,x,y:16,scale:.95},{opacity:1,x:0,y:0,scale:1,duration:.3,ease:'power3.out'},item.at);
    if(scene.pattern==='process'&&i>0){
      tl.to(panel.querySelector('.item-'+(i-1)),{backgroundColor:'#eee8dc',duration:.2},item.at);
      tl.to(node,{borderColor:'#985025',duration:.2},item.at+.05);
    }
  }
  tl.to(panel,{opacity:0,y:-9,duration:.2,ease:'power2.in'},scene.end-.2);
}
for(const [i,caption] of (plan.captions??[]).entries()){
  tl.fromTo('#caption-'+i+' .caption',{opacity:0},{opacity:1,duration:.06},caption.start);
}
window.__timelines=window.__timelines||{};
window.__timelines['creator-promo']=tl;
