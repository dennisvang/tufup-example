## Getting started

This example simulates a complete update cycle, for a dummy application, using the `notsotuf` package.

We start out with a dummy application that has already integrated the `notsotuf.client`.

There is also a basic PyInstaller `.spec` file that ensures the `notsotuf` root metadata file (`root.json`) is included in the application bundles.

The application specifies where all `notsotuf`-related  files will be stored.
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

Starting from a clean repo, i.e. no `repo` folder is present.

1. run `init_repo.py` 
2. run `pyinstaller main.spec --clean -y`
3. run `add_target_to_repo.py`
4. modify the app, and increment `CURRENT_VERSION` in `settings.py`
5. run `pyinstaller main.spec --clean -y`
6. run `add_target_to_repo.py`

Now we should have a `repo` dir with `metadata` and `targets`.
In the `targets` dir we find two app archives (1.0 and 2.0) and a corresponding patch file.

We can serve the repository on localhost as follows:

    python -m http.server -d repo/deploy

That's it for the repo-side.

### Client side

On the same system (for convenience):

1. manually extract the archive version 1.0 from the `repo/deploy/targets` dir into the `INSTALL_DIR` specified in settings (this simulates an installation on a client device)
2. assuming the repo files are being served on localhost, we can now run the newly extracted executable (`main.exe`), and it will perform an update
3. metadata and targets are stored in the `UPDATE_CACHE_DIR` specified in `settings.py`

