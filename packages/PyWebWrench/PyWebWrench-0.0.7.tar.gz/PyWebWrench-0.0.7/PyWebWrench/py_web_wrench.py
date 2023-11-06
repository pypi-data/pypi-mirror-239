import subprocess
import sys
import typing
import pathlib

from playwright._impl._api_structures import ProxySettings
import requests
from playwright.sync_api import sync_playwright


class UnsupportedBrowserError(Exception):
    pass


class PyWebWrench:

    def __init__(self, browser_name="firefox"):
        super().__init__()
        self.browser_name = browser_name

    def __run_command(self, command: str):
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                                   encoding="UTF-8")
        stdout, stderr = process.communicate()

        for line in stdout.splitlines():
            sys.stdout.write("\r" + line)
            sys.stdout.flush()

        process.wait()

        if process.returncode == 0:
            pass
        else:
            sys.stdout.write("\n")
            print(stderr)

    def __install_browser(self, browser_name: str):
        browser_name = browser_name.lower()

        supported_browsers_names = ["chromium", "chrome", "chrome-beta", "msedge", "msedge-beta", "msedge-dev", "firefox", "firefox-asan", "webkit"]

        if browser_name not in supported_browsers_names:
            raise UnsupportedBrowserError(f"{browser_name} doesn't support. Supported browsers {supported_browsers_names}")

        self.__run_command(f"playwright install {browser_name}")
        return {"browser_type": browser_name}

    def render_page(self, url: str):
        browser_name = self.__install_browser(self.browser_name)["browser_type"]
        with sync_playwright() as p:
            browser = p[browser_name].launch()
            page = browser.new_page()
            page.goto(url=url)
            page_content = page.content()
            browser.close()
        return page_content

    def control_page(self,
        executable_path: typing.Optional[typing.Union[str, pathlib.Path]] = None,
        channel: typing.Optional[str] = None,
        args: typing.Optional[typing.List[str]] = None,
        ignore_default_args: typing.Optional[
            typing.Union[bool, typing.List[str]]
        ] = None,
        handle_sigint: typing.Optional[bool] = None,
        handle_sigterm: typing.Optional[bool] = None,
        handle_sighup: typing.Optional[bool] = None,
        timeout: typing.Optional[float] = None,
        env: typing.Optional[typing.Dict[str, typing.Union[str, float, bool]]] = None,
        headless: typing.Optional[bool] = None,
        devtools: typing.Optional[bool] = None,
        proxy: typing.Optional[ProxySettings] = None,
        downloads_path: typing.Optional[typing.Union[str, pathlib.Path]] = None,
        slow_mo: typing.Optional[float] = None,
        traces_dir: typing.Optional[typing.Union[str, pathlib.Path]] = None,
        chromium_sandbox: typing.Optional[bool] = None,
        firefox_user_prefs: typing.Optional[
            typing.Dict[str, typing.Union[str, float, bool]]
        ] = None):
        browser_name = self.__install_browser(self.browser_name)["browser_type"]
        p = sync_playwright().start()
        browser = p[browser_name].launch(
            executable_path=executable_path,
            channel=channel,
            args=args,
            ignore_default_args=ignore_default_args,
            handle_sigint=handle_sigint,
            handle_sigterm=handle_sigterm,
            handle_sighup=handle_sighup,
            timeout=timeout,
            env=env,
            headless=headless,
            devtools=devtools,
            proxy=proxy,
            downloads_path=downloads_path,
            slow_mo=slow_mo,
            traces_dir=traces_dir,
            chromium_sandbox=chromium_sandbox,
            firefox_user_prefs=firefox_user_prefs
        )
        page = browser.new_page()
        return page

    def get(url: str, params=None, **kwargs):
        response = requests.get(url=url, params=params, **kwargs)
        return response

    def post(url: str, data=None, json=None, **kwargs):
        response = requests.post(url=url, data=data, json=json, **kwargs)
        return response

    def put(url: str, data=None, **kwargs):
        response = requests.put(url=url, data=data, **kwargs)
        return response

    def delete(url: str, **kwargs):
        response = requests.delete(url=url, **kwargs)
        return response

    def patch(url, data=None, **kwargs):
        response = requests.patch(url, data=data, **kwargs)
        return response

    def head(url, **kwargs):
        response = requests.head(url, **kwargs)
        return response
