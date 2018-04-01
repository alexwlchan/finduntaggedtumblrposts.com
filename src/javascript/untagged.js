// My Tumblr API key.  I should probably be keeping this a secret, but it's
// been online for years with no major side effects.
var API_KEY = "ii4TLRjfMoszcoDkrxBKUk5isHgx0ezQnJ8JWGntYIboVVigez";


// Tracking global state this way is quite icky, but it's a remnant of the old
// code and I don't care enough to fix it right now!
var untagged_total = 0;


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
  console.log("Calling display_results()");

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

  var request_summary = _get_request_summary(
    hostname = hostname,
    include_reblogs = include_reblogs,
    post_type = post_type
  );
  document.getElementById("request_summary").innerHTML = request_summary;

  var api_url = "http://api.tumblr.com/v2/blog/" + _normalise_hostname(hostname) + "/posts";

  // Create the function is_untagged() which determines whether a post is
  // eligible for display in the main list.  The function is defined based
  // on the query parameters, rather than a single definition that uses
  // lots of branches -- this is probably much faster in the long run.
  if (include_reblogs == "true") {

    // If we're including all posts and reblogs, then we just have to
    // look at the length of the tags attribute
    var is_untagged = function(post) {
      return !post.tags.length;
    }
  } else {
    // If we're including all posts, but not reblogs, then we look at
    // the length of the tags attribute, and whether the post has an
    // attribute that only appears on reblogs
    var is_untagged = function(post) {
      return (!post.tags.length) && (!post.hasOwnProperty("reblogged_root_id"));
    }
  }

  _make_request(
    api_url = api_url,
    is_untagged = is_untagged,
    offset = null,
    total = null,
    post_type = post_type,
    success_callback = function(response) {
      _initial_resp_callback(
        response = response,
        api_url = api_url,
        is_untagged = is_untagged,
        post_type = post_type,
      )
    }
  )
}


// Make a request to the Tumblr API.
//
// *  offset     How many posts have been retrieved so far
// *  total      The total number of posts to retrieve (if known)
// *  post_type  Based on the user's choices in the first form
// *  success_callback  Callback to run when the request is complete
//
function _make_request(api_url, is_untagged, offset, total, post_type, success_callback) {
  console.log("Calling _make_request with " + api_url + " and offset " + offset);
  var data = {
    "reblog_info": true,
    "api_key": API_KEY,
  }

  if (offset > 0) {
    data["offset"] = offset;
  }

  if (post_type != "all") {
    data["type"] = post_type;
  }

  $.ajax({
    url: api_url,
    data: data,

    // The name of the callback parameter
    callback: "JSON_CALLBACK",

    // Tell jQuery we're expecting JSON
    dataType: "json",

    success: function(response) {
      success_callback(
        response = response,
        api_url = api_url,
        is_untagged = is_untagged,
        offset = offset,
        total = total,
        post_type = post_type
      )
    }
  })
}


// Callback for the initial response to the Tumblr API.
function _initial_resp_callback(response, api_url, is_untagged, post_type) {
  console.log("Calling _initial_resp_callback with response " + response + "; offset = " + offset + "; total = " + total);
  if (response.meta.status === 200) {
    document.getElementById("first_response").innerHTML = ("<p>I found your blog! Searching for untagged posts:");

    var status_string = "<p>Looked through <span id=\"offset\">0</span> of " + response.response.total_posts + " total post";
    if (response.response.total_posts != 1) {
      status_string += "s";
    }
    status_string += ": (found <span id=\"untagged_total\">0</span> untagged posts)</p>";

    document.getElementById("status").innerHTML = status_string;

    _make_request(
      api_url = api_url,
      is_untagged = is_untagged,
      offset = 0,
      total = response.response.total_posts,
      post_type = post_type,
      success_callback = function(response) {
        _update_page_callback(
          response = response,
          api_url = api_url,
          is_untagged = is_untagged,
          offset = offset,
          total = total,
          post_type = post_type
        )
      }
    );
  } else {
    var error_msg = "<p>I tried to look up your untagged posts, but I got an error.</p>";
    error_msg += "<p>This is the message from the Tumblr API:</p>";
    error_msg += "<pre>Status code " + response.meta.status + ". " + response.meta.msg + ".</pre>";
    error_msg += "<p>If the problem persists, please <a href=\"mailto:alex@alexwlchan.net\">let me know</a>.</p>"
    document.getElementById("first_response").innerHTML = error_msg;
  }
}


// Callback for subsequent responses from the Tumblr API.
function _update_page_callback(response, api_url, is_untagged, offset, total, post_type) {
  console.log("Calling _update_page_callback with response " + response + "; offset = " + offset + "; total = " + total);
  for (var i in response.response.posts) {
    var post = response.response.posts[i];

    if (is_untagged(post)) {
      untagged_total += 1;
      document.getElementById("posts").innerHTML += ("<li><a href=\"" + post.post_url + "\">" + post.post_url + "</a></li>");
    }
  }

  document.getElementById("untagged_total").innerHTML = untagged_total;
  if (offset < total) {
    document.getElementById("offset").innerHTML = offset;

    _make_request(
      api_url = api_url,
      is_untagged = is_untagged,
      offset = offset,
      total = total,
      post_type = post_type,
      success_callback = function(response) {
        _update_page_callback(
          response = response,
          api_url = api_url,
          is_untagged = is_untagged,
          offset = offset + 20,
          total = total,
          post_type = post_type
        )
      }
    );
  } else {
    document.getElementById("first_response").innerHTML = "";
    document.getElementById("status").innerHTML = "<p>I’ve finished looking, and I found " + untagged_total + " untagged posts.</p>";
  }
}


// A function that constructs a string which explains to the user
// what inputs the site is using.  For example:
//
//    Getting untagged posts for *staff.tumblr.com* which *exclude*
//    reblogs and only includes photo posts.
//
// Returns a string.
function _get_request_summary(hostname, include_reblogs, post_type) {
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


// Utility function.  Normalises a URL into a hostname to be supplied to
// the Tumblr API.
var _normalise_hostname = function(url) {
  // First strip any http:// or https:// prefix
  url = url.replace(/^http[s]{0,}:\/\//g, "");

  // Then remove any trailing slashes
  url = url.replace(/\/$/g, "");

  return url
}