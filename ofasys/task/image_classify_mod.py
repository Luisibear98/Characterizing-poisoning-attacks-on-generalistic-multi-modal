# Copyright 2022 The OFA-Sys Team. All rights reserved.
# This source code is licensed under the Apache 2.0 license
# found in the LICENSE file in the root directory.

from typing import Any, Dict
from ofasys.configure import register_config
from ofasys.task.base import OFATask, TaskConfig


@register_config("ofasys.task", "image_classify_mod", dataclass=TaskConfig)
class ImageClassifyTaskMod(OFATask):
    def preprocess(self, data: Dict[str, Any], split: str = "train") -> Dict[str, Any]:

        data['label'] = str(data["label"])
    
        return data
