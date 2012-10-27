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
                window.location = href;
                return;
            }

            var template = Handlebars.compile(linkedin_view);
            var location = linkedin_data.location.name;
            linkedin_data.location.name = location.replace(/\sArea,\s[a-zA-Z\-\s]*/,"");
            linkedin_data.location.country = location.replace(/.*,/,"");
            $(template(linkedin_data)).modal().on('hidden', function () {
                $(this).remove();
                adjustSelection('home');
            })

            spinner.stop();

        });

     return;
  }

  window.location = href;
}
