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
  doSearch: function() {
    var val = $('#search').val();

    if (val.length > 2) {
      history.pushState(null, 'searching', location.pathname + '?q=' + val);
      $.ajax({
        url: window.location.pathname + "?q=" + val,
        dataType: 'json',
        // headers: { //'X-CSRFToken':getCookie('csrftoken'),
        //           'sessionid':getCookie('sessionid') },
      }).done(function (data) {
        console.log(data);
        if (data.length) {
          $('#ajax-response').html('');

          for (var i = 0; i < data.length; i++) {
            Search.questionsResponse(data[i]);
          }
        }
      });
    } else if (val.length == 0) {
      $('.static').removeClass('hide');
      $('#ajax-response').html('');
      history.pushState(null, 'searching', location.pathname + Search.url_query);
    }
  },

  questionsResponse: function(response) {
    // create tr
    var tr = $('<tr/>');

    var tds = [];

    // create question td
    var q_td = $('<td/>');
    if (response.fields.question_da && response.fields.answer_da) {
      var qa_da = $('<div class="question-answer"><div class="question">' +
                    response.fields.question_da + '</div>' +
                    '<div class="answer">' + response.fields.answer_da +
                    '</div></div>');
      q_td.append(qa_da);
    }

    if (response.fields.question_en && response.fields.answer_en) {
      var qa_en = $('<div class="question-answer"><div class="question">' +
                    response.fields.question_en + '</div>' +
                    '<div class="answer">' + response.fields.answer_en +
                    '</div></div>');
      q_td.append(qa_en);
    }

    tds.push(q_td);

    var date_td = $('<td/>').html(response.fields.date_added);
    tds.push(date_td);

    var last_td = $('<td/>').html(response.fields.date_last_edit);
    tds.push(last_td);

    for (var i = 0; i < tds.length; i++) {
      tr.append(tds[i]);
    }

    $('#ajax-response').append(tr);
    $('.static').addClass('hide');
  }
};
