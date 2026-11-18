# 本工作区的视频制作

新建视频、显著重做视觉方案或制作同提示词对照时，主动使用 [narration-video-director](skills/narration-video-director/SKILL.md)，按其制作入口选择相关 references 和当前所选框架版本的官方指导。新作品默认先用 HyperFrames；现有项目局部修订沿用其框架，用户明确指定工具时按指定执行。无需用户反复指定技能；只讨论方案或修改局部时保持对应范围。

获准委派的新作品完整制作与显著重做默认使用两名干净上下文的 subagent：导演统一全篇设计并负责成片合稿，制作代理实现素材、动画、声音与导出，主代理协调输入和核对交付。沿用[独立制作入口](skills/narration-video-director/references/independent-production.md)的实际交接，不按章节各自设计一套美术。局部修改沿用原分工；用户指定的分工、实验条件与宿主权限优先。关键前后镜在分镜阶段共同设计，再按连接需要生产素材，并从实际成片核对接缝。

当主体与背景的关系、光影或特效影响本片表达时，查[光影、背景与特效](skills/narration-video-director/references/lighting-and-effects.md)，用实际样段核对效果。

制作中的关键帧、动作样段和审片证据按该技能的 [执行与证据闭环](skills/narration-video-director/references/production-planning.md#执行与证据闭环) 处理，由代理完成检查与必要修订。不要把编译、导出或书面分镜当成创作要求已经落实的证据，也不要把这些内部检查变成用户逐项审批。

完整制作与显著重做采用[创作复审与停止依据](skills/narration-video-director/references/creative-iteration.md)：首版导出后进入创作复审，关键问题未处理时继续修订；最终交付前检查对应当前成片的审片记录和停止决定。记录校验通过仅证明文件与执行状态相符，不代替观看、听觉或审美判断。草稿、纯讨论、直接重新导出和局部修改保持原范围。

当前目标是同一公开提示词下的独立创作质量接近外部参考；允许不同的视觉方案。保留完整要求与已知上下文差异，不以重建参考或仅与自己的旧版比较替代该目标。

新作品先由导演从内容推导画面。用户希望参加选型，或美术取舍会实质改变交付且偏好无法推断时，按[创作方向选型](skills/narration-video-director/references/comparison-and-calibration.md#创作方向选型)提供实际预览。导演用代表性动作样段自审设计，合稿时核对全片。

为风格库选型或评估传播表现时，按[风格选型与表现数据](skills/narration-video-director/references/style-selection-and-performance.md)核对片内参考与可比数据。单片创作按当前设计难点取用参考。

公开风格参考条目见 [风格目录](docs/style-profiles.json)，仅保留出处和观察边界；历史研究截图与流量缓存不随本仓库分发。

选型与扩充以[外部调研风格](docs/researched-styles.md)为主，实验成片与事后工艺配方另作应用记录；不能用Opus对照试作的分类替代此前调研库。参考研究、素材验证和原创样片制作状态分别标明。

维护本库时，按[库维护与模型变化](skills/narration-video-director/references/library-maintenance.md)提供不同画面风格的实际作品、制作输入与素材配方，保留验证状态及局限。长期扩充同时检验普通提示词基线；新模型已能自主完成的部分逐步简化，不以维持框架复杂性为目标。[维护方法](docs/library-roadmap.md)记录本仓库的扩充与退役方向。

新的同提示词检验采用先独立创作、后揭示原片的顺序：制作前只读取公开提示词与必要输入，不看对标原片、缩略图、静帧、拆解或成片描述。完成整片及自身审片后，以源文件和成片哈希锁定版本，再看原片做完整比较。比较后的修订另存；复盘提炼可迁移的设计判断、提示词和创作结构，不把对标造型或时序写成通用模板。已看过的参考不能称为盲测。
