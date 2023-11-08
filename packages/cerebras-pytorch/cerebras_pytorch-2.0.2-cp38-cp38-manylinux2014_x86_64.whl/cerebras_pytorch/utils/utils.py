# Copyright 2016-2023 Cerebras Systems
# SPDX-License-Identifier: BSD-3-Clause

import os
import re
import socket

import torch


def is_true(value):
    if value is None:
        return False
    if isinstance(value, str):
        value = value.lower()
        if value in {"t", "true", "y", "yes"}:
            return True
        if value in {"f", "false", "n", "no"}:
            return False
        return bool(int(value))
    return not (not value)


def is_port_free(port):
    """Return True if the given port is open. False otherwise."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('', port))
            return True
        except socket.error:
            return False


def get_free_port():
    """Find a random free port on localhost and return the port number."""
    with socket.socket() as s:
        s.bind(('', 0))
        return s.getsockname()[1]


def extract_loss(model_outputs):
    if isinstance(model_outputs, torch.Tensor):
        loss = model_outputs
    elif isinstance(model_outputs, (list, tuple)) and len(model_outputs) > 0:
        loss = model_outputs[0]
    elif hasattr(model_outputs, "loss"):
        loss = model_outputs.loss
    else:
        raise TypeError(f"Invalid outputs type: {type(model_outputs)}")
    return loss


def snake_case_to_camel_case(name):
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


def to_hlo_name(name):
    """Given a name, returns a HLO compatible name:
    Replaces special characters with _"""
    return re.sub(r"[^\w.-]", "_", name, flags=re.ASCII)


def get_dir_size(path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if os.path.isfile(file_path):
                total_size += os.path.getsize(file_path)
    return total_size
