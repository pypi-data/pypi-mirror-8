describe( 'LisaCtrl', function() {
  describe( 'isCurrentUrl', function() {
    var LisaCtrl, $location, $scope;

    beforeEach( module( 'lisa-frontend' ) );

    beforeEach( inject( function( $controller, _$location_, $rootScope ) {
      $location = _$location_;
      $scope = $rootScope.$new();
      LisaCtrl = $controller( 'LisaCtrl', { $location: $location, $scope: $scope });
    }));

    it( 'should pass a dummy test', inject( function() {
      expect( LisaCtrl ).toBeTruthy();
    }));
  });
});
