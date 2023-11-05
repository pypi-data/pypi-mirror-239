from PyInstaller.utils.hooks import collect_data_files

from hpcflow.sdk import sdk_classes


# most of the modules in `sdk_classes` are imported on-demand via the app object:
hiddenimports = list(sdk_classes.values())

hiddenimports += [
    "hpcflow.sdk.data",
    "hpcflow.sdk.data.template_components",
    "hpcflow.sdk.demo.scripts",
    "hpcflow.sdk.demo.data",
    "hpcflow.sdk.demo.workflows",
    "hpcflow.sdk.core.test_utils",
    "click.testing",
]

datas = collect_data_files("hpcflow.sdk.data")
datas += collect_data_files("hpcflow.sdk.demo")
datas += collect_data_files("hpcflow.sdk.demo.data")
datas += collect_data_files("hpcflow.sdk.demo.workflows")
datas += collect_data_files("hpcflow.sdk.data.template_components")
datas += collect_data_files(
    "hpcflow.tests",
    include_py_files=True,
    excludes=("**/__pycache__",),
)
datas += collect_data_files(
    "hpcflow.sdk.demo.scripts",
    include_py_files=True,
    excludes=("**/__pycache__",),
)
