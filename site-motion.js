(() => {
 const figure=document.querySelector('.topology-canvas');
 if(!figure)return;
 const details={
 server:['Teamserver','Both operator interfaces share the same server-side policy and state.',['Access & scope','RBAC, operations and target scope'],['Identity & sessions','Enrollment records and agent check-ins'],['Tasks & storage','Task results and the SQLite journal']],
 cli:['Operator CLI','The command-line interface connects to the teamserver over gRPC with mutual TLS.',['Connection','gRPC · mTLS'],['Operator interface','Interactive CLI / REPL'],['Policy boundary','Server-side roles and operation scope']],
 dashboard:['Web dashboard','An optional browser interface to the same teamserver.',['Connection','HTTPS with CSRF protection for mutations'],['Operator interface','Browser web session'],['Policy boundary','Shared server-side authorization']],
 linux:['Linux agent','The Linux / amd64 runtime supports interactive PTY sessions.',['Capabilities','Exec, shell / PTY, port forwarding and process listing'],['Communication','Session and beacon modes; transport-dependent behavior'],['Results','Durable results and platform-specific OPSEC modules']],
 windows:['Windows agent','The Windows / amd64 runtime uses one-shot command execution.',['Capabilities','Exec, port forwarding and process listing'],['Communication','Session and beacon modes; transport-dependent behavior'],['Results','Durable results and Windows-specific OPSEC modules']]
 };
 figure.querySelectorAll('[data-topology]').forEach(button=>button.addEventListener('click',()=>{
  figure.querySelectorAll('[data-topology]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));
  const data=details[button.dataset.topology],panel=figure.querySelector('.topology-detail');
  panel.querySelector('h3').textContent=data[0];panel.querySelector('p').textContent=data[1];
  panel.querySelectorAll('li').forEach((li,i)=>{li.querySelector('strong').textContent=data[i+2][0];li.querySelector('span').textContent=data[i+2][1]});
 }));
 const toggle=figure.querySelector('.topology-motion');
 toggle.addEventListener('click',()=>{const paused=toggle.getAttribute('aria-pressed')!=='true';toggle.setAttribute('aria-pressed',String(paused));toggle.textContent=paused?'Resume motion':'Pause motion';figure.classList.toggle('topology-paused',paused)});
 const reduced=matchMedia('(prefers-reduced-motion: reduce)');
 let observer;
 const sync=()=>{observer?.disconnect();document.querySelectorAll('.motion-await').forEach(n=>n.classList.remove('motion-await'));if(reduced.matches||!('IntersectionObserver'in window))return;observer=new IntersectionObserver(entries=>entries.forEach(e=>{if(e.isIntersecting){e.target.classList.remove('motion-await');observer.unobserve(e.target)}}),{threshold:.05});document.querySelectorAll('.section-heading,.opsec-platform,.table-scroll,.topology-canvas').forEach(node=>{if(node.getBoundingClientRect().top>innerHeight){node.classList.add('motion-await');observer.observe(node)}})};
 reduced.addEventListener('change',sync);sync();
})();
