# Copyright 2022 The OFA-Sys Team. All rights reserved.
# This source code is licensed under the Apache 2.0 license
# found in the LICENSE file in the root directory.

import json
from dataclasses import dataclass, field
from typing import Dict, Optional

import torch

from ofasys.configure import register_config

from .base import BaseMetric, MetricConfig


@dataclass
class FMeasureConfig(MetricConfig):
    ans2label: Optional[str] = field(default=None, metadata={"help": 'json to map label string to 1 or 0'})
    f_measure_beta: Optional[float] = field(default=1.0, metadata={"help": 'a positive real facto'})


@register_config("ofasys.metric", "f_measure", FMeasureConfig)
class FMeasure(BaseMetric):
    def __init__(self, cfg: MetricConfig):
        super().__init__(cfg)
        if self.cfg.ans2label is not None:
            ans2label_dict = json.loads(self.cfg.ans2label)
            self.ans2label_dict = {k: int(v) for k, v in ans2label_dict.items()}
            assert list(sorted(self.ans2label_dict.values())) == [0, 1]
        self.beta = self.cfg.f_measure_beta

    def compute(self, hyps, refs) -> Dict:
        hyps = [self.ans2label_dict[v] for v in hyps]
        refs = [self.ans2label_dict[v] for v in refs]
        logging_output = {}
        assert len(hyps) == len(refs), (
            f'the length of hyps: {len(hyps)} ' f'must equal to the length of refs: {len(refs)}'
        )
        TP = sum([1.0 if r == 1 and h == 1 else 0.0 for r, h in zip(refs, hyps)])
        FP = sum([1.0 if r == 0 and h == 1 else 0.0 for r, h in zip(refs, hyps)])
        FN = sum([1.0 if r == 1 and h == 0 else 0.0 for r, h in zip(refs, hyps)])
        logging_output["_score_cnt"] = len(hyps)
        logging_output["_TP"] = TP
        logging_output["_FP"] = FP
        logging_output["_FN"] = FN
        return logging_output

    def report(self, logging_outputs: Dict) -> None:
        def sum_logs(key):
            result = sum(log.get(key, 0) for log in logging_outputs)
            if torch.is_tensor(result):
                result = result.cpu()
            return result

        if sum_logs("_score_cnt") > 0:
            # log counts as numpy arrays -- log_scalar will sum them correctly
            self.metrics.log_scalar("_sample_cnt", sum_logs("_score_cnt"))
            self.metrics.log_scalar("_TP", sum_logs("_TP"))
            self.metrics.log_scalar("_FP", sum_logs("_FP"))
            self.metrics.log_scalar("_FN", sum_logs("_FN"))

            def compute_f1(meters):
                TP = meters["_TP"].sum
                FP = meters["_FP"].sum
                FN = meters["_FN"].sum
                try:
                    score = (1 + self.beta**2) * TP / ((1 + self.beta**2) * TP + self.beta**2 * FN + FP)
                except ZeroDivisionError:
                    score = 0.0
                score = score if isinstance(score, float) else score.item()
                return round(score, 4)

            self.metrics.log_derived(f"f_{self.beta}", compute_f1)
