#!/usr/bin/env bash
pyinstaller main.spec --clean -y --distpath temp/dist --workpath temp/build
