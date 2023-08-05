module.exports = function ( karma ) {
  karma.set({
    /** 
     * From where to look for files, starting with the location of this file.
     */
    basePath: '../',

    /**
     * This is the list of file patterns to load into the browser during testing.
     */
    files: [
      'vendor/angular/angular.js',
      'vendor/angular-bootstrap/ui-bootstrap-tpls.min.js',
      'vendor/placeholders/angular-placeholders-0.0.1-SNAPSHOT.min.js',
      'vendor/angular-ui-router/release/angular-ui-router.js',
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
      'vendor/angular-scroll-glue/scrollglue.js',
      'vendor/ng-flags/src/directives/ng-flags.js',
      'vendor/ng-table/ng-table.js',
      'build/templates-app.js',
      'build/templates-common.js',
      'vendor/angular-mocks/angular-mocks.js',
      
      'src/**/*.js',
      'src/**/*.coffee',
    ],
    exclude: [
      'src/assets/**/*.js'
    ],
    frameworks: [ 'jasmine' ],
    plugins: [ 'karma-jasmine', 'karma-firefox-launcher', 'karma-coffee-preprocessor' ],
    preprocessors: {
      '**/*.coffee': 'coffee',
    },

    /**
     * How to report, by default.
     */
    reporters: 'dots',

    /**
     * On which port should the browser connect, on which port is the test runner
     * operating, and what is the URL path for the browser to use.
     */
    port: 9018,
    runnerPort: 9100,
    urlRoot: '/',

    /** 
     * Disable file watching by default.
     */
    autoWatch: false,

    /**
     * The list of browsers to launch to test on. This includes only "Firefox" by
     * default, but other browser names include:
     * Chrome, ChromeCanary, Firefox, Opera, Safari, PhantomJS
     *
     * Note that you can also use the executable name of the browser, like "chromium"
     * or "firefox", but that these vary based on your operating system.
     *
     * You may also leave this blank and manually navigate your browser to
     * http://localhost:9018/ when you're running tests. The window/tab can be left
     * open and the tests will automatically occur there during the build. This has
     * the aesthetic advantage of not launching a browser every time you save.
     */
    browsers: [
      'Firefox'
    ]
  });
};

