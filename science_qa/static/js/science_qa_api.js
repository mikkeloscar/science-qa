/**
 * QASearch exception
 */
function QASearchException( message ) {
  this.message = message;
  this.name = "QASearchException";
}

(function ( $ ) {
  // qaSearch definition
  $.fn.qaSearch = function( options ) {

    var self = this;

    // defaults
    var defaults = {
      // API key for intranet.ku.dk
      api_key: 'addcdcfcd5164664a083fa9e4d137c0f',
      type: 'search', // can be either 'search' (default), 'list' or 'contact'
      degree: null,
      categories: [],
      locale: null,
      searchPlaceHolder_da: 'Søg..',
      searchPlaceHolder_en: 'Search..',
      emailPlaceHolder_da: 'Din email',
      emailPlaceHolder_en: 'Your email',
      contactTitlePlaceHolder_da: 'Emne',
      contactTitlePlaceHolder_en: 'Subject',
      contactBodyPlaceHolder_da: 'Besked',
      contactBodyPlaceHolder_en: 'Message',
      contactSubmitText_da: 'Send',
      contactSubmitText_en: 'Send',
      listTitle_da: 'Ofte stillede spørgsmål',
      listTitle_en: 'Frequently asked questions',
      locale_id: '#ctl00_PlaceHolderGlobalNavigation_LanguageLink',
      user_menu_id: '#zz2_ID_PersonalInformation',
      user_sp_link_re: /\\[\\a-z\d_.=?]+/i,
      user_id_re: /^var _spUserId=\d+;$/,
      get_user_id_re: /\d+/g,
      username_re: /[b-df-hj-np-tv-z]{3}\d{3}/i,
      alumni_mail: '@alumni.ku.dk',
      degree_re: /^[a-z_]+(ba|ma)$/i,
      category_re: /^[a-z]+$/,
      backend: 'https://qa.moscar.net/',
      result: null,
    };

    // settings
    var settings = $.extend( {}, defaults, options );

    // check for API Key
    checkForAPIKey();

    // set locale
    setLocale();

    // parse page url
    parsePageURL();

    // setup UI
    setupUI();

    /**
     * Check if an API Key is set
     *
     * It dosn't check if the key is valid, the server will tell us when we do
     * a request.
     *
     * @throws "API Key not set" if api_key is null
     */
    function checkForAPIKey() {
      if (!settings.api_key) {
        throw new QASearchException("API Key not set");
      }
    }

    /**
     * Sets locale based on the value of the locale link on KUnet.
     */
    function setLocale() {
      if (settings.locale_id && !settings.locale) {
        var locale = $(settings.locale_id).html();
        if (locale === "Danish") {
          settings.locale = 'en';
        } else {
          settings.locale = 'da';
        }
      }
    }

    /**
     * Parse page URL in degree and categories haven't been defined
     * programmatically
     *
     * throws "Not on kunet.dk" if the plugin has been initialized outside
     * kunet.dk
     */
    function parsePageURL() {
      if (settings.degree && settings.categories.length > 0) return

      if (location.host === "intranet.ku.dk") {
        // split path and pull out degree and categories
        var path = location.pathname.split('/');
        // only parse degree from url, if it has not been set programmatically.
        if (!settings.degree) {
          if (settings.degree_re.test(path[0])) {
            settings.degree = path[0];
          }
        }
        // only parse categories from url, if they has not been set
        // programmatically.
        if (settings.categories.length == 0) {
          for (var i = 1; i < path.length; i++) {
            if (settings.category_re.test(path[i])) {
              settings.categories.push(path[i]);
            }
          }
        }
      } else {
        throw new QASearchException("Not on kunet.dk");
      }
    }

    /**
     * Sets up search UI
     */
    function setupSearch() {
      var superWrapper = $('<div class="js-qa" />');
      var wrapper = $('<div class="js-qa-search"></div>');
      if (settings.locale == 'en') {
        var placeHolder = settings.searchPlaceHolder_en;
      } else {
        var placeHolder = settings.searchPlaceHolder_da;
      }
      var header = $('<div class="js-qa-header">Søg</div>');
      var input = $('<input type="text" id="js-qa-search" placeholder="'
                    + placeHolder + '" />');
      var results = $('<div class="js-qa-results"></div>');

      var result = $('<div class="js-qa-result">' +
                      '<div class="js-qa-result-title"></div>' +
                      '<div class="js-qa-result-body"></div></div>');

      settings.result = result;

      // combine
      wrapper.append(header);
      wrapper.append(input);
      wrapper.append(results);
      superWrapper.append(wrapper);

      // append to page
      $(self).append(superWrapper);

      // setup binds for search form
      $('#js-qa-search').on('input', function(e) {
        // do stuff
        console.log($(this).val());
        var search = $(this).val();

        if (search.length > 2) {
          searchAPI($(this).val());
        }
      });
    }

    /**
     * Sets up contact form UI
     */
    function setupContact() {
      var superWrapper = $('<div class="js-qa" />');
      var wrapper = $('<div class="js-qa-contact-form"></div>');
      if (settings.locale == 'en') {
        var titlePlaceHolder = settings.contactTitlePlaceHolder_en;
        var bodyPlaceHolder = settings.contactBodyPlaceHolder_en;
        var submitText = settings.contactSubmitText_en;
        var emailPlaceHolder = settings.emailPlaceHolder_en;
      } else {
        var titlePlaceHolder = settings.contactTitlePlaceHolder_da;
        var bodyPlaceHolder = settings.contactBodyPlaceHolder_da;
        var submitText = settings.contactSubmitText_da;
        var emailPlaceHolder = settings.emailPlaceHolder_da;
      }

      var header = $('<div class="js-qa-header">Contact</div>');

      var form = $('<form id="js-qa-contact-form"></form>');
      var email = $('<div><input id="js-qa-email" type="text" placeholder="'
                    + emailPlaceHolder + '" disabled="disabled" /></div>');
      var subject = $('<div><input type="text" id="js-qa-contact-subject"'
                    + ' placeholder="' + titlePlaceHolder + '" /></div>');
      var results = $('<div class="js-qa-results"></div>');
      var body = $('<div><textarea id="js-qa-contact-message" placeholder="'
                    + bodyPlaceHolder + '" rows="7"></textarea></div>');
      var submit = $('<button type="submit">' + submitText + '</button>');

      // append to form
      form.append(email);
      form.append(subject);
      form.append(results);
      form.append(body);
      form.append(submit);

      // append form to wrapper
      wrapper.append(header);
      wrapper.append(form);
      superWrapper.append(wrapper);

      // append to page
      $(self).append(superWrapper);

      // find user name and show alumni-mail for current user
      findUsername(showUserMail, showUserMail);

    }

    /**
     * find KU-username
     *
     * this will obviously only work when logged into KUnet
     *
     * @param callback, callback function called on ajax done
     */
    function findUsername(done_callback, fail_callback) {
      // find user menu
      // var menu = $(settings.user_menu_id);
      // var onClick = menu.attr('onMenuClick');
      // parse link

      var userId = getSharepointUserID();
      var userLink = getSharepointUserLink();

      if (userId !== null && userLink !== null) {
        var link = userLink + userId;

        $.ajax({
          url: link,
        }).done(function (data) {
          // parse user page and get KU-username
          var html = data.trim();
          var emails = [];
          $(html).find('a[href^="mailto:"]').each( function() {
            emails.push($(this).html());
          });

          var username = null;

          for (var i = 0; i < emails.length; i++) {
            var kuUsername = emails[i].split('@');
            if(settings.username_re.test(kuUsername[0])) {
              username = kuUsername[0];
              break;
            }
          }
          if (username !== null) {
            // Pass username to the callback
            done_callback(username);
          } else {
            fail_callback();
          }
        }).fail(function () {
          fail_callback();
        });
      } else {
        fail_callback();
      }
    }

    /**
     * Find sharepoint userId on KUnet
     */
    function getSharepointUserID() {
      var userId = null;
      $(document).find('script').filter(function () {
        if (settings.user_id_re.test(this.textContent)) {
          var userID = this.textContent.match(settings.get_user_id_re)[0];
          userId = userID;
          return false;
        }
      });

      return userId;
    }

    function getSharepointUserLink() {
      var link = null;
      var js_link = $(settings.user_menu_id).attr('onmenuclick');

      if (typeof js_link !== "undefined") {
        var result = js_link.match(settings.user_sp_link_re);
        link = result[0];
      }

      if (link !== null) {
        link = parseURI(link);
      }

      return link;
    }

    /**
     * Parse sharepoint URI and replace utf-8 chars with chars
     */
    function parseURI(uri) {
      var new_uri = uri;

      var replace = [
        { orig: /\\u002f/g, new: "/" },
        { orig: /\\u0026/g, new: "&" },
        { orig: /\\u00252d/g, new: "-" },
        { orig: /\\u00257d/g, new: "%7d" },
        { orig: /\\u00257b/g, new: "%7b" }
      ];

      for (var i = 0; i < replace.length; i++) {
        new_uri = new_uri.replace(replace[i].orig, replace[i].new);
      }

      return new_uri;
    }

    /**
     * Setup List UI
     */
    function setupList() {
      var superWrapper = $('<div class="js-qa" />');
      var wrapper = $('<div class="js-qa-list"></div>');
      if (settings.locale == 'en') {
        var title = settings.listTitle_en;
      } else {
        var title = settings.listTitle_da;
      }
      var header = $('<div class="js-qa-header">' + title + '</div>');
      var results = $('<div class="js-qa-results-list"></div>');

      // combine
      wrapper.append(header);
      wrapper.append(results);
      superWrapper.append(wrapper);

      // append to page
      $(self).append(superWrapper);

      // populate results
      listAPI();
    }

    /**
     * Show alumnimail or inputfield
     */
    function showUserMail(username) {
      var email = $('#js-qa-email');
      if (typeof username !== "undefined") {
        email.val(username + settings.alumni_mail);
      }
      email.prop('disabled', false);
    }

    /**
     * Setup either search UI or contactform UI depending on settings.type
     *
     * Valid types are 'search', 'contact' and 'list'
     *
     * throws "Invalid type" on invalid type
     */
    function setupUI() {
      // setup css
      setupCss();

      var tpl = '<div class="js-qa-qa"><div class="js-qa-question">' +
                  '</div><div class="js-qa-answer"></div></div>';

      settings.result_tpl = tpl;

      if (settings.type === 'search') {
        // setup search UI
        setupSearch();
      } else if (settings.type === 'contact') {
        // setup contact UI
        setupContact();
      } else if (settings.type === 'list') {
        // setup list UI
        setupList();
      } else {
        throw new QASearchException("Invalid type");
      }
    }

    /**
     * Load in custom CSS
     */
    function setupCss() {
      var cssId = 'qa-css';
      var css_elem = $('#' + cssId);
      if (css_elem.length == 0) {
        var head = $('head');
        var link = $('<link/>');
        link.attr('id', cssId);
        link.attr('type', 'text/css');
        link.attr('href', settings.backend + 'static/css/qa_science_api.css');
        link.attr('rel', 'stylesheet');
        link.attr('media', 'screen');
        head.append(link);
      }
    }

    /**
     * build a SearchRequestURI object based on search and settings
     */
    function buildSearchRequestURI( search ) {
      // format: /api/search/?q=search+term&degree=degree_ba&category_1=
      var uri = {}
      if (search) {
        uri['q'] = search;
      }

      if (settings.degree) {
        uri['degree'] = settings.degree;
      }

      if (settings.categories.length > 0) {
        uri['categories'] = settings.categories.join('-');
      }

      if (settings.locale) {
        uri['locale'] = settings.locale;
      }

      return uri;
    }

    /**
     * make API Request
     */
    function makeAPIRequest( api_call, data, callback ) {
      var url = settings.backend + 'api/' + api_call + '/' +
                settings.api_key + '/';

      console.log(url);

      $.ajax({
        url: url,
        data: data,
        dataType: 'json',
      }).done(function (response) {
        callback(response);
      }).fail(function (data, textStatus, errorThrown) {
        console.log("FAIL");
        console.log(data);
        console.log(textStatus);
        console.log(errorThrown);
      });
    }

    /**
     * Search
     */
    function searchAPI( search ) {
      var params = buildSearchRequestURI(search);

      makeAPIRequest('search', params, APIResponse);
    }

    /**
     * list
     */
    function listAPI() {
      var params = buildSearchRequestURI(null);

      makeAPIRequest('list', params, APIResponse);
    }

    /**
     * Handle API Response
     *
     * @param response, assume response to be javascript obj
     */
    function APIResponse( response ) {
      console.log(response);

      switch (response['call']) {
        case 'list':
          populateList(response);
          break;
        case 'search':
          populateSearch(reponse);
          break;
        default:
          console.log(reponse);
      }
    }

    function populateList( response ) {
      var res = $('.js-qa-results-list');
      if ('error' in response) {
        console.log(response['error']);
      } else {
        for (var i = 0; i < response['results'].length; i++) {
          var res_tpl = $(settings.result_tpl);
          res_tpl.find('.js-qa-question').append(response['results'][i]['question']);
          res_tpl.find('.js-qa-answer').append(response['results'][i]['answer']);
          res.append(res_tpl);
        }
      }
    }

  };
})( jQuery );
