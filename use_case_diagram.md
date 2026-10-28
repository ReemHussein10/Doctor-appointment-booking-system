# Use Case Diagram - Doctor Appointment Booking System

```mermaid
flowchart LR
    Patient([Patient])
    Doctor([Doctor])

    subgraph System["Doctor Appointment Booking System"]
        UC1(UC1: View Doctor Availability)
        UC2(UC2: Book Appointment)
        UC3(UC3: Check Upcoming Appointment Limit)
        UC4(UC4: Accept or Decline Appointment Request)
    end

    Patient --> UC1
    Patient --> UC2
    Doctor --> UC4
    UC2 -. include .-> UC3
```
