---
layout: page
---

<script>
  // http://stackoverflow.com/questions/316781/how-to-build-query-string-with-javascript
  function buildUrl(url, parameters){
  var qs = "";
  for(var key in parameters) {
    var value = parameters[key];
    qs += encodeURIComponent(key) + "=" + encodeURIComponent(value) + "&";
  }
  if (qs.length > 0){
    qs = qs.substring(0, qs.length-1); //chop off last "&"
    url = url + "?" + qs;
  }
  return url;
  }
  var get_untagged_posts = function() {
    if (document.getElementById("hostname").value == "") {
      alert("Please enter a URL!"); return;
    }
    var parameters = new Array();
    parameters["hostname"] = document.getElementById("hostname").value;
    parameters["include_reblogs"] = (document.getElementById("reblog_filter").value == "include reblogs");
    parameters["type"] = document.getElementById("post_filter").value.split(" ")[0];
    document.location.href = buildUrl("results", parameters);
  }
</script>
<noscript>
  <p><strong>For this tool to work, please enable JavaScript. </strong></p>
  <p><strong> If you don't want to or can't enable JavaScript, then there's an alternative which involves downloading and executing a Python script <a href="https://alexwlchan.net/2013/08/untagged-tumblr-posts/">on my website</a>.
  </strong></p>
  <hr>
</noscript>

<form action="javascript:myfunction();">
  Enter your Tumblr URL:
  <p>
    <center>
      <input type="text" id="hostname" placeholder="example.tumblr.com" autofocus spellcheck="false">
    </center>
  </p>
  <p>
    The results should <select class="styled-select" id="reblog_filter">
      <option>include reblogs</option>
      <option>exclude reblogs</option>
    </select>
    and show
    <select class="styled-select" id="post_filter">
      <option>all types of post</option>
      <option>text posts</option>
      <option>photo posts</option>
      <option>quotes</option>
      <option>link posts</option>
      <option>chat posts</option>
      <option>audio posts</option>
      <option>videos</option>
      <option>answer posts</option>
    </select>.
  </p>
</form>

<center>
  <button type="submit" id="untagged_posts_button" onclick="get_untagged_posts();"> Get my untagged posts!</button>
</center>
