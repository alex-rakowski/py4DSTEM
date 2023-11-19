import os
import warnings
from itertools import chain

import gdown
import requests
from emdfile import tqdmnd


def check_links(file_ids: dict[str, tuple[str, str]], verbose: bool = True) -> None:
    """
    Checks the validity of Google Drive links provided in a dictionary.

    Args:
        file_ids (dict[str, tuple[str, str]]): A dictionary of file IDs and their corresponding filenames and links.
        verbose (bool, optional): Whether to print verbose output. Defaults to True.

    Returns:
        None
    """
    # we store the UUID or whatnot string we need to covert to URL link
    gdrive_string_prefix = r"https://drive.google.com/file/d/"
    gdrive_string_sufix = r"/view"
    # loop over the dict items
    # could maybe a progress bar

    for key, (filename, link) in tqdmnd(
        file_ids.items(),
        desc="Checking Download Links",
        unit="Link",
        unit_scale=True,
        disable=not verbose,
    ):
        # create the URL
        check_link = f"{gdrive_string_prefix}{link}{gdrive_string_sufix}"
        # option to print to something to show progress
        # if verbose:
        #     print(f"checking {filename = } : {check_link = }")
        # get the header for the link
        resp = requests.head(check_link)
        # valid response is 200, raise warning if anything else
        if resp.status_code != 200:
            warnings.warn(
                f"Invalid link found for: {(key, filename, link, check_link)}",
                stacklevel=2,
            )
    return None


### File IDs

# single files
file_ids = {
    "sample_diffraction_pattern": (
        "a_diffraction_pattern.h5",
        "1ymYMnuDC0KV6dqduxe2O1qafgSd0jjnU",
    ),
    "Au_sim": (
        "Au_sim.h5",
        "1PmbCYosA1eYydWmmZebvf6uon9k_5g_S",
    ),
    "carbon_nanotube": (
        "carbon_nanotube.h5",
        "1bHv3u61Cr-y_GkdWHrJGh1lw2VKmt3UM",
    ),
    "Si_SiGe_exp": (
        "Si_SiGe_exp.h5",
        "1fXNYSGpe6w6E9RBA-Ai_owZwoj3w8PNC",
    ),
    "Si_SiGe_probe": (
        "Si_SiGe_probe.h5",
        "141Tv0YF7c5a-MCrh3CkY_w4FgWtBih80",
    ),
    "Si_SiGe_EELS_strain": (
        "Si_SiGe_EELS_strain.h5",
        "1klkecq8IuEOYB-bXchO7RqOcgCl4bmDJ",
    ),
    "AuAgPd_wire": (
        "AuAgPd_wire.h5",
        "1OQYW0H6VELsmnLTcwicP88vo2V5E3Oyt",
    ),
    "AuAgPd_wire_probe": (
        "AuAgPd_wire_probe.h5",
        "17OduUKpxVBDumSK_VHtnc2XKkaFVN8kq",
    ),
    "polycrystal_2D_WS2": (
        "polycrystal_2D_WS2.h5",
        "1AWB3-UTPiTR9dgrEkNFD7EJYsKnbEy0y",
    ),
    "WS2cif": (
        "WS2.cif",
        "13zBl6aFExtsz_sew-L0-_ALYJfcgHKjo",
    ),
    "polymers": (
        "polymers.h5",
        "1lK-TAMXN1MpWG0Q3_4vss_uEZgW2_Xh7",
    ),
    "vac_probe": (
        "vac_probe.h5",
        "1QTcSKzZjHZd1fDimSI_q9_WsAU25NIXe",
    ),
    "small_dm3_3Dstack": ("small_dm3_3Dstack.dm3", "1B-xX3F65JcWzAg0v7f1aVwnawPIfb5_o"),
    "FCU-Net": (
        "filename.name",
        "1-KX0saEYfhZ9IJAOwabH38PCVtfXidJi",
    ),
    "small_datacube": (
        "small_datacube.dm4",
        # TODO - change this file to something smaller - ideally e.g. shape (4,8,256,256) ~= 4.2MB'
        "1QTcSKzZjHZd1fDimSI_q9_WsAU25NIXe",
    ),
    "legacy_v0.9": (
        "legacy_v0.9_simAuNanoplatelet_bin.h5",
        "1AIRwpcj87vK3ubLaKGj1UiYXZByD2lpu",
    ),
    "legacy_v0.13": ("legacy_v0.13.h5", "1VEqUy0Gthama7YAVkxwbjQwdciHpx8rA"),
    "legacy_v0.14": (
        "legacy_v0.14.h5",
        "1eOTEJrpHnNv9_DPrWgZ4-NTN21UbH4aR",
    ),
    "test_realslice_io": ("test_realslice_io.h5", "1siH80-eRJwG5R6AnU4vkoqGWByrrEz1y"),
    "test_arina_master": (
        "STO_STEM_bench_20us_master.h5",
        "1q_4IjFuWRkw5VM84NhxrNTdIq4563BOC",
    ),
    "test_arina_01": (
        "STO_STEM_bench_20us_data_000001.h5",
        "1_3Dbm22-hV58iffwK9x-3vqJUsEXZBFQ",
    ),
    "test_arina_02": (
        "STO_STEM_bench_20us_data_000002.h5",
        "1x29RzHLnCzP0qthLhA1kdlUQ09ENViR8",
    ),
    "test_arina_03": (
        "STO_STEM_bench_20us_data_000003.h5",
        "1qsbzdEVD8gt4DYKnpwjfoS_Mg4ggObAA",
    ),
    "test_arina_04": (
        "STO_STEM_bench_20us_data_000004.h5",
        "1Lcswld0Y9fNBk4-__C9iJbc854BuHq-h",
    ),
    "test_arina_05": (
        "STO_STEM_bench_20us_data_000005.h5",
        "13YTO2ABsTK5nObEr7RjOZYCV3sEk3gt9",
    ),
    "test_arina_06": (
        "STO_STEM_bench_20us_data_000006.h5",
        "1RywPXt6HRbCvjgjSuYFf60QHWlOPYXwy",
    ),
    "test_arina_07": (
        "STO_STEM_bench_20us_data_000007.h5",
        "1GRoBecCvAUeSIujzsPywv1vXKSIsNyoT",
    ),
    "test_arina_08": (
        "STO_STEM_bench_20us_data_000008.h5",
        "1sTFuuvgKbTjZz1lVUfkZbbTDTQmwqhuU",
    ),
    "test_arina_09": (
        "STO_STEM_bench_20us_data_000009.h5",
        "1JmBiMg16iMVfZ5wz8z_QqcNPVRym1Ezh",
    ),
    "test_arina_10": (
        "STO_STEM_bench_20us_data_000010.h5",
        "1_90xAfclNVwMWwQ-YKxNNwBbfR1nfHoB",
    ),
    "test_strain": (
        "downsample_Si_SiGe_analysis_braggdisks_cal.h5",
        "1bYgDdAlnWHyFmY-SwN3KVpMutWBI5MhP",
    ),
}

notebook_file_ids = {
    "vacuum_probe_20x20": (
        "vacuum_probe_20x20.dm4",
        "1QTcSKzZjHZd1fDimSI_q9_WsAU25NIXe",
    ),
    "sim_Au_data_all_binned": (
        "sim_Au_data_all_binned.h5",
        "1m-jfXnStFWq0jo_hPY-3OtYaO62wHP3A",
    ),
    "calibrationData_simulatedAuNanoplatelet_binned_v14": (
        "calibrationData_simulatedAuNanoplatelet_binned_v14.h5",
        "1BJ_1qWFlbaJuOlKe7TapLFbEbQ0S600U",
    ),
    "carbon_nanotube_data": (
        "carbon_nanotube_data.h5",
        "1bHv3u61Cr-y_GkdWHrJGh1lw2VKmt3UM",
    ),
    "ptycho_sim_01_data": (
        "ptycho_sim_01_data.h5",
        "1uyeQAQa4DaMwHqN9EHQFCMKAve0_Fgfz",
    ),
    "ptycho_sim_01_probe": (
        "ptycho_sim_01_probe.h5",
        "1xJgQoxhWMBbtknwRfqB_BkULvgiJe-c1",
    ),
    "dataset19_bin4": (
        "dataset19_bin4.h5",
        "1lK-TAMXN1MpWG0Q3_4vss_uEZgW2_Xh7",
    ),
    "polycrystal_2D_WS2": (
        "polycrystal_2D_WS2.h5",
        "1AWB3-UTPiTR9dgrEkNFD7EJYsKnbEy0y",
    ),
    "WS2": (
        "WS2.cif",
        "13zBl6aFExtsz_sew-L0-_ALYJfcgHKjo",
    ),
    "small_AuAgPd_wire_dataset_04": (
        "small_AuAgPd_wire_dataset_04.h5",
        "1OQYW0H6VELsmnLTcwicP88vo2V5E3Oyt",
    ),
    "downsampled_AuAgPd_wire_probe": (
        "downsampled_AuAgPd_wire_probe.h5",
        "17OduUKpxVBDumSK_VHtnc2XKkaFVN8kq",
    ),
    "ptycho_gold_data": (
        "ptycho_gold_data.h5",
        "1KYxE-RbPIXm7A_BCb0V85NnuOWGufHE1",
    ),
    "ptycho_gold_probe": (
        "ptycho_gold_probe.h5",
        "15AuJoEDeb8HXnUyhJqq7jNEfErKgPr7p",
    ),
    "ptycho_MoS2_bin2": (
        "ptycho_MoS2_bin2.h5",
        "1C3tXV5BXz0JXbmyu3wTu3NutuIYYsN8A",
    ),
    "ptycho_Si-110_18nm": (
        "ptycho_Si-110_18nm.h5",
        "19NiTlzHFN8CJFbgUKFahLIytwwqijQgp",
    ),
    "ptycho_Si-110_28nm": (
        "ptycho_Si-110_28nm.h5",
        "1-jE77b86TH-3ISr5615prRLQA-bBHWvY",
    ),
    "ptycho_Si-110_37nm": (
        "ptycho_Si-110_37nm.h5",
        "1z9MJUN4NakdkAJpKMgb5qlR9jLOmKP3s",
    ),
    "ptycho_STO-110_mixed-state": (
        "ptycho_STO-110_mixed-state.h5",
        "1q-bDqxiHCXsITxMxS7X63B1sQtbgMyL2",
    ),
    "double_walled_cnt_m90-p90_6deg": (
        "double_walled_cnt_m90-p90_6deg.h5",
        "1Zq0u9lw0MaIlZaANcfIq8eIX6qKb2ecH",
    ),
    "downsample_Si_SiGe_exp": (
        "downsample_Si_SiGe_exp.h5",
        "1fXNYSGpe6w6E9RBA-Ai_owZwoj3w8PNC",
    ),
    "downsample_Si_SiGe_probe": (
        "downsample_Si_SiGe_probe.h5",
        "141Tv0YF7c5a-MCrh3CkY_w4FgWtBih80",
    ),
    "Si_SiGe_EELS_strain": (
        "Si_SiGe_EELS_strain.mat",
        "1klkecq8IuEOYB-bXchO7RqOcgCl4bmDJ",
    ),
    "Particle_1_Stack_1_45x90_ss30nm_0p09s_spot8_alpha=0p48_bin2_cl-600mm_300kV_bin8": (
        "Particle_1_Stack_1_45x90_ss30nm_0p09s_spot8_alpha=0p48_bin2_cl-600mm_300kV_bin8.h5",
        "1uYB23czoa7U05CtHVx9zfiVQFjiPfJUy",
    ),
}
### update the file_ids dict ###
# best for single combo of dicts
# file_ids.update(notebook_file_ids)
# best for multiple combo of dicts
file_ids = dict(
    chain(file_ids.items(), notebook_file_ids.items())
)  # can't replace dict with {}
# collections of files
collection_ids = {
    "tutorials": (
        "Au_sim",
        "carbon_nanotube",
        "Si_SiGe_exp",
        "Si_SiGe_probe",
        "Si_SiGe_EELS_strain",
        "AuAgPd_wire",
        "AuAgPd_wire_probe",
        "polycrystal_2D_WS2",
        "WS2cif",
        "polymers",
        "vac_probe",
    ),
    "test_io": (
        "small_dm3_3Dstack",
        "vac_probe",
        "legacy_v0.9",
        "legacy_v0.13",
        "legacy_v0.14",
        "test_realslice_io",
    ),
    "test_arina": (
        "test_arina_master",
        "test_arina_01",
        "test_arina_02",
        "test_arina_03",
        "test_arina_04",
        "test_arina_05",
        "test_arina_06",
        "test_arina_07",
        "test_arina_08",
        "test_arina_09",
        "test_arina_10",
    ),
    "test_braggvectors": ("Au_sim",),
    "strain": ("test_strain",),
    "notebooks": tuple(notebook_file_ids.keys()),  # can't replace tuple with ()
}


def get_sample_file_ids():
    return {"files": file_ids.keys(), "collections": collection_ids.keys()}


### Downloader


def gdrive_download(
    id_,
    destination=None,
    overwrite=False,
    filename=None,
    verbose=True,
):
    """
    Downloads a file or collection of files from google drive.

    Parameters
    ----------
    id_ : str
        File ID for the desired file.  May be either a key from the list
        of files and collections of files accessible at get_sample_file_ids(),
        or a complete url, or the portions of a google drive link specifying
        it's google file ID, i.e. for the address
        https://drive.google.com/file/d/1bHv3u61Cr-y_GkdWHrJGh1lw2VKmt3UM/,
        the id string '1bHv3u61Cr-y_GkdWHrJGh1lw2VKmt3UM'.
    destination : None or str
        The location files are downloaded to. If a collection of files has been
        specified, creates a new directory at the specified destination and
        downloads the collection there.  If None, downloads to the current
        working directory. Otherwise must be a string or Path pointint to
        a valid location on the filesystem.
    overwrite : bool
        Turns overwrite protection on/off.
    filename : None or str
        Used only if `id_` is a url or gdrive id. In these cases, specifies
        the name of the output file.  If left as None, saves to
        'gdrivedownload.file'. If `id_` is a key from the sample file id list,
        this parameter is ignored.
    verbose : bool
        Toggles verbose output
    """
    # parse destination
    if destination is None:
        destination = os.getcwd()
    assert os.path.exists(
        destination
    ), f"`destination` must exist on filesystem. Received {destination}"

    # download single files
    if id_ not in collection_ids:
        # assign the name and id
        kwargs = {"fuzzy": True}
        if id_ in file_ids:
            f = file_ids[id_]
            filename = f[0]
            kwargs["id"] = f[1]

        # if its not in the list of files we expect

        # TODO simplify the logic here
        else:
            filename = "gdrivedownload.file" if filename is None else filename
            # check if its a url
            if id_.startswith("http"):
                # check the url is the correct format i.e. https://drive.google.com/uc?id=<id>
                # and not https://drive.google.com/file/d/<id>
                # if correct format
                if "uc?id=" in id_:
                    kwargs["url"] = id_
                # if incorrect format, strip the google ID from the URL
                # making http/https agnostic
                elif "drive.google.com/file/d/" in id_:
                    # warn the user the the url syntax was incorrect and this is making a guess
                    warnings.warn(
                        f"URL provided {id_} was not in the correct format https://drive.google.com/uc?id=<id>, attempting to interpret link and download the file. Most likely a URL with this format was provided https://drive.google.com/file/d/<id>"
                    )
                    # try stripping
                    stripped_id = id_.split("/")[-1]
                    # Currently the length of the google drive IDs appears to always be 33 characters
                    # check for length and warn if it appears malformed, if so raise warning and the ID it guessed
                    if len(stripped_id) != 33:
                        warnings.warn(
                            f"Guessed ID {stripped_id}: appears to be in the wrong length (not 33 characters), attempting download"
                        )
                    kwargs["id"] = stripped_id
            # if its just a Google Drive string
            else:
                kwargs["id"] = id_

        # download
        kwargs["output"] = os.path.join(destination, filename)
        if not (overwrite) and os.path.exists(kwargs["output"]):
            if verbose:
                print(f"A file already exists at {kwargs['output']}, skipping...")
        else:
            gdown.download(**kwargs)

    # download a collections of files
    else:
        # set destination
        destination = os.path.join(destination, id_)
        if not os.path.exists(destination):
            os.mkdir(destination)

        # loop
        for x in collection_ids[id_]:
            file_name, file_id = file_ids[x]
            output = os.path.join(destination, file_name)
            # download
            if not (overwrite) and os.path.exists(output):
                if verbose:
                    print(f"A file already exists at {output}, skipping...")
            else:
                gdown.download(id=file_id, output=output, fuzzy=True)
