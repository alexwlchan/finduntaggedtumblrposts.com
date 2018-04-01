// This is called by the form on the front page when the user clicks the
// "Get My Untagged Posts" button.  It redirects the user to /results.
function load_results_page() {

  var hostname = document.getElementById("hostname").value;
  var include_reblogs = (
    document.getElementById("reblog_filter").value == "include reblogs"
  );
  var post_filter = document.getElementById("post_filter").value.split(" ")[0];

  if (hostname == "") {
    alert("Please enter a URL!");
    return;
  }

  var parameters = {
    "hostname": hostname,
    "include_reblogs": include_reblogs,
    "post_filter": post_filter,
  }

  var results_url = _build_url_with_qs("/results", parameters = parameters)
  document.location.href = results_url;
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
