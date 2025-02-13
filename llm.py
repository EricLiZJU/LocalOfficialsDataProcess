import ollama

res=ollama.chat(model="deepseek-r1:7b",stream=False,messages=[{"role": "user","content": "锐评一下浙江大学数学学院"}],options={"temperature":0})
print(res.message.content)
res1=ollama.chat(model="deepseek-r1:7b",stream=False,messages=[{"role": "user","content": "重点说一下不足之处"}],options={"temperature":0})
print(res1.message.content)