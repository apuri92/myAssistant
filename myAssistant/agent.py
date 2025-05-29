import os
import asyncio
from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types # For creating message Content/Parts
from datetime import datetime
import tzlocal
from .tools import create_calendar_event

import warnings
# Ignore all warnings
warnings.filterwarnings("ignore")

import logging
logging.basicConfig(level=logging.ERROR)

print("Libraries imported.")


root_agent = Agent(
    name="weather_time_agent",
    model="gemini-2.0-flash",
    description="A helpful AI Assistant",
    instruction=f"""You are a helpful agent who can answer user questions and create calendar events.
    When using the create_calendar_event tool, make sure to use ISO 8601 format and IANA timezone names. also return to the user a link to the calendar event that they can click on. this is available under the response: htmlLink key in the tool response. Before you invoke the tool, if the user is adding a flight, ask for the booking id and use that for the description. Todays date is {datetime.now(tzlocal.get_localzone()).date()} and we are in the timezone {tzlocal.get_localzone()}.""",
    tools=[create_calendar_event],
)