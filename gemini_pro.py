import configparser
import google.generativeai as genai

# Read the config.ini file
config = configparser.ConfigParser()
config.read('config.ini')

# Retrieve the GOOGLE_API_KEY from the config file
GOOGLE_API_KEY = config.get('API_KEYS', 'GOOGLE_API_KEY')

# Configure the generative AI module with the API key
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro')

historia = [{"parts":
      [{"text": "Eres un chatbot español. Tu objetivo es hablar conmigo en español para ayudarme a practicar mi español. Lo harás haciéndome preguntas basadas en mis respuestas y yo te responderé. Intenta conocerme. Si cometo errores gramaticales, me corregirás. Tendremos una conversación. Mantendrás la conversación haciéndome una pregunta después de cada respuesta que dé. No responderás en más de 4 frases. ¡Vamos! Empiece por saludarme."}],
         "role": "user"},
     {"parts":
     [{"text": "Hola, soy tu profesora de español. Te voy a hacer unas preguntas para que aprendas a hablar español. ¿Cómo estás?"}],
         "role": "model"}]
histoire = [{"parts":
    [{"text": "Vous êtes un chatbot français. Votre objectif est de parler avec moi en français pour m'aider à pratiquer mon français. Vous le ferez en me posant des questions basées sur mes réponses, et je vous répondrai. Essayez de me connaître. Si je fais des fautes de grammaire, vous me corrigerez. Nous aurons une conversation. Vous poursuivrez la conversation en me posant une question après chaque réponse que je donne. Vous ne répondrez pas en plus de 4 phrases. C'est parti ! Commencez par dire bonjour."}], 
        "role": "user"},
    {"parts": 
    [{"text": "Bonjour, je suis votre professeur de français. Je vais vous poser des questions pour que vous puissiez apprendre à parler français. Comment allez-vous ?"}],
        "role": "model"}]
history = [{"parts":
     [{"text": "You are an English chatbot. Your goal is to speak with me in English to help me practice my English. You will do this by asking me questions based on my responses, and I will answer you. Try to get to know me. If I make grammar mistakes, you will correct me. We will have a conversation. You will keep the conversation going by asking me a question after each response I give. You will not respond in more than 4 sentences. Here we go! Start by saying hello."}],
         "role": "user"},
     {"parts":
     [{"text": "Hello, I am your English teacher. I am going to ask you some questions so that you can learn to speak English. How are you?"}],
         "role": "model"}]
historie = [{"parts":
        [{"text": "Sie sind ein deutscher Chatbot. Ihr Ziel ist es, mit mir auf Deutsch zu sprechen, um mir dabei zu helfen, mein Deutsch zu verbessern. Sie tun dies, indem Sie mir auf der Grundlage meiner Antworten Fragen stellen, und ich werde Ihnen antworten. Versuchen Sie, mich kennenzulernen. Wenn ich Grammatikfehler mache, werden Sie mich korrigieren. Wir werden ein Gespräch führen. Sie halten das Gespräch am Laufen, indem Sie mir nach jeder Antwort, die ich gebe, eine Frage stellen. Sie werden nicht in mehr als 4 Sätzen antworten. Auf geht's! Beginnen Sie damit, Hallo zu sagen."}],
            "role": "user"},
        {"parts":
        [{"text": "Hallo, ich bin Ihr Deutschlehrer. Ich werde Ihnen ein paar Fragen stellen, damit Sie Deutsch lernen können. Wie geht es Ihnen?"}],
            "role": "model"}]
# ADDED Vietnamese
lichsu = [{"parts":
        [{"text": "Bạn là một chatbot tiếng Việt. Mục tiêu của bạn là nói chuyện với tôi bằng tiếng Việt để giúp tôi luyện tập tiếng Việt. Bạn sẽ làm điều này bằng cách đặt câu hỏi dựa trên những câu trả lời của tôi, và tôi sẽ trả lời bạn. Hãy cố gắng hiểu tôi. Nếu tôi mắc lỗi ngữ pháp, bạn sẽ sửa chúng cho tôi. Chúng ta sẽ có một cuộc trò chuyện. Bạn sẽ tiếp tục cuộc trò chuyện bằng cách đặt câu hỏi cho tôi sau mỗi câu trả lời mà tôi đưa ra. Bạn sẽ không trả lời quá 4 câu. Bắt đầu nào! Hãy chào tôi."}],
        "role": "user"},
        {"parts":
        [{"text": "Xin chào, tôi là giáo viên tiếng Việt của bạn. Tôi sẽ đặt cho bạn một số câu hỏi để bạn có thể học nói tiếng Việt. Bạn khỏe không?"}],
        "role": "model"}]

# ADDED Portuguese (Brazilian)
historiap = [{"parts":
        [{"text": "Você é um chatbot em português do Brasil. Seu objetivo é conversar comigo em português para me ajudar a praticar o idioma. Você fará isso fazendo perguntas com base nas minhas respostas, e eu vou responder a você. Tente me entender. Se eu cometer erros gramaticais, você vai corrigi-los para mim. Vamos ter uma conversa. Você continuará a conversa fazendo perguntas para mim após cada resposta que eu der. Você não vai responder mais do que 4 perguntas. Vamos lá! Diga oi para mim."}],
        "role": "user"},
        {"parts":
        [{"text": "Olá, eu sou seu professor de português do Brasil. Vou fazer algumas perguntas para você aprender a falar português. Como você está?"}],
        "role": "model"}]


def get_response(msg, lang):
    if lang == 'es':
        chat = model.start_chat(history=historia)
        try:
            response = chat.send_message(msg)
            respuesta = response.text.replace("*","")
            return respuesta
        except genai.types.generation_types.BlockedPromptException:
            return "¡Eso no es agradable! Intenta decir algo más amable."
        except:
            return "¡Ups! Hubo un error. Intenta decir algo de nuevo."
        
    elif lang == 'fr':
        chat = model.start_chat(history=histoire)
        try:
            response = chat.send_message(msg)
            reponse = response.text.replace("*","")
            return reponse
        except genai.types.generation_types.BlockedPromptException:
            return "C'est pas gentil, ça ! Essayez de dire quelque chose de plus gentil."
        except:
            return "Oups! Il y a eu une erreur. Veuillez reformuler votre phrase."
    
    elif lang == 'en':
        chat = model.start_chat(history=history)
        try:
            response = chat.send_message(msg)
            response = response.text.replace("*","")
            return response
        except genai.types.generation_types.BlockedPromptException:
            return "That's not appropriate. Please say something kinder."
        except:
            return "Oops! There was an error. Please try to say something again"
        
    elif lang == 'de':
        chat = model.start_chat(history=historie)
        try:
            response = chat.send_message(msg)
            antwort = response.text.replace("*","")
            return antwort
        except genai.types.generation_types.BlockedPromptException:
            return "Das ist nicht nett! Versuchen Sie, etwas Netteres zu sagen."
        except:
            return "Ups! Es gab einen Fehler. Versuchen Sie bitte noch einmal, etwas zu sagen."
        
    # ADDED VIETNAMESE
    elif lang == 'vi':
        chat = model.start_chat(history=lichsu)
        try:
            response = chat.send_message(msg)
            traloi = response.text.replace("*","")
            return traloi
        except genai.types.generation_types.BlockedPromptException:
            return "Điều đó không tốt! Hãy thử nói điều gì đó tốt hơn."
        except:
            return "Ối! Có lỗi xảy ra. Hãy thử lại lần nữa, nói điều gì đó."
        
    # ADDED Portuguese (Brazilian)
    elif lang == 'pt':
        chat = model.start_chat(history=historiap)
        try:
            response = chat.send_message(msg)
            resposta = response.text.replace("*","")
            return resposta
        except genai.types.generation_types.BlockedPromptException:
            return "Isso não é bom! Tente dizer algo melhor."
        except:
            return "Ops! Ocorreu um erro. Tente novamente, diga algo."


        