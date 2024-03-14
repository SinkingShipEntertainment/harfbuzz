name = "harfbuzz"

authors = [
    "harfbuzz"
]

# NOTE: version = <external_version>.sse.<sse_version>
version = "8.2.1.sse.1.1.0"

description = """Text shaping engine"""

with scope("config") as c:
    import os
    c.release_packages_path = os.environ["SSE_REZ_REPO_RELEASE_EXT"]

requires = [
    "freetype",
    "libpng",
]

private_build_requires = [
]

variants = [
]

# If want to use Ninja, run:
# rez-build -i --cmake-build-system "ninja"
# rez-release --cmake-build-system "ninja"
#
# Pass cmake arguments (with debug symbols):
# rez-build -i --build-system cmake --bt Debug
# rez-release --build-system cmake --bt Debug

uuid = "repository.harfbuzz"

def pre_build_commands():

    info = {}
    with open("/etc/os-release", 'r') as f:
        for line in f.readlines():
            if line.startswith('#'):
                continue
            line_info = line.replace('\n', '').split('=')
            if len(line_info) != 2:
                continue
            info[line_info[0]] = line_info[1].replace('"', '')
    linux_distro = info.get("NAME", "centos")
    print("Using Linux distro: " + linux_distro)

    if linux_distro.lower().startswith("centos"):
        command("source /opt/rh/devtoolset-6/enable")
    elif linux_distro.lower().startswith("rocky"):
        pass

def commands():
    # NOTE: REZ package versions can have ".sse." to separate the external
    # version from the internal modification version.
    split_versions = str(version).split(".sse.")
    external_version = split_versions[0]
    internal_version = None
    if len(split_versions) == 2:
        internal_version = split_versions[1]

    env.HARFBUZZ_VERSION = external_version
    env.HARFBUZZ_PACKAGE_VERSION = external_version
    if internal_version:
        env.HARFBUZZ_PACKAGE_VERSION = internal_version

    env.HARFBUZZ_ROOT.append("{root}")
    env.HARFBUZZ_LOCATION.append("{root}")

    env.HARFBUZZ_INCLUDE_DIR = "{root}/include"
    env.HARFBUZZ_LIBRARY_DIR = "{root}/lib64"

    env.PATH.append("{root}/lib64")
    env.LD_LIBRARY_PATH.append("{root}/lib64")

    env.PKG_CONFIG_PATH.append("{root}/lib64/pkgconfig")
