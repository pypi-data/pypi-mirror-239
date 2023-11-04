import datetime
import uuid
from enum import Enum

from promptedgraphs.models import EntityReference
from pydantic import BaseModel, Field

from taskforceagents.models import UserIntent


class EventType(Enum):
    MESSAGE = "message"
    EVENT = "event"


class ConversationMessage(BaseModel):
    username: str
    role: str = "assistant"
    msg_id: str = str(uuid.uuid4())
    user_id: str | None = None
    event: EventType = EventType.MESSAGE
    message: str | None = None
    created_at: datetime.datetime = datetime.datetime.now(datetime.timezone.utc)
    entities: list[EntityReference] = []
    intents: list[UserIntent] = []
    embeddings: list[dict] = []
    state: dict = {}
    context: dict = {}


class AgentContext(BaseModel):
    history: list[ConversationMessage] = []


class DefaultStateModel(BaseModel):
    """Defines the workflow state types for the AI Agent."""

    user_emotion: str | None = Field(None, title="Implied emotional state of the user")


class Property(BaseModel):
    """The property class."""

    name: str = Field(
        title="Property Name",
        description="Name of the property",
        examples=["age", "address", "ingredientQuantity"],
    )
    data_type: str = Field(
        title="Data Type",
        description="Data type of the property",
        examples=["string", "int", "float"],
    )
    description: str | None = Field(
        title="Property Description",
        description="Description of what the property represents",
    )


class Relationship(BaseModel):
    """The relationship class."""

    name: str = Field(
        title="Relationship Name",
        description="Name of the relationship",
        examples=["contains", "belongs_to", "produced_by"],
    )
    target_entity: str = Field(
        title="Target Entity",
        description="The entity this relationship points to",
        examples=["Recipe", "RecipeIngredient", "Manufacturer"],
    )
    description: str | None = Field(
        title="Relationship Description",
        description="Description of what the relationship represents",
    )


class Entities(BaseModel):
    """The entities class."""

    name: str = Field(
        title="Entity Name",
        description="Canonical entity name in title case with no spaces",
        examples=["Person", "Recipe", "RecipeIngredient"],
    )
    description: str = Field(
        title="Concise definition entities of this type",
        description="A detailed and specific description",
    )
    properties: list[Property] = Field(
        default=[],
        title="Properties",
        description="List of properties that this entity has",
    )
    relationships: list[Relationship] = Field(
        default=[],
        title="Relationships",
        description="List of relationships that this entity has with other entities",
    )


class UserIntent(BaseModel):
    """The UserIntent entity, representing the canonical description of what a user desires to achieve in a given conversation."""

    intent_name: str = Field(
        title="Intent Name",
        description="Canonical name of the user's intent",
        examples=[
            "ask_question",
            "issue_command",
            "get_clarification",
            "chit_chat",
            "give_feedback",
            "nonsensical",
            "greeting",
            "closing",
            "harrass",
            "unknown",
        ],
    )
    description: str | None = Field(
        title="Intent Description",
        description="A detailed explanation of the user's intent",
    )
