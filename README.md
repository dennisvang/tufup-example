# Tufup (TUF-updater) example application 

This repository shows how to use the [tufup][1] package for automated application updates.

This is done by means of a dummy Windows-application, called `myapp`, that uses `tufup` in combination with `pyinstaller`. 

NOTE: Although the example `myapp` is bundled using `pyinstaller`, this is not required: `tufup` is completely independent of `pyinstaller`, and can be used with *any* bundle of files.

NOTE: Although the example application is written for Windows (or macOS), this only pertains to the directories, defined in `settings.py`, and the script used to run `pyinstaller`.
You can simply adapt these to use the example on other operating systems.

## Setup

Create a virtualenv (or equivalent) and install requirements:

`pip install -r requirements.txt -r requirements-dev.txt --upgrade`

## Getting started

For basic terminology, see documentation for [TUF (The Update Framework)][2].

We start out with a dummy application that has already integrated the `tufup.client`.
See `src/myapp/__init__.py` for details.

The dummy application is bundled using [PyInstaller][3], but `tufup` works with any type of "application bundle" (i.e. just a directory with content representing the application).

The example includes a basic PyInstaller `.spec` file that ensures the `tufup` root metadata file (`root.json`) is included in the application bundle.

The dummy *application* specifies where all `tufup`-related  files will be stored.
This is illustrated in `settings.py`. 

The following basic steps are covered:

1. initialize a repository
2. initial release   
   1. build the application, including trusted root metadata from the repository
   2. create an archive for the application and register it in the repo
3. second release
   1. build the new release
   2. create an archive for the new release, create a patch, and register both in the repo
4. serve the repository on a local test server
5. run the "installed" application, so it can perform an automatic update

### Repo side

Some example scripts are provided for initializing a tufup repository and for adding new versions, see `repo_*.py`.

Alternatively, `tufup` offers a command line interface (CLI) for repository actions. 
Type `tufup -h` on the command line for more information. 

Here's how to set up the example tufup repository, starting from a clean repo, i.e. no `temp` dir is present in the repo root (as defined by `DEV_DIR` in `settings.py`):

Note: If you use the CLI, see `repo_settings.py` for sensible values.

1. run `repo_init.py` (CLI: `tufup init`)
2. run `create_pyinstaller_bundle_win.bat` or `create_pyinstaller_bundle_mac.sh`
   (note that our `main.spec` ensures that the latest `root.json` metadata file is included in the bundle)
3. run `repo_add_bundle.py` (CLI: `tufup targets add 1.0 temp/dist/main temp/keystore`)
4. modify the app, and/or increment `APP_VERSION` in `myapp/settings.py`
5. run the `create_pyinstaller_bundle` script again
6. run `repo_add_bundle.py` again (CLI: `tufup targets add 2.0 temp/dist temp/keystore`)

Note: When adding a bundle, `tufup` creates a patch by default, which can take quite some time.
If you want to skip patch creation, either set `skip_patch=True` in the `Repository.add_bundle()` call, or add the  `-s` option to the CLI command: `tufup targets add -s 2.0 ...`.

Now we should have a `temp` dir with the following structure:

```text
temp
├ build
├ dist
├ keystore
└ repository
  ├ metadata
  └ targets 
```

In the `targets` dir we find two app archives (1.0 and 2.0) and a corresponding patch file.

We can serve the repository on localhost as follows (relative to project root):

    python -m http.server -d temp/repository

That's it for the repo-side.

### Client side

On the same system (for convenience):

1. To simulate the initial installation on a client device, we do a manual extraction of the archive version 1.0 from the `repository/targets` dir into the `INSTALL_DIR`, specified in `myapp/settings.py`. 

   #### On Windows:
   In the default example the `INSTALL_DIR` would be the `C:\users\<username>\AppData\Local\Programs\my_app` directory. 
   You can use `tar -xf my_app-1.0.tar.gz` in PowerShell to extract the bundle.

   #### On macOS:
   To install the bundle on macOS to the default location, you can use 
   `mkdir -p ~/Applications/my_app && tar -xf temp/repository/targets/my_app-1.0.tar.gz -C ~/Applications/my_app`.

2. [optional] To try a patch update, copy the archive version 1.0 into the `TARGET_DIR` (this would normally be done by an installer).
3. Assuming the repo files are being served on localhost, as described above, we can now run the newly extracted executable, `main.exe` or `main`, depending on platform, directly from the `INSTALL_DIR`, and it will perform an update.
4. Metadata and targets are stored in the `UPDATE_CACHE_DIR`.

BEWARE: The steps above refer to the `INSTALL_DIR` for the `FROZEN` state, typically `C:\users\<username>\AppData\Local\Programs\my_app` on Windows.
In development, when running the `myapp` example directly from source, i.e. `FROZEN=False`, the `INSTALL_DIR` is different from the actual install dir that would be used in production. See details in [settings.py][4]. 

### Troubleshooting

When playing around with this example-app, it is easy to wind up in an inconsistent state, e.g. due to stale metadata files.
This may result in tuf role verification errors, for example.
If this is the case, it is often easiest to start from a clean slate for both repo and client:

1. for the client-side, remove `UPDATE_CACHE_DIR` and `INSTALL_DIR`
2. for the repo-side, remove `DEV_DIR` (i.e. the `temp` dir described above)
3. remove `.tufup_repo_config`
4. follow the steps above to set up the repo-side and client-side

[1]: https://github.com/dennisvang/tufup
[2]: https://theupdateframework.io/
[3]: https://pyinstaller.org/en/stable/
[4]: https://github.com/dennisvang/tufup-example/blob/2af43175d39417f9d3d855d7e8fb2cb6ebd3c155/src/myapp/settings.py#L38
