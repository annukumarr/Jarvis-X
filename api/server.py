from fastapi import FastAPI, Cookie
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


from brain.ai import ask_ai

from brain.knowledge import (
    build_legacy_context,
    SOCIAL,
    CONTACT,
    PROJECTS,
)

from brain.visitor_scope import (
    is_legacy_related,
    get_visitor_scope_response,
)

from brain.intent_router import route_intent

from brain.action_manager import (
    check_command,
    handle_confirmation,
)

from brain.pending_action import (
    get_pending_action,
)

from brain.action_executor import (
    execute_action,
)


from commands.memory import handle_memory


from api.analytics import (
    create_visitor_session,
    update_session,
    save_visitor_event,
    get_analytics_summary,
)


from database.memory_db import (
    save_memory as db_save_memory,
    get_memory as db_get_memory,
    get_all_memories as db_get_all_memories,
)


from api.auth import router as auth_router
from api.auth import is_owner


# ==========================================================
# FASTAPI APPLICATION
# ==========================================================

app = FastAPI(
    title="JARVIS-X API",
    version="1.0.0",
    description=(
        "JARVIS-X intelligence API for Legacy portfolio."
    ),
)


# ==========================================================
# CORS
# ==========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================================
# AUTHENTICATION
# ==========================================================

app.include_router(auth_router)


# ==========================================================
# KNOWLEDGE
# ==========================================================

LEGACY_CONTEXT = build_legacy_context()


# ==========================================================
# OWNER CONTEXT
# ==========================================================

OWNER_CONTEXT = """
==========================================================
IDENTITY MODE: OWNER
==========================================================

The authenticated user is the owner of JARVIS-X.

The owner is Boss.

You may address the authenticated owner as "Boss".

Private owner memory may be accessed only after
successful owner authentication.
"""


# ==========================================================
# VISITOR CONTEXT
# ==========================================================

USER_CONTEXT = """
==========================================================
IDENTITY MODE: VISITOR
==========================================================

The current user is a normal visitor of the Legacy
portfolio.

Do NOT call this user "Boss".

Never reveal private owner memory.

Only answer questions that are related to Legacy,
its projects, technologies, features, work, public
information, navigation, or JARVIS-X as part of Legacy.

Do NOT answer unrelated general-knowledge questions.

If a visitor asks something outside Legacy scope,
return the standard Legacy scope response.

If a visitor asks for private owner information,
politely refuse to provide it.
"""


# ==========================================================
# REQUEST MODELS
# ==========================================================

class ChatRequest(BaseModel):
    message: str


class MemoryRequest(BaseModel):
    category: str
    key: str
    value: str


class MemoryLookupRequest(BaseModel):
    category: str
    key: str


class AnalyticsSessionRequest(BaseModel):
    visitor_id: str | None = None
    page: str | None = None
    referrer: str | None = None


class AnalyticsEventRequest(BaseModel):
    visitor_id: str
    session_id: str
    event_type: str
    event_data: dict | None = None


class AnalyticsUpdateRequest(BaseModel):
    visitor_id: str
    session_id: str
    page: str | None = None


# ==========================================================
# NAVIGATION RESPONSE MAP
# ==========================================================

NAVIGATION_ACTIONS = {

    "navigate_home": {
        "action": "home",
        "message": "Taking you home.",
    },

    "navigate_projects": {
        "action": "projects",
        "message": "Opening the projects section.",
    },

    "navigate_journey": {
        "action": "journey",
        "message": "Opening the journey section.",
    },

    "navigate_contact": {
        "action": "contact",
        "message": "Opening the contact section.",
    },

}


# ==========================================================
# SOCIAL RESPONSES
# ==========================================================

def get_social_response(intent: str):

    """
    Return deterministic public social information.

    This avoids unnecessary AI hallucination for
    exact public profile information.
    """

    if intent == "instagram":

        return {
            "response": (
                "You can find Annu on Instagram at "
                "@annuofficiall__."
            ),
            "url": SOCIAL["instagram"]["url"],
        }


    if intent == "linkedin":

        return {
            "response": (
                "You can connect with Annu on LinkedIn "
                "through his public profile."
            ),
            "url": SOCIAL["linkedin"]["url"],
        }


    if intent == "github":

        return {
            "response": (
                "Annu's GitHub username is "
                "annukumarr."
            ),
            "url": SOCIAL["github"]["url"],
        }


    if intent == "email":

        return {
            "response": (
                "You can contact Annu at "
                f"{CONTACT['email']}."
            ),
            "url": None,
        }


    return None


# ==========================================================
# PROJECT RESPONSE
# ==========================================================

def get_projects_response():

    """
    Return public project information directly
    from the structured knowledge layer.
    """

    project_lines = []


    for project in PROJECTS.values():

        project_lines.append(
            f"• {project['name']}: "
            f"{project['description']}"
        )


    return (
        "Here are Annu's main projects:\n\n"
        + "\n".join(project_lines)
    )


# ==========================================================
# HEALTH CHECK
# ==========================================================

@app.get("/")
def root():

    return {
        "status": "online",
        "name": "JARVIS-X",
        "version": "1.0.0",
    }


# ==========================================================
# CHAT
# ==========================================================

@app.post("/api/chat")
def chat(
    request: ChatRequest,
    jarvis_owner_token: str | None = Cookie(default=None),
):

    message = request.message.strip()


    if not message:

        return {
            "success": False,
            "response": "Please provide a message.",
        }


    # ======================================================
    # DETERMINE USER ROLE
    # ======================================================

    owner = is_owner(
        jarvis_owner_token
    )


    # ======================================================
    # PENDING CONFIRMATION
    #
    # IMPORTANT:
    # Confirmation must be checked BEFORE normal
    # intent processing.
    #
    # Otherwise "yes" / "no" would go to AI.
    # ======================================================

    pending = get_pending_action()


    if pending is not None:

        # --------------------------------------------------
        # Visitor protection
        # --------------------------------------------------

        if not owner:

            return {
                "success": True,
                "response": (
                    "There is no visitor-accessible "
                    "confirmation workflow."
                ),
                "source": "security",
                "role": "user",
                "confirmation_required": False,
            }


        # --------------------------------------------------
        # Handle YES / NO
        # --------------------------------------------------

        confirmation = handle_confirmation(
            message
        )


        # --------------------------------------------------
        # UNKNOWN CONFIRMATION RESPONSE
        # --------------------------------------------------

        if confirmation is not None:


            # ==============================================
            # CONFIRMED
            # ==============================================

            if confirmation["confirmed"] is True:

                action = confirmation["action"]
                data = confirmation["data"]


                response = execute_action(
                    action,
                    data,
                )


                return {
                    "success": True,
                    "response": response,
                    "source": "action_executor",
                    "role": "owner",
                    "intent": "system_action",
                    "route": "system_action",
                    "action": action,
                    "confirmation_required": False,
                    "confirmed": True,
                }


            # ==============================================
            # CANCELLED
            # ==============================================

            if confirmation["confirmed"] is False:

                action = confirmation["action"]


                if action == "delete_file":

                    action_name = "Delete"

                else:

                    action_name = action.capitalize()


                return {
                    "success": True,
                    "response": (
                        f"{action_name} action "
                        f"cancelled, Boss."
                    ),
                    "source": "confirmation",
                    "role": "owner",
                    "intent": "system_action",
                    "route": "system_action",
                    "action": action,
                    "confirmation_required": False,
                    "confirmed": False,
                }


            # ==============================================
            # UNKNOWN RESPONSE
            # ==============================================

            return {
                "success": True,
                "response": (
                    "Please answer yes or no, Boss."
                ),
                "source": "confirmation",
                "role": "owner",
                "intent": "system_action",
                "route": "system_action",
                "action": pending["action"],
                "confirmation_required": True,
            }


    # ======================================================
    # DETECT INTENT
    # ======================================================

    routed = route_intent(
        message
    )

    intent = routed["intent"]
    route = routed["route"]


    # ======================================================
    # SYSTEM ACTION
    # ======================================================

    if route == "system_action":

        # --------------------------------------------------
        # VISITOR SECURITY
        # --------------------------------------------------

        if not owner:

            return {
                "success": True,
                "response": (
                    "That is an owner-only system action. "
                    "I cannot execute system commands for "
                    "visitors."
                ),
                "source": "security",
                "role": "user",
                "intent": intent,
                "route": route,
                "confirmation_required": False,
            }


        # --------------------------------------------------
        # CREATE LOCAL CONFIRMATION
        # --------------------------------------------------

        confirmation_message = check_command(
            message
        )


        # --------------------------------------------------
        # CONFIRMATION CREATED
        # --------------------------------------------------

        if confirmation_message:

            pending_action = get_pending_action()


            return {
                "success": True,
                "response": confirmation_message,
                "source": "action_manager",
                "role": "owner",
                "intent": intent,
                "route": route,
                "action": (
                    pending_action["action"]
                    if pending_action
                    else routed.get("action")
                ),
                "confirmation_required": True,
            }


        # --------------------------------------------------
        # SAFETY FALLBACK
        # --------------------------------------------------

        return {
            "success": True,
            "response": (
                "I could not prepare that system action "
                "for confirmation, Boss."
            ),
            "source": "action_manager",
            "role": "owner",
            "intent": intent,
            "route": route,
            "confirmation_required": False,
        }


    # ======================================================
    # NAVIGATION
    # ======================================================

    if route == "navigation":

        navigation = NAVIGATION_ACTIONS.get(
            intent
        )


        if navigation:

            return {
                "success": True,
                "response": navigation["message"],
                "source": "navigation",
                "role": (
                    "owner"
                    if owner
                    else "user"
                ),
                "intent": intent,
                "route": route,
                "action": navigation["action"],
            }


    # ======================================================
    # SOCIAL
    # ======================================================

    if route == "social":

        social = get_social_response(
            intent
        )


        if social:

            result = {
                "success": True,
                "response": social["response"],
                "source": "knowledge",
                "role": (
                    "owner"
                    if owner
                    else "user"
                ),
                "intent": intent,
                "route": route,
            }


            if social["url"]:

                result["url"] = social["url"]


            return result


    # ======================================================
    # PUBLIC PROJECTS
    # ======================================================

    if (
        route == "information"
        and intent == "projects"
    ):

        return {
            "success": True,
            "response": get_projects_response(),
            "source": "knowledge",
            "role": (
                "owner"
                if owner
                else "user"
            ),
            "intent": intent,
            "route": route,
        }


    # ======================================================
    # MEMORY
    # OWNER ONLY
    # ======================================================

    if route == "memory":

        if not owner:

            return {
                "success": True,
                "response": (
                    "Private JARVIS-X memory is available "
                    "only to the owner."
                ),
                "source": "security",
                "role": "user",
                "intent": intent,
                "route": route,
            }


        memory_response = handle_memory(
            message
        )


        if memory_response:

            return {
                "success": True,
                "response": memory_response,
                "source": "memory",
                "role": "owner",
                "intent": intent,
                "route": route,
            }


        # --------------------------------------------------
        # AI FALLBACK
        # --------------------------------------------------

        contextual_message = f"""
{LEGACY_CONTEXT}

{OWNER_CONTEXT}

The user is the authenticated owner.

The user is asking about JARVIS-X memory.

USER QUESTION:

{message}
"""


        response = ask_ai(
            contextual_message
        )


        return {
            "success": True,
            "response": response,
            "source": "ai",
            "role": "owner",
            "intent": intent,
            "route": route,
        }


    # ======================================================
    # VISITOR LEGACY SCOPE GUARD
    # ======================================================
    #
    # Visitor JARVIS-X is strictly limited to Legacy.
    # Unrelated questions must never reach the AI model.
    #
    # Owner mode is intentionally untouched.
    # ======================================================

    if not owner and not is_legacy_related(message):

        return {
            "success": True,
            "response": get_visitor_scope_response(),
            "source": "scope_guard",
            "role": "user",
            "intent": intent,
            "route": route,
        }


    # ======================================================
    # INFORMATION / GENERAL AI
    # ======================================================

    contextual_message = f"""
{LEGACY_CONTEXT}

{"OWNER MODE:" if owner else "VISITOR MODE:"}

{OWNER_CONTEXT if owner else USER_CONTEXT}

==========================================================
DETECTED INTENT
==========================================================

Intent:
{intent}

Route:
{route}

==========================================================
USER QUESTION
==========================================================

{message}
"""


    response = ask_ai(
        contextual_message
    )


    return {
        "success": True,
        "response": response,
        "source": "ai",
        "role": (
            "owner"
            if owner
            else "user"
        ),
        "intent": intent,
        "route": route,
    }


# ==========================================================
# MEMORY — SAVE
# OWNER ONLY
# ==========================================================

@app.post("/api/memory/save")
def save_memory_endpoint(
    request: MemoryRequest,
    jarvis_owner_token: str | None = Cookie(default=None),
):

    if not is_owner(
        jarvis_owner_token
    ):

        return {
            "success": False,
            "message": (
                "Owner authentication required."
            ),
            "role": "user",
        }


    category = request.category.strip()
    key = request.key.strip()
    value = request.value.strip()


    if not category or not key or not value:

        return {
            "success": False,
            "message": (
                "Category, key and value are required."
            ),
        }


    db_save_memory(
        category,
        key,
        value,
    )


    return {
        "success": True,
        "message": "Memory saved successfully.",
        "category": category,
        "key": key,
        "role": "owner",
    }


# ==========================================================
# MEMORY — GET ONE
# OWNER ONLY
# ==========================================================

@app.post("/api/memory/get")
def get_memory_endpoint(
    request: MemoryLookupRequest,
    jarvis_owner_token: str | None = Cookie(default=None),
):

    if not is_owner(
        jarvis_owner_token
    ):

        return {
            "success": False,
            "memory": None,
            "message": (
                "Owner authentication required."
            ),
            "role": "user",
        }


    category = request.category.strip()
    key = request.key.strip()


    if not category or not key:

        return {
            "success": False,
            "memory": None,
            "message": (
                "Category and key are required."
            ),
        }


    value = db_get_memory(
        category,
        key,
    )


    return {
        "success": True,
        "category": category,
        "key": key,
        "memory": value,
        "role": "owner",
    }


# ==========================================================
# MEMORY — GET ALL
# OWNER ONLY
# ==========================================================

@app.get("/api/memory")
def get_all_memory_endpoint(
    jarvis_owner_token: str | None = Cookie(default=None),
):

    if not is_owner(
        jarvis_owner_token
    ):

        return {
            "success": False,
            "memories": None,
            "message": (
                "Owner authentication required."
            ),
            "role": "user",
        }


    memories = db_get_all_memories()


    return {
        "success": True,
        "memories": memories,
        "role": "owner",
    }


# ==========================================================
# ANALYTICS — CREATE SESSION
# ==========================================================

@app.post("/api/analytics/session")
def analytics_session(
    request: AnalyticsSessionRequest,
):

    result = create_visitor_session(
        visitor_id=request.visitor_id,
        page=request.page,
        referrer=request.referrer,
    )


    return {
        "success": True,
        "visitor_id": result["visitor_id"],
        "session_id": result["session_id"],
    }


# ==========================================================
# ANALYTICS — UPDATE SESSION
# ==========================================================

@app.post("/api/analytics/session/update")
def analytics_session_update(
    request: AnalyticsUpdateRequest,
):

    update_session(
        visitor_id=request.visitor_id,
        session_id=request.session_id,
        page=request.page,
    )


    return {
        "success": True,
        "message": "Visitor session updated.",
    }


# ==========================================================
# ANALYTICS — SAVE EVENT
# ==========================================================

@app.post("/api/analytics/event")
def analytics_event(
    request: AnalyticsEventRequest,
):

    save_visitor_event(
        visitor_id=request.visitor_id,
        session_id=request.session_id,
        event_type=request.event_type,
        event_data=request.event_data,
    )


    return {
        "success": True,
        "message": "Visitor event recorded.",
    }


# ==========================================================
# ANALYTICS — SUMMARY
# OWNER ONLY
# ==========================================================

@app.get("/api/analytics")
def analytics_endpoint(
    jarvis_owner_token: str | None = Cookie(default=None),
):

    if not is_owner(
        jarvis_owner_token
    ):

        return {
            "success": False,
            "analytics": None,
            "message": (
                "Owner authentication required."
            ),
            "role": "user",
        }


    analytics = get_analytics_summary()


    return {
        "success": True,
        "analytics": analytics,
        "role": "owner",
    }