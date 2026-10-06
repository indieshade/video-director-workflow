# 工具与技能入口

本仓库提供原创导演 skill；下列官方和第三方能力单独安装，不把它们的完整 skill 源码复制成我们的成果。

| 能力 | 上游入口 | 如何使用 |
| --- | --- | --- |
| HyperFrames | https://github.com/heygen-com/hyperframes | 新作品默认入口，使用与实际项目版本相符的 authoring、GSAP、CLI、Registry、audio 指导 |
| Remotion skills | https://www.remotion.dev/docs/ai/skills | 已有工程或明确指定时使用；不必迁移局部修订 |
| GSAP | https://gsap.com/docs/v3/ | 时间线、缓动与编排；服从视频框架时间 |
| Three.js | https://threejs.org/docs/ | 空间、材质和受光有明确收益时使用 |
| FFmpeg | https://ffmpeg.org/documentation.html | 冻结混音、编码检查和媒体处理 |
| 图像工具 | 当前宿主可用的生成或素材工具 | 实际参考、透明素材、来源与使用范围准确记录 |

样例固定 HyperFrames 0.8.137 与 GSAP 3.13.0。项目 package-lock 锁定安装依赖；这里不是最新版本推荐。新作品按其实际版本阅读指导。

样例复现要求完整 FFmpeg 安装（包含 FFprobe）并加入 PATH。只安装一个剪辑软件内置的 FFmpeg，可能缺少 FFprobe，从而不能渲染。图形素材与字体不依赖原工作区，操作系统、浏览器/GPU及媒体运行时仍是实际环境的一部分。

外部 motion-design、shotcraft、cut-motion 等资料可以按难点参考，但其适用范围、许可和版本由采用时核对。导演不要求把所有技能全部读取或安装；调用是否有效以实际画面和声音判断。
