// llama-server.exe -m Ministral-3-3B-Instruct-2512-Q8_0.gguf -c 4096
import OpenAI from "openai";

const client = new OpenAI({
    apiKey: "not-needed",          // llama.cpp ignores this
    baseURL: "http://localhost:8080/v1"
});

const stream = await client.chat.completions.create({
    model: "local-model",
    messages: [{ role: "user", content: "Tell me a story." }],
    stream: true,
});

for await (const chunk of stream) {
    const token = chunk.choices[0]?.delta?.content;
    if (token) process.stdout.write(token);
}
