/**
 * Tests sit right alongside the file they are testing, which is more intuitive
 * and portable than separating `src` and `test` directories. Additionally, the
 * build process will exclude all `.spec.js` files from the build
 * automatically.
 */
describe( 'chat section', function() {
  beforeEach( module( 'lisa-frontend.chat' ) );

  it( 'should have a dummy test', inject( function() {
    expect( true ).toBeTruthy();
  }));
});

