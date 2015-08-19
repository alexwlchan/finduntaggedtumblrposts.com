// Set up the Angular app
var tumblrPostsApp = angular.module('untaggedTumblrPostsApp', []);

// Supply my Tumblr API key.  This should probably be obfuscated, but
// it's been sitting on GitHub for over two years and I've not had
// any complaints from Tumblr.  Live with it, I guess.
var API_KEY = 'ii4TLRjfMoszcoDkrxBKUk5isHgx0ezQnJ8JWGntYIboVVigez'



/*====================================*\
  # UTILITY FUNCTIONS
\*====================================*/

/**
 * Cleans up a URL so that it's suitable for passing to the
 * Tumblr API as a hostname.
 * @param {String} url
 * @return {String} hostname
 */
var normalise_url = function(url) {
    // Strip 'http://' and 'https://' from the start of the URL
    url = url.replace(/^http[s]{0,}:\/\//g, "");

    // Strip trailing slashes
    hostname = url.replace(/\/$/g, "");

    return hostname
}



/*====================================*\
  # ANGULAR CONTROLLER
\*====================================*/

untaggedTumblrPostsApp.controller('untaggedTumblrPostsCtrl',
    function($scope, $http, $q) {

        // Set an empty hostname as the default
        $scope.hostname = '';
    }
)