import sys
from subprocess import CalledProcessError, run

from importlib_resources import files

# Commands: install_brew_ec2, install_pip_ec2, install_codebuild


mount_efs_sh = str(files("pulumi_lambda_efs.bin").joinpath("mount_efs.sh"))
install_brew_sh = str(files("pulumi_lambda_efs.bin").joinpath("install_brew.sh"))
install_pip_sh = str(files("pulumi_lambda_efs.bin").joinpath("install_pip.sh"))


def main():
    if len(sys.argv) <= 1:
        print_usage()
        return

    if sys.argv[1] == "install_brew_azl":
        install_brew_azl()
    else:
        print_usage()


def install_brew_azl():
    if len(sys.argv) <= 2:
        print_usage()
        return

    filesystem_id = sys.argv[2]

    try:
        run(["sudo", "bash", mount_efs_sh, filesystem_id], check=True)
        run(["sudo", "bash", install_brew_sh, filesystem_id], check=True)
    except CalledProcessError:
        print("Command install_brew_azl failed.")


def install_pip_azl():
    if len(sys.argv) <= 2:
        print_usage()
        return

    filesystem_id = sys.argv[2]

    try:
        run(["sudo", "bash", mount_efs_sh, filesystem_id], check=True)
        run(["sudo", "bash", install_pip_sh, filesystem_id], check=True)
    except CalledProcessError:
        print("Command install_pip_azl failed.")


def print_usage():
    print("Usage:")
    print()
    print("  python -m pulumi_lambda_brew install_brew_azl [filesystem-id]")
    print("    Installs the Linuxbrew formulae specified in Brewfile to the EFS ")
    print("    dependencies directory, mounting it if necessary.  Designed to be ")
    print("    run on an Amazon Linux EC2 instance.")
    print()
    print("  python -m pulumi_lambda_brew install_pip_azl [filesystem-id]")
    print("    Installs the pip packages specified in requirements.txt to the EFS ")
    print("    dependencies directory, mounting it if necessary.  Designed to be ")
    print("    run on an Amazon Linux EC2 instance.")
    print()


if __name__ == "__main__":
    main()
