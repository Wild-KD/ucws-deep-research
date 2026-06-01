/**
 * Language toggle for Research Engine pages.
 * Usage: add data-en="English text" to any element. Its innerHTML is the Chinese default.
 * Include this script at the bottom of every page, then call initLang().
 */
(function () {
  var KEY = 'research-engine-lang';

  function normalizeLang(lang) {
    return lang === 'zh' || lang === 'zh-CN' ? 'zh' : 'en';
  }

  function getStoredLang(defaultLang) {
    return normalizeLang(localStorage.getItem(KEY) || defaultLang || 'en');
  }

  function notifyLangChange(lang) {
    if (typeof window.onResearchLangChange === 'function') {
      window.onResearchLangChange(lang);
    }
    window.dispatchEvent(new CustomEvent('research-lang-change', { detail: { lang: lang } }));
  }

  function applyTextMap(lang) {
    var map = window.RESEARCH_TEXT_MAP;
    if (!map || !document.body) return;

    var entries = Array.isArray(map)
      ? map
      : Object.keys(map).map(function (from) { return [from, map[from]]; });
    entries = entries.slice().sort(function (a, b) { return b[0].length - a[0].length; });
    if (!entries.length) return;

    var skipTags = {
      SCRIPT: true,
      STYLE: true,
      NOSCRIPT: true,
      TEXTAREA: true,
      INPUT: true,
      CANVAS: true,
      SVG: true,
    };
    var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {
      acceptNode: function (node) {
        var parent = node.parentElement;
        if (!parent) return NodeFilter.FILTER_REJECT;
        if (skipTags[parent.tagName]) return NodeFilter.FILTER_REJECT;
        if (!node.nodeValue.trim()) return NodeFilter.FILTER_REJECT;
        return NodeFilter.FILTER_ACCEPT;
      },
    });

    var node;
    while ((node = walker.nextNode())) {
      if (node._researchZhText === undefined) node._researchZhText = node.nodeValue;
      if (lang !== 'en') {
        node.nodeValue = node._researchZhText;
        continue;
      }

      var translated = node._researchZhText;
      entries.forEach(function (entry) {
        var from = entry[0];
        var to = entry[1];
        translated = translated.split(from).join(to);
      });
      node.nodeValue = translated;
    }
  }

  function applyLang(lang) {
    lang = normalizeLang(lang);
    if (document._researchZhTitle === undefined) document._researchZhTitle = document.title;
    document.querySelectorAll('[data-en]').forEach(function (el) {
      if (!el._zh) el._zh = el.innerHTML;
      el.innerHTML = lang === 'en' ? el.dataset.en : el._zh;
    });
    document.querySelectorAll('[data-ph-en]').forEach(function (el) {
      if (!el._phZh) el._phZh = el.placeholder;
      el.placeholder = lang === 'en' ? el.dataset.phEn : el._phZh;
    });
    document.documentElement.lang = lang === 'en' ? 'en' : 'zh-CN';
    var titleEn = window.RESEARCH_TITLE_EN ||
      document.documentElement.getAttribute('data-title-en') ||
      (document.body && document.body.getAttribute('data-title-en'));
    if (titleEn) document.title = lang === 'en' ? titleEn : document._researchZhTitle;
    var btn = document.getElementById('langToggle');
    if (btn) btn.textContent = lang === 'en' ? '中文' : 'EN';
    applyTextMap(lang);
    notifyLangChange(lang);
  }

  window.getResearchLang = function () {
    return getStoredLang();
  };

  window.setResearchLang = function (lang) {
    lang = normalizeLang(lang);
    localStorage.setItem(KEY, lang);
    applyLang(lang);
  };

  window.toggleLang = function () {
    window.setResearchLang(getStoredLang() === 'en' ? 'zh' : 'en');
  };

  window.initLang = function (defaultLang) {
    applyLang(getStoredLang(defaultLang));
  };
})();
