import lisa.plugins
import pip
import shutil
import inspect
from lisa.server.web.manageplugins.models import Plugin, Description, Rule, Cron, Intent
import json
from twisted.python.reflect import namedAny
from django.template.loader import render_to_string
import datetime
from pymongo import MongoClient
from twisted.python import log
import os
import re
import gettext
from lisa.server.ConfigManager import ConfigManagerSingleton

configuration = ConfigManagerSingleton.get().getConfiguration()
dir_path = ConfigManagerSingleton.get().getPath()
path = '/'.join([ConfigManagerSingleton.get().getPath(), 'lang'])
_ = translation = gettext.translation(domain='lisa', localedir=path, fallback=True,
                                              languages=[configuration['lang']]).ugettext


class PluginManager(object):
    """
    """

    def __init__(self):
        self.pkgpath = os.path.dirname(lisa.plugins.__file__)
        self.enabled_plugins = []
        mongo = MongoClient(configuration['database']['server'], configuration['database']['port'])
        self.database = mongo.lisa

    def versioncompare(self, version1, version2):
        def normalize(v):
            return [int(x) for x in re.sub(r'(\.0+)*$', '', v).split(".")]
        return cmp(normalize(version1), normalize(version2))

    def getEnabledPlugins(self):
        return self.enabled_plugins

    def loadPlugins(self):
        for plugin in self.database.plugins.find({"enabled": True, "lang": configuration['lang']}):
            self.enabled_plugins.append(str(plugin['name']))

        return self.enabled_plugins

    def getPluginByName(self, plugin_name):
        """
        Get the plugin correspoding to a given name
        """
        return None

    def installPlugin(self, plugin_name=None, test_mode=False, dev_mode=False, version=None):
        version_str = ""
        if Plugin.objects(name=plugin_name):
            return {'status': 'fail', 'log': unicode(_('Plugin already installed'))}

        if version:
            version_str = ''.join(["==", version])
        if not dev_mode:
            # This test mode is here only for travis to allow installing plugin in a readable directory
            if test_mode:
                pip.main(['install', '--quiet', '--install-option=--install-platlib=' + os.getcwd() + '/../',
                          '--install-option=--install-purelib=' + os.getcwd() + '/../', 'lisa-plugin-' +
                                                                                        plugin_name + version_str])
            else:
                pip.main(['install', 'lisa-plugin-' + plugin_name + version_str])
        jsonfile = self.pkgpath + '/' + plugin_name + '/' + plugin_name.lower() + '.json'
        metadata = json.load(open(jsonfile))

        plugin = Plugin()
        description_list = []
        for item in metadata:
            if item != 'crons' and item != 'rules':
                if item == 'description':
                    for description in metadata[item]:
                        oDescription = Description()
                        for k,v in description.iteritems():
                            setattr(oDescription, k, v)
                        description_list.append(oDescription)
                    setattr(plugin, item, description_list)
                elif item == 'enabled':
                    if metadata[item] == 0:
                        setattr(plugin, item, False)
                    else:
                        setattr(plugin, item, True)
                else:
                    setattr(plugin, item, metadata[item])
        plugin.save()

        for item in metadata:
            if item == 'rules':
                for rule_item in metadata['rules']:
                    rule = Rule()
                    for parameter in rule_item:
                        if parameter == 'enabled':
                            if rule_item[parameter] == 0:
                                setattr(rule, parameter, False)
                            else:
                                setattr(rule, parameter, True)
                        else:
                            setattr(rule, parameter, rule_item[parameter])
                    rule.plugin = plugin
                    rule.save()
            if item == 'crons':
                for cron_item in metadata['crons']:
                    cron = Cron()
                    for parameter in cron_item:
                        if parameter == 'enabled':
                            if cron_item[parameter] == 0:
                                setattr(cron, parameter, False)
                            else:
                                setattr(cron, parameter, True)
                        else:
                            setattr(cron, parameter, cron_item[parameter])
                    cron.plugin = plugin
                    cron.save()

        for intent, value in metadata['configuration']['intents'].iteritems():
            oIntent = Intent()
            oIntent.name = intent
            oIntent.function = value['method']
            oIntent.module = '.'.join(['lisa.plugins', plugin_name, 'modules', plugin_name.lower(),
                                       plugin_name])
            oIntent.enabled = True
            oIntent.plugin = plugin
            oIntent.save()
        return {'status': 'success', 'log': unicode(_('Plugin installed'))}

    def enablePlugin(self, plugin_name=None, plugin_pk=None):
        if plugin_pk:
            plugin_list = Plugin.objects(pk=plugin_pk)
        else:
            plugin_list = Plugin.objects(name=plugin_name)
        for plugin in plugin_list:
            if plugin.enabled:
                return {'status': 'fail', 'log': unicode(_('Plugin already enabled'))}
            else:
                plugin.enabled = True
                plugin.save()
                for cron in Cron.objects(plugin=plugin):
                    cron.enabled = True
                    cron.save()
                for rule in Rule.objects(plugin=plugin):
                    rule.enabled = True
                    rule.save()

                intent_list = Intent.objects(plugin=plugin)
                for oIntent in intent_list:
                    oIntent.enabled = True
                    oIntent.save()
                return {'status': 'success', 'log': unicode(_('Plugin enabled'))}

    def disablePlugin(self, plugin_name=None, plugin_pk=None):
        if plugin_pk:
            plugin_list = Plugin.objects(pk=plugin_pk)
        else:
            plugin_list = Plugin.objects(name=plugin_name)
        for plugin in plugin_list:
            if not plugin.enabled:
                return {'status': 'fail', 'log': unicode(_('Plugin already disabled'))}
            else:
                plugin.enabled = False
                plugin.save()
                for cron in Cron.objects(plugin=plugin):
                    cron.enabled = False
                    cron.save()
                for rule in Rule.objects(plugin=plugin):
                    rule.enabled = False
                    rule.save()

                intent_list = Intent.objects(plugin=plugin)
                for oIntent in intent_list:
                    oIntent.enabled = False
                    oIntent.save()

                return {'status': 'success', 'log': unicode(_('Plugin disabled'))}

    def uninstallPlugin(self, plugin_name=None, plugin_pk=None, dev_mode=False):
        if plugin_pk:
            plugin_list = Plugin.objects(pk=plugin_pk)
        else:
            plugin_list = Plugin.objects(name=plugin_name)
        if not plugin_list:
            return {'status': 'fail', 'log': unicode(_('Plugin not installed'))}
        else:
            for plugin in plugin_list:
                if not dev_mode:
                    pip.main(['uninstall', '--quiet', 'lisa-plugin-' + plugin_name])
                plugin.delete()
                for cron in Cron.objects(plugin=plugin):
                    cron.delete()
                for rule in Rule.objects(plugin=plugin):
                    rule.delete()
                intent_list = Intent.objects(plugin=plugin)
                for oIntent in intent_list:
                    oIntent.delete()

            return {'status': 'success', 'log': unicode(_('Plugin uninstalled'))}

    def methodListPlugin(self, plugin_name=None):
        if plugin_name:
            plugin_list = Plugin.objects(name=plugin_name)
        else:
            plugin_list = Plugin.objects
        listallmethods = []
        for plugin in plugin_list:
            plugininstance = namedAny('.'.join(('lisa.plugins',str(plugin.name), 'modules', str(plugin.name).lower(), str(plugin.name))))()
            listpluginmethods = []
            for m in inspect.getmembers(plugininstance, predicate=inspect.ismethod):
                if not "__init__" in m and not "_" in m:
                    listpluginmethods.append(m[0])
            listallmethods.append({ 'plugin': plugin.name, 'methods': listpluginmethods})
        for f in os.listdir(os.path.normpath(dir_path + '/core')):
            fileName, fileExtension = os.path.splitext(f)
            if os.path.isfile(os.path.join(os.path.normpath(dir_path + '/core'), f)) and not f.startswith('__init__') and fileExtension != '.pyc':
                coreinstance = namedAny('.'.join(('lisa.server.core', str(fileName).lower(), str(fileName).capitalize())))()
                listcoremethods = []
                for m in inspect.getmembers(coreinstance, predicate=inspect.ismethod):
                    #init shouldn't be listed in methods and _ is for translation
                    if not "__init__" in m:
                        listcoremethods.append(m[0])
                listallmethods.append({'core': fileName, 'methods': listcoremethods})
        log.msg(listallmethods)
        return listallmethods

    def _template_to_file(self, filename, template, context):
        import codecs
        codecs.open(filename, 'w', 'utf-8').write(render_to_string(template, context))

    def createPlugin(self, plugin_name, author_name, author_email):
        import requests
        import pytz

        pypireq = requests.get('-'.join(['https://pypi.python.org/pypi/lisa-plugin', plugin_name]))
        if(pypireq.ok):
            return {'status': 'fail', 'log': unicode(_('Plugin already exist on Pypi'))}

        metareq = requests.get('/'.join([configuration['plugin_store'], 'plugins.json']))
        if(metareq.ok):
            for item in json.loads(metareq.text or metareq.content):
                if item['name'].lower() == plugin_name.lower():
                    return {'status': 'fail', 'log': unicode(_('Plugin already exist in the store'))}
        context = {
            'plugin_name': plugin_name,
            'plugin_name_lower': plugin_name.lower(),
            'author_name': author_name,
            'author_email': author_email,
            'creation_date': pytz.UTC.localize(datetime.datetime.now()).strftime("%Y-%m-%d %H:%M%z")
        }
        os.mkdir(os.path.normpath(self.pkgpath + '/' + plugin_name))

        # Lang stuff
        os.mkdir(os.path.normpath(self.pkgpath + '/' + plugin_name + '/lang'))
        os.mkdir(os.path.normpath(self.pkgpath + '/' + plugin_name + '/lang/en'))
        os.mkdir(os.path.normpath(self.pkgpath + '/' + plugin_name + '/lang/en/LC_MESSAGES'))
        self._template_to_file(filename=os.path.normpath(self.pkgpath + '/' + plugin_name + '/lang/en/LC_MESSAGES/' +
                                                    plugin_name.lower() + '.po'),
                          template='plugin/lang/en/LC_MESSAGES/module.po',
                          context=context)

        # Module stuff
        os.mkdir(os.path.normpath(self.pkgpath + '/' + plugin_name + '/modules'))
        self._template_to_file(filename=os.path.normpath(self.pkgpath + '/' + plugin_name + '/modules/' +
                               plugin_name.lower() + '.py'),
                               template='plugin/modules/module.tpl',
                               context=context)
        open(os.path.normpath(self.pkgpath + '/' + plugin_name + '/modules/__init__.py'), "a")

        # Web stuff
        os.mkdir(os.path.normpath(self.pkgpath + '/' + plugin_name + '/web'))
        os.mkdir(os.path.normpath(self.pkgpath + '/' + plugin_name + '/web/templates'))
        shutil.copy(src=os.path.normpath(dir_path + '/web/manageplugins/templates/plugin/web/templates/widget.html'),
                    dst=os.path.normpath(self.pkgpath + '/' + plugin_name + '/web/templates/widget.html'))
        shutil.copy(src=os.path.normpath(dir_path + '/web/manageplugins/templates/plugin/web/templates/index.html'),
                    dst=os.path.normpath(self.pkgpath + '/' + plugin_name + '/web/templates/index.html'))
        open(os.path.normpath(self.pkgpath + '/' + plugin_name + '/web/__init__.py'), "a")
        self._template_to_file(filename=os.path.normpath(self.pkgpath + '/' + plugin_name + '/web/api.py'),
                          template='plugin/web/api.tpl',
                          context=context)
        self._template_to_file(filename=os.path.normpath(self.pkgpath + '/' + plugin_name + '/web/models.py'),
                          template='plugin/web/models.tpl',
                          context=context)
        self._template_to_file(filename=os.path.normpath(self.pkgpath + '/' + plugin_name + '/web/tests.py'),
                              template='plugin/web/tests.tpl',
                              context=context)
        self._template_to_file(filename=os.path.normpath(self.pkgpath + '/' + plugin_name + '/web/urls.py'),
                              template='plugin/web/urls.tpl',
                              context=context)
        self._template_to_file(filename=os.path.normpath(self.pkgpath + '/' + plugin_name + '/web/views.py'),
                          template='plugin/web/views.tpl',
                          context=context)

        # Plugin stuff (metadata)
        self._template_to_file(filename=os.path.normpath(self.pkgpath + '/' + plugin_name + '/__init__.py'),
                          template='plugin/__init__.tpl',
                          context=context)
        self._template_to_file(filename=os.path.normpath(self.pkgpath + '/' + plugin_name + '/README.rst'),
                          template='plugin/README.rst',
                          context=context)
        self._template_to_file(filename=os.path.normpath(self.pkgpath + '/' + plugin_name +
                                                    '/' + plugin_name.lower() + '.json'),
                          template='plugin/module.json',
                          context=context)

        return {'status': 'success', 'log': unicode(_('Plugin created'))}

    def upgradePlugin(self, plugin_name=None, plugin_pk=None, test_mode=False, dev_mode=False):
        if plugin_pk:
            plugin_list = Plugin.objects(pk=plugin_pk)
        else:
            plugin_list = Plugin.objects(name=plugin_name)

        if not plugin_list:
            return {'status': 'fail', 'log': unicode(_('Plugin not installed'))}

        if not dev_mode:
            # This test mode is here only for travis to allow installing plugin in a readable directory
            if test_mode:
                pip.main(['install', '--quiet', '--install-option=--install-platlib=' + os.getcwd() + '/../',
                              '--install-option=--install-purelib=' + os.getcwd() + '/../', 'lisa-plugin-' +
                                                                                            plugin_name, '--upgrade'])
            else:
                pip.main(['install', 'lisa-plugin-' + plugin_name, '--upgrade'])

        jsonfile = self.pkgpath + '/' + plugin_name + '/' + plugin_name.lower() + '.json'
        try:
            metadata = json.load(open(jsonfile))
        except:
            return {'status': 'fail', 'log': unicode(_("The json of the plugin can't be loaded"))}

        for plugin in plugin_list:
            if self.versioncompare(version1=metadata['version'], version2=plugin.version) > 0:
                description_list = []
                for item in metadata:
                    if item != 'crons' and item != 'rules':
                        if item == 'description':
                            # Does we really need to update description object ?
                            pass
                        elif item == 'configuration':
                            #TODO Shouldn't override the configuration of the user
                            # But we should add only the missing entries (only adding)
                            pass
                        elif item == 'enabled':
                            # Shouldn't override the choice of the user
                            pass
                        else:
                            setattr(plugin, item, metadata[item])
                plugin.save()

                for item in metadata:
                    if item == 'rules':
                        for rule_item in metadata['rules']:
                            oRule_list = Rule.objects(name=rule_item['name'])
                            for rule in oRule_list:
                                for parameter in rule_item:
                                    if parameter == 'enabled':
                                        if rule_item[parameter] == 0:
                                            setattr(rule, parameter, False)
                                        else:
                                            setattr(rule, parameter, True)
                                    else:
                                        setattr(rule, parameter, rule_item[parameter])
                                rule.plugin = plugin
                                rule.save()

                    if item == 'crons':
                        for cron_item in metadata['crons']:
                            oCron_list = Cron.objects(name=cron_item['name'])
                            for cron in oCron_list:
                                for parameter in cron_item:
                                    if parameter == 'enabled':
                                        if cron_item[parameter] == 0:
                                            setattr(cron, parameter, False)
                                        else:
                                            setattr(cron, parameter, True)
                                    else:
                                        setattr(cron, parameter, cron_item[parameter])
                                cron.plugin = plugin
                                cron.save()

                for intent, value in metadata['configuration']['intents'].iteritems():
                    oIntent_list = Intent.objects(name=intent)
                    for oIntent in oIntent_list:
                        oIntent.name = intent
                        oIntent.function = value['method']
                        oIntent.module = '.'.join(['lisa.plugins', plugin_name, 'modules', plugin_name.lower(),
                                                   plugin_name])
                        oIntent.enabled = True
                        oIntent.plugin = plugin
                        oIntent.save()
            else:
                return {'status': 'fail', 'log': unicode(_('Plugin already up to date'))}
        return {'status': 'success', 'log': unicode(_('Plugin upgraded'))}

class PluginManagerSingleton(object):
    """
    Singleton version of the plugin manager.

    Being a singleton, this class should not be initialised explicitly
    and the ``get`` classmethod must be called instead.

    To call one of this class's methods you have to use the ``get``
    method in the following way:
    ``PluginManagerSingleton.get().themethodname(theargs)``
    """

    __instance = None

    def __init__(self):
        """
        Initialisation: this class should not be initialised
        explicitly and the ``get`` classmethod must be called instead.
        """

        if self.__instance is not None:
            raise Exception(unicode(_("Singleton can't be created twice !")))

    def get(self):
        """
        Actually create an instance
        """
        if self.__instance is None:
            self.__instance = PluginManager()
        return self.__instance
    get = classmethod(get)