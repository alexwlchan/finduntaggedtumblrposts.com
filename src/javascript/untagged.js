// This is called by the form on the front page when the user clicks the
// "Get My Untagged Posts" button.  It redirects the user to /results.
function load_results_page() {

  var hostname = document.getElementById("hostname").value;
  var include_reblogs = (
    document.getElementById("reblog_filter").value == "include reblogs"
  );
  var post_type = document.getElementById("post_type").value.split(" ")[0];

  if (hostname == "") {
    alert("Please enter a URL!");
    return;
  }

  var parameters = {
    "hostname": hostname,
    "include_reblogs": include_reblogs,
    "post_type": post_type,
  }

  var results_url = _build_url_with_qs("/results", parameters = parameters)
  document.location.href = results_url;
}


// This is called on /results to display the results to the user.
//
// It assumes the user landed on the page via load_results_page().
function display_results() {

  // https://stackoverflow.com/a/3855394/1558022
  var qs = (function(a) {
    if (a == "") return {};
    var b = {};
    for (var i = 0; i < a.length; ++i) {
      var p=a[i].split('=', 2);
      if (p.length == 1)
        b[p[0]] = "";
      else
        b[p[0]] = decodeURIComponent(p[1].replace(/\+/g, " "));
    }
    return b;
  })(window.location.search.substr(1).split('&'));

  var hostname = qs["hostname"];
  var include_reblogs = qs["include_reblogs"];
  var post_type = qs["post_type"];

  var display_option_string = _get_display_option_string(
    hostname = hostname,
    include_reblogs = include_reblogs,
    post_type = post_type
  );
  document.getElementById("option_string").innerHTML = display_option_string;


  // var post_type
  //
  //
  // var hostname = queryParams["hostname"];
  // var include_reblogs = queryParams["include_reblogs"];
  //
  // /**
  //  * We have to special-case these two post types so that they match the
  //  * values which should be supplied to the Tumblr API.
  //  */
  // var post_type = queryParams["type"];
  // if (post_type == "quotes") { post_type = "quote"; }
  // if (post_type == "videos") { post_type = "video"; }
  //
  // var get_results = function() {
  //     document.getElementById("option_string").innerHTML = optionString(hostname, include_reblogs, post_type);
  //     makeRequest(null, null, post_type, initial_success);
  // }
}


// A function that constructs a string which explains to the user
// what inputs the site is using.  For example:
//
//    Getting untagged posts for *staff.tumblr.com* which *exclude*
//    reblogs and only includes photo posts.
//
// Returns a string.
function _get_display_option_string(hostname, include_reblogs, post_type) {
  var optString = "Getting untagged posts for <span class=\"option\">" + hostname + "</span> which ";

  optString += "<span class=\"option\">";
  if (include_reblogs == "true") {
    optString += "include";
  } else {
    optString += "exclude";
  }
  optString += " reblogs</span>";

  if (post_type == "all") {
    return (optString + ".");
  }

  optString += " and only includes <span class=\"option\">" + post_type + " posts</span>.";

  return optString;
}


// Utility function.  Builds a query string.
// Based on https://stackoverflow.com/q/316781/1558022.
function _build_url_with_qs(url, parameters) {
  var qs = "";
  for (var key in parameters) {
    var value = parameters[key]
    qs += encodeURIComponent(key) + "=" + encodeURIComponent(value) + "&";
  }
  if (qs.length > 0) {
    qs = qs.substring(0, qs.length - 1);  // trim the last "&"
    url = url + "?" + qs;
  }
  return url;
}
