import numpy as np
from math_tools.RK4 import RK4
from trajectory_planning.auxiliar_codes.pol_processor import *

# from trajectory_planning.auxiliar_codes.get_f1f2 import *
from trajectory_planning.auxiliar_codes.compute_omega import compute_omega_np
from trajectory_planning.auxiliar_codes.compute_omega_dot import compute_omega_dot_np
from trajectory_planning.auxiliar_codes.compute_omega_dot_dot import compute_omega_dot_dot_np


def fun_R(x, u):
    """Compute the derivative of the rotation matrix R.

    Args:
        x (list): List containing the variables of the system. The first 9 elements are the rotation matrix R,
            the next 3 elements are the angular velocity omega_world.

        u (control input): 0 since it's just the kinematic model.

    Returns:
        R_dot: Derivative of the rotation matrix R.
    """
    e1bx = x[0]
    e1by = x[1]
    e1bz = x[2]
    e2bx = x[3]
    e2by = x[4]
    e2bz = x[5]
    e3bx = x[6]
    e3by = x[7]
    e3bz = x[8]
    omega_world = x[9:12]

    R = np.array(
        [
            [e1bx, e2bx, e3bx],
            [e1by, e2by, e3by],
            [e1bz, e2bz, e3bz],
        ]
    )

    omega = R.T @ omega_world

    R_dot = R @ np.array(
        [
            [0, -omega[2], omega[1]],
            [omega[2], 0, -omega[0]],
            [-omega[1], omega[0], 0],
        ]
    )

    u_dot = np.array(
        [
            R_dot[0, 0],
            R_dot[1, 0],
            R_dot[2, 0],
            R_dot[0, 1],
            R_dot[1, 1],
            R_dot[2, 1],
            R_dot[0, 2],
            R_dot[1, 2],
            R_dot[2, 2],
            0,  # not interested, but needed to compute R_dot
            0,  # not interested, but needed to compute R_dot
            0,  # not interested, but needed to compute R_dot
        ]
    )

    return u_dot


def traj_post_processing(Px_coeffs, Py_coeffs, Pz_coeffs, t, env_params, rocket_params, controller_params):
    """This function computes the trajectory parameters for the 2D case using differential flatness.
        One shall mind that the polinomials are for the trajectory of the oscillation point, but the
        returned variables are converted for the center of gravity of the rocket.

    Args:
        Px_coeffs (list): List of coefficients for the x position.
        Py_coeffs (list): List of coefficients for the y position.
        Pz_coeffs (List): List of coefficients for the z position.
        t (list): List of time points.
        env_params (dict): Dictionary containing the environment parameters. Currently only g is used.
        rocket_params (dict): Dictionary containing the rocket parameters. Currently only m, l_tvc and J_z are used.
        controller_params (dict): List of controller parameters. Currently only dt is used.

    Returns:
        trajectory_params (dict): Dictionary containing the trajectory parameters.
            The variables were computed for the center of gravity of the rocket,
            but the polinomials are for the oscillation point.
    """

    print("Starting post-processing step...")
    g = env_params["g"]
    m = rocket_params["m"]
    l_tvc = rocket_params["l_tvc"]
    J = rocket_params["J"]
    dt = controller_params["dt"]
    x0 = controller_params["x0"]

    t_list = np.linspace(t[0], t[-1], int((t[-1] - t[0]) / dt) + 1, endpoint=True)

    x_o = np.zeros_like(t_list)
    y_o = np.zeros_like(t_list)
    z_o = np.zeros_like(t_list)
    vx_o = np.zeros_like(t_list)
    vy_o = np.zeros_like(t_list)
    vz_o = np.zeros_like(t_list)
    ax_o = np.zeros_like(t_list)
    ay_o = np.zeros_like(t_list)
    az_o = np.zeros_like(t_list)
    jx_o = np.zeros_like(t_list)
    jy_o = np.zeros_like(t_list)
    jz_o = np.zeros_like(t_list)
    sx_o = np.zeros_like(t_list)
    sy_o = np.zeros_like(t_list)
    sz_o = np.zeros_like(t_list)
    cx_o = np.zeros_like(t_list)
    cy_o = np.zeros_like(t_list)
    cz_o = np.zeros_like(t_list)
    f1 = np.zeros_like(t_list)
    f1_dot = np.zeros_like(t_list)

    for i in range(len(t) - 1):
        t0 = t[i]
        tf = t[i + 1]
        i0 = np.searchsorted(t_list, t0)
        i1 = np.searchsorted(t_list, tf, side="right")

        x_o[i0:i1] = pos_processor(Px_coeffs[:, i], [t[i], t[i + 1]], t_list[i0:i1])
        y_o[i0:i1] = pos_processor(Py_coeffs[:, i], [t[i], t[i + 1]], t_list[i0:i1])
        z_o[i0:i1] = pos_processor(Pz_coeffs[:, i], [t[i], t[i + 1]], t_list[i0:i1])

        vx_o[i0:i1] = vel_processor(Px_coeffs[:, i], [t[i], t[i + 1]], t_list[i0:i1])
        vy_o[i0:i1] = vel_processor(Py_coeffs[:, i], [t[i], t[i + 1]], t_list[i0:i1])
        vz_o[i0:i1] = vel_processor(Pz_coeffs[:, i], [t[i], t[i + 1]], t_list[i0:i1])

        ax_o[i0:i1] = acc_processor(Px_coeffs[:, i], [t[i], t[i + 1]], t_list[i0:i1])
        ay_o[i0:i1] = acc_processor(Py_coeffs[:, i], [t[i], t[i + 1]], t_list[i0:i1])
        az_o[i0:i1] = acc_processor(Pz_coeffs[:, i], [t[i], t[i + 1]], t_list[i0:i1])

        jx_o[i0:i1] = jerk_processor(Px_coeffs[:, i], [t[i], t[i + 1]], t_list[i0:i1])
        jy_o[i0:i1] = jerk_processor(Py_coeffs[:, i], [t[i], t[i + 1]], t_list[i0:i1])
        jz_o[i0:i1] = jerk_processor(Pz_coeffs[:, i], [t[i], t[i + 1]], t_list[i0:i1])

        sx_o[i0:i1] = snap_processor(Px_coeffs[:, i], [t[i], t[i + 1]], t_list[i0:i1])
        sy_o[i0:i1] = snap_processor(Py_coeffs[:, i], [t[i], t[i + 1]], t_list[i0:i1])
        sz_o[i0:i1] = snap_processor(Pz_coeffs[:, i], [t[i], t[i + 1]], t_list[i0:i1])

        cx_o[i0:i1] = crackle_processor(Px_coeffs[:, i], [t[i], t[i + 1]], t_list[i0:i1])
        cy_o[i0:i1] = crackle_processor(Py_coeffs[:, i], [t[i], t[i + 1]], t_list[i0:i1])
        cz_o[i0:i1] = crackle_processor(Pz_coeffs[:, i], [t[i], t[i + 1]], t_list[i0:i1])

    e3bx = np.zeros_like(t_list)
    e3by = np.zeros_like(t_list)
    e3bz = np.zeros_like(t_list)

    # estimate the trajectory parameters for the 3D case
    for i in range(len(t_list)):
        t = np.array([ax_o[i], ay_o[i], az_o[i] + g])
        temp = np.linalg.norm(t)

        e3bx[i] = t[0] / temp
        e3by[i] = t[1] / temp
        e3bz[i] = t[2] / temp

    omega_world = np.zeros((3, len(e3bx)))
    omega_dot_world = np.zeros((3, len(e3bx)))
    omega_dot_dot_world = np.zeros((3, len(e3bx)))

    for i in range(len(e3bx)):
        omega_world[:, i] = compute_omega_np(
            ax_o[i],
            ay_o[i],
            az_o[i],
            jx_o[i],
            jy_o[i],
            jz_o[i],
            g,
        )

        omega_dot_world[:, i] = compute_omega_dot_np(
            ax_o[i],
            ay_o[i],
            az_o[i],
            jx_o[i],
            jy_o[i],
            jz_o[i],
            sx_o[i],
            sy_o[i],
            sz_o[i],
            g,
        )

        omega_dot_dot_world[:, i] = compute_omega_dot_dot_np(
            ax_o[i],
            ay_o[i],
            az_o[i],
            jx_o[i],
            jy_o[i],
            jz_o[i],
            sx_o[i],
            sy_o[i],
            sz_o[i],
            cx_o[i],
            cy_o[i],
            cz_o[i],
            g,
        )

    e1bx = np.zeros_like(t_list)
    e1by = np.zeros_like(t_list)
    e1bz = np.zeros_like(t_list)
    e2bx = np.zeros_like(t_list)
    e2by = np.zeros_like(t_list)
    e2bz = np.zeros_like(t_list)

    # load initial state
    e1bx[0] = x0[6]
    e1by[0] = x0[7]
    e1bz[0] = x0[8]
    e2bx[0] = x0[9]
    e2by[0] = x0[10]
    e2bz[0] = x0[11]

    for i in range(len(t_list) - 1):
        x_var = np.array(
            [
                e1bx[i],
                e1by[i],
                e1bz[i],
                e2bx[i],
                e2by[i],
                e2bz[i],
                e3bx[i],
                e3by[i],
                e3bz[i],
                omega_world[0, i],
                omega_world[1, i],
                omega_world[2, i],
            ]
        )
        R_new = RK4(fun_R, x_var, None, dt)

        norm_e1b = np.sqrt(R_new[0] ** 2 + R_new[1] ** 2 + R_new[2] ** 2)
        norm_e2b = np.sqrt(R_new[3] ** 2 + R_new[4] ** 2 + R_new[5] ** 2)
        norm_e3b = np.sqrt(R_new[6] ** 2 + R_new[7] ** 2 + R_new[8] ** 2)
        e1bx[i + 1] = R_new[0] / norm_e1b
        e1by[i + 1] = R_new[1] / norm_e1b
        e1bz[i + 1] = R_new[2] / norm_e1b
        e2bx[i + 1] = R_new[3] / norm_e2b
        e2by[i + 1] = R_new[4] / norm_e2b
        e2bz[i + 1] = R_new[5] / norm_e2b
        e3bx[i + 1] = R_new[6] / norm_e3b
        e3by[i + 1] = R_new[7] / norm_e3b
        e3bz[i + 1] = R_new[8] / norm_e3b

    # compute the angular velocity and acceleration in body frame
    omega_body = np.zeros((3, len(e1bx)))
    omega_dot_body = np.zeros((3, len(e1bx)))
    omega_dot_dot_body = np.zeros((3, len(e1bx)))

    f1 = np.zeros_like(t_list)
    f2 = np.zeros_like(t_list)
    f3 = np.zeros_like(t_list)
    f = np.zeros_like(t_list)
    f1_dot = np.zeros_like(t_list)
    f2_dot = np.zeros_like(t_list)
    f3_dot = np.zeros_like(t_list)
    f_dot = np.zeros_like(t_list)

    x_g = np.zeros_like(t_list)
    y_g = np.zeros_like(t_list)
    z_g = np.zeros_like(t_list)
    vx_g = np.zeros_like(t_list)
    vy_g = np.zeros_like(t_list)
    vz_g = np.zeros_like(t_list)
    ax_g = np.zeros_like(t_list)
    ay_g = np.zeros_like(t_list)
    az_g = np.zeros_like(t_list)

    for i in range(len(e1bx)):
        # Build rotation matrix
        Ri = np.array(
            [
                [e1bx[i], e2bx[i], e3bx[i]],
                [e1by[i], e2by[i], e3by[i]],
                [e1bz[i], e2bz[i], e3bz[i]],
            ]
        )  # body to world

        # compute the angular velocity and acceleration in body frame
        omega_body[:, i] = Ri.T @ omega_world[:, i]
        omega_dot_body[:, i] = Ri.T @ omega_dot_world[:, i]
        omega_dot_dot_body[:, i] = Ri.T @ omega_dot_dot_world[:, i]

        # Compute the derivative of the rotation matrix
        Ri_dot = Ri @ np.array(
            [
                [0, -omega_body[2, i], omega_body[1, i]],
                [omega_body[2, i], 0, -omega_body[0, i]],
                [-omega_body[1, i], omega_body[0, i], 0],
            ]
        )

        # Compute state of the center of gravity
        r_go = Ri @ np.array([0, 0, J / (m * l_tvc)])

        x_g[i] = x_o[i] - r_go[0]
        y_g[i] = y_o[i] - r_go[1]
        z_g[i] = z_o[i] - r_go[2]

        temp = np.cross(omega_body[:, i], r_go)
        vx_g[i] = vx_o[i] - temp[0]
        vy_g[i] = vy_o[i] - temp[1]
        vz_g[i] = vz_o[i] - temp[2]

        temp = np.cross(omega_dot_body[:, i], r_go) + np.cross(omega_body[:, i], temp)
        ax_g[i] = ax_o[i] - temp[0]
        ay_g[i] = ay_o[i] - temp[1]
        az_g[i] = az_o[i] - temp[2]

        # compute the thrust force and the thrust force derivative
        e3b_t = np.array([e3bx[i], e3by[i], e3bz[i]])
        f1[i] = -J * omega_dot_body[1, i] / l_tvc
        f2[i] = J * omega_dot_body[0, i] / l_tvc
        f3[i] = m * e3b_t @ np.array([ax_o[i], ay_o[i], az_o[i] + g]).T + (J / l_tvc) * (
            omega_body[0, i] ** 2 + omega_body[1, i] ** 2
        )
        f[i] = np.sqrt(f1[i] ** 2 + f2[i] ** 2 + f3[i] ** 2)

        temp = m * Ri_dot.T @ np.array([ax_o[i], ay_o[i], az_o[i] + g]).T + m * Ri.T @ np.array(
            [jx_o[i], jy_o[i], jz_o[i]]
        )

        f1_dot[i] = -(J / l_tvc) * omega_dot_dot_body[1, i]
        f2_dot[i] = (J / l_tvc) * omega_dot_dot_body[0, i]
        f3_dot[i] = temp[2] + (J / l_tvc) * (
            2 * omega_body[0, i] * omega_dot_body[0, i] + 2 * omega_body[1, i] * omega_dot_body[1, i]
        )
        f_dot[i] = (f1[i] * f1_dot[i] + f2[i] * f2_dot[i] + f3[i] * f3_dot[i]) / f[i]

    trajectory_params = {
        "t": t_list,
        "x": x_g,
        "y": y_g,
        "z": z_g,
        "vx": vx_g,
        "vy": vy_g,
        "vz": vz_g,
        "ax": ax_g,
        "ay": ay_g,
        "az": az_g,
        "e1bx": e1bx,
        "e1by": e1by,
        "e1bz": e1bz,
        "e2bx": e2bx,
        "e2by": e2by,
        "e2bz": e2bz,
        "e3bx": e3bx,
        "e3by": e3by,
        "e3bz": e3bz,
        "f1": f1,
        "f2": f2,
        "f3": f3,
        "f1_dot": f1_dot,
        "f2_dot": f2_dot,
        "f3_dot": f3_dot,
        "f": f,
        "f_dot": f_dot,
        "omega": omega_body,
        "omega_dot": omega_dot_body,
    }

    print("Post-processing step done.")
    return trajectory_params
