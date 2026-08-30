"""
brain/knowledge.py

Structured public knowledge for JARVIS-X.

This module contains only public Legacy / Annu Pal
information that JARVIS-X is allowed to provide
to normal visitors.

Private owner memory is NOT stored here.
"""


# ==========================================================
# IDENTITY
# ==========================================================

IDENTITY = {
    "name": "Annu Pal",
    "full_name": "Annu Kumar Pal",
    "role": "AI / ML Engineer",
    "education": (
        "MCA — Artificial Intelligence & Machine Learning "
        "at Chandigarh University, Mohali"
    ),
}


# ==========================================================
# CURRENT FOCUS
# ==========================================================

CURRENT_FOCUS = {
    "building": "Legacy v2 Portfolio",
    "learning": "LLMs & AI Agents",
    "next_project": "JARVIS-X AI Assistant",
    "goal": "AI Internship 2027",
}


# ==========================================================
# LEGACY
# ==========================================================

LEGACY = {
    "name": "Legacy",
    "description": (
        "Annu Kumar Pal's personal AI/ML engineering portfolio."
    ),
    "purpose": (
        "An interactive AI-focused engineering platform "
        "where visitors can explore Annu's work, projects, "
        "technical journey, and interact with JARVIS-X."
    ),
    "technologies": [
        "Next.js",
        "React",
        "TypeScript",
        "Tailwind CSS",
        "Motion / animations",
        "FastAPI",
        "Python",
        "JARVIS-X integration",
    ],
}


# ==========================================================
# PROJECTS
# ==========================================================

PROJECTS = {
    "JARVIS-X": {
        "name": "JARVIS-X",
        "description": (
            "An AI operating system / intelligent assistant "
            "project and the intelligence layer of Legacy."
        ),
        "features": [
            "AI reasoning",
            "Memory",
            "Voice interaction",
            "Automation",
            "Action execution",
            "Authentication",
            "Visitor analytics",
            "Modular architecture",
        ],
    },

    "Legacy": {
        "name": "Legacy",
        "description": (
            "Annu Kumar Pal's AI/ML engineering portfolio."
        ),
        "technologies": [
            "Next.js",
            "React",
            "TypeScript",
            "Tailwind CSS",
            "Motion / animations",
            "FastAPI",
            "Python",
            "JARVIS-X integration",
        ],
    },

    "Sales Forecasting": {
        "name": "Sales Forecasting",
        "description": (
            "A machine learning project focused on analysing "
            "sales data and predicting future sales."
        ),
    },
}


# ==========================================================
# SOCIAL
# ==========================================================

SOCIAL = {
    "instagram": {
        "handle": "@annuofficiall__",
        "url": "https://www.instagram.com/annuofficiall__/",
    },

    "linkedin": {
        "name": "Annu Kumar Pal",
        "url": (
            "https://www.linkedin.com/in/"
            "annu-kumar-1463a81b1/"
        ),
    },

    "github": {
        "username": "annukumarr",
        "url": "https://github.com/annukumarr",
    },
}


# ==========================================================
# CONTACT
# ==========================================================

CONTACT = {
    "email": "annulegacyai@gmail.com",
}


# ==========================================================
# BUILD PUBLIC KNOWLEDGE CONTEXT
# ==========================================================

def build_legacy_context() -> str:
    """
    Convert structured public knowledge into a
    concise AI-readable context.
    """

    project_lines = []

    for project in PROJECTS.values():
        project_lines.append(
            f"- {project['name']}: "
            f"{project['description']}"
        )

        if project.get("features"):
            project_lines.append(
                "  Features: "
                + ", ".join(
                    project["features"]
                )
            )

        if project.get("technologies"):
            project_lines.append(
                "  Technologies: "
                + ", ".join(
                    project["technologies"]
                )
            )

    technology_list = ", ".join(
        LEGACY["technologies"]
    )

    return f"""
==========================================================
JARVIS-X PUBLIC KNOWLEDGE
==========================================================

You are JARVIS-X, the embedded intelligence layer of
Legacy — Annu Kumar Pal's personal AI/ML engineering
portfolio.

==========================================================
ABOUT ANNU
==========================================================

Name:
{IDENTITY["full_name"]}

Preferred Public Name:
{IDENTITY["name"]}

Professional Role:
{IDENTITY["role"]}

Education:
{IDENTITY["education"]}

==========================================================
CURRENT FOCUS
==========================================================

Building:
{CURRENT_FOCUS["building"]}

Learning:
{CURRENT_FOCUS["learning"]}

Next Project:
{CURRENT_FOCUS["next_project"]}

Goal:
{CURRENT_FOCUS["goal"]}

==========================================================
LEGACY
==========================================================

Name:
{LEGACY["name"]}

Description:
{LEGACY["description"]}

Purpose:
{LEGACY["purpose"]}

Technology:
{technology_list}

==========================================================
PROJECTS
==========================================================

{chr(10).join(project_lines)}

==========================================================
SOCIAL / PUBLIC CONTACT
==========================================================

Instagram:
{SOCIAL["instagram"]["handle"]}

Instagram URL:
{SOCIAL["instagram"]["url"]}

LinkedIn:
{SOCIAL["linkedin"]["name"]}

LinkedIn URL:
{SOCIAL["linkedin"]["url"]}

GitHub:
{SOCIAL["github"]["username"]}

GitHub URL:
{SOCIAL["github"]["url"]}

Email:
{CONTACT["email"]}

==========================================================
PUBLIC INFORMATION RULES
==========================================================

Use this structured knowledge when answering questions
about Annu, Legacy, JARVIS-X, projects, technical work,
social profiles, or public contact information.

Do not invent information.

If requested public information is not available in this
knowledge base, clearly say that the information is not
currently available.

Keep responses:

- concise
- natural
- professional
- helpful

==========================================================
NAVIGATION ACTION AWARENESS
==========================================================

When the visitor asks to navigate the Legacy website,
the frontend action system may handle the command.

Examples:

"Show me the projects"
"Take me to projects"
"Show my journey"
"Go to contact"
"Take me home"

Do not claim that navigation was completed unless the
website action system actually performs it.
"""


# ==========================================================
# PUBLIC KNOWLEDGE ACCESS
# ==========================================================

def get_public_knowledge() -> dict:
    """
    Return the structured public knowledge.

    Useful for future JARVIS-X modules.
    """

    return {
        "identity": IDENTITY,
        "current_focus": CURRENT_FOCUS,
        "legacy": LEGACY,
        "projects": PROJECTS,
        "social": SOCIAL,
        "contact": CONTACT,
    }