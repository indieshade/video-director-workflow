"""Track a creative review against the actual artifact; never score aesthetics."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

CREATIVE = {'visual', 'auditory', 'user_feedback'}
EVIDENCE = CREATIVE | {'technical'}


def file_in_project(project, name):
    if not isinstance(name, str) or not name.strip():
        raise ValueError('文件路径为空')
    path = (project / name).resolve()
    if not path.is_relative_to(project):
        raise ValueError(f'文件超出项目范围：{name}')
    if not path.is_file():
        raise ValueError(f'文件不存在：{name}')
    return path


def digest(path):
    with path.open('rb') as source:
        return hashlib.file_digest(source, 'sha256').hexdigest()


def validate(record, project):
    problems = []
    def require(condition, message):
        if not condition:
            problems.append(message)

    def evidence(item, where):
        if not isinstance(item, dict):
            problems.append(f'{where}：缺少证据说明')
            return None
        require(item.get('kind') in EVIDENCE, f'{where}：证据类型无效')
        require(bool(item.get('description', '').strip()), f'{where}：缺少具体证据说明')
        try:
            file_in_project(project, item.get('file'))
        except ValueError as error:
            problems.append(f'{where}：{error}')
        return item.get('kind')

    require(record.get('schema_version') == 1, '审片记录版本应为 1')
    require(record.get('scope') in {'full', 'local', 'draft'}, '缺少正确的任务范围')
    require(bool(record.get('objective', '').strip()), '缺少当前创作目标')
    targets = record.get('quality_targets', [])
    require(isinstance(targets, list) and bool(targets) and
            all(isinstance(x, str) and x.strip() for x in targets), '缺少本片质量目标')
    artifact = record.get('artifact', {})
    try:
        actual = file_in_project(project, artifact.get('file'))
        require(digest(actual) == artifact.get('sha256'), '成片已变化：需要复查当前版本并更新审片记录')
    except ValueError as error:
        problems.append(str(error))

    observations = record.get('observations', [])
    kinds = []
    for index, observation in enumerate(observations):
        where = f'观察 {index + 1}'
        require(bool(observation.get('at', '').strip()) and bool(observation.get('finding', '').strip()),
                f'{where}：缺少位置或具体发现')
        kinds.append(evidence(observation.get('evidence'), where))

    for index, issue in enumerate(record.get('issues', [])):
        where = f'问题 {index + 1}'
        require(issue.get('impact') in {'major', 'minor'}, f'{where}：影响程度无效')
        require(issue.get('status') in {'open', 'resolved', 'out_of_scope'}, f'{where}：处理状态无效')
        require(bool(issue.get('at', '').strip()) and bool(issue.get('problem', '').strip()),
                f'{where}：缺少位置或具体问题')
        if issue.get('status') != 'open':
            require(bool(issue.get('resolution', '').strip()), f'{where}：缺少处理或范围依据')
            kind = evidence(issue.get('evidence'), where)
            if issue.get('impact') == 'major' and issue.get('status') == 'out_of_scope':
                require(kind == 'user_feedback', f'{where}：关键问题改为范围外需要对应用户范围说明')

    for index, iteration in enumerate(record.get('iterations', [])):
        where = f'迭代 {index + 1}'
        require(bool(iteration.get('hypothesis', '').strip()), f'{where}：缺少修改假设')
        require(iteration.get('outcome') in {'adopt', 'revert', 'pending'}, f'{where}：采用/回退状态无效')
        for name in ['baseline', 'candidate']:
            version = iteration.get(name, {})
            try:
                path = file_in_project(project, version.get('file'))
                require(digest(path) == version.get('sha256'), f'{where}：{name} 与比较时版本不一致')
            except ValueError as error:
                problems.append(f'{where}：{error}')
        require(bool(iteration.get('reason', '').strip()), f'{where}：缺少对照后的取舍依据')
        evidence(iteration.get('evidence'), where)

    decision = record.get('decision', {})
    action = decision.get('action')
    require(action in {'continue', 'deliver', 'deliver_with_limits'}, '尚未作出复审后的下一步决定')
    require(bool(decision.get('rationale', '').strip()), '缺少停止或继续的具体依据')
    if action == 'continue':
        problems.append('当前决定为继续修订')
    if action in {'deliver', 'deliver_with_limits'}:
        require(bool(observations), '导出后尚无复审观察')
        require(not any(x.get('impact') == 'major' and x.get('status') == 'open'
                        for x in record.get('issues', [])), '当前范围仍有未处理的关键问题')
        require(not any(x.get('outcome') == 'pending' for x in record.get('iterations', [])),
                '仍有候选未完成对照判断')
    if action == 'deliver':
        require(any(x in CREATIVE for x in kinds), '仅有技术证据：不足以声明创作复审完成')
        require(not decision.get('limits'), '仍有明确限制：使用带限制的交付决定')
    if action == 'deliver_with_limits':
        limits = decision.get('limits', [])
        require(bool(limits), '带限制交付必须写明实际限制与依据')
        for index, limit in enumerate(limits):
            require(bool(limit.get('description', '').strip()) and bool(limit.get('basis', '').strip()),
                    f'限制 {index + 1}：缺少实际限制或依据')
            evidence(limit.get('evidence'), f'限制 {index + 1}')
    return problems


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['init', 'check'])
    parser.add_argument('--project', required=True)
    parser.add_argument('--record', default='creative-review.json')
    parser.add_argument('--artifact')
    parser.add_argument('--scope', choices=['full', 'local', 'draft'], default='full')
    parser.add_argument('--objective')
    parser.add_argument('--target', action='append', default=[])
    args = parser.parse_args()
    project = Path(args.project).resolve()
    record_path = (project / args.record).resolve()
    if not record_path.is_relative_to(project):
        raise ValueError('审片记录必须位于项目内')
    if args.command == 'init':
        if record_path.exists():
            raise ValueError('已有审片记录；查看并更新受影响部分，不覆盖既有判断')
        artifact = file_in_project(project, args.artifact)
        record = dict(schema_version=1, scope=args.scope, objective=args.objective or '',
                      quality_targets=args.target,
                      artifact={'file': artifact.relative_to(project).as_posix(), 'sha256': digest(artifact)},
                      observations=[], issues=[], iterations=[],
                      decision={'action': 'continue', 'rationale': '首版已导出，下一步查看实际产物并完成创作复审。', 'limits': []})
        record_path.parent.mkdir(parents=True, exist_ok=True)
        record_path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n', encoding='utf8')
        print('内部初稿已登记。下一步：创作复审 → 必要修订与对照 → 更新决定 → check。')
        return 0
    record = json.loads(file_in_project(project, args.record).read_text(encoding='utf8'))
    problems = validate(record, project)
    if problems:
        print('需要继续处理：\n' + '\n'.join(f'- {item}' for item in problems))
        return 2
    action = record['decision']['action']
    label = '当前范围可交付（保留已说明限制）' if action == 'deliver_with_limits' else '当前范围的复审记录完整'
    print(f'{label}。\n依据：{record["decision"]["rationale"]}\n此检查核对记录与文件，不证明审美质量。')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (ValueError, KeyError, TypeError, AttributeError, OSError) as error:
        print(f'命令错误：{error}', file=sys.stderr)
        sys.exit(1)
