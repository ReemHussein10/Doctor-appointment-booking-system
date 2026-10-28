# Sequence Diagram — Book an Appointment

```mermaid
sequenceDiagram
    actor Patient
    participant BS as BookingService
    participant Slot as TimeSlot
    participant Appt as Appointment
    participant Doctor

    Patient->>BS: bookAppointment(patientId, slotId)
    BS->>Slot: isAvailable()
    Slot-->>BS: availability result

    alt Slot is unavailable
        BS-->>Patient: Reject booking — choose another slot
    else Slot is available
        BS->>BS: hasReachedLimit(patient)

        alt Patient has reached N = 3 upcoming appointments
            BS-->>Patient: Reject booking — upcoming appointment limit reached
        else Patient has fewer than 3 upcoming appointments
            BS->>Appt: Create appointment with status PENDING
            BS->>Slot: markBooked()
            BS->>Doctor: Add appointment to pending requests
            BS-->>Patient: Booking request submitted (PENDING)
        end
    end
```

## Notes
- `N = 3`.
- Only future appointments with status `PENDING` or `ACCEPTED` count toward the limit.
- `DECLINED`, `CANCELLED`, and past appointments do not count.
- The request remains `PENDING` until the doctor accepts or declines it.
