class PluginManager():

    def __init__(self, path=None, plugin_init_args={}):
        if path:
            self.plugin_dir = path
        else:
            self.plugin_dir = os.path.dirname(__file__) + '/plugins/'

        self.plugins = []
        self._load_plugins()

        self._register_plugins(**plugin_init_args)

    def _load_plugins(self):
        sys.path.append(self.plugin_dir)
        plugin_files = [fn for fn in os.listdir(self.plugin_dir) if
                       fn.startswitch('plugin_') and
                       fn.endswitch('.py')]
        plugin_modules = [m.split('.')[0] for m in plugin_files]
        for module in plugin_modules:
            m = __import__(module)

