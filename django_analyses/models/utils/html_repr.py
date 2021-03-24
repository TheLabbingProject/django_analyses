from pathlib import Path

# from lxml import etree
# from django.apps import apps
# from django.urls import reverse
from nilearn.plotting import cm, view_img, view_surf

DEFAULT_NIFTI_SIZE = {"width": 1000, "height": 500}
# EMBEDDED_PDF = """
# <object data="{url}" type="application/pdf">
#   <embed src="{url}" type="application/pdf" />
# </object>
# """


# def xml_to_html(path: Path) -> str:
#     root = etree.parse(str(path)).getroot()
#     return etree.tostring(
#         root, encoding="unicode", method="text", pretty_print=True
#     )


def plot_nii(path: Path) -> str:
    html_doc = view_img(
        str(path), bg_img=False, cmap=cm.black_blue, symmetric_cmap=False,
    )
    return html_doc.get_iframe(**DEFAULT_NIFTI_SIZE)


def plot_gii(path: Path) -> str:
    html_doc = view_surf(str(path), symmetric_cmap=False)
    return html_doc.get_iframe(**DEFAULT_NIFTI_SIZE)


# def embed_pdf(path: Path) -> str:
#     FileOutput = apps.get_model("django_analyses", "FileOutput")
#     instance = FileOutput.objects.get(value=str(path))
#     url = reverse("analyses:file_output_download", args=(instance.id,))
#     return EMBEDDED_PDF.format(url=url)


SUPPORTED_FILE_TYPES = {
    (".nii",): plot_nii,
    (".nii", ".gz"): plot_nii,
    (".gii",): plot_gii,
    # (".xml",): xml_to_html,
    # (".pdf",): embed_pdf,
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
