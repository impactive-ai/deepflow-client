class DeepflowClient:
    _jwt: str = None
    _jwt_exp: float = None

    def __init__(self, *, api_key: str, tenant_id: str):
        from .._consts import DEEPFLOW_API_URL
        import os

        self._api_url = os.environ.get("DEEPFLOW_API_URL", DEEPFLOW_API_URL)
        self._api_key = api_key
        self._tenant_id = tenant_id

    def try_auth(self):
        import requests
        from .._consts import DEEPFLOW_API_URL
        from datetime import datetime

        if self._jwt and datetime.now().timestamp() < self._jwt_exp:
            return

        resp = requests.post(
            f"{DEEPFLOW_API_URL}/auth",
            json={"apiKey": self._api_key, "tenantId": self._tenant_id},
        )
        resp.raise_for_status()

        content = resp.json()
        self._jwt = content["token"]
        self._jwt_exp = content["expiresIn"]

    def send(self, command):
        import requests
        from dataclasses import asdict

        action_path = command.action_path
        action_method = command.method
        path_var_props = command.path_var_props
        cmd_dict = asdict(command)

        url = f"{self._api_url}{action_path}"
        if len(path_var_props) > 0:
            url_param = {k: cmd_dict[k] for k in cmd_dict if k in path_var_props}
            url = url.format(**url_param)
            for k in path_var_props:
                del cmd_dict[k]

        param = {}
        if len(cmd_dict) > 0:
            if action_method in ["POST", "PUT"]:
                param["json"] = cmd_dict
            elif action_method == "GET":
                param["params"] = cmd_dict

        self.try_auth()
        resp = requests.request(
            action_method,
            url,
            **param,
            headers={"Authorization": f"Bearer {self._jwt}"},
        )
        status = resp.status_code

        return dict(_status=status, **resp.json())
