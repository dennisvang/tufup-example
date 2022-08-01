# TUF-Updater (tufup) example application

This repository shows how to use the [tufup][1] package for automated application updates.
This is done by means of a dummy application `myapp` that uses `tufup` in combination with `pyinstaller`. 

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
2. run `create_pyinstaller_bundle.bat` (note that our `main.spec` ensures that the latest `root.json` metadata file is included in the bundle)
3. run `repo_add_bundle.py` (CLI: `tufup targets add 1.0 temp/dist temp/keystore`)
4. modify the app, and/or increment `APP_VERSION` in `myapp/settings.py`
5. run `create_pyinstaller_bundle.bat` again
6. run `repo_add_bundle.py` again (CLI: `tufup targets add 2.0 temp/dist temp/keystore`)

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

1. manually extract the archive version 1.0 from the `repository/targets` dir into the `INSTALL_DIR` specified in `myapp/settings.py`, e.g. using `tar -xf my_app-1.0.tar.gz` on the command line (this simulates an installation on a client device)
2. [optional] to try a patch update, copy the archive version 1.0 into the `TARGET_DIR` (this would normally be done by an installer)
3. assuming the repo files are being served on localhost, we can now run the newly extracted executable from `INSTALL_DIR` (`main.exe`), and it will perform an update
4. metadata and targets are stored in the `UPDATE_CACHE_DIR`

### Troubleshooting

When playing around with this example-app, it is easy to wind up in an inconsistent state, e.g. due to stale metadata files.
This may result in tuf role verification errors, for example.
If this is the case, it is often easiest to start from a clean slate for both repo and client:

1. for the client-side, remove `UPDATE_CACHE_DIR` and `INSTALL_DIR`
2. for the repo-side, remove `DEV_DIR` (i.e. the `temp` dir described above)
3. follow the steps above for both repo-side and client-side

[1]: https://github.com/dennisvang/tufup
[2]: https://theupdateframework.io/
[3]: https://pyinstaller.org/en/stable/
