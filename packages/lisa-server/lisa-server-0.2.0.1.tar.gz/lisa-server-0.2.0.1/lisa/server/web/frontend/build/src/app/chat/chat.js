/**
 * Each section of the site has its own module. It probably also has
 * submodules, though this boilerplate is too simple to demonstrate it. Within
 * `src/app/home`, however, could exist several additional folders representing
 * additional modules that would then be listed as dependencies of this one.
 * For example, a `note` section could have the submodules `note.create`,
 * `note.delete`, `note.edit`, etc.
 *
 * Regardless, so long as dependencies are managed correctly, the build process
 * will automatically take take of the rest.
 *
 * The dependencies block here is also where component dependencies should be
 * specified, as shown below.
 */
angular.module( 'lisa-frontend.chat', [
  'ui.router',
  'gettext',
  'restangular',
  'ConfigurationManager',
  'luegg.directives'
])

/**
 * Each section or module of the site can also have its own routes. AngularJS
 * will handle ensuring they are all available at run-time, but splitting it
 * this way makes each module more "self-contained".
 */
.config(function config( $stateProvider, gettext ) {
})

.directive('lisaChat', function() {
    return {
        restrict: 'EAC',
        templateUrl: 'chat/chat.tpl.html'
    };
})

/**
 * And of course we define a controller for our route.
 *
 * TODO Create a singleton here
 */
.controller( 'ChatCtrl', function ChatController( $rootScope, $location, $scope, Restangular, $Configuration ) {
    var $port = '';
    if($location.port()){
        $port = ':' + $location.port();
    }

    var sock = new SockJS('http://' + $location.host() + $port + '/websocket');

         var source;
        var context;
        try {
            // Fix up for prefixing
            window.AudioContext = window.AudioContext||window.webkitAudioContext;
            context = new AudioContext();
        }
        catch(e) {
            alert('Web Audio API is not supported in this browser');
        }
        var analyser = context.createAnalyser();
        var canvas=document.getElementById('lisa-canvas');
        var canvasContext=canvas.getContext('2d');
        var isFinished = false;

        var playSound = function(buffer) {
            // TODO Implement a queue to avoid playing multiple sound in the same time
            source = context.createBufferSource();
            source.buffer = buffer;
            source.connect(analyser);
            analyser.connect(context.destination);
            source.onended = function() {
                isFinished = true;
            };
            source.start(0);
        };

        var genSound = function(message) {
            var data = new FormData();
            data.append('message', message);
            data.append('lang', $Configuration.configuration.lang);

            Restangular
                .all('lisa/tts-google/')
                .withHttpConfig({responseType: 'arraybuffer'})
                .post(angular.toJson({message: message, lang: $Configuration.configuration.lang}))
                .then(function(response){
                    context.decodeAudioData(response, function(buffer) {
                    playSound(buffer);
                });
                }, function(response){
                    console.log('Problem with sound generation');
                });
        };

    $scope.messages = [];

    $scope.sendMessage = function() {
        if ($scope.messageText) {
            //var text = '{"body": "' + $scope.messageText + '", "type": "chat", "from": "Lisa-Web", "zone": "WebSocket"}';
            var text = $scope.messageText;
            sock.send(text);
            $scope.messages.push({'body':$scope.messageText, 'class': 'message-me'});
            $scope.messageText = "";
        }
    };

    sock.onmessage = function(e) {
        $scope.isopen = true;
        var oResponse = angular.fromJson(e.data);
        if ($scope.sound) {
            genSound(oResponse.body);
        }
        $scope.messages.push({'body':oResponse.body, 'class': 'message-lisa'});
        $scope.$apply();
    };

    $scope.isopen = false;
    $scope.sound = true;


})
;

