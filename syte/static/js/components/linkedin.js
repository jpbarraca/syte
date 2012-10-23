function setupLinkedin(url, el) {
  var href = el.href;
  if ($('#linkedin-profile').length > 0) {
    window.location = href;
    return;
  }

  var params = url.attr('path').split('/').filter(function(w) {
      if (w.length)
          return true;
      return false;
  })

  if (params.length == 2) {
     var username = params[1];
     
     var spinner = new Spinner(spin_opts).spin();
     $('#linkedin-link').append(spinner.el);
     require(["json!/linkedin/" + username, "text!templates/linkedin-profile.html"],
        function(linkedin_data, linkedin_view) {
            if (linkedin_data.error || linkedin_data.length == 0) {
		alert("Going to href");
                window.location = href;
                return;
            }

            spinner.stop();

        });

     return;
  }

  window.location = href;
}
