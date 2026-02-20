'use client'

import FullCalendar from '@fullcalendar/react';
import dayGridPlugin from '@fullcalendar/daygrid';
import iCalendarPlugin from '@fullcalendar/icalendar';

export default function Calendar() {
  return (
    <FullCalendar
      plugins={[ dayGridPlugin, iCalendarPlugin ]}
      initialView="dayGridMonth"
      events = {{
         url: 'https://adiy.io/assets/cal.ical',
         format: 'ics'
       }}
    />
  )
}
