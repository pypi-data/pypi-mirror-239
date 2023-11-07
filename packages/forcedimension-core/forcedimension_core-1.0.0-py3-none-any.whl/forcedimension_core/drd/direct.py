from ctypes import c_byte, c_double, c_int

import forcedimension_core.runtime as _runtime
from forcedimension_core.typing import (
    SupportsPtr, SupportsPtrs3, c_int_ptr
)


def getPositionAndOrientation(
    p_out: SupportsPtrs3[c_double],
    o_out: SupportsPtrs3[c_double],
    pg_out: c_double,
    matrix_out: SupportsPtr[c_double],
    ID: int = -1,
) -> int:
    """
    Retrieve the position (in [m]) about the X, Y, and Z axes,
    the angle of each joint (in [rad]), (if applicable) the
    gripper  position (in [m]), and orientation frame matrix of
    the end-effector. Please refer to your device user manual
    for more information on your device coordinate system.

    Note
    ----
    Unlike
    :func:`forcedimension_core.dhd.getPositionAndOrientation()`,
    this function returns immediately. It loads from an internal
    buffer that is refreshed by the robotic control loop. For
    more information about regulation see :ref:`regulation`.


    :param SupportsPtrs3[ctypes.c_double] p_out:
        Output buffer to store the end-effector position (in
        [m]).

    :param SupportsPtrs3[ctypes.c_double] o_out:
        Output buffer to store the angle of each joint (in
        [rad]).

    :param ctypes.c_double pg_out:
        Output buffer to store the gripper opening gap (in [m]).

    :param MutableFloatMatrixLike matrix_out:
        Output buffer to store the orientation matrix.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for
        details)

    :raises AttributeError:
        If ``p_out.ptrs`` is not a valid attribute of ``p_out``

    :raises AttributeError:
        If ``o_out.ptrs`` is not a valid attribute of ``o_out``

    :raises AttributeError:
        If ``matrix_out.ptrs`` is not a valid attribute of
        ``matrix_out``

    :raises TypeError:
        If ``p_out.ptrs`` is not iterable.

    :raises TypeError:
        If ``o_out.ptrs`` is not iterable.

    :raises ctypes.ArgumentError:
        If ``p_out.ptrs`` does not expand into a tuple of 3
        ``Pointer[c_double]`` types.

    :raises ctypes.ArgumentError:
        If ``o_out.ptrs`` does not expand into a tuple of 3
        ``Pointer[c_double]`` types.

    :raises ctypes.ArgumentError:
        If ``matrix_out.ptr`` is not a Pointer[c_double] type

    :raises ctypes.ArgumentError:
        If ``pg_out`` is not a c_double type.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C int.

    :returns:
        0 or :data:`forcedimension_core.constants.TIMEGUARD`
        on success, -1 otherwise.

    See Also
    --------
    | :class:`forcedimension_core.containers.Vec3`
    | :class:`forcedimension_core.containers.Mat3x3`
    | :class:`forcedimension_core.containers.numpy.Vec3`
    | :class:`forcedimension_core.containers.numpy.Mat3x3`
    """

    return _runtime._libdrd.drdGetPositionAndOrientation(
        *p_out.ptrs, *o_out.ptrs, pg_out, matrix_out.ptr, ID
    )


def getVelocity(
    v_out: SupportsPtrs3[c_double],
    w_out: SupportsPtrs3[c_double],
    vg_out: c_double,
    ID: int = -1
) -> int:
    """
    Retrieve the linear velocity of the end-effector (in [m/s])
    as well as the angular velocity (in [rad/s]) about the X, Y,
    and Z axes. Please refer to your device user manual for more
    information on your device coordinate system.

    Note
    ----
    Unlike :func:`forcedimension_core.dhd.getLinearVelocity()`,
    :func:`forcedimension_core.dhd.getAngularVelocityRad()`, and
    :func:`forcedimension_core.dhd.getAngularVelocityDeg()` this
    function returns immediately. It loads from an internal
    buffer that is refreshed by the robotic control loop. For
    more information about regulation see :ref:`regulation`.


    :param int ID:
        Device ID (see :ref:`multiple_devices` section for
        details)

    :param SupportsPtrs3[ctypes.c_double] v_out:
        Output buffer for the linear velocity (in [m/s]).

    :param SupportsPtrs3[ctypes.c_double] w_out:
        Output buffer for the angular velocity (in [rad/s]).

    :param SupportsPtrs3[ctypes.c_double] vg_out:
        Output buffer for the gripper linear velocity (in [m/s]).

    :raises AttributeError:
        If ``v_out.ptrs`` is not a valid attribute of ``v_out``

    :raises AttributeError:
        If ``w_out.ptrs`` is not a valid attribute of ``w_out``

    :raises TypeError:
        If ``p_out.ptrs`` is not iterable.

    :raises TypeError:
        If ``o_out.ptrs`` is not iterable.

    :raises ctypes.ArgumentError:
        If ``p_out.ptrs`` does not expand into a tuple of 3
        ``Pointer[c_double]`` types.

    :raises ctypes.ArgumentError:
        If ``o_out.ptrs`` does not expand into a tuple of 3
        ``Pointer[c_double]`` types.

    :raises ctypes.ArgumentError:
        If ``pg_out`` is not a c_double type.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C int.

    :returns:
        0 on success and -1 otherwise.

    See Also
    --------
    | :class:`forcedimension_core.containers.Vec3`
    | :class:`forcedimension_core.containers.numpy.Vec3`
    """

    return _runtime._libdrd.drdGetVelocity(*v_out.ptrs, *w_out.ptrs, vg_out, ID)


def moveTo(pos: SupportsPtr[c_double], block: bool, ID: int = -1):
    """
    Send the robot end-effector to a desired Cartesian 7-DOF
    configuration. The motion uses smooth
    acceleration/deceleration. The acceleration and velocity
    profiles can be controlled by adjusting the trajectory
    generation parameters.

    Note
    ----
    The paths generated by this function are not guarunteed to
    be continuous if a command is interrupted by another call to
    this function while still in the process of being executed.
    If you want to guaruntee continuity use
    :func:`forcedimension_core.drd.track()`. For more information
    see :ref:`regulation`.


    :param SupportsPtr[ctypes.c_double] pos:
        Buffer of target positions/orientations for each DOF.
        DOFs 0-2 correspond to position about the X, Y, and Z
        axes (in [m]). DOFs 3-6 correspond to the target
        orientation about the first, second and third joints (in
        [rad]). DOF 7 corresponds to the gripper gap (in [m]).

    :param bool block:
        If ``True``, the call blocks until the destination is
        reached. If
        ``False``, the call returns immediately.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for
        details).

    :raises AttributeError:
        If ``pos.ptr`` is not a valid attribute of ``pos``

    :raises ctypes.ArgumentError:
        If ``pos.ptr`` is not a ``Pointer[c_double]`` type.

    :raises ctypes.ArgumentError:
        If ``ID`` is not convertible to a C char.'

    :returns:
        0 on success, and -1 otherwise.

    See Also
    --------
    | :class:`forcedimension_core.containers.DOFFloat`
    | :class:`forcedimension_core.containers.numpy.DOFFloat`
    | :func:`forcedimension_core.drd.moveToAllEnc()`

    """

    return _runtime._libdrd.drdMoveTo(pos.ptr, block, ID)


def moveToAllEnc(enc: SupportsPtr[c_int], block: bool, ID: int = -1):
    """
    Send the robot end-effector to a desired encoder position.
    The motion follows a straight line in the encoder space,
    with smooth acceleration/deceleration. The acceleration and
    velocity profiles can be controlled by adjusting the
    trajectory generation parameters.

    Note
    ----
    The paths generated by this function are not guarunteed to
    be continuous if a command is interrupted by another call to
    this function while still in the process of being executed.
    If you want to guaruntee continuity use
    :func:`forcedimension_core.drd.trackAllEnc()`.
    For more information see :ref:`regulation`.


    :param SupportsPtr[ctypes.c_int] enc:
        Target encoder positions.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for
        details).

    :param bool block:
        If ``True``, the call blocks until the destination is
        reached. If ``False``, the call returns immediately.

    :raises AttributeError:
        If ``enc.ptr`` is not a valid attribute of ``enc``

    :raises ValueError:
        If ``enc.ptr`` is not a ``Pointer[c_int]`` type.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to C char.

    :returns:
        0 on success, and -1 otherwise.

    See Also
    --------
    | :class:`forcedimension_core.containers.DOFInt`
    | :class:`forcedimension_core.containers.numpy.DOFInt`
    | :func:`forcedimension_core.drd.direct.moveTo()`
    """
    return _runtime._libdrd.drdMoveToAllEnc(enc.ptr, block, ID)


def track(pos: SupportsPtr[c_double], ID: int = -1):
    """
    Send the robot end-effector to a desired Cartesian 7-DOF
    configuration. If motion filters are enabled, the motion
    follows a smooth acceleration/deceleration. The acceleration
    and velocity profiles can be controlled by adjusting the
    trajectory generation parameters.


    Note
    ----
    For more information see :ref:`regulation`.


    :param SupportsPtr[ctypes.c_double] pos:
        Buffer of target positions/orientations for each DOF.
        DOFs 0-2 correspond to position about the X, Y, and Z
        axes (in [m]). DOFs 3-6 correspond to the target
        orientation about the first, second and third joints (in
        [rad]). DOF 7 corresponds to the gripper gap (in [m]).

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for
        details).

    :raises AttributeError:
        If ``pos.ptr`` is not a valid attribute of ``pos``.

    :raises ctypes.ArgumentError:
        If ``pos.ptr`` is not a ``Pointer[c_double]`` type.

    :raises ctypes.ArgumentError:
        If ``ID`` is not convertible to a C char.'

    :returns:
        0 on success, and -1 otherwise.

    See Also
    --------
    | :class:`forcedimension_core.containers.DOFFloat`
    | :class:`forcedimension_core.containers.numpy.DOFFloat`
    | :func:`forcedimension_core.drd.direct.trackAllEnc()`
    """

    return _runtime._libdrd.drdTrack(pos.ptr, ID)


_runtime._libdrd.drdTrackAllEnc.argtypes = [c_int_ptr, c_byte]
_runtime._libdrd.drdTrackAllEnc.restype = c_int


def trackAllEnc(enc: SupportsPtr[c_int], ID: int = -1):
    """
    Send the robot end-effector to a desired encoder position. If
    motion filters are enabled, th emotion follows a smooth
    acceleration/deceleration constraint on each encoder axis.
    The acceleration and velocity profiles can be controlled by
    adjusting the trajectory generation parameters.

    Note
    ----
    For more information see :ref:`regulation`.


    :param SupportsPtr[ctypes.c_int] enc:
        Target encoder positions.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details)

    :raises AttributeError:
        If ``enc.ptr`` is not a valid attribute of ``enc``

    :raises ctypes.ArgumentError:
        If ``enc.ptr`` is not a ``Pointer[c_int]`` type.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to C char.

    :returns:
        0 on success, and -1 otherwise.

    See Also
    --------
    | :class:`forcedimension_core.containers.DOFInt`
    | :class:`forcedimension_core.containers.numpy.DOFInt`
    | :func:`forcedimension_core.drd.direct.track()`
    """
    return _runtime._libdrd.drdTrackAllEnc(enc.ptr, ID)
