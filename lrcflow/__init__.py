# Copyright (C) 2025 bpype.
#
# This file is part of lrcflow from bpype.
#
# lrcflow is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# deep_paint is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with deep_paint.  If not, see <http://www.gnu.org/licenses/>.
import importlib
from typing import List

from bpy.utils import register_class, unregister_class

bl_info = {
    "name": "lrcflow",
    "author": "bpype",
    "version": (0, 1, 0),
    "blender": (4, 2, 0),
    "location": "",
    "description": "LRC Workflow",
    "warning": "",
    "doc_url": "https://github.com/bpype/lrcflow",
    "category": "Pipeline",
}


modules = ()


#! REGISTRATION
def register_unregister_modules(modules: List, register: bool):
    """Recursively register or unregister modules by looking for either
    un/register() functions or lists named `classes` which should be a list of
    registerable classes.
    """
    register_func = register_class if register else unregister_class

    for m in modules:
        if register:
            importlib.reload(m)
        if hasattr(m, "classes"):
            for c in m.classes:
                try:
                    register_func(c)
                except Exception as e:
                    un = "un" if not register else ""
                    print(
                        f"Warning: Failed to {un}register class: {c.__name__}"
                    )
                    print(e)

        if hasattr(m, "modules"):
            register_unregister_modules(m.modules, register)

        if register and hasattr(m, "register"):
            m.register()
        elif hasattr(m, "unregister"):
            m.unregister()


def register():
    register_unregister_modules(modules, True)


def unregister():
    register_unregister_modules(modules, False)
