# Video Director Workflow

用流程、提示词与专项 skills，把 AI 视频从“能运行”推进到有内容设计、美术、动作和声音判断的作品。

这是 indieshade 与 AI 持续试作、反馈、修订形成的工作流。我们尝试在同一公开提示词下，让独立创作的设计质量靠近公开分享中的 Opus 作品，**目前仍有明显差距，尚未证明能够稳定追平，也没有建立受控模型排名**。仓库公开不同风格的实际作品、可迁移的方法、失败教训和一个可运行样例。

## 不同画面风格，实际作品

| 风格与作品静帧 | 成片与制作内容 |
| --- | --- |
| [![摄影印刷剪贴](gallery/collage/poster.jpg)](gallery/collage/README.md) | **摄影印刷剪贴** · 5 秒。摄影裁片、纸片箭头、印刷字形、有限姿态。[视频](gallery/collage/film.mp4) · [提示词与制作方法](gallery/collage/prompt.md) |
| [![平涂图形编排](gallery/shape-play/poster.jpg)](gallery/shape-play/README.md) | **平涂图形与群体编排** · 15 秒。实心轮廓、形变接力、错峰群体与声音编排。[视频](gallery/shape-play/film.mp4) · [提示词与制作方法](gallery/shape-play/prompt.md) |
| [![立体材质与光影](gallery/material-field/poster.jpg)](gallery/material-field/README.md) | **立体材质与空间光影** · 30 秒。曲面、反射、空间穿行；包含意义与节奏不够成立的失败教训。[视频](gallery/material-field/film.mp4) · [提示词与制作方法](gallery/material-field/prompt.md) |
| [![像素角色表演](gallery/pixel-wizard/poster.jpg)](gallery/pixel-wizard/README.md) | **像素角色与法术表演** · 11.2 秒，无声。轮廓、色阶、受力、像素光效。[视频](gallery/pixel-wizard/film.mp4) · [提示词与制作方法](gallery/pixel-wizard/prompt.md) |
| [![极简UI形变](gallery/ui-morph/poster.jpg)](gallery/ui-morph/README.md) | **极简 UI 连续形变** · 14 秒。连续外壳、游标与图表关系、音乐节拍。[视频](gallery/ui-morph/film.mp4) · [提示词与制作方法](gallery/ui-morph/prompt.md) |

[完整展示与输入边界](docs/showcase.md) · [十五条素材提示词](library/README.md) · [交互展示页源码](showcase.html) · [实验复盘](docs/experiment-notes.md)

这是不同题材的风格展示，不是同题排名。每例记录是否看过参考、额外选择及不足；复用提示词为事后提炼，十五条素材配方尚未逐条生成验证。除剪贴样例外，其余案例目前公开成片与方法，未打包完整源工程。

## 长期方向：让指导最终不再必要

持续扩充风格和素材提示词库，并用新模型在普通提示词、风格素材卡、完整流程三种条件下的实际作品检验收益。当模型能自主完成同等设计判断时，逐步删减对应指导；若创作补偿框架已无收益，就允许它退役。具体扩充、比较与简化方式见[长期维护方法](docs/library-roadmap.md)。

## 先用哪个入口

| 需要 | 入口 |
| --- | --- |
| 让代理主动执行视频制作流程 | [AGENTS.md](AGENTS.md) |
| 安装、调用导演 skill | [narration-video-director](skills/narration-video-director/SKILL.md) |
| 理解制作过程与提示词结构 | [工作流](docs/workflow.md) · [提示词示例](docs/prompts.md) |
| 选择画面风格 | [风格条目](docs/style-profiles.json) · [剪贴画指导](skills/narration-video-director/references/vox-collage.md) |
| 查看实际作品与选择素材配方 | [五种风格作品](docs/showcase.md) · [素材库](library/README.md) |
| 扩充库与评估新模型 | [维护方法](docs/library-roadmap.md) · [导演库维护指导](skills/narration-video-director/references/library-maintenance.md) |
| 判断首版之后还该做什么 | [创作复审](skills/narration-video-director/references/creative-iteration.md) |
| 复现这个五秒样段 | [样例说明](examples/collage-paper-study/README.md) |

## 安装导演 skill

将 `skills/narration-video-director` 整个目录复制到代理可发现的 skills 目录。例如 Codex 使用 `~/.codex/skills/`；其他宿主按其技能安装规范配置。将本仓库 AGENTS.md 中的视频指令加入实际视频项目，注意保留原项目约束。

示例调用：

> 使用 $narration-video-director，先理解我的脚本、已有录音与制作限制，主动选择相关官方 skills 和工具。先明确画面如何服务每段口播，再提出风格帧与动作短样；制作后按实际产物审片并修订，准确区分技术检查与观看、听觉证据。

导演 skill 是创作调度层，不打包第三方官方 skills。新作品默认使用 HyperFrames，现有工程局部修改沿用原框架；Remotion 同样可用。依赖、官方入口与工具范围见 [安装与工具](docs/tooling.md)。图像生成是可选能力：有可用图片工具时按素材需求生成，不能生成时使用明确来源的素材或标记占位。

## 快速运行样例

需要 Node.js 22+ 和 npm；渲染还需要已安装并加入 PATH 的 FFmpeg 与 FFprobe，重新混入声音使用 FFmpeg。仓库包含已准备好的剪贴素材、字体子集和声音，不必购买生成服务或重新生成图片。

```sh
npm ci
npm run setup
npm run preview
npm run check:demo
npm run render:demo
npm run mix:demo
```

`preview` 打开画面工程；最终带声视频使用上面的 MP4。声音与画面分开冻结，在最后混入。FFmpeg 不在 PATH 时设置 `FFMPEG_PATH`。验证脚本和审片记录使用 Python 3.10+ 标准库；Windows 上命令名为 `py` 时，把说明中的 `python` 替换为 `py`。

## 这套流程改变什么

理解输入 → 提炼观看任务 → 查相关技能与参考 → 用预览选方向 → 设计关键状态与动作 → 制作与声音编排 → 实际审片、候选修订 → 明确停止依据。

它鼓励代理主动发现可用能力，而不是等待用户提醒；让画面匹配口播，减少无用标题和角落标签；将材料、字体、线条、光影和动作作为同一设计系统。它不会强制固定色板、镜头数、特效数量或动画曲线，技术成功也不作为审美成功的替代。

同提示词比较采用先独立制作、自审和哈希锁定，再揭示对标的顺序。已看过原片的试作明确记录为带参考比较。

## 范围与许可

公开版不包含私人录音、App 对话截图、用户头像、工作区历史或下载的对标原片。历史案例保留文字复盘，未附原始实验媒体的案例不能当作完整可复核结果。风格目录是有日期和观察范围的研究记录，不是“高流量风格”的因果证明。

原创指导、脚本与样例编排采用 MIT；第三方字体、纹理、依赖与声音保留各自许可。样例透明人物为 AI 生成概念素材，不是真实人物证据，也不是作者本人。[素材与许可](THIRD_PARTY_NOTICES.md)记录具体来源及例外。
