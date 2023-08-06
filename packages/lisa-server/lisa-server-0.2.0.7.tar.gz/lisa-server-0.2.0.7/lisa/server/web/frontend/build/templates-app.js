angular.module('templates-app', ['chat/chat.tpl.html', 'chat/microphone.tpl.html', 'dashboard/dashboard.tpl.html', 'interface/breadcrumb.tpl.html', 'interface/interface.tpl.html', 'interface/login.tpl.html', 'interface/profile.tpl.html', 'interface/upgrade.tpl.html', 'plugins/modal_configuration.tpl.html', 'plugins/plugins.tpl.html', 'plugins/plugins_create.tpl.html']);

angular.module("chat/chat.tpl.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("chat/chat.tpl.html",
    "<section class=\"chatmodule\" ng-controller=\"ChatCtrl\">\n" +
    "    <div class=\"tile\" ng-click=\"isopen=!isopen\">\n" +
    "      <h1 translate class=\"tile-title\">L.I.S.A Chat</h1>\n" +
    "\n" +
    "      <div class=\"tile-config\">\n" +
    "        <i ng-class=\"{true:'fa-bell-o', false:'fa-bell-slash-o'}[sound]\" class=\"fa\" ng-click=\"sound=!sound\"></i>\n" +
    "        <i ng-class=\"{true:'fa-minus', false:'fa-plus'}[isopen]\" class=\"fa\"  ng-click=\"isopen=!isopen\"></i>\n" +
    "      </div>\n" +
    "\n" +
    "    </div>\n" +
    "\n" +
    "    <ol ng-show=\"isopen\" class=\"discussion\" scroll-glue>\n" +
    "        <li ng-repeat=\"message in messages\" class=\"{{ message.class }}\">\n" +
    "            <img class=\"avatar\" />\n" +
    "            <div class=\"messages\">\n" +
    "                <p ng-bind-html=\"message.body\"></p>\n" +
    "            </div>\n" +
    "        </li>\n" +
    "    </ol>\n" +
    "\n" +
    "    <form ng-show=\"isopen\" ng-submit=\"sendMessage()\">\n" +
    "        <input type=\"text\" ng-model=\"messageText\" class=\"form-control input-sm\" />\n" +
    "    </form\n" +
    "</section>");
}]);

angular.module("chat/microphone.tpl.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("chat/microphone.tpl.html",
    "<section class=\"microphonemodule\" ng-controller=\"MicrophoneCtrl\">\n" +
    "    <div id=\"microphone\" class=\"fa fa-microphone fa-2x\" ng-controller=\"MicrophoneCtrl\"></div>\n" +
    "</section>");
}]);

angular.module("dashboard/dashboard.tpl.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("dashboard/dashboard.tpl.html",
    "<!-- Breadcrumb -->\n" +
    "                <div ncy-breadcrumb></div>\n" +
    "                <!-- /Breadcrumb -->\n" +
    "                <hr class=\"whiter\" />\n" +
    "\n" +
    "                <!-- Main Widgets -->\n" +
    "\n" +
    "                <div class=\"block-area\">\n" +
    "                    <div class=\"row\">\n" +
    "                        <div class=\"col-md-8\">\n" +
    "\n" +
    "                            <!--  Widget 1 -->\n" +
    "                            <div class=\"row\">\n" +
    "                                <div class=\"col-md-6\">\n" +
    "                                    <div class=\"tile\">\n" +
    "                                        <h2 class=\"tile-title\">Widget 1</h2>\n" +
    "                                        <div class=\"tile-config dropdown\">\n" +
    "                                            <a data-toggle=\"dropdown\" href=\"\" class=\"tile-menu\"></a>\n" +
    "                                            <ul class=\"dropdown-menu animated pull-right text-right\">\n" +
    "                                                <li><a href=\"\">Refresh</a></li>\n" +
    "                                                <li><a href=\"\">Settings</a></li>\n" +
    "                                            </ul>\n" +
    "                                        </div>\n" +
    "\n" +
    "                                        <div class=\"listview narrow\">\n" +
    "                                            <div class=\"media p-l-5\">\n" +
    "                                                <div class=\"media-body\">\n" +
    "                                                    <p>data 1</p>\n" +
    "                                                </div>\n" +
    "                                            </div>\n" +
    "                                            <div class=\"media p-l-5\">\n" +
    "                                                <div class=\"media-body\">\n" +
    "                                                    <p>data 2</p>\n" +
    "                                                </div>\n" +
    "                                            </div>\n" +
    "                                            <div class=\"media p-l-5\">\n" +
    "                                                <div class=\"media-body\">\n" +
    "                                                    <p>data 3</p>\n" +
    "                                                </div>\n" +
    "                                            </div>\n" +
    "                                            <div class=\"media p-l-5\">\n" +
    "                                                <div class=\"media-body\">\n" +
    "                                                    <p>data 4</p>\n" +
    "                                                </div>\n" +
    "                                            </div>\n" +
    "                                            <div class=\"media p-5 text-center l-100\">\n" +
    "                                                <a href=\"\"><small>VIEW ALL</small></a>\n" +
    "                                            </div>\n" +
    "                                        </div>\n" +
    "                                    </div>\n" +
    "                                </div>\n" +
    "\n" +
    "                                <!-- Widget 2 -->\n" +
    "                                <div class=\"col-md-6\">\n" +
    "                                    <div class=\"tile\">\n" +
    "                                        <h2 class=\"tile-title\">Widget 2</h2>\n" +
    "                                        <div class=\"tile-config dropdown\">\n" +
    "                                            <a data-toggle=\"dropdown\" href=\"\" class=\"tile-menu\"></a>\n" +
    "                                            <ul class=\"dropdown-menu pull-right text-right\">\n" +
    "                                                <li><a href=\"\">Refresh</a></li>\n" +
    "                                                <li><a href=\"\">Settings</a></li>\n" +
    "                                            </ul>\n" +
    "                                        </div>\n" +
    "                                        <div class=\"listview narrow\">\n" +
    "                                            <div class=\"media p-l-5\">\n" +
    "                                                <div class=\"media-body\">\n" +
    "                                                    <p>data 2</p>\n" +
    "                                                </div>\n" +
    "                                            </div>\n" +
    "                                            <div class=\"media p-l-5\">\n" +
    "                                                <div class=\"media-body\">\n" +
    "                                                    <p>data 2</p>\n" +
    "                                                </div>\n" +
    "                                            </div>\n" +
    "                                            <div class=\"media p-l-5\">\n" +
    "                                                <div class=\"media-body\">\n" +
    "                                                    <p>data 2</p>\n" +
    "                                                </div>\n" +
    "                                            </div>\n" +
    "                                        </div>\n" +
    "                                    </div>\n" +
    "                                </div>\n" +
    "                            </div>\n" +
    "                            <div class=\"clearfix\"></div>\n" +
    "                        </div>\n" +
    "                    </div>\n" +
    "                </div>\n" +
    "");
}]);

angular.module("interface/breadcrumb.tpl.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("interface/breadcrumb.tpl.html",
    "<ol class=\"breadcrumb\" style=\"float: left\">\n" +
    "    <li ng-repeat=\"step in steps | limitTo:(steps.length-1)\">\n" +
    "        <a href=\"{{step.ncyBreadcrumbLink}}\" ng-bind-html=\"step.ncyBreadcrumbLabel | translate\"></a>\n" +
    "    </li>\n" +
    "    <li ng-repeat=\"step in steps | limitTo:-1\" class=\"active\">\n" +
    "        <span ng-bind-html=\"step.ncyBreadcrumbLabel | translate\"></span>\n" +
    "    </li>\n" +
    "</ol>");
}]);

angular.module("interface/interface.tpl.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("interface/interface.tpl.html",
    "");
}]);

angular.module("interface/login.tpl.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("interface/login.tpl.html",
    "<div class=\"container\">\n" +
    "        <div class=\"row\">\n" +
    "            <div class=\"col-md-4 col-md-offset-4\">\n" +
    "                <div class=\"login-panel panel panel-default\">\n" +
    "                    <div class=\"panel-heading\">\n" +
    "                        <h3 class=\"panel-title\" translate>Please Sign In</h3>\n" +
    "                    </div>\n" +
    "                    <div class=\"panel-body\">\n" +
    "                        <form role=\"form\" novalidate class=\"login-form\" ng-controller=\"LoginController\">\n" +
    "                            <fieldset>\n" +
    "                                <div class=\"alert alert-warning\" ng-show=\"authReason\">\n" +
    "                                  {{authReason}}\n" +
    "                                </div>\n" +
    "                                <div class=\"alert alert-error\" ng-show=\"authError\">\n" +
    "                                  {{authError}}\n" +
    "                                </div>\n" +
    "                                <div class=\"form-group\">\n" +
    "                                    <input class=\"form-control\" ng-model=\"username\" placeholder=\"Username\" name=\"login\" type=\"text\" autofocus required>\n" +
    "                                </div>\n" +
    "                                <div class=\"form-group\">\n" +
    "                                    <input class=\"form-control\" ng-model=\"password\" placeholder=\"Password\" name=\"pass\" type=\"password\" required value=\"\">\n" +
    "                                </div>\n" +
    "                                <!-- Change this to a button or input when using this as a form -->\n" +
    "                                <button class=\"btn btn-primary btn-block login\" ng-click=\"Login()\" translate>Sign in</button>\n" +
    "                            </fieldset>\n" +
    "                        </form>\n" +
    "                    </div>\n" +
    "                </div>\n" +
    "            </div>\n" +
    "        </div>\n" +
    "    </div>");
}]);

angular.module("interface/profile.tpl.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("interface/profile.tpl.html",
    "<div class=\"profile\">\n" +
    "    <h1 translate>{{ Session.User.username }}'s profile</h1>\n" +
    "\n" +
    "    <form name=\"profile_form\" class=\"form-horizontal\" role=\"form\" novalidate>\n" +
    "      <div class=\"form-group\">\n" +
    "        <label for=\"inputUsername\" class=\"col-sm-2 control-label\" translate>Username</label>\n" +
    "        <div class=\"col-sm-10\">\n" +
    "          <input type=\"text\" name=\"username\" class=\"form-control\" id=\"inputUsername\" data-ng-model=\"Session.User.username\" required>\n" +
    "        </div>\n" +
    "      </div>\n" +
    "      <div class=\"form-group\">\n" +
    "        <label for=\"inputFirstname\" class=\"col-sm-2 control-label\" translate>Firstname</label>\n" +
    "        <div class=\"col-sm-4\">\n" +
    "          <input type=\"text\" name=\"firstname\" class=\"form-control\" id=\"inputFirstname\" data-ng-model=\"Session.User.first_name\">\n" +
    "        </div>\n" +
    "\n" +
    "        <label for=\"inputLastname\" class=\"col-sm-2 control-label\" translate>Lastname</label>\n" +
    "        <div class=\"col-sm-4\">\n" +
    "          <input type=\"text\" name=\"lastname\" class=\"form-control\" id=\"inputLastname\" data-ng-model=\"Session.User.last_name\">\n" +
    "        </div>\n" +
    "      </div>\n" +
    "      <div class=\"form-group\">\n" +
    "        <label for=\"inputEmail\" class=\"col-sm-2 control-label\" translate>Email</label>\n" +
    "        <div class=\"col-sm-10\">\n" +
    "          <input type=\"email\" name=\"email\" class=\"form-control\" id=\"inputEmail\" data-ng-model=\"Session.User.email\">\n" +
    "        </div>\n" +
    "      </div>\n" +
    "      <div class=\"form-group\">\n" +
    "        <label for=\"inputPassword\" class=\"col-sm-2 control-label\" translate>Password</label>\n" +
    "        <div class=\"col-sm-10\">\n" +
    "          <input type=\"password\" name=\"password\" class=\"form-control\" id=\"inputPassword\">\n" +
    "        </div>\n" +
    "      </div>\n" +
    "      <div class=\"form-group\">\n" +
    "        <label for=\"inputLastname\" class=\"col-sm-2 control-label\" translate>API Key</label>\n" +
    "        <div class=\"col-sm-7\">\n" +
    "          <input type=\"text\" name=\"apikey\" class=\"form-control\" readonly id=\"inputAPIKey\" data-ng-model=\"Session.User.apikey\">\n" +
    "        </div>\n" +
    "        <div class=\"col-sm-3\">\n" +
    "          <button ng-click=\"regenerateAPIKey()\" class=\"btn btn-primary\" translate>Regenerate</button>\n" +
    "        </div>\n" +
    "      </div>\n" +
    "      <div class=\"form-group\">\n" +
    "        <div class=\"col-sm-offset-2 col-sm-10 action-bar\">\n" +
    "          <button ng-click=\"submit()\" ng-disabled=\"profile_form.$invalid\" type=\"submit\" class=\"btn btn-success\" translate>Submit</button>\n" +
    "          <button ng-click=\"cancel()\" class=\"btn btn-danger\" translate>Cancel</button>\n" +
    "        </div>\n" +
    "      </div>\n" +
    "    </form>\n" +
    "</div>");
}]);

angular.module("interface/upgrade.tpl.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("interface/upgrade.tpl.html",
    "<div ui-view=\"upgrade\">\n" +
    "    <!-- Breadcrumb -->\n" +
    "    <div ncy-breadcrumb></div>\n" +
    "    <!-- /Breadcrumb -->\n" +
    "    <hr class=\"whiter\" />\n" +
    "\n" +
    "    <div class=\"block-area\">\n" +
    "        <div class=\"row\">\n" +
    "            <div class=\"col-md-6\">\n" +
    "                <div class=\"row\">\n" +
    "                    <div class=\"col-md-8\">\n" +
    "                        <div ng-if=\"LisaServerVersion.should_upgrade == true\" class=\"tile\">\n" +
    "                            <h2 class=\"tile-title\" translate>You should upgrade your version of L.I.S.A Server</h2>\n" +
    "                            <div class=\"listview narrow row v-center\">\n" +
    "                                <div class=\"col-md-8\">\n" +
    "                                    <dl class=\"m-l-10 m-t-5\">\n" +
    "                                        <dt translate>Local version</dt>\n" +
    "                                        <dd>{{ LisaServerVersion.local_version }}</dd>\n" +
    "                                        <dt translate>Remote version</dt>\n" +
    "                                        <dd>{{ LisaServerVersion.remote_version }}</dd>\n" +
    "                                    </dl>\n" +
    "                                </div>\n" +
    "                                <div class=\"col-md-4\">\n" +
    "                                    <button class=\"btn btn-primary btn-xs\" ng-click=\"upgrade()\" translate>Upgrade</button>\n" +
    "                                </div>\n" +
    "                            </div>\n" +
    "                        </div>\n" +
    "                        <div ng-if=\"LisaServerVersion.should_upgrade == false\" class=\"tile\">\n" +
    "                            <h2 class=\"tile-title\" translate>You already have the last version of L.I.S.A Server</h2>\n" +
    "                            <div class=\"listview narrow\">\n" +
    "                                <dl class=\"m-l-10 m-t-5\">\n" +
    "                                    <dt translate>Local version</dt>\n" +
    "                                    <dd>{{ LisaServerVersion.local_version }}</dd>\n" +
    "                                    <dt translate>Remote version</dt>\n" +
    "                                    <dd>{{ LisaServerVersion.remote_version }}</dd>\n" +
    "                                </dl>\n" +
    "                            </div>\n" +
    "                        </div>\n" +
    "                    </div>\n" +
    "                </div>\n" +
    "            </div>\n" +
    "        </div>\n" +
    "    </div>\n" +
    "</div>");
}]);

angular.module("plugins/modal_configuration.tpl.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("plugins/modal_configuration.tpl.html",
    "<div class=\"configuration\">\n" +
    "    <h1 translate>Configuration of plugin {{ plugin.name }}</h1>\n" +
    "    <div ui-ace=\"{ onLoad : aceLoaded }\"></div>\n" +
    "    <div class=\"action-bar\">\n" +
    "        <button class=\"btn btn-success\" ng-click=\"save()\" translate>Save</button>\n" +
    "        <button class=\"btn btn-danger\" ng-click=\"cancel()\" translate>Cancel</button>\n" +
    "    </div>\n" +
    "</div>");
}]);

angular.module("plugins/plugins.tpl.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("plugins/plugins.tpl.html",
    "<div ui-view=\"plugins\">\n" +
    "    <!-- Breadcrumb -->\n" +
    "    <div ncy-breadcrumb></div>\n" +
    "    <!-- /Breadcrumb -->\n" +
    "    <hr class=\"whiter\" />\n" +
    "\n" +
    "    <div class=\"row block-area\">\n" +
    "        <div class=\"col-md-12\">\n" +
    "    <table ng-table=\"tablePlugins\" show-filter=\"true\" class=\"table ng-table tile\">\n" +
    "        <thead>\n" +
    "            <tr>\n" +
    "                <th class=\"sortable\" ng-class=\"{\n" +
    "                    'sort-asc': tableParams.isSortBy('name', 'asc'),\n" +
    "                    'sort-desc': tableParams.isSortBy('name', 'desc')\n" +
    "                  }\"\n" +
    "                    ng-click=\"tableParams.sorting({'name' : tablePlugins.isSortBy('name', 'asc') ? 'desc' : 'asc'})\" translate>\n" +
    "                    Name\n" +
    "                </th>\n" +
    "                <th translate>Description</th>\n" +
    "                <th translate>Version</th>\n" +
    "                <th translate>Enabled</th>\n" +
    "                <th translate>Lang</th>\n" +
    "                <th translate>Author</th>\n" +
    "                <th translate>Actions</th>\n" +
    "            </tr>\n" +
    "        </thead>\n" +
    "        <tbody>\n" +
    "            <tr ng-repeat=\"plugin in plugins\">\n" +
    "                <td data-title=\"'Name'\" sortable=\"'name'\" filter=\"{ 'name': 'text' }\"><b>{{ plugin.name }}</b></td>\n" +
    "                <td>\n" +
    "                    <div ng-repeat=\"oDescription in plugin.description\" ng-if=\"oDescription.lang == configuration.lang\">\n" +
    "                        {{ oDescription.description }}\n" +
    "                    </div>\n" +
    "                </td>\n" +
    "                <td>{{ plugin.version }}</td>\n" +
    "                <td>\n" +
    "                    <div ng-if=\"plugin.enabled == true\" translate>\n" +
    "                        Yes\n" +
    "                    </div>\n" +
    "                    <div ng-if=\"plugin.enabled == false\" translate>\n" +
    "                        No\n" +
    "                    </div>\n" +
    "                </td>\n" +
    "                <td>\n" +
    "                    <span ng-repeat=\"lang in plugin.lang\"> <span flag=\"'{{ lang }}'\" flag-size=\"f16\"></span></span>\n" +
    "                </td>\n" +
    "                <td>{{ plugin.author }}</td>\n" +
    "                <td>\n" +
    "                    <div ng-if=\"plugin.enabled == true\">\n" +
    "                        <button class=\"btn btn-primary btn-xs\" ng-click=\"disable(plugin.id)\" translate> Disable</button>\n" +
    "                    </div>\n" +
    "                    <div ng-if=\"plugin.enabled == false\">\n" +
    "                        <button class=\"btn btn-primary btn-xs\" ng-click=\"enable(plugin.id)\" translate> Enable</button>\n" +
    "                    </div>\n" +
    "                    <button class=\"btn btn-primary btn-xs fa fa-code\" ng-click=\"editConfiguration(plugin)\" translate> Configuration</button>\n" +
    "                </td>\n" +
    "            </tr>\n" +
    "        </tbody>\n" +
    "    </table>\n" +
    "    </div>\n" +
    "</div>\n" +
    "</div>\n" +
    "");
}]);

angular.module("plugins/plugins_create.tpl.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("plugins/plugins_create.tpl.html",
    "<!-- Breadcrumb -->\n" +
    "<div ncy-breadcrumb></div>\n" +
    "<!-- /Breadcrumb -->\n" +
    "<div ui-ace=\"{ onLoad : aceLoaded }\"></div>");
}]);
