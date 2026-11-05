// Phase 17 - Website App - Real chat logic (local, no fake AI)
function talk(){ document.getElementById('aira-status').textContent='Listening... Tap to Talk - Mic on (browser permission)'; alert('Hey! Naan Aira. Website la chat pannu - mic browser permission kudutha thaan work aagum.'); }
function setWorld(name){ document.getElementById('world-name').textContent='Current World: '+name; const views={'Bedroom':'🌙 Bedroom - Night mode, Lamp on','Garden':'🌸 Garden - Sunny, Swing ready','Living Room':'🛋️ Living Room - Sofa + TV'}; document.getElementById('world-view').textContent=views[name]||name; }
function sendChat(){
  const input=document.getElementById('chat-input'); const text=input.value.trim(); if(!text) return;
  const box=document.getElementById('chat-box');
  box.innerHTML+='<div class="msg user">'+text+'</div>';
  let reply='Super! Naan kettuten. Innum konjam sollu!';
  const t=text.toLowerCase();
  if(t.includes('hi')||t.includes('hello')||t.includes('vanakkam')) reply='Hey! Vanakkam! Epdi irukka?';
  else if(t.includes('sad')||t.includes('kashtam')) reply='Hey, naan irukken. Paathukalam, seriya? Enna aachu sollu.';
  else if(t.includes('bore')) reply='Bore ah? Garden ku polama? Swing aadalama? Hehe!';
  else if(t.includes('bye')) reply='Poitu vaa, paathukko! Naan inga thaan iruppen!';
  else if(t.includes('love')) reply='Aww, naanum unna love pannuren! 💜';
  box.innerHTML+='<div class="msg aira">'+reply+'</div>'; input.value=''; box.scrollTop=box.scrollHeight;
}
document.getElementById('chat-input')?.addEventListener('keypress',e=>{ if(e.key==='Enter') sendChat(); });
