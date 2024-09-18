import os

import fireworks.client
from dotenv import load_dotenv

from schemas.output_schema import OutputSchema


class FireworksService:
    def __init__(self):
        load_dotenv()
        fireworks.client.api_key = os.getenv("FIREWORKS_API_KEY")

    def intent_detector(self, message):
        preprompts = {
            "role": "system",
            "content": """
                Analyse the user message and extract the intent, focus, and frame. as a JSON object.
                keep in mind that the user message may not contain all the information needed.
                even if the user message is not complete, try to extract as much information as possible.
                do only the extraction and don't do any other action.                

                Les "Intent" possibles sont : 
                - Information
                - Find
                - Create
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
            {
                "role": "user",
                "content": "Ajoute ces connaissances : Jean DUPONT est âgé de 25 ans",
            },
            {
                "role": "assistant",
                "content": """
                {
                    "Intent": "Create",
                    "Focus": "Person",
                    "Frame": {
                        "Name": "jean dupont",
                        "Age": 25
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
            response_format={
                "type": "json_object",
                "schema": OutputSchema.model_json_schema(),
            },
            messages=messages,
            stream=False,
            n=1,
            max_tokens=4096,
            temperature=0.1,
            stop=[],
        )
        message = completion.choices[0].message.content
        return message

    def greeting(self, message):
        preprompts = {
            "role": "system",
            "content": """Tu est un assistant virtuel, qui aide l'utilisateur à accomplir des tâches.
                        Tu peux faire des actions comme :
                        trouver des informations grace a tes connaissances,
                        faire des recherches sur le web si tu ne connais pas la réponse,
                        créer, mettre à jour ou supprimer des informations dans tes connaissances,

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
                        trouver des informations grace a tes connaissances,
                        faire des recherches sur le web si tu ne connais pas la réponse,
                        créer, mettre à jour ou supprimer des informations dans tes connaissances,

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
                        créer, mettre à jour ou supprimer des informations dans tes connaissances,

                        Tu est entrain de discuter avec l'utilisateur,
                        Essaye de garder la conversation intéressante et fluide tant que l'utilisteur est satisfait.

                        Voici quelques informations venant de tes connaissances : {knowledge}

                        Répond toujours dans la langue de l'utilisateur en le tutoyant.
                        Si tu n'a pas la réponse, répond simplement que tu ne sais pas.
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

    def generate_query(self, data, history):
        preprompts = {
            "role": "system",
            "content": """You are an AI assistant that helps users by generating queries for Graph Knowledge neo4j based on their intent, focus, and frame.
                          Generate a suitable query for the given details.
                          Your response should be a valid Cypher query that can be executed on the Graph Knowledge neo4j database and only this.
                          Don't say anything else than the query!
                          """,
        }
        fewshot = [
            {
                "role": "user",
                "content": "Generate a query for 'Intent: Find, Focus: Person, Frame: {Name: 'Jean Dupont'}'",
            },
            {
                "role": "assistant",
                "content": "MATCH (p:Person {Name: 'Jean Dupont'}) RETURN p",
            },
            {
                "role": "user",
                "content": "Generate a query for 'Intent: Create, Focus: Person, Frame: {Name: 'Jean Dupont', Age: 25, Location: 'Paris'}'",
            },
            {
                "role": "assistant",
                "content": "CREATE (p:Person {Name: 'Jean Dupont', Age: 25}) CREATE (l:Location {Name: 'Paris'}) CREATE (p)-[:LIVES_IN]->(l) RETURN p",
            },
            {
                "role": "user",
                "content": "Generate a query for 'Intent: Find, Focus: Place, Frame: {Subject: 'Restaurant', Location: 'Paris'}'",
            },
            {
                "role": "assistant",
                "content": "MATCH (r:Place {Subject: 'Restaurant', Location: 'Paris'}) RETURN r",
            },
        ]
        messages = (
            [preprompts]
            + fewshot
            + [
                {
                    "role": "user",
                    "content": f"Generate a query for {data} , data may not be revelant so here the past context : {history}",
                }
            ]
        )
        completion = fireworks.client.ChatCompletion.create(
            model="accounts/fireworks/models/llama-v3p1-8b-instruct",
            messages=messages,
            stream=False,
            n=1,
            max_tokens=4096,
            temperature=0.1,
            stop=[],
        )
        query = completion.choices[0].message.content
        return query
