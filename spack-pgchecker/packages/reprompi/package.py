from spack.package import *


class Reprompi(CMakePackage):
    """ReproMPI benchmark suite with optional PGChecker support."""

    homepage = "https://github.com/hunsa/reprompi"
    git = "https://github.com/hunsa/reprompi.git"

    version("main", branch="main")

    variant("pgchecker", default=False, description="Enable PGChecker")
    variant("hwloc", default=False, description="Enable hwloc support")

    depends_on("mpi")
    depends_on("gsl")
    depends_on("cmake@3.24:", type="build")

    depends_on("hwloc", when="+hwloc")
    depends_on("pgchecker.pgmpitunelib", when="+pgchecker")

    def patch(self):
        filter_file(
            'INSTALL_RPATH "$<TARGET_FILE_DIR:MPITS::mpits>"',
            'INSTALL_RPATH "$ORIGIN/../lib;$<TARGET_FILE_DIR:MPITS::mpits>"',
            "CMakeLists.txt",
            string=True,
        )
        filter_file(
            'INSTALL_RPATH "${PGMPICLI_LIB_DIR};$<TARGET_FILE_DIR:MPITS::mpits>"',
            'INSTALL_RPATH "$ORIGIN/../lib;${PGMPICLI_LIB_DIR};$<TARGET_FILE_DIR:MPITS::mpits>"',
            "src/pgcheck/CMakeLists.txt",
            string=True,
        )

    def cmake_args(self):
        args = []

        args.append(self.define_from_variant("OPTION_ENABLE_PGCHECKER", "pgchecker"))

        if "+hwloc" in self.spec:
            args.append(self.define("HWLOC_LIBRARY_DEFAULT_PATH", self.spec["hwloc"].prefix))

        if "+pgchecker" in self.spec:
            args.append(
                self.define(
                    "PGTUNELIB_PATH",
                    self.spec["pgmpitunelib"].prefix,
                )
            )

        # Installed binaries should find libraries installed by ReproMPI itself.
        rpaths = ["$ORIGIN/../lib"]
        if "+pgchecker" in self.spec:
            rpaths.append(self.spec["pgmpitunelib"].prefix.lib)

        args.append(self.define("CMAKE_INSTALL_RPATH", ";".join(rpaths)))
        args.append(self.define("CMAKE_BUILD_WITH_INSTALL_RPATH", True))
        args.append(self.define("CMAKE_INSTALL_RPATH_USE_LINK_PATH", True))

        return args

    def setup_run_environment(self, env):
        env.prepend_path("LD_LIBRARY_PATH", self.prefix.lib)
        if "+pgchecker" in self.spec:
            env.prepend_path("LD_LIBRARY_PATH", self.spec["pgmpitunelib"].prefix.lib)
