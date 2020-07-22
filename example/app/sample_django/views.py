import ctypes
import os
import shutil
import subprocess
from ctypes.util import find_library

from django.http import HttpResponse


def welcome(request):

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

    # Simple test to call the `proj_area_create` function on the proj library and the
    # `exif_content_new` function on the exif library.  If they return a pointer,
    # they are working.

    proj_result = None
    exif_result = None

    try:
        projlib = ctypes.CDLL(find_library("proj"))
        proj_result = projlib.proj_area_create()
        print("Call proj_area_create result:", proj_result)
    except Exception:
        pass

    try:
        exiflib = ctypes.CDLL(find_library("exif"))
        exif_result = exiflib.exif_content_new()
        print("Call exif_content_new result:", exif_result)
    except Exception:
        pass

    return HttpResponse(
        f"""
<b>Django is working!</b><br/>
<h1>Homebrew Formulae</h1>
<b>libproj:</b> {proj_result is not None}<br/>
<b>libexif:</b> {exif_result is not None}<br/>
"""
    )
