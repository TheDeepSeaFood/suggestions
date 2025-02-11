/*  Wizard */
jQuery(function ($) {
  "use strict";
  // Chose below which method to send the email, available:
  // Simple phpmail text/plain > send_email_1.php
  // PHPMailer text/html > phpmailer/send_email_1_phpmailer.php (default)
  // PHPMailer text/html SMTP > phpmailer/send_email_1_phpmailer_smtp.php
  // PHPMailer with html template > phpmailer/send_email_1_phpmailer_template.php
  // PHPMailer with html template SMTP > phpmailer/send_email_1_phpmailer_template_smtp.php
  // $("form#wrapped").attr("action", "phpmailer/send_email_1_phpmailer.php");
  $("#wizard_container")
    .wizard({
      stepsWrapper: "#wrapped",
      submit: ".submit",
      unidirectional: false,
      beforeSelect: function (event, state) {
        if ($("input#website").val().length != 0) {
          return false;
        }
        if (!state.isMovingForward) return true;
        var inputs = $(this).wizard("state").step.find(":input");
        return !inputs.length || !!inputs.valid();
      },
    })
    .validate({
      errorPlacement: function (error, element) {
        if (element.is(":radio") || element.is(":checkbox")) {
          error.insertBefore(element.next());
        } else {
          error.insertAfter(element);
        }
      },
    });
  //  progress bar
  $("#progressbar").progressbar();
  $("#wizard_container").wizard({
    afterSelect: function (event, state) {
      $("#progressbar").progressbar("value", state.percentComplete);
      $("#location").text(
        "" + state.stepsComplete + " of " + state.stepsPossible + " completed"
      );
    },
  });
});

$("#wizard_container").wizard({
  transitions: {
    branchtype: function ($step, action) {
      var branch = $step.find(":checked").val();
      if (!branch) {
        $("form").valid();
      }
      return branch;
    },
  },
});

$("form#wrapped").validate({
  rules: {
    fileupload: {
      fileType: {
        types: ["image/jpeg", "image/png"], // Use MIME types
      },
      maxFileSize: {
        unit: "KB",
        size: 5000, // Maximum file size is 5000 KB (5 MB)
      },
      minFileSize: {
        unit: "KB",
        size: 2, // Minimum file size is 2 KB
      },
    },
  },
  messages: {
    fileupload: {
      fileType:
        "File must be an image of the following types: .jpg, .jpeg, .png.",
      maxFileSize: "File size cannot exceed 5 MB.",
      minFileSize: "File size must be at least 2 KB.",
    },
  },
});

// Input name and email value
function getVals(formControl, controlType) {
  switch (controlType) {
    case "name_field":
      // Get the value for input and set it to the summary area
      var value = $(formControl).val();
      $("#name_field_summary").text(value); // Change the ID here to a new one
      break;

    case "feedback_suggestions":
      // Get the value for input and set it to the summary area
      var value = $(formControl).val();
      $("#feedback_suggestions_summary").text(value); // Change the ID here to a new one
      break;

    case "branch":
      // Get the value for input and set it to the summary area
      var value = $(formControl).find("option:selected").text();
      $("#branch_summary").text(value); // Change the ID here to a new one
      break;

    case "department":
      // Get the value for input and set it to the summary area
      var value = $(formControl).val();
      $("#department_summary").text(value); // Change the ID here to a new one
      break;

    case "related-department":
      // Get the value for input and set it to the summary area
      var value = $(formControl).find("option:selected").text();
      $("#related_department_summary").text(value); // Change the ID here to a new one
      break;
  }
}

// Add event listener to scroll to the bottom of the page
// document
//   .getElementById("scrollToBottom")
//   .addEventListener("click", function () {
//     window.scrollTo({
//       top: document.body.scrollHeight,
//       behavior: "smooth", // Smooth scrolling effect
//     });
//   });

document.addEventListener("DOMContentLoaded", function () {
  let scrollButton = document.getElementById("scrollToBottom");

  // Function to check if the user is at the bottom of the page
  function checkScroll() {
    if (
      window.innerHeight + window.scrollY >=
      document.body.scrollHeight - 10
    ) {
      scrollButton.style.display = "none"; // Hide button
    } else {
      scrollButton.style.display = "block"; // Show button
    }
  }

  // Scroll event listener
  window.addEventListener("scroll", checkScroll);

  // Click event listener for scrolling to bottom
  scrollButton.addEventListener("click", function () {
    window.scrollTo({
      top: document.body.scrollHeight,
      behavior: "smooth",
    });
  });

  // Initial check in case the page loads already scrolled to bottom
  checkScroll();
});
