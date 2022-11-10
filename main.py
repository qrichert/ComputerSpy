#!/usr/bin/env python3

import atexit
import datetime as dt
import io
import os
import time
from pathlib import Path
from typing import TypeVar

import mss
import requests
import yaml
from PIL import Image

os.chdir(os.path.dirname(os.path.realpath(__file__)))

mssScreenShot: TypeVar = TypeVar("mssScreenShot")


class Logger:
    def __init__(self, settings: dict) -> None:
        self._init_from_settings(settings)
        self._create_directory_structure()
        self._register_start_and_close()

        self.main_loop()

    def _init_from_settings(self, settings: dict) -> None:
        self.screenshots_interval = int(settings.get("screenshots_interval"))
        self.img_max_height = int(settings.get("img_max_height"))
        self.img_compression = int(settings.get("img_compression"))
        self.network_timeout = self.screenshots_interval * 2 / 3

        self.local_path = (
            Path(settings.get("local_path")).resolve()
            if settings.get("local_path")
            else None
        )
        self.remote_host = settings.get("remote_host") or None
        self.remote_password = settings.get("remote_password") or None
        self.remote_instance_id = settings.get("remote_instance_id") or None

    def _create_directory_structure(self) -> None:
        if self.do_save_locally():
            self.local_path.mkdir(parents=True, exist_ok=True)

    def do_save_locally(self) -> bool:
        return bool(self.local_path)

    def do_save_on_remote(self) -> bool:
        return bool(self.remote_host)

    def _register_start_and_close(self) -> None:
        self.log_start()
        atexit.register(self.log_close)

    def log_start(self) -> None:
        # Add \n here because if the program doesn't close correctly,
        # the next datetime would be on the wrong line.
        self._log_start_close("\n{} -> ")

    def log_close(self) -> None:
        self._log_start_close("{}")

    def _log_start_close(self, log) -> None:
        now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log = log.format(now)

        if self.do_save_locally():
            self.write_start_close(log)
        if self.do_save_on_remote():
            self.post_start_close(log)

    def write_start_close(self, message) -> None:
        with open(self.local_path / "log.txt", "a") as f:
            f.write(message)

    def post_start_close(self, log) -> None:
        post_data = {"log_start_close": log}

        if self.remote_password:
            post_data["password"] = self.remote_password
        if self.remote_instance_id:
            post_data["instance"] = self.remote_instance_id

        with requests.Session() as session:
            try:
                session.post(
                    self.remote_host,
                    data=post_data,
                    timeout=self.network_timeout,
                )
            except requests.exceptions.RequestException:
                pass

    def main_loop(self) -> None:
        start_time: float = time.monotonic()
        while True:
            try:
                self.log_screen()
                drift = (time.monotonic() - start_time) % self.screenshots_interval
                time.sleep(self.screenshots_interval - drift)
            except KeyboardInterrupt:
                exit()
            except:
                pass

    def log_screen(self) -> None:
        now = dt.datetime.now().strftime("%H.%M.%S")
        file_name = now + ".jpg"

        screenshot = self._grab_screenshot()
        if not screenshot:
            return
        screenshot = self._resize_image(screenshot)

        with io.BytesIO() as output:
            screenshot.save(
                output,  # Write to buffer.
                "JPEG",
                optimize=True,
                quality=self.img_compression,
            )

            if self.do_save_locally():
                self.write_screenshot(output, file_name)
            if self.do_save_on_remote():
                self.post_screenshot(output, file_name)

    @staticmethod
    def _grab_screenshot() -> mssScreenShot | None:
        with mss.mss() as sct:
            monitor = sct.monitors[0]  # 0 = all-in-one monitors
            try:
                return sct.grab(monitor)
            except mss.exception.ScreenShotError:
                # Usually when screen is locked.
                pass
        return None

    def _resize_image(self, img) -> Image.Image:
        img = Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX")
        img.thumbnail((10000, self.img_max_height), Image.Resampling.BICUBIC)
        return img

    def write_screenshot(self, img_buffer, file_name) -> None:
        # Create folders.
        path = self.local_path
        path /= dt.datetime.now().strftime("%Y-%m/%d")
        path.mkdir(parents=True, exist_ok=True)

        with open(path / file_name, "wb") as f:
            f.write(img_buffer.getvalue())

    def post_screenshot(self, img_buffer, file_name) -> None:
        post_data = {}

        if self.remote_password:
            post_data["password"] = self.remote_password
        if self.remote_instance_id:
            post_data["instance"] = self.remote_instance_id

        post_files = {"screenshot": (file_name, img_buffer.getvalue(), "image/jpeg")}

        with requests.Session() as session:
            try:
                session.post(
                    self.remote_host,
                    data=post_data,
                    files=post_files,
                    timeout=self.network_timeout,
                )
            except requests.exceptions.RequestException:
                pass


def main() -> None:
    settings: dict
    with open("./config.yaml") as f:
        settings = yaml.safe_load(f)

    logger: Logger = Logger(settings or {})
    logger.log_screen()


if __name__ == "__main__":
    main()
