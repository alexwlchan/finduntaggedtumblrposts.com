// Trigger a new task.
function start_long_task() {
  hostname = $('#hostname')[0].value;
  if (hostname == "") {
    alert('You must enter a hostname');
    return;
  }

  // TODO: This should discard any existing progress
  $('#progress').html('<hr/><p id="status"></p><ol id="untagged"></ol>');

  // Trigger a POST request to the 'trigger_task' endpoint that
  // kicks off a new task, and tells us where to look for progress.
  $.ajax({
    type: 'POST',
    url: '/trigger_task?hostname=' + hostname,
    success: function(data, status, request) {
      $('#start-bg-job')[0].style.display = "none";
      status_url = request.getResponseHeader('Location');
      update_progress(status_url);
    },
    error: function() {
      // TODO: This should be an error shown to screen, possibly printed?
      alert('Unexpected error');
    }
  });
}

// Ask the server for a progress update, and report it to the user
// by updating the page.
function update_progress(status_url) {
  // TODO: What if this request fails?
  $.getJSON(status_url, function(data) {
    console.log(data);

    // Start by giving the user an update.
    if (data['state'] == "PENDING") {
      $('#status').text('Pending...')
    } else if (data['state'] == "PROGRESS") {
      $('#status').text('In progress, checked ' + data['info']['post_count'] + ' of ' + data['info']['total_posts'] + ':');
    } else if (data['state'] == "SUCCESS") {
      $('#status').text('Complete: found ' + data['info']['posts'].length + ' untagged posts among ' + data['info']['total_posts'] + ' total.');
    } else if (data['state'] == "FAILURE") {
      $('#status').text('Something went wrong.');
    }

    // If the task returned a successful response, add any posts
    // we don't already have to the list of untagged posts shown
    // to the user.
    if (data['state'] == "PROGRESS" || data['state'] == "SUCCESS") {
      current = $('#untagged').find('li').length;
      for (i = current; i < data['info']['posts'].length; i++) {
        post = data['info']['posts'][i];
        li = $('<li class="post__' + post[1] + '"><a href=' + post[0] + '>' + post[0] + '</a></li>');
        $('#untagged').append(li);
      }
    }

    // If the task didn't fail and hasn't finished yet, go back for
    // a progress update in another second.
    if (data['state'] != "FAILURE" && data['state'] != "SUCCESS") {
      setTimeout(function() {
        update_progress(status_url);
      }, 1000);
    }
  })
}


$(function() {
  $('#start-bg-job').click(start_long_task);
});
