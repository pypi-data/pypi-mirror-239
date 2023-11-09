"""
Notes

TODO determine if should leverage prefect or other system to manage
dependencies

move to asyncio.TaskGroup() when Python 3.11 is supported
async with asyncio.TaskGroup() as tg:
    intent = tg.create_task(self.get_intent(context))
    introspection = tg.create_task(self.introspect(context))
"""
import asyncio
import datetime
import logging
import time
import uuid

from promptedgraphs.config import Config
from promptedgraphs.data_extraction import extract_data
from promptedgraphs.entity_recognition import extract_entities
from rich import print

from taskforceagents.models import (
    AgentContext,
    ConversationMessage,
    DefaultStateModel,
    EventType,
    UserIntent,
)
from taskforceagents.sse_helpers import sse_chatevent, sse_done, sse_stop, sse_text

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def green(s: str):
    return f"\033[32m{s}\033[0m"


def gpt_entity_mentions(*args, **kwargs):
    print((args, kwargs))
    raise NotImplementedError(
        "gpt_entity_mentions is not implemented review implementation in quantready_vendor.pipeline.nlp_openai"
    )


def format_as_context(msg: any) -> AgentContext:
    if isinstance(msg, str):
        return AgentContext(
            history=[
                ConversationMessage(
                    username="user", event=EventType.MESSAGE, message=msg
                )
            ]
        )
    elif isinstance(msg, ConversationMessage):
        return AgentContext(history=[msg])
    elif isinstance(msg, list):
        return AgentContext(history=msg)
    elif isinstance(msg, AgentContext):
        return msg
    else:
        raise ValueError(f"Cannot format {type(msg)} as AgentContext")


def to_sse(msg: ConversationMessage) -> dict:
    msg_id = str(uuid.uuid4())
    if msg.event != EventType.EVENT:
        return sse_text(msg.message, role=msg.username, id=msg_id)
    details = {
        k: v for k, v in msg.model_dump().items() if k not in ["message", "name", "id"]
    }
    return sse_chatevent(msg.message, msg.username, id=msg_id, **details)


class AIAgent:
    """The AI Agent class."""

    def __init__(
        self,
        name="agent",
        system_message="You are an AI Agent built by ClosedLoop Technologies.",
        config=None,
        output_format="cli",
        dso_labels: dict[str, str] | None = None,
        workflow_state_model=None,
        understanding_prompts: list[str] | None = None,
    ):
        """Initialize the AI Agent."""
        self.config = config

        assert output_format in ["cli", "sse", "http"]
        self.name = name
        self.output_format = output_format
        self.dso_labels = dso_labels or {}
        self.workflow_state_model = workflow_state_model or DefaultStateModel
        self.understanding_prompts = understanding_prompts or []
        self.system_message = (
            system_message or "You are an AI Agent, you shall do no harm."
        )

    async def emit(self, event: AgentContext | ConversationMessage):
        """Outputs events to appropriate channels"""
        if event is None:
            return
        if isinstance(event, AgentContext):
            if len(event.history) == 0:
                return
            msg = event.history[-1]
        else:
            msg = event

        if self.output_format == "sse":
            return to_sse(msg)
        elif self.output_format == "http":
            return msg.to_json()
        elif self.output_format == "cli":
            print(f"> {msg.username}: {msg}")
            return
        else:
            raise NotImplementedError(
                f"Output format {self.output_format} not implemented"
            )

    async def execute(self, msg: str = "Hello World!"):
        async for response in self.ooda_loop(msg):
            yield response

        if self.output_format == "sse":
            yield sse_stop()
            yield sse_done()

    async def async_run(self, msg: str = "Hello World!"):
        """Run the AI Agent asynchronously."""
        try:
            tuple([i async for i in self.execute(msg=msg)])
            logger.info("completed")
        except ValueError as e:
            logger.error(e)

    def run(self, msg: str = "Hello World!"):
        loop = asyncio.get_event_loop()
        task = loop.create_task(self.async_run(msg=msg))
        try:
            loop.run_until_complete(task)
        except KeyboardInterrupt:
            loop.stop()
        finally:
            loop.close()

    async def ooda_loop(self, msg: str):
        """Run the AI Agent asynchronously.
        1. Receives a message or subscribes to a queue
        1. Reformats the message using to have the AgentConverstation format
        2. `Observing` models: `intent` and `introspection`, `understanding`
        3. `Orienting` models: `enrichment` and `orientation` models
        4. `Deciding` models: `enrichment` and `planning` models
        - Computationally expensive, so we want to do this as little as possible
        5. `Acting` models: `selection`, `configuration`, `execution`, `communication` models
        """
        yield await self.emit(
            ConversationMessage(
                username="agent",
                event=EventType.EVENT,
                message=f"Received message: {msg}",
            )
        )
        context = format_as_context(msg)
        yield await self.emit(context)

        print(f"Observing at {time.strftime('%X')}")
        state = {}

        async for k, v in self.step_observing(context):
            # TODO support streaming deltas
            state[k] = v
            print(f"------------ {time.strftime('%X')} {k}")
            yield await self.emit(v)

        print(f"Orienting at {time.strftime('%X')}")
        async for k, v in self.step_orienting(context):
            # TODO support streaming deltas
            state[k] = v
            print(f"------------ {time.strftime('%X')} {k}")
            yield await self.emit(v)

        print(f"Deciding at {time.strftime('%X')}")
        async for k, v in self.step_deciding(context):
            # TODO support streaming deltas
            state[k] = v
            print(f"------------ {time.strftime('%X')} {k}")
            yield await self.emit(v)

        print(f"Acting at {time.strftime('%X')}")
        async for k, v in self.step_acting(context):
            # TODO support streaming deltas
            state[k] = v
            print(f"------------ {time.strftime('%X')} {k}")
            yield await self.emit(v)

    async def step_observing(self, context: AgentContext):
        # Set of pending tasks to track which ones we're still waiting for
        pending_tasks = {
            asyncio.create_task(self.enrich_intents(context)),
            asyncio.create_task(self.enrich_state(context)),
            asyncio.create_task(self.enrich_understanding(context)),
        }

        if context and len(context.history) > 0:
            msg = context.history[-1]
            if msg.message:
                for i, prompt in enumerate(self.understanding_prompts):
                    pending_tasks.add(
                        asyncio.create_task(
                            self.enrich_custom_understanding(
                                msg.message or "", prompt, name=f"understanding_{i}"
                            )
                        )
                    )

        while pending_tasks:
            # Wait for the first task to complete
            done, _ = await asyncio.wait(
                pending_tasks, return_when=asyncio.FIRST_COMPLETED
            )
            for task in done:
                yield await task
            # Remove the completed tasks from our set of pending tasks
            pending_tasks -= done

    async def step_orienting(self, context: AgentContext):
        pending_tasks = {
            asyncio.create_task(self.enrich(context)),
            asyncio.create_task(self.orient(context)),
        }

        while pending_tasks:
            done, _ = await asyncio.wait(
                pending_tasks, return_when=asyncio.FIRST_COMPLETED
            )
            for task in done:
                yield await task
            pending_tasks -= done

    async def step_deciding(self, context: AgentContext):
        # Set of pending tasks to track which ones we're still waiting for
        pending_tasks = {
            asyncio.create_task(self.plan(context)),
        }

        while pending_tasks:
            # Wait for the first task to complete
            done, _ = await asyncio.wait(
                pending_tasks, return_when=asyncio.FIRST_COMPLETED
            )
            for task in done:
                yield await task
            # Remove the completed tasks from our set of pending tasks
            pending_tasks -= done

    async def step_acting(self, context: AgentContext):
        # `selection`, `configuration`, `execution`
        pending_tasks = {}
        while pending_tasks:
            # Wait for the first task to complete
            done, _ = await asyncio.wait(
                pending_tasks, return_when=asyncio.FIRST_COMPLETED
            )
            for task in done:
                yield await task
            # Remove the completed tasks from our set of pending tasks
            pending_tasks -= done

    ### OBSERVING FUNCTIONS ###
    async def enrich_intents(self, context: AgentContext):
        """Enrich message contexts and yield any updates."""

        new_intents = []
        for msg in context.history:
            if msg.event != EventType.MESSAGE:
                break
            if (
                msg.role in ["system", "assistant", "agent", "bot"]
                or msg.username
                in [
                    "system",
                    "assistant",
                    "agent",
                    "bot",
                ]
                or msg.username.startswith("example_")
            ):
                break
            if msg.intents and len(msg.intents) > 0:
                break
            if msg.message is None or len(msg.message) == 0:
                break

            intents = []
            async for intent in extract_data(
                text=msg.message, output_type=list[UserIntent], config=Config()
            ):
                intents.append(intent)

            msg.intents = intents
            new_intents.extend(intents)

        return (
            "intent",
            ConversationMessage(
                username="agent",
                event=EventType.EVENT,
                message="intents",
                intents=new_intents,
            )
            if new_intents
            else None,
        )

    async def introspect(self, context: AgentContext):
        """Introspect the message."""
        # TODO compare the embedding of the message to the embedding of similar requests
        # to determine likely success of the request and cost
        return "introspection", None

    async def enrich_custom_understanding(
        self, text: str, prompt, name="understanding"
    ):
        new_ents = gpt_entity_mentions(
            text=text,
            prompt=prompt,
            model_name="gpt-3.5-turbo-0613",
            temperature=0.0,
            today=datetime.datetime.now().strftime("%Y-%m-%d"),
        )
        return (
            name,
            ConversationMessage(
                username="agent",
                event=EventType.EVENT,
                message="entities",
                entities=new_ents,
            )
            if new_ents
            else None,
        )

    async def enrich_understanding(self, context: AgentContext):
        """Enrich message contexts and yield new Domain Specific Ontology labels in the messages"""

        new_ents = []
        for msg in context.history:
            if msg.event != EventType.MESSAGE:
                break
            if msg.username in ["system"] or msg.username.startswith("example_"):
                break
            if msg.entities and len(msg.entities) > 0:
                break
            if msg.message is None or len(msg.message) == 0:
                break

            entities = []
            async for entity in extract_entities(
                text=msg.message,
                labels=self.dso_labels,
                temperature=0.0,
                config=Config(),
            ):
                entities.append(entity)

            msg.entities = entities
            new_ents.extend(entities)

        return (
            "understanding",
            ConversationMessage(
                username="agent",
                event=EventType.EVENT,
                message="entities",
                entities=new_ents,
            )
            if new_ents
            else None,
        )

    async def enrich_state(self, context: AgentContext):
        """Enrich message contexts and yield new Domain Specific Ontology labels in the messages"""
        # State is a dictionary that is updated with each message
        updated = False
        new_state = {}
        for msg in context.history:
            if msg.event != EventType.MESSAGE:
                break
            if msg.username in ["system"] or msg.username.startswith("example_"):
                break
            if msg.state and len(msg.state) > 0:
                new_state = msg.state  # self.workflow_state_model(**msg.state)
                break
            if msg.message is None or len(msg.message) == 0:
                break

            async for state in extract_data(
                text=msg.message, output_type=self.workflow_state_model, config=Config()
            ):
                s = state.model_dump(
                    exclude_defaults=True, exclude_unset=True, exclude_none=True
                )
                for k, v in s.items():
                    updated = True
                    new_state[k] = v

            if updated is False:
                labels = {
                    k: f"{v.get('description', v.get('title',''))}".strip()
                    for k, v in self.workflow_state_model.model_json_schema()
                    .get("properties")
                    .items()
                }

                async for state in extract_entities(
                    text=msg.message, labels=labels, temperature=0.0, config=Config()
                ):
                    updated = True
                    new_state[state.label] = state.text
            msg.state = new_state
        return (
            "state",
            ConversationMessage(
                username="agent",
                event=EventType.EVENT,
                message="state",
                state=new_state,
            )
            if updated
            else None,
        )

    ### ORIENTING FUNCTIONS ###
    async def enrich(self, context: AgentContext):
        """Create queries to .
        Apply Domain Specific Ontology to label entities in the messages

        In this example context.history[0].locations -> google maps
        context.history[0].entities of type DSO

        DS0 - DG

        message_id -> entity_reference_by_type -> DSO to link to cannonical entities

        Context = DG enriched with the DSO

        """

    async def orient(self, context: AgentContext):
        """Understand which workflow to use and where we are in the workflow."""
        # await asyncio.sleep(2)
        return "orientation", ConversationMessage(
            username="agent",
            event=EventType.EVENT,
            message=f"Understood: {context}",
        )

    async def plan(self, context: AgentContext):
        """Chain together several actions."""
        # await asyncio.sleep(2)
        return "plan", ConversationMessage(
            username="agent",
            event=EventType.EVENT,
            message=f"Understood: {context}",
        )
