jQuery(document).ready(function ($) {
  $("[id$=reassign_owner]").autocomplete("../subjects", {
    formatItem: formatItem
  });

  $("#field-cc").autocomplete("../subjects", {
    multiple: true,
    formatItem: formatItem
  });

  $("input:text#field-reporter").autocomplete("../subjects", {
    formatItem: formatItem
  });

  for (var i = 0; i < autocomplete_fields.length; i++) {
    $("#field-" + autocomplete_fields[i]).autocomplete("../subjects", {
      formatItem: formatItem
    });
  }
});
