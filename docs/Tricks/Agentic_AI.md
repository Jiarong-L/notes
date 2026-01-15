

## 吴恩达 [Agentic AI](https://www.bilibili.com/video/BV1aaxyz8ELY/)

Generative AI 一步获得输出 ```Input -> Memory/Reasoning -> Output```，不能自主跨系统操作或根据用户反馈进行调整；Agentic AI 是一个工作流，可以加入 Planning / Tool Use / Decision Making / Feedback 等多个步骤模块

以 [Deep Research](https://metaso.cn/) 为例，它的流程可以拆解为以下模块：

```bash
LLM  接受用户输入，生成大纲
Loop: 
    LLM 针对大纲的部分，生成搜索关键词
    API Web Search 获得网页内容
    LLM 对搜索结果进行内容提炼，生成 Draft
    LLM 检查 Draft 中的逻辑漏洞或信息缺失
        若缺失，返回搜索阶段补足，或由Reviewer补全
```

工作流的优势在于可以组合各模型的长处、组合成新的功能（“像人一样拆解任务”），且对于一些耗时步骤可以并行处理（e.g.网页搜索）；它需要在自动化与灵活性之间进行权衡，因为AI并不一直准确、对于一些关键步骤还需要人工规范（e.g. 人为指定流程/用一个LLM灵活设计步骤，限制工具库/由AI自行生成工具 ...）


### Workflow Designs

一些流程设计技巧，用以提升最终输出的质量

```bash

Reflection --- 让 LLM自己/另一个LLM/用户/运行结果/... 评价输出，所得反馈可用于迭代的优化输出

    "Write code"  →  LLM  →  "Code"  →  LLM/Execute  →  "Suggest/ErrLog" or "Code Final"
                      ↑                                           
                      └─────────────────────────────────────────────┘


Tool use --- 开发者为LLM提供各种工具的API

Planning --- 由LLM决定一些功能的行动顺序，开发者无需硬编码操作流程；较难控制

Multi-agent collaboration --- 多个agent协调工作
```

为什么 Reflection 流程的效果会比之间输出更好？因为在迭代中LLM接收了更多提示，这比 [Zero-Shot Prompting](https://www.tipkay.com/institute/article/748928354799177728) 更可控


### Eval and Optimize



基于使用体验设计硬指标，或使用另一个模型作为 Judge


端到端 / by component 检测中间输出












### Where to use



[AI4Protein -- Antibody Design](./Agentic_AI/Antibody_Design.png)


[检索增强生成(RAG)](https://syhya.github.io/zh/posts/2025-02-03-rag/)



