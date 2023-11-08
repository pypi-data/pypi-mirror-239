# The AIConsole Project
# 
# Copyright 2023 10Clouds
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
# http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import os
from pathlib import Path
import tomlkit
from typing import Dict, List, Optional
import watchdog.events
import watchdog.observers
from aiconsole.materials.material import MaterialContentType, MaterialStatus, MaterialWithStatus
from aiconsole.materials.material import MaterialLocation, Material
from aiconsole.project_settings.project_settings import get_aiconsole_settings
from aiconsole.utils.BatchingWatchDogHandler import BatchingWatchDogHandler
from aiconsole.utils.list_files_in_file_system import list_files_in_file_system
from aiconsole.utils.list_files_in_resource_path import list_files_in_resource_path
from aiconsole.utils.resource_to_path import resource_to_path
from aiconsole.websockets.outgoing_messages import ErrorWSMessage, MaterialsUpdatedWSMessage, NotificationWSMessage
import rtoml

_log = logging.getLogger(__name__)


class Materials:
    """
    Materials' class is for managing the .md and .py material files.
    """

    _materials: Dict[str, Material]

    def __init__(self, core_resource: str, user_agents_directory: str):
        self.core_resource = core_resource
        self.user_directory = user_agents_directory
        self._materials = {}

        self.observer = watchdog.observers.Observer()

        os.makedirs(self.user_directory, exist_ok=True)
        self.observer.schedule(BatchingWatchDogHandler(self.reload),
                               self.user_directory,
                               recursive=True)
        self.observer.start()

    def stop(self):
        self.observer.stop()

    def all_materials(self) -> List[Material]:
        """
        Return all loaded materials.
        """
        return list(self._materials.values())

    def enabled_materials(self) -> List[Material]:
        """
        Return all enabled loaded materials.
        """
        settings = get_aiconsole_settings()
        return [
            material for material in self._materials.values() if
            settings.get_material_status(material.id) in [MaterialStatus.ENABLED]
        ]

    def forced_materials(self) -> List[Material]:
        """
        Return all forced loaded materials.
        """
        settings = get_aiconsole_settings()
        return [
            material for material in self._materials.values() if
            settings.get_material_status(material.id) in [MaterialStatus.FORCED]
        ]

    @property
    def materials_project_dir(self) -> Dict[str, Material]:
        """
        Return all forced loaded materials.
        """
        return {
            material.id: material
            for material in self._materials.values()
            if material.defined_in == MaterialLocation.PROJECT_DIR
        }

    @property
    def materials_aiconsole_core(self) -> Dict[str, Material]:
        """
        Return all forced loaded materials.
        """
        return {
            material.id: material
            for material in self._materials.values()
            if material.defined_in == MaterialLocation.AICONSOLE_CORE
        }

    def save_material(self, material: Material, new: bool, old_material_id: Optional[str] = None):
        if material.defined_in != MaterialLocation.PROJECT_DIR:
            raise Exception("Cannot save material not defined in project.")

        path = Path(self.user_directory)
        file_path = path / f"{material.id}.toml"

        if new and file_path.exists():
            raise Exception(f"Material {material.id} already exists.")

        if not new and not (path / f"{old_material_id}.toml").exists():
            raise Exception(f"Material {old_material_id} does not exist.")

        if not new and not file_path.exists():
            self.move(old_material_id, material.id)

        current_version = self.materials_project_dir.get(
            material.id,
            Material(
                id="unknown",
                version="0.0.1",
                name="",
                defined_in=MaterialLocation.PROJECT_DIR,
                usage="",
            )).version

        # Parse version number
        current_version = current_version.split(".")

        # Increment version number
        current_version[-1] = str(int(current_version[-1]) + 1)

        # Join version number
        material.version = ".".join(current_version)

        self._materials[material.id] = material


        # Save to .toml file
        with (path / f"{material.id}.toml").open("w") as file:
            # FIXME: preserve formatting and comments in the file using tomlkit

            # Ignore None values in model_dump
            model_dump = material.model_dump()
            for key in list(model_dump.keys()):
                if model_dump[key] is None:
                    del model_dump[key]

            def make_sure_starts_and_ends_with_newline(s: str):
                if not s.startswith('\n'):
                    s = '\n' + s

                if not s.endswith('\n'):
                    s = s + '\n'

                return s

            doc = tomlkit.document()
            doc.append("name", tomlkit.string(material.name))
            doc.append("version", tomlkit.string(material.version))
            doc.append("usage", tomlkit.string(material.usage))
            doc.append("content_type", tomlkit.string(material.content_type))

            {
                MaterialContentType.STATIC_TEXT:
                lambda: doc.append(
                    "content_static_text",
                    tomlkit.string(make_sure_starts_and_ends_with_newline(
                        material.content_static_text),
                                   multiline=True)),
                MaterialContentType.DYNAMIC_TEXT:
                lambda: doc.append(
                    "content_dynamic_text",
                    tomlkit.string(make_sure_starts_and_ends_with_newline(
                        material.content_dynamic_text),
                                   multiline=True)),
                MaterialContentType.API:
                lambda: doc.append(
                    "content_api",
                    tomlkit.string(make_sure_starts_and_ends_with_newline(
                        material.content_api),
                                   multiline=True)),
            }[material.content_type]()

            file.write(doc.as_string())

    def move(self, old_material_id: str, new_material_id: str) -> None:
        path = Path(self.user_directory)
        old_material_file_path = path / f"{old_material_id}.toml"
        new_material_file_path = path / f"{new_material_id}.toml"

        # Check if the old file exists
        if not old_material_file_path.exists():
            raise FileNotFoundError(f"'{old_material_id}' does not exist.")

        # Check if the new file already exists
        if new_material_file_path.exists():
            raise FileExistsError(f"'{new_material_id}' already exists.")

        # Move (rename) the file
        old_material_file_path.rename(new_material_file_path)

    async def load_material(self, material_id: str):
        """
        Load a specific material.
        """

        project_dir_path = Path(self.user_directory)
        core_resource_path = resource_to_path(self.core_resource)

        if (project_dir_path / f"{material_id}.toml").exists():
            # if material exists in core
            if (core_resource_path / f"{material_id}.toml").exists():
                await NotificationWSMessage(
                    title=f"Material {material_id} exists in core and project directory",
                    message="Project directory version will be used.",
                ).send_to_all()
            location = MaterialLocation.PROJECT_DIR
            path = project_dir_path / f"{material_id}.toml"
        elif (core_resource_path / f"{material_id}.toml").exists():
            location = MaterialLocation.AICONSOLE_CORE
            path = core_resource_path / f"{material_id}.toml"
        else:
            raise KeyError(f"Material {material_id} not found")

        with open(path, "r") as file:
            tomldoc = rtoml.loads(file.read())

        material_id = os.path.splitext(os.path.basename(path))[0]

        self._materials[material_id] = Material(
            id=material_id,
            version=str(tomldoc.get("version", "0.0.1")).strip(),
            name=str(tomldoc.get("name", material_id)).strip(),
            defined_in=location,
            usage=str(tomldoc["usage"]).strip(),
            content_type=MaterialContentType(
                str(tomldoc["content_type"]).strip()))

        if "content_static_text" in tomldoc:
            self._materials[material_id].content_static_text = \
                str(tomldoc["content_static_text"]).strip()

        if "content_dynamic_text" in tomldoc:
            self._materials[material_id].content_dynamic_text = \
                str(tomldoc["content_dynamic_text"]).strip()

        if "content_api" in tomldoc:
            self._materials[material_id].content_api = \
                str(tomldoc["content_api"]).strip()

    def get_material(self, name):
        """
        Get a specific material.
        """
        if name not in self._materials:
            raise KeyError(f"Material {name} not found")
        return self._materials[name]

    def delete_material(self, material_id):
        """
        Delete a specific material.
        """
        if material_id in self.materials_project_dir:
            material = self.materials_project_dir[material_id]

            path = {
                MaterialLocation.PROJECT_DIR: Path(self.user_directory),
            }[material.defined_in]

            material_file_path = path / f"{material_id}.toml"
            if material_file_path.exists():
                material_file_path.unlink()
                del self._materials[material_id]
                return

        raise KeyError(f"Material with ID {material_id} not found")

    async def reload(self):
        _log.info("Reloading materials ...")

        self._materials = {}

        material_ids = set([
            os.path.splitext(os.path.basename(path))[0]
            for paths_yielding_function in [
                list_files_in_resource_path(self.core_resource),
                list_files_in_file_system(self.user_directory),
            ] for path in paths_yielding_function
            if os.path.splitext(Path(path))[-1] == ".toml"
        ])

        for id in material_ids:
            try:
                await self.load_material(id)
            except Exception as e:
                await ErrorWSMessage(
                    error=f"Invalid material {id} {e}",
                ).send_to_all()
                continue

        await MaterialsUpdatedWSMessage(
            count=len(self._materials),
        ).send_to_all()
