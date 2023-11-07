import os
import math
import json
import time
import faiss
import pickle
import pinecone
import threading
import importlib
import concurrent.futures
from datetime import timedelta

from .tools import (
    datetime,
    text_from_inapp_list,
    get_thai_datetime,
    text_chat_hist,
    get_text_from_docs,
    Mem_Type,
    Agent_Type,
    RateLimiter,
)

from .time_weighted_retriever import TimeWeightedVectorStoreRetrieverModified


from langchain.chains import LLMChain
from langchain.schema import Document
from langchain.docstore import InMemoryDocstore
from langchain.vectorstores import FAISS, Pinecone
from langchain.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)


def relevance_score_fn(score: float) -> float:
    """Return a similarity score on a scale [0, 1]."""
    # This will differ depending on a few things:
    # - the distance / similarity metric used by the VectorStore
    # - the scale of your embeddings (OpenAI's are unit norm. Many others are not!)
    # This function converts the euclidean norm of normalized embeddings
    # (0 is most similar, sqrt(2) most dissimilar)
    # to a similarity function (0 to 1)
    return 1.0 - score / math.sqrt(2)


def use_textllm_with_prompt(textllm, prompt_template, inps, verbose):
    prompt = PromptTemplate(
        input_variables=prompt_template["input_variables"],
        template=prompt_template["prompt_template"],
    )
    chain = LLMChain(llm=textllm, prompt=prompt, verbose=verbose)
    return chain(inputs=inps)["text"]


def use_chatllm_with_prompt(chatllm, prompt_template, inps, verbose):
    chat_prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(
                template=prompt_template["system"]["prompt_template"],
                input_variables=prompt_template["system"]["input_variables"],
            ),
            HumanMessagePromptTemplate.from_template(
                template=prompt_template["user"]["prompt_template"],
                input_variables=prompt_template["user"]["input_variables"],
            ),
        ]
    )
    chain = LLMChain(llm=chatllm, prompt=chat_prompt, verbose=verbose)
    return chain(inputs=inps)["text"]


class custom_agent:
    def __init__(
        self,
        textllm,
        chatllm,
        embeddings_model,
        name: str = None,
        age=None,
        agent_type: Agent_Type = None,
        traits: str = None,
        summary: str = None,
        inappropiates=None,
        chat_memlen: int = 10,
        load_memory=False,
        key_id=None,
        verbose=False,
    ):
        self.textllm = textllm
        self.chatllm = chatllm
        self.embeddings_model = embeddings_model

        self.name = name if name else ""
        self.age = age if age else 0
        self.agent_type = agent_type
        self.traits = traits if traits else ""
        self.summary = summary if summary else ""
        self.inappropiates = (
            text_from_inapp_list(inappropiates) if inappropiates else []
        )

        self.status = ""
        self.feelings = ""
        self.place = ""
        self.plan = []
        self.chat_history = []
        self.chat_hist_summary = ""

        self.chat_memlen = chat_memlen
        self.verbose = verbose
        self.data_path = f"agents/{self.name}/data"
        self.start_interview = False
        self.load_memory = load_memory
        self.key_id = key_id
        if self.load_memory:
            self.create_new_memory_retriever(embeddings_model=self.embeddings_model)
            if self.key_id == None:
                raise ValueError(
                    "If you set load_memory=True, you need to include key_id too!"
                )

        # limiter for GCP VertexAI Quota limit -> It is around 60 Requests per minute:RPM
        self.rate_limiter = RateLimiter(rate_limit=30, time_window=timedelta(minutes=1))

        if agent_type:
            # Check what type of agent, so we can import prompt and chat examples.
            self._check_agent_type()
            if load_memory == False:
                if self.verbose:
                    print("Create new memory")
                self.create_new_memory_retriever(embeddings_model=self.embeddings_model)
                self.add_character(self.summary.split("\n"))

            # Multithread process agent self summarization
            # set routine function
            self.start_routine_func(self._update_summary, 300)
            self.start_routine_func(self._update_status, 300)
            self.start_routine_func(self._update_place, 300)
        # with concurrent.futures.ThreadPoolExecutor() as executor:
        #     # Submit the functions with input parameters for concurrent execution
        #     summary_future = executor.submit(self._update_summary)
        #     status_future = executor.submit(self._update_status)
        #     place_future = executor.submit(self._update_place)
        #     futures = [summary_future, status_future, place_future]
        #     for future in concurrent.futures.as_completed(futures):
        #         # Handle any exceptions that occurred during execution
        #         try:
        #             result = future.result()
        #             # Handle the result if needed
        #         except Exception as e:
        #             # Handle the exception here
        #             print(f"An error occurred: {e}")

        if self.verbose:
            print("Finish create Generative Agent: {}".format(self.name))

    def __str__(self):
        return f"""name: {self.name}
age: {self.age}
traits: {self.traits}
summary: {self.summary}
status: {self.status}
feeling: {self.feelings}
at place: {self.place}
plan: {self.plan}
inapp_topics: {self.inappropiates}
chat_hist: {self.chat_history}
chat_summ: {self.chat_hist_summary }"""

    def create_new_memory_retriever(
        self,
        embeddings_model,
        score_weight: dict = dict({"time": 0.3, "importance": 0.1}),
    ):
        """Create a new vector store retriever unique to the agent."""
        # Define your embedding model

        # Initialize the vectorstore as empty
        embedding_size = 768  # 1536
        env = "gcp-starter"
        api = "c6a53942-0232-4c19-910e-f5425d294923"
        pinecone.init(
            api_key=api,  # find at app.pinecone.io
            environment=env,  # next to api key in console
        )
        index_name = "bel-agents"
        if self.load_memory == False:
            if index_name in pinecone.list_indexes():
                pinecone.delete_index(index_name)
            if index_name not in pinecone.list_indexes():
                pinecone.create_index(
                    name=index_name, metric="cosine", dimension=embedding_size
                )
                index = pinecone.Index(index_name=index_name)
        else:
            if index_name not in pinecone.list_indexes():
                pinecone.create_index(
                    name=index_name, metric="cosine", dimension=embedding_size
                )
                index = pinecone.Index(index_name=index_name)
            if index_name in pinecone.list_indexes():
                index = pinecone.Index(index_name=index_name)
        self.vectorstore = Pinecone(
            embedding=embeddings_model, index=index, text_key="text"
        )
        self.retriever = TimeWeightedVectorStoreRetrieverModified(
            vectorstore=self.vectorstore,
            score_weight=score_weight,
            other_score_keys=["importance"],
            k=5,
        )

    def _check_agent_type(self):
        self.lang = self.agent_type.value["lang"]
        self.kind = self.agent_type.value["kind"]
        module_name = f"generative_agent.conversation_examples"
        try:
            imported_module = importlib.import_module(module_name)
            print(imported_module)
            self.chat_examples = getattr(
                imported_module, f"{self.lang}_{self.kind}_CONV_EX"
            )
            self.guard_examples = getattr(
                imported_module, f"{self.lang}_{self.kind}_GUARD_EX"
            )
        except ModuleNotFoundError:
            print(
                f"{self.lang}_{self.kind}_CONV_EX or {self.lang}_{self.kind}_GUARD_EX is not implemented."
            )

        module_name = f"generative_agent.prompt.{self.lang.lower()}_prompt"
        try:
            self.prompt = importlib.import_module(module_name)
        except ModuleNotFoundError:
            print(f"{self.lang.lower()}_prompt is not implemented.")

    def start_routine_func(self, func, timesleep):
        t = threading.Thread(target=func, kwargs={"timesleep": timesleep})
        t.start()

    def add_character(self, list_of_character):
        threads = []
        for character in list_of_character:
            t = threading.Thread(
                target=self.add_memory_with_rate_limiting,
                args=(character, Mem_Type.BEHAVIOR.value),
            )
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

    def add_knowledge(self, list_of_knowledge):
        threads = []
        for knowledge in list_of_knowledge:
            t = threading.Thread(
                target=self.add_memory_with_rate_limiting,
                args=(knowledge, Mem_Type.KNOWLEDGE.value),
            )
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

    # Modify the add_memory function to include rate limiting
    def add_memory_with_rate_limiting(self, mem_info, mem_type):
        if self.verbose:
            print("adding memory...")

        mem_time = datetime.now()
        inps = {"mem": mem_info}
        rate = use_textllm_with_prompt(
            textllm=self.textllm,
            prompt_template=self.prompt.PROMPT_ADDMEM,
            inps=inps,
            verbose=self.verbose,
        )
        if len(rate) > 2:
            rate = 1
        rate_score = int(rate) / 10
        request = {
            "function": self.retriever.add_documents,
            "kwargs": {
                "documents": [
                    Document(
                        page_content=mem_info,
                        metadata={
                            "importance": rate_score,
                            "memory_type": mem_type,
                            "created_at": mem_time,
                        },
                    )
                ],
                "current_time": mem_time,
            },
        }  # Modified argument passing using kwargs

        self.rate_limiter.add_to_queue(request)

    def _update_summary(self, timesleep=None):
        while True:
            if self.verbose:
                print("update summary...")
            core_character = ""
            feeling = ""
            if len(self.retriever.memory_stream) != 0:
                core_character = self._get_core_character()
                feeling = self._get_feeling()
            description = core_character + " " + feeling
            if self.lang == "TH":
                self.summary = (
                    f"ชื่อ: {self.name} (อายุ: {self.age})"
                    + f"\nอุปนิสัย: {self.traits}"
                    + f"\nสรุปลักษณะของ{self.name}: {description}"
                )
            else:
                self.summary = (
                    f"Name: {self.name} (Age: {self.age})"
                    + f"\Traits: {self.traits}"
                    + f"\n{self.name}'s characteristics summary: {description}"
                )
            if timesleep:
                time.sleep(timesleep)

    def _update_status(self, timesleep=None):
        while True:
            if self.verbose:
                print("update status...")
            now = datetime.now()
            for each_plan in self.plan:
                if now >= each_plan["from"] and now <= each_plan["to"]:
                    self.status = each_plan["task"]
                    return
            else:
                self._get_plan()
                recently_task = self.plan[0]
                self.status = recently_task["task"]
            if timesleep:
                time.sleep(timesleep)

    def _update_place(self, timesleep=None):
        while True:
            if self.verbose:
                print("update place...")
            inps = {"name": self.name, "place": self.status}
            self.place = use_textllm_with_prompt(
                textllm=self.textllm,
                prompt_template=self.prompt.PROMPT_PLACE,
                inps=inps,
                verbose=self.verbose,
            )
            if timesleep:
                time.sleep(timesleep)

    def _update_chat_hist(self, timesleep):
        while True:
            if self.verbose:
                print("Chat summarizing...")
            if (self.chat_hist_summary == "" and len(self.chat_history) > 0) or len(
                self.chat_history
            ) >= self.chat_memlen:
                inps = {"chat_history": text_chat_hist(self.chat_history)}
                incoming_chatsum = use_textllm_with_prompt(
                    textllm=self.textllm,
                    prompt_template=self.prompt.PROMPT_CHATSUM,
                    inps=inps,
                    verbose=self.verbose,
                )
                inps = {"chatsum": self.chat_hist_summary + incoming_chatsum}
                self.chat_hist_summary = use_textllm_with_prompt(
                    textllm=self.textllm,
                    prompt_template=self.prompt.PROMPT_SUMHIST,
                    inps=inps,
                    verbose=self.verbose,
                )
                self.chat_history = []
                if self.verbose:
                    print("Chat summarized")
            if (
                self.verbose
                and self.chat_hist_summary == ""
                and len(self.chat_history) == 0
            ):
                print("sleep first because no chat history")
            time.sleep(timesleep)
            if self.verbose:
                print("Out from sleep")

    def _get_core_character(self):
        # CORE Character
        if self.verbose:
            print("get core characteristic...")
        query = (
            "ลักษณะสำคัญของ" + self.name + "คืออะไร"
            if self.lang == "TH"
            else "What is a core characteristic of " + self.name
        )
        print(query)
        docs = self.retriever.get_relevant_documents(
            query,
            current_time=datetime.now(),
            mem_type=Mem_Type.BEHAVIOR.value,
        )
        result = get_text_from_docs(docs)
        inps = {"name": self.name, "statements": result}
        core_charac = use_textllm_with_prompt(
            textllm=self.textllm,
            prompt_template=self.prompt.PROMPT_CORE,
            inps=inps,
            verbose=self.verbose,
        )
        return core_charac

    def _get_feeling(self):
        if self.verbose:
            print("get feeling...")
        query = (
            "ความรู้สึกเกี่ยวกับความก้าวหน้าในชีวิตล่าสุดของ" + self.name
            if self.lang == "TH"
            else "Feelings about recent progress in life of" + self.name
        )
        docs = self.retriever.get_relevant_documents(
            query,
            current_time=datetime.now(),
            mem_type=Mem_Type.BEHAVIOR.value,
        )
        statement = get_text_from_docs(docs)
        inps = {"name": self.name, "statements": statement}
        feel = use_textllm_with_prompt(
            textllm=self.textllm,
            prompt_template=self.prompt.PROMPT_FEELING,
            inps=inps,
            verbose=self.verbose,
        )
        return feel

    def _get_plan(self):
        inps = {
            "name": self.name,
            "datetime": get_thai_datetime(),
            "current_time": datetime.now().strftime("%H:%M"),
            "place": self.place,
            "summary": self.summary,
        }
        plan = use_textllm_with_prompt(
            textllm=self.textllm,
            prompt_template=self.prompt.PROMPT_PLAN,
            inps=inps,
            verbose=self.verbose,
        )
        plan = plan.split("\n")
        # clean
        plan = [p.lstrip().rstrip().replace("24", "00") for p in plan]
        for p in plan:
            if (
                not ("ตั้งแต่" in p or "From" in p)
                or not ("ถึง" in p or "to" in p)
                or not (":" in p)
                or (len(p.split(" ")) < 5)
            ):
                plan.remove(p)
        if self.verbose:
            print(plan)
        plan_list = []
        for task in plan:
            tmp = {}
            split_temp = task.split(" ")
            split_temp[0] = split_temp[0][1:]
            split_temp[3] = split_temp[3][:-2]

            today_date = datetime.today().date()

            from_time = datetime.strptime(split_temp[1], "%H:%M").time()
            from_datetime = datetime.combine(today_date, from_time)

            to_time = datetime.strptime(split_temp[3], "%H:%M").time()
            to_datetime = datetime.combine(today_date, to_time)

            tmp["from"] = from_datetime
            tmp["to"] = to_datetime
            tmp["task"] = split_temp[-1]
            plan_list.append(tmp)
        self.plan = plan_list

    def interview(self, user, query):
        docs = self.retriever.get_relevant_documents(
            query=query, current_time=datetime.now(), mem_type=Mem_Type.KNOWLEDGE.value
        )
        context = get_text_from_docs(docs)
        if not (self.start_interview):
            # start thread for updating chat summary every 5 minutes
            self.start_routine_func(self._update_chat_hist, 300)
            self.start_interview = True

        inps = {
            "current_time": get_thai_datetime(),
            "name": self.name,
            "status": self.status,
            "place": self.place,
            "summary": self.summary,
            "context": context,
            "exam_conversation": self.chat_examples.format(
                Player=user, Character=self.name
            ),
            "chatsum": self.chat_hist_summary,
            "chat_history": self.chat_history,
            "user": user,
            "question": query,
        }
        self.chat_history.append("{}: {}".format(user, query))
        # response = self._guarding(query)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Submit the functions with input parameters for concurrent execution
            guard = executor.submit(self._guarding, question=query)
            interview = executor.submit(
                use_chatllm_with_prompt,
                chatllm=self.chatllm,
                prompt_template=self.prompt.PROMPT_INTERVIEW,
                inps=inps,
                verbose=self.verbose,
            )

            # Retrieve the return values from the futures
        guard_resp = guard.result()
        int_resp = interview.result()
        if self.verbose:
            print("Guard response: {}".format(guard_resp))
            print("Interview response: {}".format(int_resp))
        if guard_resp["related"]:
            guard_resp["emotion"] = "Neutral"
            self.chat_history.append("{}: {}".format(self.name, guard_resp["response"]))
            return guard_resp
        self.chat_history.append("{}: {}".format(self.name, int_resp))
        return json.loads(int_resp)

    def save_state_memory(self):
        if not os.path.isdir(self.data_path):
            os.makedirs(self.data_path, exist_ok=True)
        self.vectorstore.save_local(self.data_path)
        mem = self.retriever.memory_stream
        fileObj = open(os.path.join(self.data_path, "memory_stream.pkl"), "wb")
        pickle.dump(mem, fileObj)
        fileObj.close()
        infos = {
            "name": self.name,
            "age": self.age,
            "traits": self.traits,
            "summary": self.summary,
            "status": self.status,
            "feelings": self.feelings,
            "place": self.place,
            "plan": json.dumps(
                [
                    {
                        "from": item["from"].isoformat(),
                        "to": item["to"].isoformat(),
                        "task": item["task"],
                    }
                    for item in self.plan
                ]
            ),
            "chat_history": self.chat_history,
            "inappropiates": self.inappropiates,
            "chat_hist_summary": self.chat_hist_summary,
            "chat_memlen": self.chat_memlen,
            "verbose": self.verbose,
        }
        with open(os.path.join(self.data_path, "infos.json"), "w") as f:
            json.dump(infos, f)
        self.db.save_custom_agent(self, self.data_path)

    def _guarding(self, question):
        inps = {
            "name": self.name,
            "inappropiate_topic": self.inappropiates,
            "guard_exam": self.guard_examples.format(name=self.name),
            "chatsum": self.chat_hist_summary,
            "question": question,
        }
        response = use_chatllm_with_prompt(
            chatllm=self.chatllm,
            prompt_template=self.prompt.PROMPT_GUARD,
            inps=inps,
            verbose=self.verbose,
        )
        if (
            response.lstrip()
            == "I'm not able to help with that, as I'm only a language model. If you believe this is an error, please send us your feedback."
        ):
            if self.lang == "TH":
                response = (
                    f"{self.name}ไม่สามารถสนทนาเกี่ยวกับเรื่องที่คุณพูดถึงได้จริงๆ"
                )
            else:
                response = f"{self.name} can't really have a conversation about the topic you're talking about."
            return {
                "related": True,
                "type": "unknown",
                "response": response,
            }
        print(response)
        response = json.loads(response.lstrip())
        return response
