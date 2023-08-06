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
angular.module( 'lisa-frontend.plugins', [
  'ConfigurationManager',
  'ui.router',
  'growlNotifications',
  'gettext',
  'ngTable'
])

/**
 * Each section or module of the site can also have its own routes. AngularJS
 * will handle ensuring they are all available at run-time, but splitting it
 * this way makes each module more "self-contained".
 */
.config(function config( $stateProvider, gettext ) {
  $stateProvider
      .state( 'plugins', {
          url: '/plugins',
          views: {
              "main": {
                  controller: 'PluginsCtrl',
                  templateUrl: 'plugins/plugins.tpl.html'
              }
          },
          data: {
              pageTitle: 'Plugins',
              ncyBreadcrumbLabel: gettext('<i class="fa fa-plug"></i> Plugins')
          }
          })
      .state( 'plugins.create', {
          url: '/create',
          views: {
              "plugins": {
                  controller: 'PluginsCtrl',
                  templateUrl: 'plugins/plugins_create.tpl.html'
              }
          },
          data: {
              pageTitle: gettext('Plugins Create'),
              ncyBreadcrumbLabel: gettext('Create')
          }
      })
  ;
})

.factory('StorePluginsRestangular', function(Restangular) {
  return Restangular.withConfig(function(RestangularConfigurer) {
    RestangularConfigurer.setBaseUrl('http://plugins.lisa-project.net');
    RestangularConfigurer.setRequestSuffix('.json');
  });
})

/**
 * And of course we define a controller for our route.
 */
.controller( 'PluginsCtrl', function PluginsController( $scope, $filter, StorePluginsRestangular, Restangular, $Configuration, growlNotifications, $modal, ngTableParams) {
    $scope.refreshPlugins = function(){
        StorePluginsRestangular
            .all('plugins')
            .getList()
            .then(function(storeResponse){
                $scope.store = storeResponse;
                console.log($scope.store);
            });

            Restangular.all('plugin').getList().then(function(localPluginsResponse){
                $scope.plugins = localPluginsResponse;
                console.log($scope.plugins);
            });

        $scope.plugins = Restangular.all('plugin').getList().$object;
        $scope.tablePlugins = new ngTableParams({
                page: 1,            // show first page
                count: 10           // count per page
            }, {
                total: $scope.plugins.length, // length of plugins
                getData: function($defer, params) {
                    // use build-in angular filter
                    var orderedData = params.sorting() ?
                            $filter('orderBy')($scope.plugins, params.orderBy()) :
                            $scope.plugins;

                    $defer.resolve(orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count()));
                }
            });
    };



    $scope.enable = function($pluginId){
        Restangular
            .one('plugin', $pluginId).one('enable')
            .get().then(function(response){
                if(response.status == 'success') {
                    growlNotifications.add(response.log, 'success');
                    $scope.refreshPlugins();
                } else {
                    growlNotifications.add(response.log, 'error');
                }
            }, function(response){
                console.error("Error retrieving plugin api.");
            });
    };

    $scope.disable = function($pluginId){
        Restangular
            .one('plugin', $pluginId).one('disable')
            .get().then(function(response){
                if(response.status == 'success') {
                    growlNotifications.add(response.log, 'success');
                    $scope.refreshPlugins();
                } else {
                    growlNotifications.add(response.log, 'error');
                }
            }, function(response){
                console.error("Error retrieving plugin api.");
            });
    };

    $scope.refreshPlugins();
    $scope.configuration = $Configuration.configuration;

    $scope.editConfiguration = function (plugin) {
        console.log(plugin);
        var modalInstance = $modal.open({
            templateUrl: 'plugins/modal_configuration.tpl.html',
            controller: 'PluginsConfigurationCtrl',
            resolve: {
              plugin: function () {
                return plugin;
              }
            }
        });
    };

})

.controller( 'PluginsConfigurationCtrl', function PluginsConfigurationController($scope, $modalInstance, plugin, growlNotifications, gettextCatalog, Restangular) {
    var publicEditor;

    $scope.plugin = plugin;
    $scope.aceLoaded = function(_editor){
        // Editor part
        var _session = _editor.getSession();
        var _renderer = _editor.renderer;
        publicEditor = _session;
        // Options
        _session.setMode("ace/mode/json");
        _editor.setTheme("ace/theme/clouds_midnight");
        _session.setUndoManager(new ace.UndoManager());
        _renderer.setShowGutter(true);
        //_renderer.setuseWrapMode(true);

        _editor.setValue(js_beautify(angular.toJson(plugin.configuration)));


    };

    $scope.save = function () {
        try {
            JSON.parse(publicEditor.getValue());
            plugin.configuration = angular.fromJson(publicEditor.getValue());
            plugin.save();
            growlNotifications.add(gettextCatalog.getString('Configuration has been updated'),'success');
            $modalInstance.close();

        } catch (e) {
            growlNotifications.add(gettextCatalog.getString('Please write a valid JSON'),'warning');
        }

    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };
});
