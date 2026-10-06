"""Regression checks for stopping too early; fixtures do not model aesthetics."""
from copy import deepcopy
import tempfile
from pathlib import Path
import unittest
from creative_review import digest, validate


class ReviewDecisionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name).resolve()
        (self.project / 'film.mp4').write_bytes(b'artifact-version-one')
        (self.project / 'evidence.md').write_text('Review evidence fixture', encoding='utf8')
        self.evidence = dict(kind='visual', file='evidence.md', description='关键姿态和负空间观察')
        self.record = dict(schema_version=1, scope='full', objective='动作展示片',
                           quality_targets=['主体运动具有可辨认的性格'],
                           artifact={'file': 'film.mp4', 'sha256': digest(self.project / 'film.mp4')},
                           observations=[dict(at='全片', finding='主要动作的关键姿态与目标相符', evidence=self.evidence)],
                           issues=[], iterations=[],
                           decision=dict(action='deliver', rationale='主要目标有对应观察，没有已知关键问题', limits=[]))

    def test_technical_checks_cannot_replace_creative_review(self):
        record = deepcopy(self.record)
        record['observations'][0]['evidence']['kind'] = 'technical'
        self.assertTrue(any('仅有技术证据' in x for x in validate(record, self.project)))

    def test_major_open_issue_blocks_even_limited_delivery(self):
        record = deepcopy(self.record)
        record['issues'] = [dict(at='2秒', problem='关键动作未出现', impact='major', status='open')]
        record['decision'] = dict(action='deliver_with_limits', rationale='已有部分效果',
                                 limits=[dict(description='没有听觉证据', basis='当前观察工具不提供听觉', evidence=self.evidence)])
        self.assertTrue(any('未处理的关键问题' in x for x in validate(record, self.project)))

    def test_new_artifact_invalidates_old_review(self):
        (self.project / 'film.mp4').write_bytes(b'artifact-version-two')
        self.assertTrue(any('成片已变化' in x for x in validate(self.record, self.project)))

    def test_pending_candidate_blocks_delivery(self):
        record = deepcopy(self.record)
        record['iterations'] = [dict(hypothesis='更换姿态会改善重量感', baseline=record['artifact'],
                                     candidate=record['artifact'], outcome='pending', reason='尚未比较', evidence=self.evidence)]
        self.assertTrue(any('未完成对照判断' in x for x in validate(record, self.project)))

    def test_scope_cannot_hide_major_issue_without_user_basis(self):
        record = deepcopy(self.record)
        record['issues'] = [dict(at='2秒', problem='关键动作未出现', impact='major', status='out_of_scope',
                                 resolution='不再处理', evidence=self.evidence)]
        self.assertTrue(any('用户范围说明' in x for x in validate(record, self.project)))

    def test_keep_good_version_without_forced_iteration(self):
        self.assertEqual(validate(self.record, self.project), [])

    def test_actual_evidence_limitation_can_be_reported(self):
        record = deepcopy(self.record)
        record['decision'] = dict(action='deliver_with_limits', rationale='交付已复审的视觉范围，声音不声明通过',
                                 limits=[dict(description='没有实际听觉证据', basis='此测试仅覆盖视觉复审', evidence=self.evidence)])
        self.assertEqual(validate(record, self.project), [])

    def test_missing_evidence_is_not_a_review(self):
        record = deepcopy(self.record)
        record['observations'][0]['evidence']['file'] = 'missing.png'
        self.assertTrue(any('文件不存在' in x for x in validate(record, self.project)))


if __name__ == '__main__':
    unittest.main()
