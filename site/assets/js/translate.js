---
---
var default_lang = '{{site.lang}}';
var stored_lang = sessionStorage.getItem("lang");
var lang = default_lang;


var available_languages = [
{%- for item in site.lang_toggle.languages -%}
    "{{item.code}}",
{%- endfor -%}
];

var translations = {}

function getXHR () {
    return window.XMLHttpRequest ? new window.XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP')
}

function createStateChangeListener (xhr, callback) {
    return function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
        try {
            callback(null, JSON.parse(xhr.responseText))
        } catch (err) {
            callback(err, null)
        }
        }
    }
}

function load (location, callback) {
    const xhr = getXHR()
    xhr.open('GET', location, true)
    xhr.onreadystatechange = createStateChangeListener(xhr, callback)
    xhr.send()
}

function loadLang(lang, callback){
    if(lang in translations){
        callback()
        return
    }
    load("{{'/assets/js/' | relative_url}}strings_" + lang + ".json", function (err, json) {
        if (err) {
          throwError('failed to get JSON (' + url + ')')
        }
        translations[lang] = json;
        callback()
    });
}

translatePage =  function(){
    const elements = document.querySelectorAll("[data-i18n-key]");
    elements.forEach((element) => {
        const key = element.getAttribute("data-i18n-key");
        const translation = translations[lang][key];
        const interpolations = element.getAttribute("data-i18n-opt");
        const parsedInterpolations = interpolations ? JSON.parse(interpolations) : null;
        if(!translation & !parsedInterpolations) return;
        element.innerHTML = parsedInterpolations ? interpolate(translation, parsedInterpolations) : translation;
    });
}

function interpolate(message, interpolations) {
    return Object.keys(interpolations).reduce(
        (interpolated, key) => {
        var value = formatDate(interpolations[key], key)
        return interpolated.replace(
            new RegExp(`{\s*${key}\s*}`, "g"),
            value,
        )}, message);
}

function formatDate(value, key){
    if (key == "month") {
        return translateMonth(value)
    }
    if (key == "year") {
        return translateYear(value)
    }
    if (key=="date"){
        return translateDate(value)
    }
    return value;
}

function translateMonth(month){
    var date = new Date("1 " + month + ", 2000");
    var new_month = date.toLocaleString(lang, { month: 'long' });
    return new_month;
}

function translateYear(year){
    var date = new Date("1 1 " + year);
    var new_year = date.toLocaleString(lang, { year: "numeric" });
    return new_year;
}

function translateDate(date){
    var date = Date.parse(date);
    return new Intl.DateTimeFormat(lang, {dateStyle: "long"}).format(date)
}

setLang = function(new_lang) {
    sessionStorage.setItem("lang", new_lang)
    lang = new_lang;
    setDocumentAttrs(lang);
    loadLang(lang, function(){
        translatePage()
    });
}

function setDocumentAttrs(lang) {
  document.documentElement.lang = lang;
  document.documentElement.dir =
    lang === "ar" ? "rtl" : "ltr";
}

function bindLangSwitcher(initialValue) {
  const switcher = document.querySelector("[data-i18n-switcher]");
  switcher.value = initialValue;
  switcher.onchange = (e) => {
    setLang(e.target.value);
  };
}

window.translate = function(){
    var new_lang = default_lang;
    if(stored_lang) new_lang = stored_lang;
    setLang(new_lang)
    return new_lang;
}

document.addEventListener('DOMContentLoaded', function() {
    var new_lang = translate()
    bindLangSwitcher(new_lang)
});

function throwError (message) {
    throw new Error('Translate --- ' + message)
}