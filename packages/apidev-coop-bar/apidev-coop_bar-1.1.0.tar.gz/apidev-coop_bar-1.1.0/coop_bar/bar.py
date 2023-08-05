# -*- coding: utf-8 -*-

from django.utils.importlib import import_module
from django.conf import settings

class CoopBar:
    __we_all_are_one = {}

    def __init__(self):
        self.__dict__ = self.__we_all_are_one #Borg pattern

        if not self.__dict__: #Don't reload for each instance
            self._callbacks = []
            self._headers = []
            self._css_classes = []
            coop_bar_modules = getattr(settings, 'COOP_BAR_MODULES', None)
            if coop_bar_modules:
                for module_name in coop_bar_modules:
                    try:
                        app_admin_bar_module = import_module(module_name)
                        loader_fct = getattr(app_admin_bar_module, 'load_commands')
                        loader_fct(self)
                    except ImportError, msg:
                        raise ImportError(u"coop_bar : error while loading '{0}': {1}".format(module_name, msg))
            else:
                for app in settings.INSTALLED_APPS:
                    try:
                        #load dynamically the admin_bar module of all apps
                        app_admin_bar_module = import_module(app+'.coop_bar_cfg')
                        if hasattr(app_admin_bar_module, 'load_commands'):
                            #call the load_commands function in this module
                            #This function should call the AdminBar:register_command for
                            #every item it want to insert in the bar
                            loader_fct = getattr(app_admin_bar_module, 'load_commands')
                            loader_fct(self)
                    except ImportError:
                        pass

    def register_header(self, callback):
        self._headers.append(callback)

    def register_command(self, callback):
        self._callbacks.append(callback)

    def register_separator(self):
        self._callbacks.append(None)
        
    def register_css_classes(self, callback):
        self._css_classes.append(callback)

    def register(self, list_of_list_of_cmds):
        for list_of_cmds in list_of_list_of_cmds:
            for callback in list_of_cmds:
                self.register_command(callback)
            self.register_separator()

    def get_commands(self, request, context):
        commands = []
        separator = '<div class="separator"></div>'
        for c in self._callbacks:
            if c == None:
                #Replace None by separator. Avoid 2 following separators
                if commands and commands[-1] != separator:
                    html = separator
                else:
                    html = ''
            else:
                #when a page wants to display the admin_bar
                #calls the registred callback in order to know what to display
                html = c(request, context)
            if html:
                commands.append(html)
        if commands and commands[-1] == separator:
            commands = commands[:-1]
        return commands

    def get_headers(self, request, context):
        headers = []
        for c in self._headers:
            html = c(request, context)
            if html:
                headers.append(html)
        return headers
    
    def get_css_classes(self, request, context):
        css_classes = []
        for c in self._css_classes:
            css_class = c(request, context)
            if css_class:
                if type(css_class) in (list, tuple):
                    css_classes.extend(css_class)
                else:
                    css_classes.append(css_class)
        return u" ".join(list(set(css_classes)))