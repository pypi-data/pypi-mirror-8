jQuery(document).ready(function($) {
  $("input[name=deformField4]").change(function(event) {
    /* Act on the event */
    if ($(this).val() == "text"){
      $("input[name=correct_answer]").parent().show();
    }
    else {
      $("input[name=correct_answer]").val("").parent().hide();

    }
  });
  if ($("input[name=deformField4]").val() == "text"){
    $("input[name=correct_answer]").parent().show();
  }
  else {
    $("input[name=correct_answer]").parent().hide();
  }
});

