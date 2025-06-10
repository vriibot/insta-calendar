/*!
  * Simple-Jekyll-Search
  * Copyright 2015-2020, Christian Fei
  * Licensed under the MIT License.
  */

(function(){
  'use strict'
  
  var _$Templater_7 = {
    compile: compile,
    setOptions: setOptions
  }
  
  const options = {}
  options.pattern = /\{(.*?)\}/g
  options.template = ''
  options.middleware = function () {}
  
  function setOptions (_options) {
    options.pattern = _options.pattern || options.pattern
    options.template = _options.template || options.template
    if (typeof _options.middleware === 'function') {
      options.middleware = _options.middleware
    }
  }
  
  function compile (data) {
    return options.template.replace(options.pattern, function (match, prop) {
      const value = options.middleware(prop, data[prop], options.template)
      if (typeof value !== 'undefined') {
        return value
      }
      return data[prop] || match
    })
  }
  
  'use strict';
  
  var _$Repository_4 = {
    put: put,
    clear: clear,
    search: search,
    setOptions: __setOptions_4
  }
  
  function NoSort () {
    return 0
  }
  
  const data = []
  let opt = {}
  
  opt.limit = 10
  opt.sort = NoSort
  
  function put (data) {
    if (isObject(data)) {
      return addObject(data)
    }
    if (isArray(data)) {
      return addArray(data)
    }
    return undefined
  }
  function clear () {
    data.length = 0
    return data
  }
  
  function isObject (obj) {
    return Boolean(obj) && Object.prototype.toString.call(obj) === '[object Object]'
  }
  
  function isArray (obj) {
    return Boolean(obj) && Object.prototype.toString.call(obj) === '[object Array]'
  }
  
  function addObject (_data) {
    data.push(_data)
    return data
  }
  
  function addArray (_data) {
    const added = []
    clear()
    for (let i = 0, len = _data.length; i < len; i++) {
      if (isObject(_data[i])) {
        added.push(addObject(_data[i]))
      }
    }
    return added
  }
  
  function search (startDate, endDate) {
    return findMatches(data, startDate, endDate, opt).sort(opt.sort)
  }
  
  function __setOptions_4 (_opt) {
    opt = _opt || {}
  
    opt.limit = _opt.limit || 10
    opt.sort = _opt.sort || NoSort
  }
  
  function findMatches (data, startDate, endDate, opt) {
    const matches = []
    for (let i = 0; i < data.length && matches.length < opt.limit; i++) {
      const match = findMatchesInObject(data[i], startDate, endDate)
      if (match) {
        matches.push(match)
      }
    }
    return matches
  }
  
  function findMatchesInObject (obj, startDate, endDate) {
    var date = obj['date'];
    if(!date) return;
    date = new Date(date)
    if(date >= startDate){
      if(!endDate) return obj;
      if(endDate && date <= endDate) return obj;
    }
  }
  
  /* globals ActiveXObject:false */
  
  'use strict'
  
  var _$JSONLoader_2 = {
    load: load
  }
  
  function load (location, callback) {
    const xhr = getXHR()
    xhr.open('GET', location, true)
    xhr.onreadystatechange = createStateChangeListener(xhr, callback)
    xhr.send()
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
  
  function getXHR () {
    return window.XMLHttpRequest ? new window.XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP')
  }
  
  'use strict'
  
  var _$OptionsValidator_3 = function OptionsValidator (params) {
    if (!validateParams(params)) {
      throw new Error('-- OptionsValidator: required options missing')
    }
  
    if (!(this instanceof OptionsValidator)) {
      return new OptionsValidator(params)
    }
  
    const requiredOptions = params.required
  
    this.getRequiredOptions = function () {
      return requiredOptions
    }
  
    this.validate = function (parameters) {
      const errors = []
      requiredOptions.forEach(function (requiredOptionName) {
        if (typeof parameters[requiredOptionName] === 'undefined') {
          errors.push(requiredOptionName)
        }
      })
      return errors
    }
  
    function validateParams (params) {
      if (!params) {
        return false
      }
      return typeof params.required !== 'undefined' && params.required instanceof Array
    }
  }
  
  'use strict'
  
  var _$utils_9 = {
    merge: merge,
    isJSON: isJSON
  }
  
  function merge (defaultParams, mergeParams) {
    const mergedOptions = {}
    for (const option in defaultParams) {
      mergedOptions[option] = defaultParams[option]
      if (typeof mergeParams[option] !== 'undefined') {
        mergedOptions[option] = mergeParams[option]
      }
    }
    return mergedOptions
  }
  
  function isJSON (json) {
    try {
      if (json instanceof Object && JSON.parse(JSON.stringify(json))) {
        return true
      }
      return false
    } catch (err) {
      return false
    }
  }
  
  var _$src_8 = {};
  (function (window) {
    'use strict'
  
    let options = {
      searchInput: null,
      resultsContainer: null,
      json: [],
      success: Function.prototype,
      searchFinished: Function.prototype,
      searchResultTemplate: '<li><a href="{url}" title="{desc}">{title}</a></li>',
      templateMiddleware: Function.prototype,
      sortMiddleware: function () {
        return 0
      },
      noResultsText: '',
      resultsText: '',
      limit: 10,
      fuzzy: false,
      debounceTime: 500,
      exclude: [],
      startDate: null,
      endDate:null,
    }
  
    let debounceTimerHandle
    const debounce = function (func, delayMillis) {
      if (delayMillis) {
        clearTimeout(debounceTimerHandle)
        debounceTimerHandle = setTimeout(func, delayMillis)
      } else {
        func.call()
      }
    }
  
    const requiredOptions = ['startDate', 'resultsContainer', 'json']
  
    const optionsValidator = _$OptionsValidator_3({
      required: requiredOptions
    })
    /* removed: const _$utils_9 = require('./utils') */;
  
    window.DateFilter = function (_options) {
      const errors = optionsValidator.validate(_options)
      if (errors.length > 0) {
        throwError('You must specify the following required options: ' + requiredOptions)
      }
  
      options = _$utils_9.merge(options, _options)
  
      _$Templater_7.setOptions({
        template: options.searchResultTemplate,
        middleware: options.templateMiddleware
      })
  
      _$Repository_4.setOptions({
        fuzzy: options.fuzzy,
        limit: options.limit,
        sort: options.sortMiddleware,
        exclude: options.exclude
      })
  
      if (_$utils_9.isJSON(options.json)) {
        initWithJSON(options.json)
      } else {
        initWithURL(options.json)
      }

      debounce(function () { search(options.startDate, options.endDate) }, options.debounceTime)
  
      const rv = {
        search: search
      }
  
      typeof options.success === 'function' && options.success.call(rv)
      return rv
    }
  
    function initWithJSON (json) {
      _$Repository_4.put(json)
    }
  
    function initWithURL (url) {
      _$JSONLoader_2.load(url, function (err, json) {
        if (err) {
          throwError('failed to get JSON (' + url + ')')
        }
        initWithJSON(json)
      })
    }
  
    function emptyResultsContainer () {
      options.resultsContainer.innerHTML = ''
    }
  
    function appendToResultsContainer (text) {
      options.resultsContainer.innerHTML += text
    }
  
    function search (startDate, endDate) {
      if(startDate) startDate = new Date(startDate);
      if(endDate) endDate = new Date(endDate);
      console.log([startDate, endDate])
      emptyResultsContainer()
      render(_$Repository_4.search(startDate, endDate))
    }

    window.search = search;
  
    function render (results) {
      const len = results.length
      typeof options.searchFinished === 'function' && options.searchFinished(len)
      if (len === 0) {
        return appendToResultsContainer(options.noResultsText)
      } 
      appendToResultsContainer(options.resultsText.replace("{#}", len))
      for (let i = 0; i < len; i++) {
        appendToResultsContainer(_$Templater_7.compile(results[i]))
      }
    }
  
    function throwError (message) {
      throw new Error('DateFilter --- ' + message)
    }
  })(window)
  
  }());