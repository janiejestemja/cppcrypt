from cx_Freeze import setup, Executable

executables = [Executable("runner.py", target_name="my_app.exe")]

build_exe_options = {
    "include_files": ["pyaes.cp313-win_amd64.pyd"]
    }

setup(
    name="MyApp",
    version="1.0",
    description="MyApp description",
    options={"build_exe": build_exe_options},
    executables=executables,
)
