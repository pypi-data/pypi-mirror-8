from __future__ import absolute_import
from __future__ import unicode_literals

from git_code_debt.file_diff_stat import SpecialFileType
from git_code_debt.file_diff_stat import Status
from git_code_debt.metrics.base import DiffParserBase
from git_code_debt.metric import Metric


class SubmoduleCount(DiffParserBase):
    def get_metrics_from_stat(self, file_diff_stats):
        submodule_delta = 0

        for file_diff_stat in file_diff_stats:
            if (
                    file_diff_stat.special_file is not None and (
                        file_diff_stat.special_file.file_type is
                        SpecialFileType.SUBMODULE
                    )
            ):
                if file_diff_stat.status is Status.ADDED:
                    submodule_delta += 1
                elif file_diff_stat.status is Status.DELETED:
                    submodule_delta -= 1

        yield Metric(type(self).__name__, submodule_delta)

    def get_possible_metric_ids(self):
        return [type(self).__name__]
