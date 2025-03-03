class BaseCommand:
    _method: str
    _action_path: str
    _path_var_props: list[str] = []

    @property
    def method(self):
        return self._method

    @property
    def action_path(self):
        return self._action_path

    @property
    def path_var_props(self):
        return self._path_var_props
