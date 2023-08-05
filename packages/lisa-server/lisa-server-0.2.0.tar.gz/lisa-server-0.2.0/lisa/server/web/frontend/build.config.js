/**
 * This file/module contains all configuration for the build process.
 */
module.exports = {
  /**
   * The `build_dir` folder is where our projects are compiled during
   * development and the `compile_dir` folder is where our app resides once it's
   * completely built.
   */
  build_dir: 'build',
  compile_dir: 'bin',

  /**
   * This is a collection of file patterns that refer to our app code (the
   * stuff in `src/`). These file paths are used in the configuration of
   * build tasks. `js` is all project javascript, less tests. `ctpl` contains
   * our reusable components' (`src/common`) template HTML files, while
   * `atpl` contains the same, but for our app's code. `html` is just our
   * main HTML file, `less` is our main stylesheet, and `unit` contains our
   * app's unit tests.
   */
  app_files: {
    js: [ 'src/**/*.js', '!src/**/*.spec.js', '!src/assets/**/*.js' ],
    jsunit: [ 'src/**/*.spec.js' ],

    coffee: [ 'src/**/*.coffee', '!src/**/*.spec.coffee' ],
    coffeeunit: [ 'src/**/*.spec.coffee' ],

    atpl: [ 'src/app/**/*.tpl.html' ],
    ctpl: [ 'src/common/**/*.tpl.html' ],

    html: [ 'src/index.html' ],
    less: 'src/less/main.less'
  },

  /**
   * This is a collection of files used during testing only.
   */
  test_files: {
    js: [
      'vendor/angular-mocks/angular-mocks.js'
    ]
  },


  pot_files: [
      { 'src/app/interface/lang/interface.pot': ['src/app/interface/*.html', 'src/app/interface/*.js','src/index.html','src/common/factories/*.js'] },
      { 'src/app/chat/lang/chat.pot': ['src/app/chat/*.html', 'src/app/chat/*.js'] },
      { 'src/app/dashboard/lang/dashboard.pot': ['src/app/dashboard/*.html', 'src/app/dashboard/*.js'] },
      { 'src/app/plugins/lang/plugins.pot': ['src/app/plugins/*.html','src/app/plugins/*.js'] }
  ],

  po_compiled: [
      { 'build/assets/js/translations.js': ['src/app/**/*.po'] }
  ],

  /**
   * This is the same as `app_files`, except it contains patterns that
   * reference vendor code (`vendor/`) that we need to place into the build
   * process somewhere. While the `app_files` property ensures all
   * standardized files are collected for compilation, it is the user's job
   * to ensure non-standardized (i.e. vendor-related) files are handled
   * appropriately in `vendor_files.js`.
   *
   * The `vendor_files.js` property holds files to be automatically
   * concatenated and minified with our project source files.
   *
   * The `vendor_files.css` property holds any CSS files to be automatically
   * included in our app.
   *
   * The `vendor_files.assets` property holds any assets to be copied along
   * with our app's assets. This structure is flattened, so it is not
   * recommended that you use wildcards.
   */
  vendor_files: {
    js: [
      'vendor/angular/angular.js',
      'vendor/angular-bootstrap/ui-bootstrap-tpls.min.js',
      'vendor/placeholders/angular-placeholders-0.0.1-SNAPSHOT.min.js',
      'vendor/angular-ui-router/release/angular-ui-router.js',
      'vendor/angular-ui-utils/modules/route/route.js',
      'vendor/lodash/dist/lodash.min.js',
      'vendor/restangular/dist/restangular.min.js',
      'vendor/angular-http-auth/src/http-auth-interceptor.js',
      'vendor/angular-loading-bar/build/loading-bar.min.js',
      'vendor/lscache/lscache.min.js',
      'vendor/angular-sanitize/angular-sanitize.js',
      'vendor/angular-growl-notifications/dist/growl-notifications.min.js',
      'vendor/angular-breadcrumb/release/angular-breadcrumb.min.js',
      'vendor/ace-builds/src-min-noconflict/ace.js',
      'vendor/ace-builds/src-min-noconflict/theme-clouds_midnight.js',
      'vendor/ace-builds/src-min-noconflict/mode-json.js',
      'vendor/ace-builds/src-min-noconflict/worker-json.js',
      'vendor/ace-builds/src-min-noconflict/mode-python.js',
      'vendor/ace-builds/src-min-noconflict/mode-django.js',
      'vendor/ace-builds/src-min-noconflict/mode-css.js',
      'vendor/ace-builds/src-min-noconflict/worker-css.js',
      'vendor/ace-builds/src-min-noconflict/mode-html.js',
      'vendor/ace-builds/src-min-noconflict/worker-html.js',
      'vendor/ace-builds/src-min-noconflict/mode-javascript.js',
      'vendor/ace-builds/src-min-noconflict/worker-javascript.js',
      'vendor/ace-builds/src-min-noconflict/mode-xml.js',
      'vendor/angular-ui-ace/ui-ace.min.js',
      'vendor/angular-gettext/dist/angular-gettext.min.js',
      'vendor/angular-animate/angular-animate.min.js',
      'vendor/angular-animate/angular-animate.min.js.map',
      'vendor/angular-scroll-glue/scrollglue.js',
      'vendor/ng-flags/src/directives/ng-flags.js',
      'vendor/ng-table/ng-table.js'
    ],
    css: [
      'vendor/ng-table/ng-table.css'
    ],
    assets: [
    ]
  }
};
