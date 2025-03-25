MODEL_NAME = "cotype_nano_8bit"
URL = "http://localhost:8080/v1"
API_KEY = "NONE"
CHUNKS_COUNT = 2
CHUNKS_SIZE = 80
CHUNKS_OVERLAP = 20
TO_PRINT_CONTEXT = False
DOCUMENT_PATH = "./ustav.txt"
TOKEN_MODEL_PATH = "./LaBSE"
SYSTEM_PROMPT = 'Ты полезный и вежливый помошник. Отвечай на вопрос из секции ВОПРОС ' \
              'кратко и по делу,опираясь на предложенные данные из секции СПРАВКА. ' \
              'Никогда не ври, если секция СПРАВКА не содержит нужных фактов, ' \
              'отвечай НЕ НАЙДЕНО.'