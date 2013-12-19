var QuestionForm = {
  degrees: null,

  init: function( degrees ) {
    QuestionForm.degrees = degrees;

    $('#id_degree_all_bsc').on('change', QuestionForm.updateBsc);
    $('#id_degree_all_msc').on('change', QuestionForm.updateMsc);
  },

  updateBsc: function() {
    QuestionForm.updateDegree('bsc', '#id_degree_all_bsc');
  },

  updateMsc: function() {
    QuestionForm.updateDegree('msc', '#id_degree_all_msc');
  },

  updateDegree: function(level, id) {
    if ($(id).is(':checked')) {
      $('#id_degrees').find('option').each(function() {
        if ($.inArray(parseInt($(this).val()), QuestionForm.degrees[level]) > -1) {
          $(this).prop('selected', true);
        }
      });
    } else if (!$(id).is(':checked')) {
      $('#id_degrees').find('option').each(function() {
        if ($.inArray(parseInt($(this).val()), QuestionForm.degrees[level]) > -1) {
          $(this).prop('selected', false);
        }
      });
    }
  },
};

var QuestionIndex = {
  filter_toggle_open: false,

  init: function () {
    $('#filter').on('click', QuestionIndex.filter);

    if ($('.filters').hasClass('open')) {
      QuestionIndex.filter_toggle_open = true;
      $('#toggle-filter').removeClass('glyphicon-plus');
      $('#toggle-filter').addClass('glyphicon-minus');
    }

    $('#toggle-filter').on('click', QuestionIndex.toggleFilter);
    $('.filter-wrapper .head').on('click', QuestionIndex.toggleFilter);

    // TODO refactor
    $(document).on('click', '.question', function () {
      if ($(this).parent().hasClass('noanswer')) {
        $(this).parent().removeClass('noanswer');
      } else {
        $(this).parent().addClass('noanswer');
      }
    });
  },

  filter: function () {
    // collect clicked categories
    var categories = [];
    $('#categories').find('input').each(function () {
      if ($(this).is(':checked')) {
        var category = $(this).val();
        categories.push(category);
      }
    });

    // collect clicked degrees
    var degrees = [];
    $('#degrees').find('input').each(function () {
      if ($(this).is(':checked')) {
        var degree = $(this).val();
        degrees.push(degree);
      }
    });

    var query = location.search;
    if (query.charAt(0) === '?') {
      query = query.substring(1);
    }
    var query_list = query.split('&');

    query_list = QuestionIndex.addToQueryString(query_list, 'c', categories);
    query_list = QuestionIndex.addToQueryString(query_list, 'd', degrees);

    query = '?' + query_list.join('&');

    // load new page
    location.search = query;

    return false;
  },

  toggleFilter: function () {
    if (QuestionIndex.filter_toggle_open) {
      $('.filters').removeClass('open');
      $('#toggle-filter').removeClass('glyphicon-minus');
      $('#toggle-filter').addClass('glyphicon-plus');
      QuestionIndex.filter_toggle_open = false;
    } else {
      $('.filters').addClass('open');
      $('#toggle-filter').removeClass('glyphicon-plus');
      $('#toggle-filter').addClass('glyphicon-minus');
      QuestionIndex.filter_toggle_open = true;
    }
  },

  addToQueryString: function ( queryList, type, values ) {
    var found = false;
    for (var i = 0; i < queryList.length; i++) {
      if (queryList[i][0] === type) {
        if (values.length > 0) {
          queryList[i] = type + '=' + values.join('.');
        } else {
          queryList.splice(i, 1);
        }
        found = true;
        break;
      }
    }

    if (!found && values.length > 0) {
      queryList.push(type + '=' + values.join('.'));
    }

    return queryList;
  }
}
