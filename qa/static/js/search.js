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


var Search = {
  url_query: null,

  init: function() {
    // Store init query, so we can get it back if filter is canceled
    Search.url_query = location.search;

    // setup search/filter input
    $('#search').on('input', Search.doSearch);
  },

  /**
   * Perform a search and return and render data
   */
  doSearch: function () {
    var val = $('#search').val();

    if (val.length > 2) {
      history.pushState(null, 'searching', location.pathname + '?q=' + val);
      $.ajax({
        url: window.location.pathname + "?q=" + val,
        dataType: 'json',
        // headers: { //'X-CSRFToken':getCookie('csrftoken'),
        //           'sessionid':getCookie('sessionid') },
      }).done(function (data) {

        var questions = JSON.parse(data.questions);
        if (questions.length) {
          $('#ajax-questions').html('');

          $.each(questions, function (i, question) {
            Search.questionsResponse(question, data.edit, data.delete);
          });
        }
      });
    } else if (val.length == 0) {
      $('.static').removeClass('hide');
      $('#ajax-questions').html('');
      if (!isIE() || (isIE() && isIE() > 9)) {
        history.pushState(null, 'searching', location.pathname + Search.url_query);
      }
    }
  },

  questionsResponse: function ( question, edit, delete_ ) {

    console.log(question, edit, delete_);

    // create tr
    var tr = $('<tr/>');

    var tds = [];

    // create question td
    var q_td = $('<td/>');
    if (question.fields.question_da && question.fields.answer_da) {
      var qa_da = $('<div class="question-answer noanswer">'
                  + '<div class="question"><span class="flag dk"></span><span>'
                  + question.fields.question_da + '</span></div>' +
                    '<div class="answer">' + question.fields.answer_da +
                    '</div></div>');
      q_td.append(qa_da);
    }

    if (question.fields.question_en && question.fields.answer_en) {
      var qa_en = $('<div class="question-answer noanswer">'
                  + '<div class="question"><span class="flag uk"></span>'
                  + question.fields.question_en + '</span></div>' +
                    '<div class="answer">' + question.fields.answer_en +
                    '</div></div>');
      q_td.append(qa_en);
    }

    tds.push(q_td);

    // TODO fix rating on searches
    var rating_td = $('<td/>').html(question.fields.rating_count);
    tds.push(rating_td);

    var date_td = $('<td/>').html(question.fields.date_added);
    tds.push(date_td);

    var last_td = $('<td/>').html(question.fields.date_last_edit);
    tds.push(last_td);

    var action_td = $('<td/>');
    if (edit) {
      var edit = $('<a href="/qa/questions/' + question.pk + '"'
          + ' class="btn btn-success btn-xs" role="button">'
          + gettext('Edit') + '</a>');

      action_td.append(edit);
    }

    if (delete_) {
      var _delete = $('<a href="/qa/questions/' + question.pk + '/delete"'
          + ' class="btn btn-danger btn-xs" role="button">'
          + gettext('Delete') + '</a>');

      action_td.append(_delete);
    }

    tds.push(action_td);

    for (var i = 0; i < tds.length; i++) {
      tr.append(tds[i]);
    }

    $('#ajax-questions').append(tr);
    $('.static').addClass('hide');
  }
};
