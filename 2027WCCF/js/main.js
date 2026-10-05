/* 第二十五届华盛顿中国文化节 · 交互脚本 */
(function () {
  var root = document.documentElement;

  // ---- 语言切换：zh 中文 / en 英文 / both 中英双语（默认），记住访客的选择 ----
  var buttons = document.querySelectorAll('[data-lang-set]');
  function setLang(lang) {
    root.setAttribute('data-lang', lang);
    root.setAttribute('lang', lang === 'en' ? 'en' : 'zh-CN');
    buttons.forEach(function (b) { b.classList.toggle('on', b.dataset.langSet === lang); });
    try { localStorage.setItem('wccf-lang', lang); } catch (e) {}
  }
  var saved = root.getAttribute('data-lang');
  setLang(saved === 'zh' || saved === 'en' ? saved : 'both');
  buttons.forEach(function (b) {
    b.addEventListener('click', function () { setLang(b.dataset.langSet); });
  });

  // ---- 移动端菜单 ----
  var links = document.querySelector('.nav-links');
  document.querySelector('.menu-btn').addEventListener('click', function () {
    links.classList.toggle('open');
  });
  links.addEventListener('click', function (e) {
    if (e.target.closest('a')) links.classList.remove('open');
  });

  // ---- 滚动渐入 ----
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { threshold: 0.12 });
    document.querySelectorAll('.reveal').forEach(function (el) { io.observe(el); });
  } else {
    document.querySelectorAll('.reveal').forEach(function (el) { el.classList.add('in'); });
  }

  // ---- 图库 ----
  var CATS = [
    ['all', '全部', 'All'],
    ['opening', '开幕式', 'Opening'],
    ['stage', '第一舞台', 'Main Stage'],
    ['interactive', '第二舞台·互动', 'Interactive Stage'],
    ['parade', '文化大游行', 'Parade'],
    ['culture', '文化体验', 'Culture Booths'],
    ['food', '美食街', 'Food Street'],
    ['scene', '现场花絮', 'Scenes'],
    ['roaming', '流动机位', 'Roaming'],
    ['ambassador', '嘉宾互动', 'Guests']
  ];
  var photos = window.GALLERY || [];
  var grid = document.getElementById('gallery');
  var filters = document.getElementById('filters');
  var current = [];

  function render(cat) {
    current = photos.filter(function (p) { return cat === 'all' || p.cat === cat; });
    grid.innerHTML = current.map(function (p, i) {
      return '<img loading="lazy" src="images/photos/' + p.id + '-sm.jpg" data-i="' + i +
        '" alt="第二十四届华盛顿中国文化节现场照片 ' + p.id + '">';
    }).join('');
    filters.querySelectorAll('button').forEach(function (b) {
      b.classList.toggle('on', b.dataset.cat === cat);
    });
  }
  if (grid && filters) {
    filters.innerHTML = CATS.map(function (c) {
      return '<button type="button" data-cat="' + c[0] + '"><span lang="zh">' + c[1] +
        '</span><span lang="en">' + c[2] + '</span></button>';
    }).join('');
    filters.addEventListener('click', function (e) {
      var b = e.target.closest('button');
      if (b) render(b.dataset.cat);
    });
    render('all');
  }

  // ---- 灯箱（图库和版块拼图共用） ----
  var lb = document.getElementById('lightbox');
  var lbImg = lb.querySelector('img');
  var lbCount = lb.querySelector('.lb-count');
  var list = [], idx = 0;

  function show(i) {
    idx = (i + list.length) % list.length;
    lbImg.src = list[idx];
    lbCount.textContent = (idx + 1) + ' / ' + list.length;
  }
  function open(srcs, i) { list = srcs; lb.classList.add('open'); show(i); }
  function close() { lb.classList.remove('open'); lbImg.src = ''; }

  document.addEventListener('click', function (e) {
    var img = e.target.closest('#gallery img, .mosaic img, .map img');
    if (!img) return;
    var scope = img.closest('#gallery, .mosaic, .map');
    var imgs = Array.prototype.slice.call(scope.querySelectorAll('img'));
    var srcs = imgs.map(function (el) { return el.getAttribute('src').replace('-sm.jpg', '.jpg'); });
    open(srcs, imgs.indexOf(img));
  });
  lb.querySelector('.lb-close').addEventListener('click', close);
  lb.querySelector('.lb-prev').addEventListener('click', function () { show(idx - 1); });
  lb.querySelector('.lb-next').addEventListener('click', function () { show(idx + 1); });
  lb.addEventListener('click', function (e) { if (e.target === lb) close(); });
  document.addEventListener('keydown', function (e) {
    if (!lb.classList.contains('open')) return;
    if (e.key === 'Escape') close();
    if (e.key === 'ArrowLeft') show(idx - 1);
    if (e.key === 'ArrowRight') show(idx + 1);
  });
})();
