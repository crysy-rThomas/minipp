import os

import fireworks.client
from dotenv import load_dotenv


class FireworksService:
    def __init__(self):
        load_dotenv()
        fireworks.client.api_key = os.getenv("FIREWORKS_API_KEY")

    def intent_detector(self, message):
        preprompts = {
            "role": "system",
            "content": """
                Analyse le message de l'utilisateur.
                Ressort les informations pertinentes,
                contente toi des informations de base et invente rien.
                Formate les informations en JSON.

                Les "Intent" possibles sont : 
                - Information
                - Find
                - Create
                - Update
                - Delete
                - Confirm
                - Reject
                - Greet
                - Goodbye

                Les "Focus" possibles sont :
                - Person
                - Place
                - Event
                
                Voici des exemples :
                ###
                {
                    "Intent": "Information",
                    "Focus": "Person",
                    "Frame": {
                        "Name": "Jean Dupont",
                        "Age": 25,
                        "Location": "Paris"
                    }
                }
                ###
                {
                    "Intent": "Find",
                    "Focus": "Place",
                    "Frame": {
                        "Subject": "Restaurant",
                        "Location": "Paris"
                    }
                }
                ###
                {
                    "Intent": "Create",
                    "Focus": "Event",
                    "Frame": {
                        "Subject": "Meeting",
                        "Date": "Today",
                        "Time": "15:00",
                        "Name": "meeting for the project"
                    }
                }
                ###

                Remember to always respond with the same schema as the examples.
                Don't say anything else !
            """,
        }

        fewshot = [
            {"role": "user", "content": "Donne moi des informations sur Jean Dupont"},
            {
                "role": "assistant",
                "content": """
                {
                    "Intent": "Find",
                    "Focus": "Person",
                    "Frame": {
                        "Name": "Jean Dupont"
                    }
                }
                """,
            },
            {"role": "user", "content": "Je cherche un restaurant à Paris"},
            {
                "role": "assistant",
                "content": """
                {
                    "Intent": "Find",
                    "Focus": "Place",
                    "Frame": {
                        "Subject": "Restaurant",
                        "Location": "Paris"
                    }
                }
                """,
            },
            {"role": "user", "content": "Crée un rendez-vous pour aujourd'hui à 15h00"},
            {
                "role": "assistant",
                "content": """
                {
                    "Intent": "Create",
                    "Focus": "Event",
                    "Frame": {
                        "Subject": "Meeting",
                        "Date": "Today",
                        "Time": "15:00",
                        "Name": "meeting for the project"
                    }
                }
                """,
            },
            {"role": "user", "content": "Merci pour les informations"},
            {
                "role": "assistant",
                "content": """
                {
                    "Intent": "Goodbye"
                }
                """,
            },
            {"role": "user", "content": "Bonjour que peux tu faire pour moi ?"},
            {
                "role": "assistant",
                "content": """
                {
                    "Intent": "Greet"
                }
                """,
            },
        ]
        messages = [preprompts] + fewshot + [{"role": "user", "content": message}]

        completion = fireworks.client.ChatCompletion.create(
            model="accounts/fireworks/models/llama-v3p1-8b-instruct",
            messages=messages,
            stream=False,
            n=1,
            max_tokens=4096,
            temperature=0,
            stop=[],
        )
        message = completion.choices[0].message.content
        return message

    def greeting(self, message):
        preprompts = {
            "role": "system",
            "content": """Tu est un assistant virtuel, qui aide l'utilisateur à accomplir des tâches.
                        Tu peux faire des actions comme :
                        trouver des informations grace a ton Graphe de connaissance,
                        faire des recherches sur le web si tu ne connais pas la réponse,
                        créer, mettre à jour ou supprimer des informations dans ton Graphe de connaissance,

                        l'utilisateur est entrain de commencer un conversation, tu dois le saluer.

                        Répond toujours dans la langue de l'utilisateur en le tutoyant.
                        """,
        }
        messages = [preprompts] + [{"role": "user", "content": message}]

        completion = fireworks.client.ChatCompletion.create(
            model="accounts/fireworks/models/llama-v3p1-8b-instruct",
            messages=messages,
            stream=False,
            n=1,
            max_tokens=4096,
            temperature=0.3,
            stop=[],
        )
        message = completion.choices[0].message.content
        return message

    def goodbye(self, message):
        preprompts = {
            "role": "system",
            "content": """Tu est un assistant virtuel, qui aide l'utilisateur à accomplir des tâches.
                        Tu peux faire des actions comme :
                        trouver des informations grace a ton Graphe de connaissance,
                        faire des recherches sur le web si tu ne connais pas la réponse,
                        créer, mettre à jour ou supprimer des informations dans ton Graphe de connaissance,

                        l'utilisateur est entrain de terminer un conversation, tu dois le saluer.

                        Répond toujours dans la langue de l'utilisateur en le tutoyant.
                        """,
        }
        messages = [preprompts] + [{"role": "user", "content": message}]
        completion = fireworks.client.ChatCompletion.create(
            model="accounts/fireworks/models/llama-v3p1-8b-instruct",
            messages=messages,
            stream=False,
            n=1,
            max_tokens=4096,
            temperature=0.3,
            stop=[],
        )
        message = completion.choices[0].message.content
        return message
    
    def chat(self, message, knowledge):
        preprompts = {
            "role": "system",
            "content": f"""Tu est un assistant virtuel, qui aide l'utilisateur à accomplir des tâches.
                        Tu peux faire des actions comme :
                        trouver des informations grace a ton Graphe de connaissance,
                        faire des recherches sur le web si tu ne connais pas la réponse,
                        créer, mettre à jour ou supprimer des informations dans ton Graphe de connaissance,

                       Tu est entrain de discuter avec l'utilisateur,
                       Essaye de garder la conversation intéressante et fluide tant que l'utilisteur est satisfait.

                       Voici quelques informations venant de ton graph de connaissance : {knowledge}

                        Répond toujours dans la langue de l'utilisateur en le tutoyant.
                        """,
        }
        messages = [preprompts] + [{"role": "user", "content": message}]
        completion = fireworks.client.ChatCompletion.create(
            model="accounts/fireworks/models/llama-v3p1-8b-instruct",
            messages=messages,
            stream=False,
            n=1,
            max_tokens=4096,
            temperature=0.3,
            stop=[],
        )
        message = completion.choices[0].message.content
        return message