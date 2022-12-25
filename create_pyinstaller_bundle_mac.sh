#!/usr/bin/env bash
pyinstaller main_mac.spec --clean -y --distpath temp/dist --workpath temp/build
