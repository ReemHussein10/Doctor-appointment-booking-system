# Use Cases - Doctor Appointment Booking System

This document describes the patient and doctor use cases derived from requirements R1-R4 in `requirements.txt`. Chosen value: N = 3.

## Actors

| Actor | Description |
|---|---|
| Patient | A person who views doctor availability and books appointments. |
| Doctor | A person who reviews and responds to appointment requests. |

## Use Case Summary

| ID | Use Case | Actor | Requirement |
|---|---|---|---|
| UC1 | View Doctor Availability | Patient | R1 |
| UC2 | Book Appointment | Patient | R2, R4 |
| UC3 | Check Upcoming Appointment Limit | System | R4 |
| UC4 | Accept or Decline Appointment Request | Doctor | R3 |

## UC1: View Doctor Availability (R1)

- **Actor:** Patient
- **Precondition:** At least one doctor has availability recorded in the system.
- **Main flow:**
  1. The patient selects a doctor.
  2. The system displays the days and times when that doctor is available.
- **Alternative flow:** If the doctor has no available slots, the system displays a message stating that no times are available.
- **Postcondition:** The patient has viewed the doctor's available days and times.

## UC2: Book Appointment (R2, R4)

- **Actor:** Patient
- **Precondition:** The patient has viewed a doctor's availability (UC1).
- **Main flow:**
  1. The patient selects an available time slot.
  2. The system checks the patient's upcoming appointment limit (UC3).
  3. If the limit has not been reached, the system creates an appointment request with status `Pending` and reserves the selected time slot to prevent double booking.
  4. The system confirms to the patient that the request has been submitted.
- **Alternative flows:**
  - **3a. Appointment limit reached:** If the patient already has N (3) or more upcoming appointments with status `Pending` or `Accepted`, the system rejects the booking and explains the limit.
  - **1a. Slot unavailable:** If the selected slot is no longer available, the system rejects the booking and asks the patient to choose another slot.
- **Postcondition:** A `Pending` appointment request exists for the patient, and the selected time slot is reserved.

## UC3: Check Upcoming Appointment Limit (R4)

- **Actor:** System
- **Relationship:** Included by UC2.
- **Main flow:**
  1. The system counts the patient's future appointments with status `Pending` or `Accepted`.
  2. If the count is less than N (3), booking may continue.
  3. If the count is N (3) or more, the booking is refused.
- **Not counted:** Declined, Cancelled, and past appointments.

## UC4: Accept or Decline Appointment Request (R3)

- **Actor:** Doctor
- **Precondition:** At least one appointment request with status `Pending` exists for this doctor.
- **Main flow:**
  1. The doctor views their pending appointment requests.
  2. The doctor selects an appointment request.
  3. The doctor chooses to Accept or Decline the request.
  4. The system updates the appointment status to `Accepted` or `Declined`.
- **Alternative flow:** If there are no pending requests, the system displays a message stating that no pending requests are available.
- **Postcondition:** The appointment status is `Accepted` or `Declined`. A `Declined` appointment no longer counts toward the patient's upcoming appointment limit.

## Notes on R5-R7

R5-R7 are non-functional requirements. They are not separate use cases and will be addressed in the system design or README:

- **R5:** Patient medical data shall be accessible only to authorized staff.
- **R6:** Available appointment times shall be displayed within 2 seconds.
- **R7:** The application shall be usable on mobile phone screens.
