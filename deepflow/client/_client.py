import sys

from ..version import VERSION


class DeepflowClient:
    _safe_mode: bool = True

    def __init__(self, api_key: str = None):
        from .._consts import DEEPFLOW_API_URL
        import os

        self._api_url = os.environ.get("DEEPFLOW_API_URL", DEEPFLOW_API_URL)
        self._api_key = api_key if api_key else os.environ.get("DEEPFLOW_API_KEY")

    def set_safe_mode(self, safe_mode: bool):
        self._safe_mode = safe_mode

    def send(self, command, *, safe_mode: bool | None = None, test: bool = False):
        """
        커맨드를 전송한다
        :param command: 커맨드
        :param safe_mode: True 설정시 오류가 발생하여도 예외가 발생하지 않음
        :param test: True 설정시 실제 API 호출을 하지 않고 요청 정보만 콘솔에 출력한다
        :return: 처리 결과 응답
        """
        import requests
        from dataclasses import asdict

        if self._api_key is None:
            print("Environment variable DPANDA_API_KEY must be set", file=sys.stderr)
            exit(1)

        if safe_mode is None:
            safe_mode = self._safe_mode

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

        param = {
            "headers": {
                "x-dpanda-client": f"name=deepflow,version={VERSION}",
                "x-dpanda-api-key": self._api_key,
            }
        }

        if len(cmd_dict) > 0:
            if action_method in ["POST", "PUT"]:
                param["json"] = {k: v for k, v in cmd_dict.items() if v is not None}
            elif action_method == "GET":
                param["params"] = cmd_dict

        if test:
            print("Method:", action_method)
            print("Url:", url)
            print("Params:", param)

            return dict(_status=200)

        resp = requests.request(action_method, url, **param)

        status = resp.status_code
        if 400 <= status < 500:
            print(resp.text, file=sys.stderr)
            exit(1)

        if not safe_mode and not 200 <= status < 300:
            print(resp.text, file=sys.stderr)
            raise RuntimeError(f"Status code: {status}")

        return dict(_status=status, **resp.json())
