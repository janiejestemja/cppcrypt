from cx_Freeze import setup, Executable

executables = [Executable("runner.py", target_name="my_app.exe")]

setup(
    name="MyApp",
    version="1.0",
    description="MyApp description",
    executables=executables,
)
