
## 吴恩达 [Agentic AI](https://www.bilibili.com/video/BV1aaxyz8ELY/)

Generative AI 一步获得输出 ```Input -> Memory/Reasoning -> Output```，不能自主跨系统操作或根据用户反馈进行调整；Agentic AI 是一个工作流，可以加入 Planning / Tool Use / Decision Making / Feedback 等多个模块

以 [Deep Research](https://metaso.cn/) 为例，它的流程可以拆解为以下模块：

```bash
LLM  接受用户输入，生成大纲
Loop: 
    LLM 针对大纲的部分，生成搜索关键词
    Web Search 获得网页内容
    LLM 对搜索结果进行内容提炼，生成 Draft
    LLM 检查 Draft 中的逻辑漏洞或信息缺失
        若缺失，返回搜索阶段补足，或由Reviewer补全
```

工作流的优势在于可以组合各模型的长处，且对于一些耗时步骤可以并行处理（e.g.网页搜索）；它需要在自动化与灵活性之间进行权衡，因为AI并不一直准确、对于一些关键步骤还需要人工规范（e.g. 是否提供搜索引擎的选择，限制工具库或由AI自行生成工具 ...）


Use Case: [AI4Protein -- Antibody Design](./Agentic_AI/Antibody_Design.png)




TBA






