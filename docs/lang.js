/**
 * Language toggle for Research Engine pages.
 * Usage: add data-en="English text" to any element. Its innerHTML is the Chinese default.
 * Include this script at the bottom of every page, then call initLang().
 */
(function () {
  var KEY = 'research-engine-lang';

  function applyLang(lang) {
    document.querySelectorAll('[data-en]').forEach(function (el) {
      if (!el._zh) el._zh = el.innerHTML;
      el.innerHTML = lang === 'en' ? el.dataset.en : el._zh;
    });
    document.querySelectorAll('[data-ph-en]').forEach(function (el) {
      if (!el._phZh) el._phZh = el.placeholder;
      el.placeholder = lang === 'en' ? el.dataset.phEn : el._phZh;
    });
    document.documentElement.lang = lang === 'en' ? 'en' : 'zh-CN';
    var btn = document.getElementById('langToggle');
    if (btn) btn.textContent = lang === 'en' ? '中文' : 'EN';
  }

  window.toggleLang = function () {
    var lang = localStorage.getItem(KEY) === 'en' ? 'zh' : 'en';
    localStorage.setItem(KEY, lang);
    applyLang(lang);
  };

  window.initLang = function () {
    applyLang(localStorage.getItem(KEY) || 'en');
  };
})();
