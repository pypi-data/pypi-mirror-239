import json
import redis
import base64
import pickle
import string
import secrets
import hashlib
from datetime import datetime

import generative_agent

from langchain.llms import VertexAI
from langchain.chat_models import ChatVertexAI, ChatOpenAI
from langchain.embeddings import VertexAIEmbeddings, OpenAIEmbeddings


def generate_unique_id(original_string: str):
    unique_id = hashlib.sha256(original_string.encode()).hexdigest()
    return unique_id[:16]


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
    return encoded_string


class Redis_connector:
    def __init__(self, host: str = None, port: int = None, password: str = None):
        self.__host = host if host else "apn1-clear-vervet-33851.upstash.io"
        self.__port = port if port else 33851
        self.__password = password if password else "e248949a8af44f07aee8e6e23681862b"

        self.__info_format = "generative_agent:{agent_id}:info"
        self.__memory_stream_format = "generative_agent:{agent_id}:memory_stream"
        self.__chat_hist_format = (
            "generative_agent:{agent_id}:user:{user_id}:chat_history"
        )
        self.__chat_summ_format = (
            "generative_agent:{agent_id}:user:{user_id}:chat_history_summary"
        )

        self.__r = redis.Redis(
            host=self.__host, port=self.__port, password=self.__password
        )

    def ping(self):
        return self.__r.ping()

    def load_agent_state_memory(self, agent, user_id):
        agent_id = agent.agent_id
        info_key = self.__info_format.format(agent_id=agent_id)
        memory_stream_key = self.__memory_stream_format.format(agent_id=agent_id)
        chat_hist_key = self.__chat_hist_format.format(
            agent_id=agent_id, user_id=user_id
        )
        chat_summ_key = self.__chat_summ_format.format(
            agent_id=agent_id, user_id=user_id
        )

        stored_agent_data = self.__r.get(info_key)
        if stored_agent_data:
            agent_data = json.loads(stored_agent_data)

            # Retrieving the memory_stream from Redis
            retrieved_memory_stram = self.__r.lrange(memory_stream_key, 0, -1)
            # Deserialize the retrieved list
            memory_stream = [pickle.loads(obj) for obj in retrieved_memory_stram]

            # Retrieving the chat_history from Redis
            retrieved_chat_history = self.__r.lrange(chat_hist_key, 0, -1)
            # print(retrieved_chat_history)
            # Converting byte strings to regular strings
            chat_history = [pickle.loads(item) for item in retrieved_chat_history]

            # Retrieve the chat_history_summary from Redis
            retrieved_chat_hist_summ = self.__r.get(chat_summ_key)
            chat_hist_summ = retrieved_chat_hist_summ.decode("utf-8")

            self.__load_agent_info(
                agent=agent,
                info=agent_data,
                memory_stream=memory_stream,
                chat_history=chat_history,
                chat_history_summary=chat_hist_summ,
            )
            agent._check_agent_type()

    def save_agent_state_memory(self, agent, user):
        # Save custom agent attributes to Datastore
        agent_data = self.__get_agent_info(agent)  # Convert the object to a JSON string
        # agent_data.update(file_urls)
        agent_data = json.dumps(agent_data)
        agent_id = generate_unique_id(original_string=f"{agent.name}-{agent.age}")
        user_id = generate_unique_id(original_string=user)

        info_key = self.__info_format.format(agent_id=agent_id)
        memory_stream_key = self.__memory_stream_format.format(agent_id=agent_id)
        chat_hist_key = self.__chat_hist_format.format(
            agent_id=agent_id, user_id=user_id
        )
        chat_summ_key = self.__chat_summ_format.format(
            agent_id=agent_id, user_id=user_id
        )
        # Store the JSON string in Redis with key
        self.__r.set(info_key, agent_data)
        # Store the List of documents in Redis with key
        self.__r.delete(memory_stream_key)
        for memo in [pickle.dumps(item) for item in agent.retriever.memory_stream]:
            self.__r.rpush(memory_stream_key, memo)
        # Store the List of chat_history in Redis with key
        self.__r.delete(chat_hist_key)
        for chat_hist in [pickle.dumps(item) for item in agent.chat_history]:
            self.__r.rpush(chat_hist_key, chat_hist)
        # Store the JSON string in Redis with key
        self.__r.set(chat_summ_key, agent.chat_hist_summary)

        return {"agent_id": agent_id, "user_id": user_id}

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
            # "chat_history": agent.chat_history,
            "inappropiates": agent.inappropiates,
            # "chat_hist_summary": agent.chat_hist_summary,
            "chat_memlen": agent.chat_memlen,
            "verbose": agent.verbose,
        }
        return info

    def __load_agent_info(
        self, agent, info, memory_stream, chat_history, chat_history_summary
    ):
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
        agent.chat_history = chat_history
        agent.inappropiates = info["inappropiates"]
        agent.chat_hist_summary = chat_history_summary
        agent.chat_memlen = info["chat_memlen"]
        agent.verbose = info["verbose"]
        agent.retriever.memory_stream = memory_stream
