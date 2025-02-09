

需要[科学上网](https://www.cnblogs.com/xyz/p/17938947)，但是暂时可以使用[镜像网站 hf-mirror](https://hf-mirror.com/)

参照[官方视频教程](https://www.bilibili.com/video/BV1acqAY8Ehh/?p=15)


```bash
HF_ENDPOINT=https://hf-mirror.com python your_script.py
```

已有许多 scRNA-seq 应用，比如说 [Cell2Sentence](https://hf-mirror.com/vandijklab/C2S-Pythia-410m-diverse-single-and-multi-cell-tasks) - [Tutorials](https://github.com/vandijklab/cell2sentence) 可从 cell_sentences 生成逼真细胞 (expression)



## 使用

1. 通过关键词/标签等筛选模型，模型运行内存大约需要 1.2 倍的 xx_model.bin (Trained Weights)
2. 访问 Spaces 空间，在线查看模型使用效果 --- 目前国内访问不了，只能自行 Notebook 中 [Gradio Deploy](https://www.gradio.app/)
3. 点击 Use This Model 按钮，它会展示所需代码，pipeline中 一般同时包含预处理 Processor，直接使用模型即可


## Deploy on Huggingface Space

1. 左上角 - New Space - SDK(Gradio) - CPU/GPU
2. Add file: requirements.txt
```txt
transformers
torch
gradio
```

3. Add file: app.py
```py
import gradio as gr
from transformers import pipeline
pipe = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")


def launchFn(input):
    out = pipe(input)
    return out[0]['generated_text']

iface = gr.Interface(fn=launchFn, inputs=gr.Image(type='pil'), outputs="text")
iface.launch() ## share=True 增加生成一个 public url
```
4. 等待Building完成



## Use via API

1. Space 页面底部，点击 Use via API
2. 它会提供 gradio_client 的代码
```py
from gradio_client import Client

client = Client("https://24h-temp-link")
result = client.predict("local_input.png",api_name="/predict")
print(result) ## 假设此处输出是text
```

也许可以节省一些本地资源？

