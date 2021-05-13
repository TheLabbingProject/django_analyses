from pathlib import Path
from typing import List

import nibabel as nib
import pandas as pd
from nilearn.plotting import cm, view_img, view_surf

DEFAULT_NIFTI_SIZE = {"width": 1000, "height": 500}


def plot_nii(path: Path) -> str:
    html_doc = view_img(
        str(path), bg_img=False, cmap=cm.black_blue, symmetric_cmap=False,
    )
    return html_doc.get_iframe(**DEFAULT_NIFTI_SIZE)


def plot_mgz(path: Path) -> str:
    mgz = nib.load(path)
    data = mgz.get_fdata()
    nii = nib.Nifti1Image(
        data, mgz.affine, mgz.header, mgz.extra, mgz.file_map
    )
    title = Path(path).name
    html_doc = view_img(
        nii,
        bg_img=False,
        cmap=cm.black_blue,
        symmetric_cmap=False,
        title=title,
    )
    return html_doc.get_iframe(**DEFAULT_NIFTI_SIZE)


def plot_gii(path: Path) -> str:
    html_doc = view_surf(str(path), symmetric_cmap=False)
    return html_doc.get_iframe(**DEFAULT_NIFTI_SIZE)


FREESURFER_SURFACE_TITLES = {
    ".curv": "Curvature",
    ".sulc": "Sulcal Depth",
    ".annot": {
        (".BA_exvivo",): "Brodmann Regions",
        (".BA_exvivo", ".thresh"): "Thresholded Brodmann Regions",
        (".aparc", ".a2009s"): "Destrieux Regions",
        (".aparc", ".DKTatlas"): "Desikan-Killiany Regions",
        (".aparc",): "Desikan-Killiany Regions",
    },
}


FREESURFER_MESHES = (
    ".inflated",
    ".orig",
    ".pial",
    ".sphere",
    ".white",
)


def plot_freesurfer_surface(path: Path) -> str:
    suffix = path.suffix
    if suffix in FREESURFER_MESHES:
        return view_surf(str(path)).get_iframe(**DEFAULT_NIFTI_SIZE)
    default_title = suffix[1:].title()
    info = tuple(path.suffixes[:-1])
    hemisphere = "Left" if path.name.startswith("l") else "Right"
    description = FREESURFER_SURFACE_TITLES.get(suffix, default_title)
    if isinstance(description, dict):
        description = description.get(info, "".join(info))
    title = f"{hemisphere} Hemisphere {description}"
    mesh_key = ".orig" if suffix not in (".curv", ".sulc") else ".inflated"
    mesh = (
        str(path)
        .replace("".join(path.suffixes), mesh_key)
        .replace("label", "surf")
    )
    # if suffix == ".label":
    #     return view_img_on_surf(inflated, str(path), hemi=hemisphere.lower())

    symmetric_cmap = suffix not in (".thickness", ".curv")
    cmap = "YlOrRd" if suffix in (".thickness", ".curv") else cm.cold_hot
    return view_surf(
        mesh, str(path), title=title, symmetric_cmap=symmetric_cmap, cmap=cmap
    ).get_iframe(**DEFAULT_NIFTI_SIZE)


def read_col_headers(path: Path) -> List[str]:
    with open(path, "r") as f:
        for line in f:
            if "ColHeaders" in line:
                return line.strip().split()[2:]


def freesurfer_stats_repr(path: Path) -> str:
    try:
        column_names = read_col_headers(path)
        df = pd.read_csv(
            path,
            comment="#",
            delim_whitespace=True,
            names=column_names,
            index_col=0,
        )
    except Exception as e:
        return f"<br>Preview generation failed with the following exception:<br>{e}"
    else:
        return df.style.background_gradient()._repr_html_()


SUPPORTED_FILE_TYPES = {
    (".annot",): plot_freesurfer_surface,
    (".curv",): plot_freesurfer_surface,
    (".gii",): plot_gii,
    (".inflated",): plot_freesurfer_surface,
    # (".label",): plot_freesurfer_surface,
    (".mgz",): plot_mgz,
    (".nii",): plot_nii,
    (".nii", ".gz"): plot_nii,
    (".orig",): plot_freesurfer_surface,
    (".pial",): plot_freesurfer_surface,
    (".stats",): freesurfer_stats_repr,
    (".sphere",): plot_freesurfer_surface,
    (".sulc",): plot_freesurfer_surface,
    (".thickness",): plot_freesurfer_surface,
    (".white",): plot_freesurfer_surface,
}


def html_repr(path: Path) -> str:
    suffix = tuple(Path(path).suffixes)
    match = None
    if suffix in SUPPORTED_FILE_TYPES:
        match = suffix
    else:
        for key in SUPPORTED_FILE_TYPES:
            key_len = len(key)
            if suffix[-key_len:] == key:
                match = key
                break
    if match is not None:
        return SUPPORTED_FILE_TYPES[match](path)
