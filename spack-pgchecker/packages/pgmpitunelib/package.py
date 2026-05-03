from spack.package import *


class Pgmpitunelib(CMakePackage):
    """PG MPI tune library used by ReproMPI PGChecker."""

    homepage = "https://github.com/hunsa/pgmpitunelib"
    git = "https://github.com/hunsa/pgmpitunelib.git"

    version("main", branch="main")
    version(
        "b7416e0",
        commit="b7416e03612e5c1826646965628cf46398a32845",
        preferred=True,
    )

    depends_on("cmake@3.24:", type="build")
    depends_on("mpi")

    variant("schedule_coll", default=False, description="Enable schedule collectives support")

    def cmake_args(self):
        args = []
        return args
