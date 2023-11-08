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
from pathlib import Path
from fastapi import APIRouter
from fastapi.responses import FileResponse
from aiconsole import projects
from aiconsole.utils.resource_to_path import resource_to_path

router = APIRouter()

log = logging.getLogger(__name__)


@router.get("/profile/{image}")
async def profile_image(image: str):
    image_path = Path(projects.get_project_agents().user_directory) / image

    if image_path.exists():
        return FileResponse(str(image_path))

    static_path = resource_to_path(projects.get_project_agents().core_resource) / image
    if static_path.exists():
        return FileResponse(str(static_path))

    default_path = resource_to_path(projects.get_project_agents().core_resource) / 'default.jpg'
    return FileResponse(str(default_path))
