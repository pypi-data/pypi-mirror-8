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
  'luegg.directives',
  'bd.sockjs'
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

.directive('microphone', function() {
    return {
        restrict: 'EAC',
        templateUrl: 'chat/microphone.tpl.html'
    };
})

.factory('$lisaSocket', function ($location, socketFactory) {
    var $port = '';
    if($location.port()){
        $port = ':' + $location.port();
    }

    return socketFactory({
      url: 'http://' + $location.host() + $port + '/websocket'
    });
})

.controller( 'MicrophoneCtrl', function MicrophoneController( $rootScope, $scope, $Configuration, $lisaSocket ) {
        if ($rootScope.mic === undefined) {
            $rootScope.mic = new Wit.Microphone(document.getElementById("microphone"));
        }

        var debug = false;

        if(debug) {
            $rootScope.mic.onready = function () {
                console.log("Microphone is ready to record");
            };
            $rootScope.mic.onaudiostart = function () {
                console.log("Recording started");
            };
            $rootScope.mic.onaudioend = function () {
                console.log("Recording stopped, processing started");
            };
            $rootScope.mic.onerror = function (err) {
                console.log("Error: " + err);
            };
            $rootScope.mic.onconnecting = function () {
                console.log("Microphone is connecting");
            };
            $rootScope.mic.ondisconnected = function () {
                console.log("Microphone is not connected");
            };
        }

        $rootScope.mic.onresult = function (intent, entities, response) {
            $rootScope.chatMessages.push({'body': response.msg_body, 'class': 'message-me'});
            $lisaSocket.send(angular.toJson({'body': response.msg_body, 'outcome': response.outcome, 'type': 'chat', 'from': 'Lisa-Web', 'zone': 'WebSocket'}));

            var r = kv("intent", intent);

            for (var k in entities) {
                var e = entities[k];

                if (!(e instanceof Array)) {
                    r += kv(k, e.value);
                } else {
                    for (var i = 0; i < e.length; i++) {
                        r += kv(k, e[i].value);
                    }
                }
            }
        };

        $rootScope.mic.connect($Configuration.configuration.wit_client_token);

        function kv(k, v) {
            if (toString.call(v) !== "[object String]") {
                v = JSON.stringify(v);
            }
            return k + "=" + v + "\n";
        }
    })


/**
 * And of course we define a controller for our route.
 */
.controller( 'ChatCtrl', function ChatController( $rootScope, $location, $scope, Restangular, $Configuration, $lisaSocket ) {
    var source;

    try {
        // Fix up for prefixing
        window.AudioContext = window.AudioContext||window.webkitAudioContext;
        $rootScope.audioContext = new AudioContext();
    } catch(e) {
        alert('Web Audio API is not supported in this browser');
    }

    var analyser = $rootScope.audioContext.createAnalyser();
    var canvas=document.getElementById('lisa-canvas');
    var canvasContext=canvas.getContext('2d');
    var isFinished = false;

    var playSound = function(buffer) {
        // TODO Implement a queue to avoid playing multiple sound in the same time
        source = $rootScope.audioContext.createBufferSource();
        source.buffer = buffer;
        source.connect(analyser);
        analyser.connect($rootScope.audioContext.destination);
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
                $rootScope.audioContext.decodeAudioData(response, function(buffer) {
                    playSound(buffer);
                });
            }, function(response){
                console.log('Problem with sound generation');
            }
        );
    };

    if ($rootScope.chatMessages === undefined) {
        $rootScope.chatMessages = [];
    }

    $scope.messages = $rootScope.chatMessages;
    $scope.sendMessage = function() {
        if ($scope.messageText) {
            var text = '{"body": "' + $scope.messageText + '", "type": "chat", "from": "Lisa-Web", "zone": "WebSocket"}';
            $lisaSocket.send(text);
            $rootScope.chatMessages.push({'body':$scope.messageText, 'class': 'message-me'});
            $scope.messageText = "";
        }
    };

    $lisaSocket.setHandler('message', function(e) {
        $scope.isopen = true;
        var oResponse = angular.fromJson(e.data);
        if ($scope.sound) {
            genSound(oResponse.body);
        }
        $rootScope.chatMessages.push({'body':oResponse.body, 'class': 'message-lisa'});
        $scope.$apply();
    });

    $scope.isopen = false;
    $scope.sound = true;


})
;
