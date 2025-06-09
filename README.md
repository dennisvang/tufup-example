# Tufup (TUF-updater) example application 

This repository shows how to use the [tufup][1] package for automated application updates.

This is done by means of a dummy Windows-application, called `myapp`, that uses `tufup` in combination with `cx_Freeze`. 

Note: Although the example `myapp` is bundled using `cx_Freeze`, this is not required: `tufup` is completely independent of `cx_Freeze`, and can be used with *any* bundle of files.

Note: Although the example application is written for Windows (or macOS), this only pertains to the directories, defined in `settings.py`, and the script used to run `cx_Freeze`.
You can simply adapt these to use the example on other operating systems.

## Questions

If you have any questions, please make sure to check the [existing discussions][5] and [existing issues][6] first. (Also check [`tufup` discussions][10] and [`tufup` issues][11].)

New *questions* can be asked in the [Q&A][9] or on [stackoverflow][8], and *bugs* related to `tufup-example` can be reported [here][7].

## Setup

Create a virtualenv (or equivalent) and install requirements:

`pip install -r requirements.txt -r requirements-dev.txt --upgrade`

The project uses a `setup_env.py` script to ensure the `src` directory is in the Python path. This is automatically imported by the repository scripts.

## Getting started

For basic terminology, see documentation for [TUF (The Update Framework)][2].

We start out with a dummy application that has already integrated the `tufup.client`.
See `src/myapp/__init__.py` for details.

The dummy application is bundled using [cx_Freeze][3], but `tufup` works with any type of "application bundle" (i.e. just a directory with content representing the application).

The example includes a basic `setup.py` file that ensures the `tufup` root metadata file (`root.json`) is included in the application bundle.

The dummy *application* specifies where all `tufup`-related  files will be stored.
This is illustrated in `settings.py`. 

The following basic steps are covered:

1. Initialize a repository
2. Initial release   
   1. Build the application, including trusted root metadata from the repository
   2. Create an archive for the application and register it in the repo
3. Second release
   1. Build the new release
   2. Create an archive for the new release, create a patch, and register both in the repo
4. Serve the repository on a local test server
5. Run the "installed" application, so it can perform an automatic update

> For quick testing, these steps have been automated in the [PowerShell][12] script [`test_update_cycle.ps1`][13].

A detailed description of the steps, both for the repository-side and for the client-side, can be found in the following sections.

### Repo side

Some example scripts are provided for initializing a tufup repository and for adding new versions, see `repo_*.py`.

Alternatively, `tufup` offers a command line interface (CLI) for repository actions. 
Type `tufup -h` on the command line for more information. 

To set up the example tufup repository with both version 1.0 and 2.0, first create and activate a virtual environment:

```batch
python -m venv venv
venv\Scripts\activate
```

Then run:
```batch
setup_repo.bat
```

This script will automatically:
1. Install all required packages:
   - Install requirements from requirements.txt
   - Install development requirements from requirements-dev.txt
2. Initialize the repository
3. Create version 1.0:
   - Set version to 1.0
   - Build the MSI installer
   - Add the bundle to repository
4. Create version 2.0:
   - Set version to 2.0
   - Build the MSI installer
   - Add the bundle to repository
5. Start the HTTP server

Note: When adding a bundle, `tufup` creates a patch by default, which can take quite some time.
If you want to skip patch creation, either set `skip_patch=True` in the `Repository.add_bundle()` call, or add the  `-s` option to the CLI command: `tufup targets add -s 2.0 dist/tufup-example-2.0-win64.msi temp_my_app/keystore`.

Now we should have a `temp_my_app` dir with the following structure:

```text
temp_my_app
├ keystore
└ repository
  ├ metadata
  └ targets 
```

And in the project root, we'll have:
```text
.
├ dist
│ └ tufup-example-1.0-win64.msi
└ temp_my_app
  └ (repository files)
```

In the `targets` dir we find two MSI installers (1.0 and 2.0) and a corresponding patch file.

We can serve the repository on localhost as follows (relative to project root):

    python -m http.server -d temp_my_app/repository

That's it for the repo-side.

### Client side

On the same system (for convenience):

1. To simulate the initial installation on a client device, you can install the MSI package from the `dist` directory:
   - Double-click the MSI file to run the installer
   - Or use the command line: `msiexec /i dist/tufup-example-1.0-win64.msi`

2. [Optional] To try a patch update, copy the MSI version 1.0 into the `TARGET_DIR` (this would normally be done by an installer).
3. Assuming the repo files are being served on localhost, as described above, we can now run the installed application, and it will perform an update.
4. Metadata and targets are stored in the `UPDATE_CACHE_DIR`.

Note: The application will be installed in the default location (typically `C:\Program Files\my_app`). You may need administrator privileges to install the MSI package.