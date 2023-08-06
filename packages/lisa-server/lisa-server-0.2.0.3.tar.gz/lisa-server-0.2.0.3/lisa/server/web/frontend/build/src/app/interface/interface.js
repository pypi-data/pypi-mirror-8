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
angular.module( 'lisa-frontend.interface', [
  'ui.router',
  'SessionManager',
  'ConfigurationManager',
  'restangular',
  'gettext',
  'growlNotifications'
])

/**
 * Each section or module of the site can also have its own routes. AngularJS
 * will handle ensuring they are all available at run-time, but splitting it
 * this way makes each module more "self-contained".
 */
.config(function config( $stateProvider, gettext ) {
  $stateProvider
      .state( 'upgrade', {
          url: '/upgrade',
          views: {
              "main": {
                  controller: 'UpgradeCtrl',
                  templateUrl: 'interface/upgrade.tpl.html'
              }
          },
          data: {
              pageTitle: 'Upgrade',
              ncyBreadcrumbLabel: gettext('<i class="fa fa-upload"></i> Upgrade')
          }
      })
  ;
})

/**
 * And of course we define a controller for our route.
 */
.controller( 'UserDropdownCtrl', function UserDropdownCtrl( $scope, $Session, $Configuration, $modal) {

  $scope.Session = $Session;
  $scope.Configuration = $Configuration.configuration;

  $scope.profile = function () {
    var modalInstance = $modal.open({
      templateUrl: 'interface/profile.tpl.html',
      controller: 'ProfileCtrl'
    });
  };
})

.filter('pad', function() {
  return function(num) {
    return (num < 10 ? '0' + num : num);
  };
})

.controller("ClockController", function($scope, $timeout) {
  $scope.date = new Date();

  var tick = function() {
    $scope.date = new Date();
    $timeout(tick, 1000);
  };
  $timeout(tick, 1000);
})

.controller( 'ProfileCtrl', function ProfileCtrl($scope, $modalInstance, Restangular, gettextCatalog, growlNotifications ) {

  $scope.submit = function () {
    console.log($scope.Session.User);
    $scope.Session.User.save();
    //$modalInstance.close();
  };

  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };

  $scope.regenerateAPIKey = function () {
    Restangular
    .one('user', $scope.Session.User.id).one('regenerateapikey')
    .get().then(function(response){
      if(response.apikey) {
        growlNotifications.add(gettextCatalog.getString('The API Key has been regenerated'), 'success');
        $scope.Session.User.apikey = response.apikey;
        $scope.Session.setApiKeyAuthHeader();
      } else {
        growlNotifications.add(gettextCatalog.getString('There was an error with the API Key'), 'error');
      }
    }, function(response) {
      console.error("Error retrieving user api.");
    });
  };
})

.controller( 'UpgradeCtrl', function UpgradeCtrl( $scope, $Session, $Configuration, Restangular ) {
  $scope.Session = $Session;
  $scope.Configuration = $Configuration.configuration;
  console.log($scope.Configuration);

  var getLisaPackage = function () {
    Restangular
      .one('lisa').one('version')
      .get()
      .then(function (response) {
        $scope.LisaServerVersion = response;
        console.log($scope.LisaServerVersion);
      });
  };

  getLisaPackage();
})
;