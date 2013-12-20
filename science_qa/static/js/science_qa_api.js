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
      limit: 0,
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
      contactQFound_da: 'Måske kan du finde svaret på dit spørgsmål her',
      contactQFound_en: 'You may be able to find the answer to your question here',
      deleteAttachment_da: 'Slet vedhæftede fil',
      deleteAttachment_en: 'Delete attachment',
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
      sessionUUID: UUID(),
      backend: 'https://qa.moscar.net/'
    };

    // settings
    var settings = $.extend( {}, defaults, options );

    // Global attachments list, used for keeping track of attachments in the
    // contact form
    var attachment_list = [];

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
        var locale = $(settings.locale_id).html().trim();
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
     * format: logondata = acc=0&lgn=bcd123
     */
    function getKUUsername() {
      var data = readCookie('logondata');

      if (data) {
        var username = data.match(settings.username_re);
        settings.username = username[0];
      }
    }

    /**
     * Parse page URL if degree and categories haven't been defined
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
      if (isIE() && isIE() < 9) {
        $('#js-qa-search').on('keyup', debounce(search, 300));
      } else {
        $('#js-qa-search').on('input', debounce(search, 300));
      }
    }

    /**
     * Search for QA's
     */
    function search( e ) {
      // do stuff
      var search = $(this).val();

      if (search.length > 2) {
        searchAPI($(this).val());
      } else if( search.length == 0 ) {
        $('#js-qa-results-search .js-qa-qa').remove();
      }
    }

    /**
     * Sets up contact form UI
     */
    function setupContact() {
      if (!$(self).is('form')) {
        var superWrapper = $('<div class="js-qa" />');
        var wrapper = $('<div class="js-qa-contact-form"></div>');
        if (settings.locale == 'en') {
          var titlePlaceHolder = settings.contactTitlePlaceHolder_en;
          var bodyPlaceHolder = settings.contactBodyPlaceHolder_en;
          var submitText = settings.contactSubmitText_en;
          var emailPlaceHolder = settings.emailPlaceHolder_en;
          var qFound = settings.contactQFound_en;
          var delete_attachment = settings.deleteAttachment_en;
        } else {
          var titlePlaceHolder = settings.contactTitlePlaceHolder_da;
          var bodyPlaceHolder = settings.contactBodyPlaceHolder_da;
          var submitText = settings.contactSubmitText_da;
          var emailPlaceHolder = settings.emailPlaceHolder_da;
          var qFound = settings.contactQFound_da;
          var delete_attachment = settings.deleteAttachment_da;
        }

        var header = $('<div class="js-qa-header">Contact</div>');

        var form = $('<form id="js-qa-contact-form"></form>');
        var email = $('<div><input id="js-qa-email" name="qa_email"'
                    + ' type="text" placeholder="'
                    + emailPlaceHolder + '" disabled="disabled" /></div>');
        var subject = $('<div><input type="text" id="js-qa-contact-subject"'
                      + ' name="qa_subject", placeholder="' + titlePlaceHolder
                      + '" /></div>');
        var attachments = $('<input id="js-qa-attachments" type="file"'
                          + ' name="qa_files" multiple>');
        var files = $('<div class="js-qa-files"></div>');
        var results = $('<div class="js-qa-results-wrap">'
                      + '<div class="js-qa-results-title">' + qFound + '</div>'
                      + '<ul id="js-qa-results-contact" class="js-qa-results">'
                      + '</ul></div>');
        var body = $('<div><textarea id="js-qa-contact-message"'
                   + ' name="qa_message" placeholder="'
                   + bodyPlaceHolder + '" rows="7"></textarea></div>');
        var submit = $('<button id="js-qa-contact-submit" type="submit">'
                     + submitText + '</button>');

        // append to form
        form.append(email);
        form.append(subject);
        form.append(attachments);
        form.append(files);
        form.append(results);
        form.append(body);
        form.append(submit);

        // append form to wrapper
        wrapper.append(header);
        wrapper.append(form);
        superWrapper.append(wrapper);

        // append to page
        $(self).append(superWrapper);
      }

      // find user name and show alumni-mail for current user
      findUsername(showUserMail, showUserMail);

      // setup binds for contact form
      if (isIE() && isIE() < 9) {
        $('#js-qa-contact-subject').on('keyup', debounce(contactSearch, 300));
        $('#js-qa-contact-message').on('keyup', debounce(contactSearch, 300));
      } else {
        $('#js-qa-contact-subject').on('input', debounce(contactSearch, 300));
        $('#js-qa-contact-message').on('input', debounce(contactSearch, 300));
      }

      // setup fileupload handler for attachments
      //
      // This assumes jquery.ui.widget.js, jquery.iframe-transport.js and
      // jquery.fileupload.js has been loaded before this script.
      $('#js-qa-attachments').fileupload({
        dataType: 'json',
        url: settings.backend + 'api/attachments/' + settings.api_key + '/',
        add: function (e, data) {
          $.each(data.files, function (i, file) {
            var attached_file = $('<div class="js-qa-file"><span>' + file.name
              + '</span><a href="#" class="js-qa-delete-file" title="'
              + delete_attachment + '">x</a></div>');
            attached_file.data('filename', file.name);
            $('.js-qa-files').append(attached_file);
          })
          data.context = $('.js-qa-files');
          data.submit();
        },
        done: function (e, data) {
          if (data.result) {
            $.each(data.result.files, function (index, file) {
              // add file to global attachments list
              // addAttachment(file);
              console.log("file", file);
            });
          } else {
            console.log("attachement", attachment_list);
          }
        }
      });

      // add sessionUUID to formdata on fileuploadsubmit
      // the uuid is used to identify the clients files on the server
      $('#js-qa-attachments').bind('fileuploadsubmit', function (e, data) {
        // pass uuid as formdata
        data.formData = { uuid: settings.sessionUUID };
        if (!data.formData.uuid) {
          console.log('failed');
          return false;
        }
        // if valid add filename(s) to attachment list
        $.each(data.files, function (i, file) {
          addAttachment(file.name);
        });
      });

      // bind click to delete attachment
      // TODO add confirmBox?
      $(self).on('click', '.js-qa-file .js-qa-delete-file', function (e) {
        var name = $(this).parent().data('filename');
        deleteAttachmentAPI(name);
        return false;
      });


      // submit mailform
      $('#js-qa-contact-form').on('submit', function (e) {
        e.preventDefault();

        var formData = $(this).serialize();
        var fields = $(this).serializeArray();

        var errors = {};

        clearErrors($(this));

        $.each(fields, function (i, elem) {
          switch (elem.name) {
            case "qa_email":
              // Check if email is valid
              if (!validateEmail(elem.value)) {
                errors[elem.name] = "invalid email";
              }
              break;
            case "qa_subject":
            case "qa_message":
              // TODO fix message
              if (elem.value === "") {
                errors[elem.name] = "Empty";
              }
              break;
          }
        });

        if (!addErrors($(this), errors)) {
          var extra_formData = { uuid: settings.sessionUUID };

          $.each(attachment_list, function (i, file) {
            extra_formData['files_' + i] = file;
          });

          if (settings.degree) {
            extra_formData['degree'] = settings.degree;
          }

          if (settings.categories.length > 0) {
            extra_formData['categories'] = settings.categories.join('-');
          }

          if (settings.locale) {
            extra_formData['locale'] = settings.locale;
          }

          if (settings.username) {
            extra_formData['ku_user'] = settings.username;
          }

          formData += '&' + $.param(extra_formData);

          // make post to backend
          sendEmailAPI(formData);
        }
      });
    }

    /**
     * Add errros to form
     */
    function addErrors( form, errors ) {
      var error = false;

      for (key in errors) {
        var name = key;
        var value = errors[key];

        var field = form
          .find('textarea[name="' + name + '"], input[name="' + name + '"]');

        field.parent()
          .append('<span class="js-qa-fielderror">' + value + '</span>');

        field.addClass('js-qa-error');

        error = true;
      }

      return error;
    }

    /**
     * clear errors from form
     */
    function clearErrors( form ) {
      form.find('.js-qa-error').each(function () {
        $(this).removeClass('js-qa-error');
        if ($(this).next().hasClass('js-qa-fielderror')) {
          $(this).next().remove();
        }
      });
    }

    /**
     * Add attachment to attachment list
     */
    function addAttachment( filename ) {
      for (var i = 0; i < attachment_list.length; i++) {
        if (attachment_list[i] === filename) {
          return;
        }
      }
      attachment_list.push(filename);
    }

    /**
     * Remove attachment from attachment list
     *
     * @param name, filename of the attachment to remove.
     */
    function removeAttachment( name ) {
      $.each(attachment_list, function (i, filename) {
        if (filename === name) {
          attachment_list.splice(i, 1);
        }
      });
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
          url: link
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
     * Parse sharepoint URI and replace utf-8 chars with ASCII chars
     */
    function parseURI(uri) {
      var new_uri = uri;

      var replace = [
        { orig: /\\u002f/g, rep: "/" },
        { orig: /\\u0026/g, rep: "&" },
        { orig: /\\u00252d/g, rep: "-" },
        { orig: /\\u00257d/g, rep: "%7d" },
        { orig: /\\u00257b/g, rep: "%7b" }
      ];

      for (var i = 0; i < replace.length; i++) {
        new_uri = new_uri.replace(replace[i].orig, replace[i].rep);
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
     * Setup UI depending on settings.type
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
        // TODO fix hide when hiding whole answer div

        return false;
      });

      // disable default link behaviuour
      $(self).on('click', '.js-qa-question', function (e) {
        e.preventDefault();
        if ($(this).attr('href') !== "#") {
          if (!(isIE() && isIE() < 10)) {
            history.pushState(null, null, $(this).attr('href'));
          }
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

      if (settings.limit != 0 && /^\d+$/.test(settings.limit)) {
        uri['limit'] = settings.limit;
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
        dataType: 'jsonp'
      }).done(function (response) {
        if (typeof callback !== "undefined") {
          if (typeof type !== "udefined") {
            callback(response, type);
          } else {
            callback(response);
          }
        }
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
     * search contact
     */
    function contactSearchAPI( search ) {
      var params = buildSearchRequestURI(search);

      console.log("contact search params", params);

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

      makeAPIRequest('rate', params);
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
     * delete attachment
     */
    function deleteAttachmentAPI(name) {
      var params = { name: name, uuid: settings.sessionUUID };

      makeAPIRequest('delete_attachment', params, APIResponse);
    }

    /**
     * Send mail
     */
    function sendEmailAPI(data) {
      makeAPIRequest('send_email', data);
    }

    /**
     * Handle API Response
     *
     * @param response, assume response to be javascript obj
     */
    function APIResponse( response, type ) {

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
        case 'delete_attachment':
          removeAttachmentElem(response);
          break;
        default:
          console.log("APIResponse", response);
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
     * make category links
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
            // use inArray since indexOf isn't supported in IE8
            var index = $.inArray(link[x], cats);
            cats.splice(index, 1);
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

    /**
     * remove attachment
     */
    function removeAttachmentElem( response ) {
      if (response.success) {
        // iterate through each file-div and remove the one that was deleted
        $('.js-qa-files').children('.js-qa-file').each(function() {
          var filename = $(this).data('filename');
          if (filename === response.name) {
            $(this).remove();
            // remove from attachment_list
            removeAttachment(filename);
          }
        });
      }
    }

    /* Helper functions */

    /**
     * check if clientbrowser is IE and if so, what version of IE
     */
    function isIE() {
      var nav = navigator.userAgent.toLowerCase();
      var ie_version = false;
      if (nav.indexOf('msie') != -1) {
        ie_version = parseInt(nav.split('msie')[1]);
      }
      return ie_version;
    }

    /**
     * Create UUID
     */
    function UUID() {
        // http://www.ietf.org/rfc/rfc4122.txt
        var s = new Array(36);
        var hexDigits = "0123456789abcdef";
        for (var i = 0; i < 36; i++) {
            s[i] = hexDigits.substr(Math.floor(Math.random() * 0x10), 1);
        }
        s[14] = "4";  // bits 12-15 of the time_hi_and_version field to 0010
        // bits 6-7 of the clock_seq_hi_and_reserved to 01
        s[19] = hexDigits.substr((s[19] & 0x3) | 0x8, 1);
        s[8] = s[13] = s[18] = s[23] = "-";

        var uuid = s.join("");
        return uuid;
    }

    /**
     * Read cookie value
     *
     * Source: http://stackoverflow.com/questions/5639346/
     *                shortest-function-for-reading-a-cookie-in-javascript
     */
    function readCookie( name ) {
        name += '=';
        for (var ca = document.cookie.split(/;\s*/), i = ca.length - 1; i >= 0; i--)
            if (!ca[i].indexOf(name))
                return ca[i].replace(name, '');
    }

    /**
     * Validate email
     */
    function validateEmail(email) {
        var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(email);
    }

    /**
     * Returns a function, that, as long as it continues to be invoked, will
     * not be triggered. The function will be called after it stops being
     * called for N milliseconds. If `immediate` is passed, trigger the
     * function on the leading edge, instead of the trailing.
     *
     * Source: http://stackoverflow.com/questions/12538344/
     * asynchronous-keyup-events-how-to-short-circuit-sequential
     * -keyup-events-for-speed
     */
    function debounce( func, wait, immediate ) {
        var timeout;
        return function() {
            var context = this, arps = arguments;
            var later = function() {
                timeout = null;
                if (!immediate) {
                    func.apply(context, arps);
                }
            };
            if (immediate && !timeout) {
                func.apply(context, arps);
            }

            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
  };
})( jQuery );
