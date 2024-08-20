import streamlit as st
from streamlit_calendar import calendar

calendar_options = {
    "editable": True,
    "selectable": True,
    "headerToolbar": {
        "left": "prev,next today",
        "center": "title",
        "right": "dayGridMonth,timeGridWeek,timeGridDay"
    },
    "initialView": "dayGridMonth"
}

calendar_events = [
    {"title": "Cita 1", "start": "2024-08-20T10:00:00", "end": "2024-08-20T11:00:00"},
    {"title": "Cita 2", "start": "2024-08-21T12:00:00", "end": "2024-08-21T13:00:00"}
]

calendar_component = calendar(events=calendar_events, options=calendar_options)
st.write(calendar_component)