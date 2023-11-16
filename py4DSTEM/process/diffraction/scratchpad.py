import numpy as np

# define tiling function


def tile_atoms(
    uvw,
    pos,
    num,
    proj_dir=(0, 0, 1),
    proj_dir_cartesian=None,
    cell_size=(50, 50, 50),
):
    """
    Rotate and tile unit cell to fill a larger orthogonal cell. Imports N sites, tiles to M sites.

    Parameters
    ----------
    uvw: np.array
        (3,3) array where the rows are the (u,v,w) unit cell vectors (Angstroms).
    pos: np.array
        (N,3) array containing fractional atomic coordinates
    num: np.array
        (N, ) array containing atomic numbers.
    proj_dir: np.array
        (3, ) projection direction in terms of the u,v,w vectors.
    proj_dir_cartesian: np.array
        (3, ) projection direction in terms of (x,y,z) coordinates.
    cell_size:
        (3, ) cell size (Angstroms).

    Returns
    ----------
    xyz_tile: np.array
        (M,3) Atomic coordinates in Cartesian units (Angstroms).
    num_tile: np.array
        (M, ) Atomic numbers.

    """

    # projection vectors
    if proj_dir_cartesian is None:
        #         w_proj = uvw @ np.array(proj_dir).astype('float')
        #         w_proj = uvw @ np.array(proj_dir).astype('float')
        w_proj = (
            uvw[0, :] * proj_dir[0] + uvw[1, :] * proj_dir[1] + uvw[2, :] * proj_dir[2]
        )
    else:
        w_proj = np.array(proj_dir_cartesian).astype("float")
    w_proj /= np.linalg.norm(w_proj)
    if w_proj[0] < 1e-3:
        u_proj = np.array((1.0, 0, 0))
    else:
        u_proj = np.array((0, 1.0, 0))
    v_proj = np.cross(w_proj, u_proj)
    v_proj /= np.linalg.norm(v_proj)
    u_proj = np.cross(v_proj, w_proj)

    proj = np.linalg.inv(
        np.vstack(
            (
                u_proj,
                v_proj,
                w_proj,
            )
        )
    )
    uvw_proj = uvw @ proj

    # Determine tiling range
    pos_corner = np.array(
        (
            (0, 0, 0),
            (cell_size[0], 0, 0),
            (0, cell_size[1], 0),
            (cell_size[0], cell_size[1], 0),
            (0, 0, cell_size[2]),
            (cell_size[0], 0, cell_size[2]),
            (0, cell_size[1], cell_size[2]),
            (cell_size[0], cell_size[1], cell_size[2]),
        )
    )
    abc = pos_corner @ np.linalg.inv(uvw_proj)
    print(abc.round(2))
    a_range = (
        np.floor(np.min(abc[:, 0])).astype("int"),
        np.ceil(np.max(abc[:, 0])).astype("int"),
    )
    b_range = (
        np.floor(np.min(abc[:, 1])).astype("int"),
        np.ceil(np.max(abc[:, 1])).astype("int"),
    )
    c_range = (
        np.floor(np.min(abc[:, 2])).astype("int"),
        np.ceil(np.max(abc[:, 2])).astype("int"),
    )

    # Tiling indices
    a, b, c, ind = np.meshgrid(
        np.arange(a_range[0], a_range[1]),
        np.arange(b_range[0], b_range[1]),
        np.arange(c_range[0], c_range[1]),
        np.arange(pos.shape[0]),
        indexing="ij",
    )
    abc_ind_tile = np.vstack(
        (
            a.ravel(),
            b.ravel(),
            c.ravel(),
            ind.ravel(),
        )
    )

    # Cartesian coordinates
    abc_tile = abc_ind_tile[:3] + pos[abc_ind_tile[3, :], :].T
    xyz_tile = (
        abc_tile[0][:, None] * uvw_proj[0, :]
        + abc_tile[1][:, None] * uvw_proj[1, :]
        + abc_tile[2][:, None] * uvw_proj[2, :]
    )

    # Atomic identities
    num_tile = num[abc_ind_tile[3, :]]

    # delete atoms outsize of cell boundaries
    keep = np.logical_and.reduce(
        (
            xyz_tile[:, 0] >= 0.0,
            xyz_tile[:, 1] >= 0.0,
            xyz_tile[:, 2] >= 0.0,
            xyz_tile[:, 0] < cell_size[0],
            xyz_tile[:, 1] < cell_size[1],
            xyz_tile[:, 2] < cell_size[2],
        )
    )

    xyz_tile = xyz_tile[keep, :]
    num_tile = num_tile[keep]

    return xyz_tile, num_tile
