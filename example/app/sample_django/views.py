import ctypes
import importlib
import os
import shutil
import subprocess
from ctypes.util import find_library

from django.http import HttpResponse


def welcome(request):
    output = "<h1>Django is working!</h1>"

    output += "<h2>Homebrew Formulae</h2>"
    output += try_libproj_import()
    output += try_libexif_import()

    output += "<h2>Pip Packages</h2>"
    output += try_python_import("os")
    output += try_python_import("numpy")
    output += try_python_import("pandas")
    output += try_python_import("scipy")
    output += try_python_import("sklearn")

    return HttpResponse(output)


def try_python_import(name):
    did_import = False

    try:
        mod = importlib.import_module(name)
        did_import = True
    except ImportError:
        print(f"Exception thrown when loading {name}")
        pass

    return f"<b>{name}</b>: {did_import}<br/>"


def try_libproj_import():
    """
    Simple test to call the `proj_area_create` function on the proj library.   If it
    returns a pointer, it is working.
    """
    proj_result = None
    
    try:
        projlib = ctypes.CDLL(find_library("proj"))
        proj_result = projlib.proj_area_create()
        print("Call proj_area_create result:", proj_result)
    except Exception:
        pass

    return f"<b>libproj:</b> {proj_result is not None}<br/>"


def try_libexif_import():
    """
    Simple test to call the `exif_content_new` function on the exif library.  If it
    returns a pointer, it is working.
    """
    exif_result = None

    try:
        exiflib = ctypes.CDLL(find_library("exif"))
        exif_result = exiflib.exif_content_new()
        print("Call exif_content_new result:", exif_result)
    except Exception:
        pass

    return f"<b>libexif:</b> {exif_result is not None}<br/>"


def print_debugging_info():

    # Debugging: check that the environment variables include the EFS libraries path
    print("EFS libraries: ", os.environ.get("LAMBDA_PACKAGES_PATH"))
    print("PATH=", os.environ.get("PATH"))
    print("LD_LIBRARY_PATH=", os.environ.get("LD_LIBRARY_PATH"))

    # Debugging: check that the tools required by ctypes are present
    print(
        subprocess.run(
            ["/sbin/ldconfig", "--version"],
            check=False,
            capture_output=True,
            encoding="utf-8",
        ).stdout
    )
    print(shutil.which("objdump"))
    print(shutil.which("ld"))

    # Debugging: Check that find_library can see the libraries
    print("find_library proj:", find_library("proj"))
    print("find_library exif:", find_library("exif"))