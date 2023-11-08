# Copyright 2016-2023 Cerebras Systems
# SPDX-License-Identifier: BSD-3-Clause

"""Utilities to simplify run.py usage"""
from typing import List, Optional

import yaml
from google.protobuf import text_format

from cerebras_appliance.pb.workflow.appliance.common.common_config_pb2 import (
    DebugArgs,
)
from cerebras_appliance.pb.ws.internal_precisions_table_pb2 import (
    InternalPrecision as Precision,
)
from cerebras_appliance.pb.ws.internal_precisions_table_pb2 import (
    InternalPrecisionsTable,
)
from cerebras_appliance.pb.ws.internal_precisions_table_pb2 import (
    InternalPrecisionType as DType,
)
from cerebras_appliance.pb.ws.internal_precisions_table_pb2 import KernelFlag


def get_supported_type_maps(debug_args):
    """Get the ini maps in the DebugArgs for supported types
    """
    ini_maps = {
        bool: debug_args.ini.bools,
        int: debug_args.ini.ints,
        float: debug_args.ini.floats,
        str: debug_args.ini.strings,
    }
    return ini_maps


def write_debug_args(debug_args: DebugArgs, path: str):
    """Appliance mode write debug args file"""
    with open(path, 'w') as f:
        text_format.PrintMessage(debug_args, f)


def get_debug_args(path: Optional[str]) -> DebugArgs:
    """Appliance mode load debug args and apply defaults"""
    debug_args = DebugArgs()
    if path:
        with open(path, 'r') as f:
            text_format.Parse(f.read(), debug_args)
    return debug_args


def set_ini(debug_args: DebugArgs, **kwargs):
    """Set an Debug INI in the DebugArgs"""
    ini_maps = get_supported_type_maps(debug_args)
    for k, v in kwargs.items():
        maps = ini_maps.get(type(v))
        if maps is None:
            raise TypeError(
                f"\"{k}\"={v} is of unsupported type {type(v)}. Only "
                f"{list(ini_maps.keys())} types are supported INI values."
            )
        maps[k] = v


def set_default_ini(debug_args: DebugArgs, **kwargs):
    """Set default INI in the DebugArgs, if INI is not set"""
    ini_maps = get_supported_type_maps(debug_args)

    for k, v in kwargs.items():
        maps = ini_maps.get(type(v))
        if maps is None:
            raise TypeError(
                f"\"{k}\"={v} is of unsupported type {type(v)}. Only "
                f"{list(ini_maps.keys())} types are supported INI values."
            )
        if k not in maps:
            maps[k] = v


def set_ini_from_file(debug_args: DebugArgs, ini_path: str):
    """Read a yaml file containing debug ini and update the given DebugArgs"""
    with open(ini_path, 'r') as f:
        ini = yaml.safe_load(f)
        if ini:
            set_ini(debug_args, **ini)


def set_precision_opt_level(
    debug_args: DebugArgs, precision_opt_level: Optional[int] = None
):
    """Sets the precision opt level in the debug args.
    Sets the precision table ini string for precision opt level 2.
    For precision opt level 0 and 1, the precision table proto is used
    to set the numeric config appropriately
    Args:
        debug_args: Debug args instance to inject the POL into.
        precision_opt_level: The POL to set. If None, this method is a no-op. Defaults to None.
    """
    if precision_opt_level is not None:
        if (
            precision_opt_level == 0
        ):  # Mixed precision (fp32 reductions; ops like matmul in fp16/bf16)
            # Setting global precision level
            numeric_config = InternalPrecisionsTable()
            numeric_config.global_flag.dtype = DType.T_F32

            debug_args.debug_crd.numeric_config.CopyFrom(numeric_config)
        elif (
            precision_opt_level == 1
        ):  # Hierarchical mixed precision (custom to CS2)
            numeric_config = InternalPrecisionsTable(
                kernel_flag=[
                    KernelFlag(
                        kernel_name="AAMatMul",
                        internal_precision=[
                            Precision(name="compute_dtype", dtype=DType.T_F32)
                        ],
                    ),
                    KernelFlag(
                        kernel_name="Attention",
                        internal_precision=[
                            Precision(
                                name="oprod_accum_dtype", dtype=DType.T_F32
                            )
                        ],
                    ),
                    KernelFlag(
                        kernel_name="DAttention",
                        internal_precision=[
                            Precision(
                                name="oprod_accum_dtype", dtype=DType.T_F32
                            )
                        ],
                    ),
                    KernelFlag(
                        kernel_name="DenseAttention",
                        internal_precision=[
                            Precision(
                                name="oprod_accum_dtype", dtype=DType.T_F32
                            )
                        ],
                    ),
                    KernelFlag(
                        kernel_name="DenseDAttention",
                        internal_precision=[
                            Precision(
                                name="oprod_accum_dtype", dtype=DType.T_F32
                            )
                        ],
                    ),
                    KernelFlag(
                        kernel_name="Conv",
                        internal_precision=[
                            Precision(name="reduction_prec", dtype=DType.T_F16)
                        ],
                    ),
                    KernelFlag(
                        kernel_name="DConv",
                        internal_precision=[
                            Precision(name="reduction_prec", dtype=DType.T_F16)
                        ],
                    ),
                    KernelFlag(
                        kernel_name="DLayernorm",
                        internal_precision=[
                            Precision(
                                name="dbias_reduction_dtype", dtype=DType.T_F32,
                            ),
                            Precision(
                                name="dgamma_reduction_dtype",
                                dtype=DType.T_F32,
                            ),
                            Precision(name="compute_dtype", dtype=DType.T_F32),
                        ],
                    ),
                    KernelFlag(
                        kernel_name="DMatMul",
                        bf16_hier_accum_len=32,
                        internal_precision=[
                            Precision(
                                name="dot_product_dtype", dtype=DType.T_F16
                            )
                        ],
                    ),
                    KernelFlag(
                        kernel_name="DRelu",
                        internal_precision=[
                            Precision(name="compute_dtype", dtype=DType.T_F32)
                        ],
                    ),
                    KernelFlag(
                        kernel_name="Layernorm",
                        internal_precision=[
                            Precision(name="compute_dtype", dtype=DType.T_F32)
                        ],
                    ),
                    KernelFlag(
                        kernel_name="MatMul",
                        bf16_hier_accum_len=12,
                        internal_precision=[
                            Precision(name="reduce_dtype", dtype=DType.T_F16),
                            Precision(
                                name="inter_pe_reduce_dtype", dtype=DType.T_F32,
                            ),
                        ],
                    ),
                    KernelFlag(
                        kernel_name="Relu",
                        internal_precision=[
                            Precision(name="compute_dtype", dtype=DType.T_F32)
                        ],
                    ),
                    KernelFlag(
                        kernel_name="SoftmaxSum",
                        internal_precision=[
                            Precision(name="compute_dtype", dtype=DType.T_F32)
                        ],
                    ),
                ]
            )

            debug_args.debug_crd.numeric_config.CopyFrom(numeric_config)

        elif (
            precision_opt_level == 2
        ):  # Hierarchical mixed precision + ini's tuned for performance
            numeric_config = InternalPrecisionsTable(
                kernel_flag=[
                    KernelFlag(
                        kernel_name="MatMul",
                        internal_precision=[
                            Precision(
                                name="inter_pe_reduce_dtype", dtype=DType.T_F16,
                            ),
                        ],
                    ),
                    KernelFlag(
                        kernel_name="AAMatMul",
                        internal_precision=[
                            Precision(name="compute_dtype", dtype=DType.T_F16)
                        ],
                    ),
                    KernelFlag(
                        kernel_name="Attention",
                        internal_precision=[
                            Precision(
                                name="oprod_accum_dtype", dtype=DType.T_F16
                            )
                        ],
                    ),
                    KernelFlag(
                        kernel_name="DAttention",
                        internal_precision=[
                            Precision(
                                name="oprod_accum_dtype", dtype=DType.T_F16
                            )
                        ],
                    ),
                    KernelFlag(
                        kernel_name="DenseAttention",
                        internal_precision=[
                            Precision(
                                name="oprod_accum_dtype", dtype=DType.T_F16
                            )
                        ],
                    ),
                    KernelFlag(
                        kernel_name="DenseDAttention",
                        internal_precision=[
                            Precision(
                                name="oprod_accum_dtype", dtype=DType.T_F16
                            )
                        ],
                    ),
                    KernelFlag(
                        kernel_name="DRelu",
                        internal_precision=[
                            Precision(name="compute_dtype", dtype=DType.T_F16)
                        ],
                    ),
                    KernelFlag(
                        kernel_name="Relu",
                        internal_precision=[
                            Precision(name="compute_dtype", dtype=DType.T_F16)
                        ],
                    ),
                    KernelFlag(
                        kernel_name="SoftmaxSum",
                        internal_precision=[
                            Precision(name="compute_dtype", dtype=DType.T_F32)
                        ],
                    ),
                ]
            )
            debug_args.debug_crd.numeric_config.CopyFrom(numeric_config)

            set_ini(
                debug_args, ws_dattn_batched_col_reduce=True,
            )
        else:
            raise ValueError(
                "Unsupported precision optimization level specified. "
                "Please provide a precision_opt_level of 0, 1 or 2"
            )


def update_debug_args_with_job_labels(
    debug_args: DebugArgs, job_labels: Optional[List[str]] = None
):
    """Update debug args with job labels"""
    if not job_labels:
        return

    for label in job_labels:
        tokens = label.split("=")
        label_key = tokens[0]
        label_val = tokens[1]
        debug_args.debug_mgr.labels[label_key] = label_val


def update_debug_args_with_autogen_policy(
    debug_args: DebugArgs, autogen_policy: Optional[str] = None
):
    """Update debug args with autogen policy"""
    if not autogen_policy:
        return

    policy_map = {
        "default": DebugArgs.DebugCRD.AutogenPolicy.DEFAULT,
        "disabled": DebugArgs.DebugCRD.AutogenPolicy.DISABLED,
        "medium": DebugArgs.DebugCRD.AutogenPolicy.MEDIUM,
        "aggressive": DebugArgs.DebugCRD.AutogenPolicy.AGGRESSIVE,
    }

    if autogen_policy in policy_map:
        debug_args.debug_crd.autogen_policy = policy_map[autogen_policy]
    else:
        raise ValueError(
            f"'{autogen_policy}' is an invalid autogen policy. Valid values "
            f"are {policy_map.keys()}."
        )
