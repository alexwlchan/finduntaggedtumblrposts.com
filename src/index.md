---
layout: page
---

<noscript>
  <p><strong>For this tool to work, please enable JavaScript. </strong></p>
  <p><strong> If you don't want to or can't enable JavaScript, then there's an alternative which involves downloading and executing a Python script <a href="https://alexwlchan.net/2013/08/untagged-tumblr-posts/">on my website</a>.
  </strong></p>
  <hr>
</noscript>

<form>
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
  <button type="submit" id="untagged_posts_button" onclick="load_results_page();"> Get my untagged posts!</button>
</center>
