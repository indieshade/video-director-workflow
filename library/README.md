# 调研风格与素材提示词

[外部调研风格及制作提案](../docs/researched-styles.md) · [交互参考页](../style-library.html) · [长期维护方法](../docs/library-roadmap.md)

`docs/style-profiles.json` 是选型真值：七个外部调研分支与一个自有改编。`material-prompts.json` 的21条配方按 `source_profile` 关联这份调研；类型分别表示图片生成、程序绘图、场景、字形、照明或动作设计，不应全交给图片生成器。替换 `variables` 中的变量，再按 `acceptance` 在实际片内尺寸与动作中检查。

配方状态是 `authored_from_reference_not_generation_tested`：从既有视觉研究转成制作提案，尚未生成验证，不是原作者使用过的提示词。参考图像、动作观察、本片提案与已制作样例分别成立。标记 `generation_tested_with_evidence` 时需附实际输入、工具/版本、输出和反馈的 `evidence` 文件。

多数方向尚无自己的制作样片，不能拿此前实验片补上“已制作”状态。[剪贴样例](../examples/collage-paper-study/README.md)提供完整可运行源码，属于自有改编而非原作复刻。

## 保留的实验资料

`showcase.json` 和[实验作品页](../docs/showcase.md)索引已有实验成片。`experiment-material-prompts.json` 保留15条事后工艺配方，状态为 `authored_after_example_not_generation_tested`。这组资料不能代替外部研究分类，也不用于推断某风格已被实现。

原作通过来源链接、作者图片或播放器引用；没有将参考截图、外部原片、私人 IP 或 App 证据文件上传本库。参考播放器不可用时直接打开条目中的带时间来源链接。
