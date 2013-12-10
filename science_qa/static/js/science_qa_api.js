/**
 * QAScience exception
 */
function QAScienceException( message ) {
  this.message = message;
  this.name = "QAScienceException";
}

(function ( $ ) {
  // qaSearch definition
  $.fn.qaScience = function( options ) {

    var self = this;

    // defaults
    var defaults = {
      // API key for intranet.ku.dk
      api_key: 'addcdcfcd5164664a083fa9e4d137c0f',
      type: 'search', // can be either 'search' (default), 'list', 'contact' or 'single'
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
      contactQFound_da: 'Maaske kan du finde svaret paa dit spørgsmaal her',
      contactQFound_en: 'You may be able to find the answer to your question here',
      listTitle_da: 'Ofte stillede spørgsmål',
      listTitle_en: 'Frequently asked questions',
      ratingText_da: 'Hjalp dette svar?',
      ratingText_en: 'Was this answer helpful?',
      locale_id: '#ctl00_PlaceHolderGlobalNavigation_LanguageLink',
      user_menu_id: '#zz2_ID_PersonalInformation',
      user_sp_link_re: /\\[\\a-z\d_.=?]+/i,
      user_id_re: /^var _spUserId=\d+;$/,
      get_user_id_re: /\d+/g,
      username_re: /[b-df-hj-np-tv-z]{3}\d{3}/i,
      alumni_mail: '@alumni.ku.dk',
      username: null,
      degree_re: /^[a-z_]+(ba|ma)$/i,
      category_re: /^[a-z]+$/,
      backend: 'https://qa.moscar.net/',
    };

    // settings
    var settings = $.extend( {}, defaults, options );

    // check for API Key
    checkForAPIKey();

    // set locale
    setLocale();

    // parse page url
    parsePageURL();

    // get KU username from cookie
    getKUUsername();

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
        throw new QAScienceException("API Key not set");
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
     * try to get KU-username from cookie
     *
     * format logondata = acc=0&lgn=bcd123
     */
    function getKUUsername() {
      var data = readCookie('logondata');

      if (data) {
        var username = data.match(settings.username_re);
        settings.username = username[0];
      }
    }

    /**
     * Read cookie value
     */
    function readCookie(name) {
      var nameEQ = name + "=";
      var ca = document.cookie.split(';');
      for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) == 0)
          return c.substring(nameEQ.length, c.length);
      }
      return null;
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
          if (settings.degree_re.test(path[1])) {
            settings.degree = path[1];
          }
        }
        // only parse categories from url, if they has not been set
        // programmatically.
        if (settings.categories.length == 0) {
          for (var i = 2; i < path.length; i++) {
            if (settings.category_re.test(path[i])) {
              settings.categories.push(path[i]);
            }
          }
        }
      } else {
        throw new QAScienceException("Not on kunet.dk");
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
      var results = $('<div id="js-qa-results-search" class="js-qa-results">'
                    + '</div>');

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
        var search = $(this).val();

        if (search.length > 2) {
          searchAPI($(this).val());
        } else if( search.length == 0 ) {
          $('#js-qa-results-search .js-qa-qa').remove();
          // $('#js-qa-results-search').parent().removeClass('js-qa-results-found');
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
        var qFound = settings.contactQFound_en;
      } else {
        var titlePlaceHolder = settings.contactTitlePlaceHolder_da;
        var bodyPlaceHolder = settings.contactBodyPlaceHolder_da;
        var submitText = settings.contactSubmitText_da;
        var emailPlaceHolder = settings.emailPlaceHolder_da;
        var qFound = settings.contactQFound_da;
      }

      var header = $('<div class="js-qa-header">Contact</div>');

      var form = $('<form id="js-qa-contact-form"></form>');
      var email = $('<div><input id="js-qa-email" type="text" placeholder="'
                    + emailPlaceHolder + '" disabled="disabled" /></div>');
      var subject = $('<div><input type="text" id="js-qa-contact-subject"'
                    + ' placeholder="' + titlePlaceHolder + '" /></div>');
      var results = $('<div class="js-qa-results-wrap">'
                    + '<div class="js-qa-results-title">' + qFound + '</div>'
                    + '<ul id="js-qa-results-contact" class="js-qa-results">'
                    + '</ul></div>');
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

      // setup binds for contact form
      $('#js-qa-contact-subject').on('input', contactSearch);

      $('#js-qa-contact-message').on('input', contactSearch);
    }

    /**
     * contact search
     *
     * make search based on contact subject and contact message
     */
    function contactSearch() {
      var subject = $('#js-qa-contact-subject').val();
      var message = $('#js-qa-contact-message').val();

      if (subject.length > 2 || message.length > 2) {
        contactSearchAPI(subject + ' ' + message);
      } else if( subject.length == 0 && message.length == 0) {
          $('#js-qa-results-contact .js-qa-qa').remove();
          $('#js-qa-results-contact').parent().removeClass('js-qa-results-found');
      }
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
      var results = $('<ul id="js-qa-results-list" class="js-qa-results">'
                    + '</ul>');

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
     * Setup single UI
     *
     * Shows a single question based on URI
     */
    function setupSingle() {
      var q_id = 'js-qa-question';
      var superWrapper = $('<div class="js-qa" />');
      var results = $('<div class="js-qa-single" id="' + q_id +'"></div>');

      // combine
      superWrapper.append(results);

      // append to page
      $(self).append(superWrapper);

      // parse URI and show question if id present
      var query = location.search.substring(1);
      var vars = query.split('&');
      var id = null;
      for (var i = 0; i < vars.length; i++) {
        var pair = vars[i].split('=');
        if (pair[0] === 'qa-id') {
          id = pair[1];
          break;
        }
      }

      singleAPI(id);
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

      if (settings.locale == 'en') {
        var rating_text = settings.ratingText_en;
        var rating_yes = 'Yes';
        var rating_no = 'No';
        var rating_thanks = 'Thank you';
      } else {
        var rating_text = settings.ratingText_da;
        var rating_yes = 'Ja';
        var rating_no = 'Nej';
        var rating_thanks = 'Tak';
      }

      var tpl = '<li class="js-qa-qa"><a href="#" class="js-qa-question">'
              + '</a><div class="js-qa-answer"></div>'
              + '<div class="js-qa-categories"></div>'
              + '<div class="js-qa-rating">' + rating_text
              + '<span class="js-qa-rate"><a href="1">' + rating_yes
              + '</a> / <a href="-1">' + rating_no + '</a></span></div></li>';

      // disable rating link behaviuor
      $(self).on('click', '.js-qa-rate > a', function (e) {
        e.preventDefault();
        var href = $(this).attr('href');
        var parent = $(this).parent().parent().parent();
        var id = parent.attr('id');

        var rating = parseInt(href);

        // rate question
        rateAPI(rating, id);

        var rate_elem = $(this).parent().parent();
        rate_elem.hide();
        rate_elem.html(rating_thanks);
        rate_elem.fadeIn();

        return false;
      });

      // disable default link behaviuour
      $(self).on('click', '.js-qa-question', function (e) {
        e.preventDefault();
        if ($(this).attr('href') !== "#") {
          history.pushState(null, null, $(this).attr('href'));
        }

        // toggle show question on click
        var qa = $(this).parent();
        if (qa.hasClass('noanswer')) {
          qa.removeClass('noanswer');
        } else {
          qa.addClass('noanswer');
        }

        return false;
      });

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
      } else if (settings.type === 'single') {
        // setup single UI
        setupSingle();
      } else {
        throw new QAScienceException("Invalid type");
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

      if (settings.username) {
        uri['ku_user'] = settings.username;
      }

      return uri;
    }

    /**
     * make API Request
     */
    function makeAPIRequest( api_call, data, callback, type) {
      var url = settings.backend + 'api/' + api_call + '/' +
                settings.api_key + '/';

      $.ajax({
        url: url,
        data: data,
        dataType: 'json',
      }).done(function (response) {
        if (typeof type !== "udefined") {
          callback(response, type);
        } else {
          callback(response);
        }
      }).fail(function (data, textStatus, errorThrown) {
        console.log("FAIL");
        console.log(data);
        console.log(textStatus);
        console.log(errorThrown);
      });
    }

    /**
     * make API Post Request
     *
     * Callback is optional
     */
    function makeAPIPostRequest( api_call, data, callback ) {
      var url = settings.backend + 'api/' + api_call + '/' +
                settings.api_key + '/';

      $.ajax({
        url: url,
        type: 'POST',
        data: data,
        dataType: 'json',
      }).done(function (response) {
        if (typeof callback !== "undefined") {
          callback(response);
        }
      }).fail( function (data) {
        console.log(data);
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
     * search contact
     */
    function contactSearchAPI( search ) {
      var params = buildSearchRequestURI(search);

      console.log(params);

      makeAPIRequest('search', params, APIResponse, 'contact')
    }

    /**
     * list
     */
    function listAPI() {
      var params = buildSearchRequestURI(null);

      makeAPIRequest('list', params, APIResponse);
    }

    /**
     * rate
     */
    function rateAPI(value, id) {
      var params = null;

      if (settings.username) {
        params = { rating: value,
                   ku_user: settings.username,
                   id: id }
      }

      makeAPIPostRequest('rate', params);
    }

    /**
     * single
     */
    function singleAPI(id) {
      if (typeof id !== "undefined") {
        var params = { id: id, locale: settings.locale };

        makeAPIRequest('single', params, APIResponse);
      }
    }

    /**
     * Handle API Response
     *
     * @param response, assume response to be javascript obj
     */
    function APIResponse( response, type ) {
      console.log(response);

      switch (response['call']) {
        case 'list':
          populateResult(response, '#js-qa-results-list');
          break;
        case 'search':
          if (type === 'contact') {
            populateResult(response, '#js-qa-results-contact', true);
          } else {
            populateResult(response, '#js-qa-results-search');
          }
          break;
        case 'single':
          addSingleQuestion(response, '#js-qa-question');
          break;
        default:
          console.log(response);
      }
    }

    /**
     * populate results div
     */
    function populateResult( response, result, noanswer) {
      $(result + ' .js-qa-qa').remove();

      var res = $(result);
      res.parent().removeClass('js-qa-results-found');

      if ('error' in response) {
        console.log(response['error']);
      } else {
        if (response['results'].length > 0) {
          res.parent().addClass('js-qa-results-found');
          for (var i = 0; i < response['results'].length; i++) {
            renderQuestion(response['results'][i], response, res);
          }
        }
      }
    }

    /**
     * Render a single question
     */
    function renderQuestion( question, response, out ) {
      var res_tpl = $(settings.result_tpl);

      var url = '?qa-id=' + question['id'];

      res_tpl.attr('id', question['id']);
      res_tpl.find('.js-qa-question').append(question['question']);
      res_tpl.find('.js-qa-question').attr('href', url);
      res_tpl.find('.js-qa-answer').append(question['answer']);
      // if (noanswer) {
      res_tpl.addClass('noanswer');
      // }

      // create links to category
      for (var i = 0; i < question['categories'].length; i++) {
        categoryLink(question['categories'][i], res_tpl,
            question['categories'][i].name);
      }

      // check for rating
      if ('ratings' in response && $.inArray(question['id'],
            response['ratings']) > -1) {
        res_tpl.addClass('hasvoted');
      }

      out.append(res_tpl);
    }

    /**
     * make categor links
     * TODO sort by deeplink
     */
    function categoryLink( category, out, name ) {
      var links = walkCategories(category, []);

      for (var j = 0; j < links.length; j++) {
        var link = links[j];
        if (link.length > 1) {
          link.reverse();
        }

        var cats = settings.categories.slice();
        for (var x = 0; x < link.length; x++) {
          if ($.inArray(link[x], settings.categories) > -1) {
            cats.splice(cats.indexOf(link[x], 1));
          }
        }

        if (cats.length > 0 && settings.degree != null) {
          var href = '/' + settings.degree + '/' + link.join('/');

          // create anchor
          var a = $('<a href="' + href + '">' + name + '</a>');

          out.find('.js-qa-categories').append(a);
        }
      }
    }

    /**
     * walk through
     */
    function walkCategories( category, link ) {
      links = [];
      if (category) {
        link.push(category.id);
        if (category.parents.length > 0) {
          for (var i = 0; i < category.parents.length; i++) {
            links.push(walkCategories(category.parents[i], link));
          }
        } else {
          links.push(link);
        }
      }

      return links;
    }

    /**
     * add single question
     */
    function addSingleQuestion( response, q_id ) {
      var res = $(q_id);

      if ('error' in response) {
        console.log(response['error']);
      } else if (response['question'] != null) {
        var res_tpl = $(settings.result_tpl);
        res_tpl.attr('id', response['question']['id']);
        res_tpl.find('.js-qa-question')
               .append(response['question']['question']);
        res_tpl.find('.js-qa-answer')
               .append(response['question']['answer']);

        res.append(res_tpl);
      }
    }
  };
})( jQuery );
