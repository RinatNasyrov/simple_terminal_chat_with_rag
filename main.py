import textwrap

from sentence_transformers import SentenceTransformer
import openai
from settings import *
from utils import *
from string import Template

client = openai.OpenAI(
    base_url=URL,
    api_key=API_KEY
)

# Модель для токенизации, чтоб искать по доку
print('Загрузим модель-токенизатор...')
model = SentenceTransformer(TOKEN_MODEL_PATH)

# Поделю док на фрагменты
print('Загрузим документы...')
with open(DOCUMENT_PATH, 'r', encoding='utf-8') as f:
    full_text = f.read()
chunks = split_text(full_text, chunk_size=CHUNKS_SIZE, chunk_overlap=CHUNKS_OVERLAP)
embeddings = model.encode(chunks)

prompt = ''
context = ''
answer = ''
prompt_template = Template('СПРАВКА: $context\n'
                           'ВОПРОС: $prompt')
messanges = [{"role": "system", "content": SYSTEM_PROMPT}]
print('Погнали!')
while True:
    prompt = input('Вопрос>')
    # Ищу ближайшие по смыслу фрагменты
    query_embedding = model.encode([prompt])
    similarities = model.similarity(query_embedding, embeddings)
    most_similar_idx = {index: value for index, value in enumerate(similarities.tolist()[0])}
    most_similar_idx = dict(sorted(most_similar_idx.items(), key=lambda item: item[1], reverse=True))
    most_similar_idx = dict(list(most_similar_idx.items())[:CHUNKS_COUNT])
    context = '...'.join([chunks[id] for id in most_similar_idx])

    # Допишу новое сообщение в конец
    if TO_PRINT_CONTEXT:
        print(context)
    messanges.append({"role": "user", "content": prompt_template.substitute(context=context, prompt=prompt)})

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messanges,
    )

    answer = response.choices[0].message.content
    messanges.append({"role": "assistant", "content": answer})

    print(textwrap.fill(f'Ответ>{answer}', width=ANSWER_WIDTH))
