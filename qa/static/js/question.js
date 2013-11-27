var QuestionForm = {
  degrees: null,

  init: function(degrees) {
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
