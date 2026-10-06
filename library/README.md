# 调研风格与素材提示词

[外部调研风格及制作提案](../docs/researched-styles.md) · [交互参考页](../style-library.html) · [长期维护方法](../docs/library-roadmap.md)

`docs/style-profiles.json` 是选型真值：七个外部调研分支与一个自有改编。`material-prompts.json` 的21条配方按 `source_profile` 关联这份调研；类型分别表示图片生成、程序绘图、场景、字形、照明或动作设计，不应全交给图片生成器。替换 `variables` 中的变量，再按 `acceptance` 在实际片内尺寸与动作中检查。

配方不是原作者使用过的提示词。参考观察、素材生成、实现测试与风格通过分别记录。[首轮实测](../examples/style-prompt-audit/README.md)实际生成4条图像配方、实施12条程序化/设计配方；另5条未执行或受阻。七段首版只部分兑现，没有标为参考等效通过。

状态 `authored_from_reference_not_generation_tested` 表示未实际完成；`generation_tested_with_evidence` 与 `implementation_tested_with_evidence` 分别表示生成或实现被测试，必须附 `evidence`，不能解释为质量通过。`validation_result` 单独报告本轮结果。受阻条目保留未验证状态并附 `test_attempt`。原提示词不因状态更新而改写。

七个六秒诊断样段不能代替完整视频，不能拿此前实验片补上“风格已验证”。[剪贴样例](../examples/collage-paper-study/README.md)另提供完整可运行源码，属于自有改编而非原作复刻。

## 保留的实验资料

`showcase.json` 和[实验作品页](../docs/showcase.md)索引已有实验成片。`experiment-material-prompts.json` 保留15条事后工艺配方，状态为 `authored_after_example_not_generation_tested`。这组资料不能代替外部研究分类，也不用于推断某风格已被实现。

原作通过来源链接、作者图片或播放器引用；没有将参考截图、外部原片、私人 IP 或 App 证据文件上传本库。参考播放器不可用时直接打开条目中的带时间来源链接。
