angular.module('templates-app', ['chat/chat.tpl.html', 'dashboard/dashboard.tpl.html', 'interface/breadcrumb.tpl.html', 'interface/interface.tpl.html', 'interface/login.tpl.html', 'interface/profile.tpl.html', 'interface/upgrade.tpl.html', 'plugins/modal_configuration.tpl.html', 'plugins/plugins.tpl.html', 'plugins/plugins_create.tpl.html']);

angular.module("chat/chat.tpl.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("chat/chat.tpl.html",
    "<section class=\"chatmodule\" ng-controller=\"ChatCtrl\">\n" +
    "    <header class=\"top-bar\">\n" +
    "      <div class=\"left\"  ng-click=\"isopen=!isopen\">\n" +
    "        <span class=\"message\"></span>\n" +
    "        <h1 translate>L.I.S.A Chat</h1>\n" +
    "      </div>\n" +
    "\n" +
    "      <div class=\"right\">\n" +
    "        <i ng-class=\"{true:'fa-bell-o', false:'fa-bell-slash-o'}[sound]\" class=\"fa\" ng-click=\"sound=!sound\"></i>\n" +
    "        <i ng-class=\"{true:'fa-minus', false:'fa-plus'}[isopen]\" class=\"fa\"  ng-click=\"isopen=!isopen\"></i>\n" +
    "      </div>\n" +
    "\n" +
    "    </header>\n" +
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
    "        <input type=\"text\" ng-model=\"messageText\" />\n" +
    "    </form\n" +
    "</section>");
}]);

angular.module("dashboard/dashboard.tpl.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("dashboard/dashboard.tpl.html",
    "<!-- Breadcrumb -->\n" +
    "                <div ncy-breadcrumb></div>\n" +
    "                <!-- /Breadcrumb -->\n" +
    "\n" +
    "                <div class=\"row\">\n" +
    "                    <div class=\"col-lg-3 col-md-6\">\n" +
    "                        <div class=\"panel panel-primary\">\n" +
    "                            <div class=\"panel-heading\">\n" +
    "                                <div class=\"row\">\n" +
    "                                    <div class=\"col-xs-3\">\n" +
    "                                        <i class=\"fa fa-comments fa-5x\"></i>\n" +
    "                                    </div>\n" +
    "                                    <div class=\"col-xs-9 text-right\">\n" +
    "                                        <div class=\"huge\">26</div>\n" +
    "                                        <div>New Comments!</div>\n" +
    "                                    </div>\n" +
    "                                </div>\n" +
    "                            </div>\n" +
    "                            <a href=\"#\">\n" +
    "                                <div class=\"panel-footer\">\n" +
    "                                    <span class=\"pull-left\">View Details</span>\n" +
    "                                    <span class=\"pull-right\"><i class=\"fa fa-arrow-circle-right\"></i></span>\n" +
    "                                    <div class=\"clearfix\"></div>\n" +
    "                                </div>\n" +
    "                            </a>\n" +
    "                        </div>\n" +
    "                    </div>\n" +
    "                    <div class=\"col-lg-3 col-md-6\">\n" +
    "                        <div class=\"panel panel-green\">\n" +
    "                            <div class=\"panel-heading\">\n" +
    "                                <div class=\"row\">\n" +
    "                                    <div class=\"col-xs-3\">\n" +
    "                                        <i class=\"fa fa-tasks fa-5x\"></i>\n" +
    "                                    </div>\n" +
    "                                    <div class=\"col-xs-9 text-right\">\n" +
    "                                        <div class=\"huge\">12</div>\n" +
    "                                        <div>New Tasks!</div>\n" +
    "                                    </div>\n" +
    "                                </div>\n" +
    "                            </div>\n" +
    "                            <a href=\"#\">\n" +
    "                                <div class=\"panel-footer\">\n" +
    "                                    <span class=\"pull-left\">View Details</span>\n" +
    "                                    <span class=\"pull-right\"><i class=\"fa fa-arrow-circle-right\"></i></span>\n" +
    "                                    <div class=\"clearfix\"></div>\n" +
    "                                </div>\n" +
    "                            </a>\n" +
    "                        </div>\n" +
    "                    </div>\n" +
    "                    <div class=\"col-lg-3 col-md-6\">\n" +
    "                        <div class=\"panel panel-yellow\">\n" +
    "                            <div class=\"panel-heading\">\n" +
    "                                <div class=\"row\">\n" +
    "                                    <div class=\"col-xs-3\">\n" +
    "                                        <i class=\"fa fa-shopping-cart fa-5x\"></i>\n" +
    "                                    </div>\n" +
    "                                    <div class=\"col-xs-9 text-right\">\n" +
    "                                        <div class=\"huge\">124</div>\n" +
    "                                        <div>New Orders!</div>\n" +
    "                                    </div>\n" +
    "                                </div>\n" +
    "                            </div>\n" +
    "                            <a href=\"#\">\n" +
    "                                <div class=\"panel-footer\">\n" +
    "                                    <span class=\"pull-left\">View Details</span>\n" +
    "                                    <span class=\"pull-right\"><i class=\"fa fa-arrow-circle-right\"></i></span>\n" +
    "                                    <div class=\"clearfix\"></div>\n" +
    "                                </div>\n" +
    "                            </a>\n" +
    "                        </div>\n" +
    "                    </div>\n" +
    "                    <div class=\"col-lg-3 col-md-6\">\n" +
    "                        <div class=\"panel panel-red\">\n" +
    "                            <div class=\"panel-heading\">\n" +
    "                                <div class=\"row\">\n" +
    "                                    <div class=\"col-xs-3\">\n" +
    "                                        <i class=\"fa fa-support fa-5x\"></i>\n" +
    "                                    </div>\n" +
    "                                    <div class=\"col-xs-9 text-right\">\n" +
    "                                        <div class=\"huge\">13</div>\n" +
    "                                        <div>Support Tickets!</div>\n" +
    "                                    </div>\n" +
    "                                </div>\n" +
    "                            </div>\n" +
    "                            <a href=\"#\">\n" +
    "                                <div class=\"panel-footer\">\n" +
    "                                    <span class=\"pull-left\">View Details</span>\n" +
    "                                    <span class=\"pull-right\"><i class=\"fa fa-arrow-circle-right\"></i></span>\n" +
    "                                    <div class=\"clearfix\"></div>\n" +
    "                                </div>\n" +
    "                            </a>\n" +
    "                        </div>\n" +
    "                    </div>\n" +
    "                </div>\n" +
    "                <!-- /.row -->\n" +
    "\n" +
    "                <div class=\"row\">\n" +
    "                    <div class=\"col-lg-12\">\n" +
    "                        <div class=\"panel panel-default\">\n" +
    "                            <div class=\"panel-heading\">\n" +
    "                                <h3 class=\"panel-title\"><i class=\"fa fa-bar-chart-o fa-fw\"></i> Area Chart</h3>\n" +
    "                            </div>\n" +
    "                            <div class=\"panel-body\">\n" +
    "                                <div id=\"morris-area-chart\"></div>\n" +
    "                            </div>\n" +
    "                        </div>\n" +
    "                    </div>\n" +
    "                </div>\n" +
    "                <!-- /.row -->\n" +
    "\n" +
    "                <div class=\"row\">\n" +
    "                    <div class=\"col-lg-4\">\n" +
    "                        <div class=\"panel panel-default\">\n" +
    "                            <div class=\"panel-heading\">\n" +
    "                                <h3 class=\"panel-title\"><i class=\"fa fa-long-arrow-right fa-fw\"></i> Donut Chart</h3>\n" +
    "                            </div>\n" +
    "                            <div class=\"panel-body\">\n" +
    "                                <div id=\"morris-donut-chart\"></div>\n" +
    "                                <div class=\"text-right\">\n" +
    "                                    <a href=\"#\">View Details <i class=\"fa fa-arrow-circle-right\"></i></a>\n" +
    "                                </div>\n" +
    "                            </div>\n" +
    "                        </div>\n" +
    "                    </div>\n" +
    "                    <div class=\"col-lg-4\">\n" +
    "                        <div class=\"panel panel-default\">\n" +
    "                            <div class=\"panel-heading\">\n" +
    "                                <h3 class=\"panel-title\"><i class=\"fa fa-clock-o fa-fw\"></i> Tasks Panel</h3>\n" +
    "                            </div>\n" +
    "                            <div class=\"panel-body\">\n" +
    "                                <div class=\"list-group\">\n" +
    "                                    <a href=\"#\" class=\"list-group-item\">\n" +
    "                                        <span class=\"badge\">just now</span>\n" +
    "                                        <i class=\"fa fa-fw fa-calendar\"></i> Calendar updated\n" +
    "                                    </a>\n" +
    "                                    <a href=\"#\" class=\"list-group-item\">\n" +
    "                                        <span class=\"badge\">4 minutes ago</span>\n" +
    "                                        <i class=\"fa fa-fw fa-comment\"></i> Commented on a post\n" +
    "                                    </a>\n" +
    "                                    <a href=\"#\" class=\"list-group-item\">\n" +
    "                                        <span class=\"badge\">23 minutes ago</span>\n" +
    "                                        <i class=\"fa fa-fw fa-truck\"></i> Order 392 shipped\n" +
    "                                    </a>\n" +
    "                                    <a href=\"#\" class=\"list-group-item\">\n" +
    "                                        <span class=\"badge\">46 minutes ago</span>\n" +
    "                                        <i class=\"fa fa-fw fa-money\"></i> Invoice 653 has been paid\n" +
    "                                    </a>\n" +
    "                                    <a href=\"#\" class=\"list-group-item\">\n" +
    "                                        <span class=\"badge\">1 hour ago</span>\n" +
    "                                        <i class=\"fa fa-fw fa-user\"></i> A new user has been added\n" +
    "                                    </a>\n" +
    "                                    <a href=\"#\" class=\"list-group-item\">\n" +
    "                                        <span class=\"badge\">2 hours ago</span>\n" +
    "                                        <i class=\"fa fa-fw fa-check\"></i> Completed task: \"pick up dry cleaning\"\n" +
    "                                    </a>\n" +
    "                                    <a href=\"#\" class=\"list-group-item\">\n" +
    "                                        <span class=\"badge\">yesterday</span>\n" +
    "                                        <i class=\"fa fa-fw fa-globe\"></i> Saved the world\n" +
    "                                    </a>\n" +
    "                                    <a href=\"#\" class=\"list-group-item\">\n" +
    "                                        <span class=\"badge\">two days ago</span>\n" +
    "                                        <i class=\"fa fa-fw fa-check\"></i> Completed task: \"fix error on sales page\"\n" +
    "                                    </a>\n" +
    "                                </div>\n" +
    "                                <div class=\"text-right\">\n" +
    "                                    <a href=\"#\">View All Activity <i class=\"fa fa-arrow-circle-right\"></i></a>\n" +
    "                                </div>\n" +
    "                            </div>\n" +
    "                        </div>\n" +
    "                    </div>\n" +
    "                    <div class=\"col-lg-4\">\n" +
    "                        <div class=\"panel panel-default\">\n" +
    "                            <div class=\"panel-heading\">\n" +
    "                                <h3 class=\"panel-title\"><i class=\"fa fa-money fa-fw\"></i> Transactions Panel</h3>\n" +
    "                            </div>\n" +
    "                            <div class=\"panel-body\">\n" +
    "                                <div class=\"table-responsive\">\n" +
    "                                    <table class=\"table table-bordered table-hover table-striped\">\n" +
    "                                        <thead>\n" +
    "                                            <tr>\n" +
    "                                                <th>Order #</th>\n" +
    "                                                <th>Order Date</th>\n" +
    "                                                <th>Order Time</th>\n" +
    "                                                <th>Amount (USD)</th>\n" +
    "                                            </tr>\n" +
    "                                        </thead>\n" +
    "                                        <tbody>\n" +
    "                                            <tr>\n" +
    "                                                <td>3326</td>\n" +
    "                                                <td>10/21/2013</td>\n" +
    "                                                <td>3:29 PM</td>\n" +
    "                                                <td>$321.33</td>\n" +
    "                                            </tr>\n" +
    "                                            <tr>\n" +
    "                                                <td>3325</td>\n" +
    "                                                <td>10/21/2013</td>\n" +
    "                                                <td>3:20 PM</td>\n" +
    "                                                <td>$234.34</td>\n" +
    "                                            </tr>\n" +
    "                                            <tr>\n" +
    "                                                <td>3324</td>\n" +
    "                                                <td>10/21/2013</td>\n" +
    "                                                <td>3:03 PM</td>\n" +
    "                                                <td>$724.17</td>\n" +
    "                                            </tr>\n" +
    "                                            <tr>\n" +
    "                                                <td>3323</td>\n" +
    "                                                <td>10/21/2013</td>\n" +
    "                                                <td>3:00 PM</td>\n" +
    "                                                <td>$23.71</td>\n" +
    "                                            </tr>\n" +
    "                                            <tr>\n" +
    "                                                <td>3322</td>\n" +
    "                                                <td>10/21/2013</td>\n" +
    "                                                <td>2:49 PM</td>\n" +
    "                                                <td>$8345.23</td>\n" +
    "                                            </tr>\n" +
    "                                            <tr>\n" +
    "                                                <td>3321</td>\n" +
    "                                                <td>10/21/2013</td>\n" +
    "                                                <td>2:23 PM</td>\n" +
    "                                                <td>$245.12</td>\n" +
    "                                            </tr>\n" +
    "                                            <tr>\n" +
    "                                                <td>3320</td>\n" +
    "                                                <td>10/21/2013</td>\n" +
    "                                                <td>2:15 PM</td>\n" +
    "                                                <td>$5663.54</td>\n" +
    "                                            </tr>\n" +
    "                                            <tr>\n" +
    "                                                <td>3319</td>\n" +
    "                                                <td>10/21/2013</td>\n" +
    "                                                <td>2:13 PM</td>\n" +
    "                                                <td>$943.45</td>\n" +
    "                                            </tr>\n" +
    "                                        </tbody>\n" +
    "                                    </table>\n" +
    "                                </div>\n" +
    "                                <div class=\"text-right\">\n" +
    "                                    <a href=\"#\">View All Transactions <i class=\"fa fa-arrow-circle-right\"></i></a>\n" +
    "                                </div>\n" +
    "                            </div>\n" +
    "                        </div>\n" +
    "                    </div>\n" +
    "                </div>\n" +
    "                <!-- /.row -->\n" +
    "");
}]);

angular.module("interface/breadcrumb.tpl.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("interface/breadcrumb.tpl.html",
    "<ol class=\"breadcrumb\">\n" +
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
    "\n" +
    "\n" +
    "    <div ng-if=\"LisaServerVersion.should_upgrade == true\" class=\"panel-container\">\n" +
    "        <span class=\"panel-title\" translate>You should upgrade your version of L.I.S.A Server</span>\n" +
    "        <table class=\"table\">\n" +
    "            <thead>\n" +
    "                <tr>\n" +
    "                    <th translate>Local version</th>\n" +
    "                    <th translate>Remote version</th>\n" +
    "                    <th translate>Action</th>\n" +
    "                </tr>\n" +
    "            </thead>\n" +
    "            <tbody>\n" +
    "                <tr>\n" +
    "                    <td>{{ LisaServerVersion.local_version }}</td>\n" +
    "                    <td>{{ LisaServerVersion.remote_version }}</td>\n" +
    "                    <td>\n" +
    "                        <button class=\"btn btn-primary btn-xs\" ng-click=\"upgrade()\" translate>Upgrade</button>\n" +
    "                    </td>\n" +
    "                </tr>\n" +
    "            </tbody>\n" +
    "        </table>\n" +
    "    </div>\n" +
    "    <div ng-if=\"LisaServerVersion.should_upgrade == false\" class=\"panel-container\">\n" +
    "        <span class=\"panel-title\"  translate>You already have the last version of L.I.S.A Server</span>\n" +
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
    "\n" +
    "    <table ng-table=\"tablePlugins\" show-filter=\"true\" class=\"table ng-table\">\n" +
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
    "\n" +
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
