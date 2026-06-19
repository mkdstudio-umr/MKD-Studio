(function(){
  var nav=document.querySelector('nav');
  if(!nav)return;

  // Inject MENU button into nav (inherits mix-blend-mode + color from nav)
  var btn=document.createElement('button');
  btn.className='mob-menu-btn';
  btn.setAttribute('aria-label','Open menu');
  btn.setAttribute('aria-expanded','false');
  btn.textContent='Menu';
  nav.appendChild(btn);

  // Build full-screen overlay
  var ov=document.createElement('div');
  ov.className='mob-overlay';
  ov.setAttribute('role','dialog');
  ov.setAttribute('aria-modal','true');
  ov.setAttribute('aria-label','Navigation menu');
  ov.innerHTML=
    '<div class="mob-overlay-head">'+
      '<a class="mob-overlay-mark" href="/">mkd STUDIO</a>'+
      '<button class="mob-overlay-close" aria-label="Close menu">Close</button>'+
    '</div>'+
    '<nav class="mob-overlay-links">'+
      '<a href="/">Home</a>'+
      '<a href="/studies/">Studies</a>'+
      '<a href="/publications/">Publications</a>'+
      '<a href="/observations/">Observations</a>'+
      '<a href="/partnerships/">Partnerships</a>'+
      '<a href="/contact/">Contact</a>'+
    '</nav>';
  document.body.appendChild(ov);

  // Mark active link based on current path
  var path=window.location.pathname;
  ov.querySelectorAll('.mob-overlay-links a').forEach(function(a){
    var href=a.getAttribute('href');
    if(href==='/'?path==='/':path===href||path.startsWith(href+'/')||path.startsWith(href)){
      if(href==='/'&&path!=='/')return;
      a.classList.add('active');
    }
  });

  function openMenu(){
    ov.style.display='flex';
    requestAnimationFrame(function(){ ov.classList.add('is-visible'); });
    document.body.style.overflow='hidden';
    btn.setAttribute('aria-expanded','true');
  }

  function closeMenu(){
    ov.classList.remove('is-visible');
    btn.setAttribute('aria-expanded','false');
    document.body.style.overflow='';
    setTimeout(function(){ ov.style.display='none'; },260);
  }

  btn.addEventListener('click',openMenu);
  ov.querySelector('.mob-overlay-close').addEventListener('click',closeMenu);
  document.addEventListener('keydown',function(e){ if(e.key==='Escape')closeMenu(); });
})();
