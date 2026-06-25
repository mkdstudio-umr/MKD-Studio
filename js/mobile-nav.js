(function(){
  var nav=document.querySelector('nav');
  if(!nav)return;

  // MENU button — inherits nav's mix-blend-mode:difference + color automatically
  var btn=document.createElement('button');
  btn.className='mob-menu-btn';
  btn.setAttribute('aria-label','Open menu');
  btn.setAttribute('aria-expanded','false');
  btn.textContent='Menu';
  nav.appendChild(btn);

  // Overlay
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
    '<div class="mob-overlay-links">'+
      '<a href="/">Home</a>'+
      '<a href="/studies/">Studies</a>'+
      '<a href="/publications/">Publications</a>'+
      '<a href="/observations/">Observations</a>'+
      '<a href="/journal/">Journal</a>'+
      '<a href="/about/">About</a>'+
      '<a href="/partnerships/">Partnerships</a>'+
      '<a href="/contact/">Contact</a>'+
    '</div>';
  document.body.appendChild(ov);

  // Mark active link
  var path=window.location.pathname;
  ov.querySelectorAll('.mob-overlay-links a').forEach(function(a){
    var href=a.getAttribute('href');
    if(href==='/'&&path==='/'){ a.classList.add('active'); return; }
    if(href!=='/'&&(path===href||path.startsWith(href+'/')||path.startsWith(href))){
      a.classList.add('active');
    }
  });

  function openMenu(){
    ov.style.display='flex';
    // double rAF ensures display:flex is painted before opacity transitions
    requestAnimationFrame(function(){
      requestAnimationFrame(function(){
        ov.classList.add('is-visible');
      });
    });
    document.body.style.overflow='hidden';
    btn.setAttribute('aria-expanded','true');
  }

  function closeMenu(){
    ov.classList.remove('is-visible');
    btn.setAttribute('aria-expanded','false');
    document.body.style.overflow='';
    setTimeout(function(){ ov.style.display='none'; },280);
  }

  // Event delegation on overlay: catches CLOSE button and nav link taps reliably
  ov.addEventListener('click',function(e){
    var t=e.target;
    if(t.classList.contains('mob-overlay-close')) { closeMenu(); return; }
    // Close after link tap (allow navigation to proceed naturally)
    if(t.tagName==='A'&&t.closest('.mob-overlay-links')){ closeMenu(); }
  });

  btn.addEventListener('click',openMenu);
  document.addEventListener('keydown',function(e){ if(e.key==='Escape')closeMenu(); });
})();
