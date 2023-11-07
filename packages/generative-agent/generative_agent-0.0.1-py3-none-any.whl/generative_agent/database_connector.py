import json
import redis
import base64
import pickle
import string
import secrets
from datetime import datetime

import generative_agent

from langchain.llms import VertexAI
from langchain.chat_models import ChatVertexAI, ChatOpenAI
from langchain.embeddings import VertexAIEmbeddings, OpenAIEmbeddings


def generate_random_string(input_str, length=16):
    # alphabet = string.ascii_letters + string.digits
    # print(alphabet)
    return "".join(secrets.choice(input_str) for i in range(length))


def _encode_to_base64(original_string: str):
    # Encode the string to base64
    encoded_bytes = base64.b64encode(original_string.encode("utf-8"))
    # Convert the bytes to a string
    encoded_string = encoded_bytes.decode("utf-8")
    # Print the encoded string
    return encoded_string[:16]


class Redis_connector:
    def __init__(self, host: str = None, port: int = None, password: str = None):
        self.__host = host if host else "apn1-clear-vervet-33851.upstash.io"
        self.__port = port if port else 33851
        self.__password = password if password else "e248949a8af44f07aee8e6e23681862b"

        self.__info_format = "generative_info:{key_id}"
        self.__list_format = "memory_stream:{key_id}"

        self.__r = redis.Redis(
            host=self.__host, port=self.__port, password=self.__password
        )

    def ping(self):
        return r.ping()

    def load_agent_state_memory(self, agent):
        key_id = agent.key_id
        stored_agent_data = self.__r.get(self.__info_format.format(key_id=key_id))
        if stored_agent_data:
            agent_data = json.loads(stored_agent_data)
            # print(agent_data)

            # Retrieving the serialized list from Redis
            retrieved_memory_stram = self.__r.lrange(
                self.__list_format.format(key_id=key_id), 0, -1
            )

            # Deserialize the retrieved list
            memory_stream = [pickle.loads(obj) for obj in retrieved_memory_stram]
            # print(memory_stream)

            self.__load_agent_info(
                agent=agent, info=agent_data, memory_stream=memory_stream
            )
            agent._check_agent_type()

    def save_agent_state_memory(self, agent):
        # Save custom agent attributes to Datastore
        agent_data = self.__get_agent_info(agent)  # Convert the object to a JSON string
        # agent_data.update(file_urls)
        agent_data = json.dumps(agent_data)
        key_id = _encode_to_base64(
            original_string=self.__info_format.format(
                key_id="".join([agent.name, str(agent.age)])
            )
        )
        self.__r.set(
            self.__info_format.format(key_id=key_id), agent_data
        )  # Store the JSON string in Redis with key 'custom_agent_data'
        # self.save_attributes_to_datastore(custom_agent, file_urls)
        for obj in [pickle.dumps(item) for item in agent.retriever.memory_stream]:
            self.__r.rpush(self.__list_format.format(key_id=key_id), obj)

        return key_id

    def __get_agent_info(self, agent):
        info = {
            "name": agent.name,
            "age": agent.age,
            "agent_type": pickle.dumps(agent.agent_type).decode("latin-1"),
            "traits": agent.traits,
            "summary": agent.summary,
            "status": agent.status,
            "feelings": agent.feelings,
            "place": agent.place,
            "plan": json.dumps(
                [
                    {
                        "from": item["from"].isoformat(),
                        "to": item["to"].isoformat(),
                        "task": item["task"],
                    }
                    for item in agent.plan
                ]
            ),
            "chat_history": agent.chat_history,
            "inappropiates": agent.inappropiates,
            "chat_hist_summary": agent.chat_hist_summary,
            "chat_memlen": agent.chat_memlen,
            "verbose": agent.verbose,
        }
        return info

    def __load_agent_info(self, agent, info, memory_stream):
        agent.name = info["name"]
        agent.age = info["age"]
        agent.agent_type = pickle.loads(info["agent_type"].encode("latin-1"))
        agent.traits = info["traits"]
        agent.summary = info["summary"]
        agent.status = info["status"]
        agent.feelings = info["feelings"]
        agent.place = info["place"]
        agent.plan = [
            {
                "from": datetime.fromisoformat(item["from"]),
                "to": datetime.fromisoformat(item["to"]),
                "task": item["task"],
            }
            for item in json.loads(info["plan"])
        ]
        agent.chat_history = info["chat_history"]
        agent.inappropiates = info["inappropiates"]
        agent.chat_hist_summary = info["chat_hist_summary"]
        agent.chat_memlen = info["chat_memlen"]
        agent.verbose = info["verbose"]
        agent.retriever.memory_stream = memory_stream
