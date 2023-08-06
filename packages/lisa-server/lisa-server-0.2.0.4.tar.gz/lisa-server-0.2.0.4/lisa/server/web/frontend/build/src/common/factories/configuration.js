(function () {
  'use strict';
    angular.module("ConfigurationManager", ['restangular'])
        .constant('constConfExpiry', 20) // in minutes
        .factory("$Configuration", [
                '$rootScope',
                '$log',
                'Restangular',
                function($rootScope, $log, Restangular, constConfExpiry) {
                    return {
                        getConfig: function(){
                            var $this = this;
                            var cachedConfiguration = lscache.get('configuration');
                            if(!$this.Configuration && cachedConfiguration) {
                                $this.configuration = cachedConfiguration;
                            }
                            else if(!$this.configuration){
                                Restangular
                                    .one('lisa/configuration')
                                    .get().then(function(response){
                                        $this.configuration = response.configuration;
                                        lscache.set('configuration', $this.configuration, constConfExpiry);
                                    }, function(response){
                                        $log.error("Error retrieving configuration.");
                                    });
                            }
                        }
                    };
                }
        ]);
})();