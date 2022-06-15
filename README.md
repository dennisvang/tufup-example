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

Starting from a clean repo, i.e. no `repository` folder is present.

1. run `repo_init.py` 
2. run `create_pyinstaller_bundle.bat` (note that our `main.spec` ensures that the latest `root.json` metadata file is included in the bundle)
3. run `repo_add_bundle.py`
4. modify the app, and increment `APP_VERSION` in `myapp/settings.py`
5. run `create_pyinstaller_bundle.bat` again
6. run `repo_add_bundle.py` again

Now we should have a `temp` dir (see `DEV_DIR` in `settings.py`) with the following structure:

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

1. manually extract the archive version 1.0 from the `repository/targets` dir into the `INSTALL_DIR` specified in `myapp/settings.py` (this simulates an installation on a client device)
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
