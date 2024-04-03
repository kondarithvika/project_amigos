var $loginMsg = $(".loginMsg"),
  $login = $(".login"),
  $signupMsg = $(".signupMsg"),
  $signup = $(".signup"),
  $frontbox = $(".frontbox");

$("#switch1").on("click", function () {
  $loginMsg.toggleClass("visibility");
  $frontbox.addClass("moving");
  $signupMsg.toggleClass("visibility");

  $signup.toggleClass("hide");
  $login.toggleClass("hide");
});

$("#switch2").on("click", function () {
  $loginMsg.toggleClass("visibility");
  $frontbox.removeClass("moving");
  $signupMsg.toggleClass("visibility");

  $signup.toggleClass("hide");
  $login.toggleClass("hide");
});


document.querySelector(".signup button").addEventListener('click', function() {
  window.location.href = "/multImage";  // Navigate to multImage route
});


// $(document).ready(function() {
//   $(".signup button").on("click", function () {
//       // Redirect to multImag.html (assuming it's in the same directory)
//       window.location.href = "/templates/multImag.html";
//   });
// });


setTimeout(function () {
  $("#switch1").click();
}, 1000);

setTimeout(function () {
  $("#switch2").click();
}, 3000);

$(".login button").on("click", function () {
  var username = $(".login input[name='username']").val();
  var password = $(".login input[name='password']").val();

  if (username === "user" && password === "1234") {
    $(".loginSuccessMsg").text("Login Success");

    setTimeout(function () {
      window.location.href = "/templates/multImag.html"; // Replace with the actual URL of the user page
    }, 1000);
  }

  else if (username === "admin" && password === "admin") {
    $(".loginSuccessMsg").text("Admin Login Success");

    setTimeout(function () {
      window.location.href = "/templates/multImag.html"; // Replace with the actual URL of the admin page
    }, 1000);
   }
  else {
    window.location.href = "/templates/multImag.html"; // Replace with the actual URL of the admin page
     
   }
});
