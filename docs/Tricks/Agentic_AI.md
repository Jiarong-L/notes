<style>
img{
    width: 60%;
}
</style>


[普通人的Agent开发感受](https://www.bilibili.com/video/BV1nPq2BoEf3/)，可以看看评论区


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

工作流的优势在于可以组合各模型的长处、组合成新的功能（“像人一样拆解任务”），且对于一些耗时步骤可以并行处理（e.g.网页搜索）；它需要在自动化与灵活性之间进行权衡，因为AI并不一直准确、对于一些关键步骤还需要人工规范（e.g. 人为指定流程/用一个LLM灵活设计步骤，在系统提示词里指定工具库/由AI自行生成工具 ...）


### Workflow Designs

一些流程设计技巧，用以提升最终输出的质量

e.g. 为什么 Reflection 流程的效果会比之间输出更好？因为在迭代中LLM接收了更多反馈和提示词样本，[这比 Zero-Shot Prompting 更可控](https://www.tipkay.com/institute/article/748920162618822656) --- 关于如何获得更好的（系统）提示词样本，建议参考优秀开源软件作者的示例写法？（简洁就行了）


```bash

Reflection --- 让 LLM自己/另一个LLM/用户/运行结果/... 评价输出，所得反馈可用于迭代的优化输出
              （当然，考虑到步骤的额外消耗，一般也不会迭代太多次）

    "Write code"  →  LLM  →  "Code"  →  LLM/Execute  →  "Suggest/ErrLog" or "Code Final"
                      ↑                                           
                      └─────────────────────────────────────────────┘


Tool use --- 开发者为LLM提供各种工具的API

Planning --- 由LLM决定一些功能的行动顺序，开发者无需硬编码操作流程；较难控制

Multi-agent collaboration --- 多个agent协调工作
```

根据测试结果（LLM Judge & 基于使用体验设计的硬指标 & Accuracy/Speed/...）的对比，决定是否选取某种设计

评估可以是：端到端 / **by component 检测中间输出** 且关注经常出现的错误类型

对于表现不良的步骤，优化操作：换参数/提示词，换工具、拆解任务、微调模型，加限制（e.g.规范输出格式，过滤上下文 -- 人工设置或LLM）

对于一些主观评价，推荐使用 LLM Judge (e.g.图片是否美观)；对于客观评价，建议为测试集提供标签、进行硬指标的评估


### Trick: Use Servers

个人电脑不太可能跑得动大模型，但好在它们的 Server 一般会提供兼容 OpenAI 格式的 API（虽然付费），e.g. 申请一个 [deepseek API-key](https://api-docs.deepseek.com/zh-cn/)，就可以调用模型

通常至少会有 python / curl / 前端框架（nodejs）的接口；不会编程的人也可以用[Cherry Studio](https://www.cherry-ai.com/)或在线chatbot体验一下不同模型的效果

以 python 为例：
```bash
from openai import OpenAI

client = OpenAI.Client(api_key = 'XXX', base_url = 'https://api.deepseek.com') 

def show_stream(response):
    for chunk in response:
        print(chunk.choices[0].message.content)  ## 打印模型的回复

# Round 1
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},   ## 系统给模型的提示
        {"role": "user", "content": "what is a basketball?"},   ## 用户的输入
    ],
    stream=True   ## 此例中设置流式输出，文档示例为非流式输出
)
show_stream(response)

# Round 2
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},   
        {"role": "user", "content": "what is a basketball?"},  
        response.choices[0].message,    ## 模型在之前回合的回复
        {"role": "user", "content": "say more"},  ## 用户的新输入
    ],
    stream=True  
)
show_stream(response)

# Round ...  总之应该用一个list来保存这个chat的messages历史
```

鉴于 Token 的输入和输出都需要收钱，有些复用/转手多次的内容可以写在disk里、流程中传递文件地址即可（Memory）


### Trick: MCP or exec Tools

课程中的工具 [aisuite](https://pypi.org/project/aisuite/) 整合了常见大模型的 API 接口，用法类似上文；同时它支持 Tools 的传递调用，可以由用户提供[符合 OpenAI tool format 的代码](./Agentic_AI/Tools.png)、或由 MCP server 提供调用方法（见aisuite主页示例）

MCP 指某工具或数据源的统一访问标准（args/output 格式），例如 [github-mcp-server Toolsets](https://github.com/github/github-mcp-server?tab=readme-ov-file#tools) 可以提供查询动作 ```'get_me'```

可以[使用官方 SDK 自行构建 MCP Server/Client](https://modelcontextprotocol.io/docs/learn/server-concepts)


---------------------------------

除了提供工具库，也可以选择让大模型输出可执行的代码（"Return you answer as python code delimited with <exec> and </exec> tag"），提取后[直接运行 ```exec("CODE")```](https://www.runoob.com/python3/python3-func-exec.html)

但这样无法保证安全，因为无法预料它对系统文件造成的影响，建议在sandbox中运行（docker/E2B）

### Where to use


[Claude](https://claude.com/resources/tutorials) 通常被用于 Vibe [Coding](https://claude.com/product/claude-code)（国内推荐使用 [MiniMax M2](https://www.minimaxi.com/news/minimax-m2)），现在它也可以辅助[生命科学的研究](https://claude.com/resources/tutorials/getting-started-with-claude-for-life-sciences)（论文搜索总结，[ToolUniverse](https://zitniklab.hms.harvard.edu/ToolUniverse/zh-CN/index.html)，10x数据的分析流程）


[AI4Protein -- Antibody Design](./Agentic_AI/Antibody_Design.png)


[检索增强生成(RAG)](https://syhya.github.io/zh/posts/2025-02-03-rag/)



