(function () {
  'use strict';
    /*
        Angular Apikey Session Authentication

        This module deals with the following concepts
            - anonymous / authenticated users
            - username/password for initial session authentication
            - apikeys instead of passwords for remaining interaction
            - feature flip code checking


        :: Dataflow

            event:login-required
                perform anything you need at this point, something like
                showing a login form would be appropriate

            LoginController.login
                sends username and password via an event to the session service

            $Session.login
                performs the api post to the login endpoint
                collects the user data and stores userid, apikey, username in time limited cookies
                on success, it broadcasts a login-confirmed


        :: Elements

            Service: $Session
                .hasFeatures
                .logout
                .login
                .setApiKeyAuthHeader
                .refreshCredentials
                .cacheCredentials
                .wipeCredentials


            Controller: LoginController
                .login


            Run: Initialise Module
                sets up all the events required to decouple this module.

                event:auth-login

                event:auth-logout

                event:auth-login-required

                event:auth-loginConfirmed

                $routeChangeSuccess

     */

    angular.module("SessionManager", ['http-auth-interceptor','restangular','growlNotifications'])
        .constant('constSessionExpiry', 20) // in minutes
        .factory("$Session", [
                '$rootScope',
                '$q',
                '$location',
                '$log',
                '$http',
                '$state',
                'Restangular',
                'authService',
                'constSessionExpiry',
                'growlNotifications',

                function($rootScope, $q, $location, $log, $http, $state, Restangular, authService, constSessionExpiry, growlNotifications) {
                    return {
                        loginInProgress: false,
                        User: null,
                        hasFeatures: function(){
                            /*
                                Uses underscore _.difference to yield a list of feature
                                codes the user does not have.

                                returns:
                                    false: if the user is missing feature codes,
                                    true: if the user has all the requested feature codes

                                ::arguments, array
                                    list of feature codes you want to check for
                            */
                                // bail out early
                                if(!this.User || !this.User.features) {
                                    return false;
                                }
                                var userCodeList = this.User.features.all.split(" ");
                                return _.difference(arguments, userCodeList).length === 0;
                            },

                        authSuccess: function(){
                                this.loginInProgress = false;
                                $rootScope.$broadcast('event:session-changed');
                                authService.loginConfirmed();
                            },

                        logout: function(){
                                //$log.info("Handling request for logout");
                                this.wipeUser();
                                $rootScope.$broadcast('event:auth-logout-confirmed');
                            },

                        login: function(data){
                                //$log.info("Preparing Login Data", data);
                                var $this = this;
                                console.log();
                                return Restangular
                                    .all('user/login/')
                                    .post(data)
                                    .then(function userLoginSuccess(loginResponse){
                                            $this.User = loginResponse;
                                            // Change the route to avoid using login endpoint
                                            // to deal with this user object
                                            $this.User.route = 'user';
                                            $this.User.is_authenticated = true;
                                            $this.setApiKeyAuthHeader();
                                            $this.cacheUser();
                                            $this.authSuccess();
                                            console.log($this);
                                            $state.go('dashboard');
                                            growlNotifications.add("Login success" ,'success');
                                        }, function userLoginFailed(loginResponse){
                                            $this.logout();
                                            return $q.reject(loginResponse);
                                        });
                        },

                        setApiKeyAuthHeader: function(){
                                if(this.hasOwnProperty('User') && this.User){
                                    $http.defaults.headers.common.Authorization = "apikey "+this.User.username+':'+this.User.apikey;
                                    //$log.info("Setting Authorization Header", $http.defaults.headers.common.Authorization);
                                }else{
                                    //$log.info("No user for AuthHeader");
                                    delete $http.defaults.headers.common.Authorization;
                                }
                            },

                        refreshUser: function(){
                                var $this = this;
                                var cachedUser = lscache.get('userData');
                                //$log.info("Request to pull User from Cache");

                                //$log.info("$Session.User", $this.User);
                                //$log.info('lscache.get("userData")', cachedUser);

                                if(!$this.User && cachedUser && cachedUser.hasOwnProperty('apikey') && cachedUser.apikey){
                                    //$log.info('Attempting pull user from cache', cachedUser);
                                    $this.User = cachedUser;
                                }
                                else if(!$this.User){
                                    //$log.warn("No user available.");
                                    $rootScope.$broadcast("event:auth-login-required");
                                }

                                if($this.User && $this.User.hasOwnProperty('apikey') && $this.User.apikey){
                                    $this.setApiKeyAuthHeader();
                                    Restangular
                                        .one('user', $this.User.id)
                                        .get().then(function(response){
                                            //$log.info("User data updated from server.");
                                            $this.User = response;
                                            $this.cacheUser();
                                            $this.setApiKeyAuthHeader();
                                            $this.authSuccess();
                                        }, function(response){
                                            //$log.error("Error retrieving user. logging out.");
                                            $this.logout();
                                        });
                                }

                            },

                        cacheUser: function(){
                                if(!this.User){
                                    //$log.warn("Can't cache a null value User");
                                    return false;
                                }
                                if(!this.User.hasOwnProperty("id") && this.User.hasOwnProperty("resource_uri")){
                                    //$log.info("Building $this.User.id");
                                    var bits = this.User.resource_uri.split("/");
                                    this.User.id = Number(bits[bits.length-1]);
                                }
                                //$log.info("Caching User", this.User);
                                lscache.set('userData', this.User, constSessionExpiry);
                            },

                        wipeUser: function(){
                                //$log.info("Wiping User");
                                lscache.remove('userData');
                                this.User = null;
                                this.setApiKeyAuthHeader();
                                $rootScope.$broadcast('event:session-changed');
                            }
                    };
            }]).

        controller("LoginController", function($log, $Session, $scope, $state){
            if($Session.User){
                $state.go('dashboard');
            }
            $scope.Login = function(){
                    $scope.$emit('event:auth-login', {username: $scope.username, password: $scope.password});
                };
            }).

        run(['$rootScope',
             '$log',
             '$Session',
             '$state',

            function($rootScope, $log, $Session, $state){
                $rootScope.Session = $Session;
                // Best practice would be to hook these events in your app.config

                // login

                $rootScope.$on('event:auth-login-required', function(scope, data) {
                        //$log.info("session.login-required");
                        $state.go('login');
                    });

                $rootScope.$on('event:auth-login', function(scope, data) {
                        //$log.info("session.send-login-details");
                        $Session.login(data);
                    });

                $rootScope.$on('event:auth-loginConfirmed', function(scope, data) {
                        //$log.info("session.loginConfirmed");
                        //$state.go('dashboard');
                    });

                // logout
                $rootScope.$on('event:auth-logout', function(scope, data) {
                        //$log.info("session.request-logout");
                        $Session.logout();
                    });
                $rootScope.$on('event:auth-logout-confirmed', function(scope, data) {
                        //$log.info("session.logout-confirmed");
                        $state.go('login');
                    });

                // session state change
                $rootScope.$on('event:session-changed', function(scope){
                    //$log.info("session.changed > ", $Session.User);
                });

                $rootScope.$on('$routeChangeSuccess', function(event, next, current) {
                        if(!$Session.User && next.$$route.loginRequired){
                            //$log.info("Unauthenticated access to ", next.$$route);
                            $rootScope.$broadcast('event:auth-login-required');
                        }
                    });


                //namespace the localstorage with the current domain name.
                lscache.setBucket(window.location.hostname);

            }]);

})();