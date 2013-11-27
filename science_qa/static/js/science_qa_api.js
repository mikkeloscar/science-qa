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
      api_key: null,
      type: 'search', // can be either 'search' (default) or 'contact'
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
      locale_id: '#ctl00_PlaceHolderGlobalNavigation_LanguageLink',
      user_menu_id: '#zz2_ID_PersonalInformation',
      user_sharepoint_link: '/_layouts/userdisp.aspx?Force=True&ID=',
      user_id_re: /^var _spUserId=\{5};$/,
      get_user_id_re: /\d{5}/g,
      username_re: /[b-df-hj-np-tv-z]{3}\d{3}/i,
      degree_re: /^[a-z_]+(ba|ma)$/i,
      category_re: /^[a-z]+$/,
      backend: 'http://',
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

      // combine
      wrapper.append(header);
      wrapper.append(input);
      wrapper.append(results);
      // append to page
      $(self).append(wrapper);

      // setup binds for search form
      $('#js-qa-search').on('input', function(e) {
        // do stuff
        console.log($(this).val());
      });
    }

    /**
     * Sets up contact form UI
     */
    function setupContact() {
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
      var form = $('<form id="js-qa-contact-form"></form>');
      var email = $('<input id="js-qa-email" type="text" placeholder="'
                    + emailPlaceHolder + '" disabled="disabled" />');
      var subject = $('<input type="text" id="js-qa-contact-subject"'
                    + ' placeholder="' + titlePlaceHolder + '" />');
      var results = $('<div class="js-qa-results"></div>');
      var body = $('<textarea id="js-qa-contact-message" placeholder="'
                    + bodyPlaceHolder + '"></textarea>');
      var submit = $('<button type="submit">' + submitText + '</button>');

      // append to form
      form.append(email);
      form.append(subject);
      form.append(results);
      form.append(body);
      form.append(submit);

      // append form to wrapper
      wrapper.append(form);
      // append to page
      $(self).append(wrapper);

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
      if (getSharepointUserID() != null) {
        var link = settings.user_sharepoint_link + getSharepointUserID();

        $.ajax({
          url: link,
        }).done(function (data) {
          // parse user page and get KU-username
          data = data.trim();
          var emails = [];
          $(data).find('a[href^="mailto:"]').each( function() {
            emails.push(this.contentText);
          });

          var username = null;

          for (var i = 0; i < emails.length; i++) {
            var kuUsername = emails[i].split('@');
            if(settings.username_re.test(kuUsername[0])) {
              username = kuUsername;
              break;
            }
          }
          if (username != null) {
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
      $(document).find('script').filter(function () {
        if (settings.user_id_re.test(this.textContent)) {
          var userID = this.textContent.match(settings.get_user_id_re);
          return userID;
        }
      });

      return null;
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
     * Valid types are 'search' and 'contact'
     *
     * throws "Invalid type" on invalid type
     */
    function setupUI() {
      if (settings.type === 'search') {
        // setup search UI
        setupSearch();
      } else if (settings.type === 'contact') {
        // setup contact UI
        setupContact();
      } else {
        throw new QASearchException("Invalid type");
      }
    }

    /**
     * build a SearchRequestURI object based on search and settings
     */
    function buildSearchRequestURI( search ) {
      // format: /api/search/?q=search+term&degree=degree_ba&category_1=
      if (search) {
        var uri = { q: search };

        if (settings.degree) {
          uri['degree'] = settings.degree;
        }

        if (settings.categories.length > 0) {
          // TODO is this possible with GET and jQuery?
          uri['categories'] = settings.categories;
          // for (var i = 0; i < settings.categories.length; i++) {
          //   uri['category_'+i] = settings.categories[i];
          // }
        }

        if (settings.locale) {
          uri['locale'] = settings.locale;
        }

        return uri;
      }

      return null;
    }

    /**
     * make API Request
     */
    function makeAPIRequest(api_call, data, callback) {
      $.ajax({
        url: settings.backend + api_call,
        data: data,
        dataType: 'json',
      }).done(function (response) {
        callback(response);
      });
    }
  };
})( jQuery );
