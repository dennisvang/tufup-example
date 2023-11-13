#!/usr/bin/env bash
pyinstaller main.spec --clean -y --distpath temp_my_app/dist --workpath temp_my_app/build
