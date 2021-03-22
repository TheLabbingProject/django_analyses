from pathlib import Path

from nilearn.plotting import view_img


def plot_nii(path: Path):
    return view_img(str(path))


SUPPORTED_FILE_TYPES = {(".nii",): plot_nii, (".nii", ".gz"): plot_nii}


def html_repr(path: Path) -> str:
    suffix = tuple(Path(path).suffixes)
    if suffix in SUPPORTED_FILE_TYPES:
        return SUPPORTED_FILE_TYPES[suffix](path)
