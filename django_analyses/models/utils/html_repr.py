from pathlib import Path

from nilearn.plotting import cm, view_img

DEFAULT_NIFTI_SIZE = {"width": 1000, "height": 500}


def plot_nii(path: Path) -> str:
    html_doc = view_img(
        str(path), bg_img=False, cmap=cm.black_blue, symmetric_cmap=False,
    )
    return html_doc.get_iframe(**DEFAULT_NIFTI_SIZE)


SUPPORTED_FILE_TYPES = {(".nii",): plot_nii, (".nii", ".gz"): plot_nii}


def html_repr(path: Path) -> str:
    suffix = tuple(Path(path).suffixes)
    if suffix in SUPPORTED_FILE_TYPES:
        return SUPPORTED_FILE_TYPES[suffix](path)
