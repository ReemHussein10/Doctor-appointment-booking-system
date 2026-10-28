"""
Doctor Appointment Booking System
---------------------------------
Implements the core functional requirements R1–R4.

  R1  Patient can view a doctor's available days and times.
  R2  Patient can book an appointment during an available slot.
  R3  Doctor can accept or decline an appointment request.
  R4  A patient can have at most N upcoming appointments at any time.

Chosen N (from requirements.txt): N = 3

Non-functional requirements R5 (security), R6 (2 s display),
R7 (mobile usability) are out of scope for this CLI demo — noted
in the AI journal and README.

Run with:  python main.py
"""

from datetime import datetime

# ----- R4: maximum upcoming appointments per patient -----
N = 3


# ---------------------------------------------------------
# Domain classes (keep names consistent with class_diagram.md)
# ---------------------------------------------------------
class Doctor:
    def __init__(self, doctor_id, name, specialty):
        self.doctor_id = doctor_id
        self.name = name
        self.specialty = specialty
        # R1: available slots the doctor offers
        # each slot: {"slot_id": int, "time": str, "booked": bool}
        self.slots = []

    def add_slot(self, slot_id, time):
        self.slots.append({"slot_id": slot_id, "time": time, "booked": False})

    def view_available_slots(self):
        """R1: return only the free slots."""
        return [s for s in self.slots if not s["booked"]]

    def __str__(self):
        return f"Dr. {self.name} ({self.specialty})"


class Patient:
    def __init__(self, patient_id, name):
        self.patient_id = patient_id
        self.name = name
        # list of Appointment objects (only upcoming ones count for R4)
        self.appointments = []

    def upcoming_count(self):
        """R4: count appointments that are pending or accepted (not declined/cancelled)."""
        return sum(1 for a in self.appointments
                   if a.status in ("PENDING", "ACCEPTED"))

    def __str__(self):
        return f"Patient #{self.patient_id} - {self.name}"


class Appointment:
    def __init__(self, appt_id, patient, doctor, slot):
        self.appt_id = appt_id
        self.patient = patient
        self.doctor = doctor
        self.slot = slot          # reference to the doctor's slot dict
        self.status = "PENDING"   # PENDING -> ACCEPTED / DECLINED

    def accept(self):
        """R3: doctor accepts."""
        self.status = "ACCEPTED"

    def decline(self):
        """R3: doctor declines -> slot becomes available again."""
        self.status = "DECLINED"
        self.slot["booked"] = False

    def __str__(self):
        return (f"Appointment #{self.appt_id}: {self.patient.name} with "
                f"{self.doctor} at {self.slot['time']} [{self.status}]")


# ---------------------------------------------------------
# System / controller
# ---------------------------------------------------------
class AppointmentSystem:
    def __init__(self):
        self.doctors = {}
        self.patients = {}
        self.appointments = []
        self.next_appt_id = 1

    # ---- registration helpers ----
    def add_doctor(self, doctor):
        self.doctors[doctor.doctor_id] = doctor

    def add_patient(self, patient):
        self.patients[patient.patient_id] = patient

    # ---- R1 ----
    def view_doctor_availability(self, doctor_id):
        doctor = self.doctors.get(doctor_id)
        if not doctor:
            print(f"❌ Doctor {doctor_id} not found.")
            return []
        free = doctor.view_available_slots()
        if not free:
            print(f"⏰ {doctor} has no available slots.")
            return []
        print(f"📅 Available slots for {doctor}:")
        for s in free:
            print(f"   - Slot {s['slot_id']}: {s['time']}")
        return free

    # ---- R2 + R4 ----
    def book_appointment(self, patient_id, doctor_id, slot_id):
        patient = self.patients.get(patient_id)
        doctor = self.doctors.get(doctor_id)
        if not patient:
            print(f"❌ Patient {patient_id} not found.")
            return None
        if not doctor:
            print(f"❌ Doctor {doctor_id} not found.")
            return None

        # R4: enforce N
        if patient.upcoming_count() >= N:
            print(f"❌ Booking rejected: {patient.name} already has "
                  f"{patient.upcoming_count()} upcoming appointments (max N = {N}).")
            return None

        # find the requested slot
        slot = next((s for s in doctor.slots if s["slot_id"] == slot_id), None)
        if not slot:
            print(f"❌ Slot {slot_id} does not exist for {doctor}.")
            return None
        if slot["booked"]:
            print(f"❌ Slot {slot_id} ({slot['time']}) is already booked.")
            return None

        # R2: book
        slot["booked"] = True
        appt = Appointment(self.next_appt_id, patient, doctor, slot)
        self.next_appt_id += 1
        self.appointments.append(appt)
        patient.appointments.append(appt)

        print(f"✅ Appointment request #{appt.appt_id} created: "
              f"{patient.name} with {doctor} at {slot['time']} (PENDING).")
        return appt

    # ---- R3 ----
    def doctor_respond(self, appointment_id, accept: bool):
        appt = next((a for a in self.appointments if a.appt_id == appointment_id), None)
        if not appt:
            print(f"❌ Appointment {appointment_id} not found.")
            return
        if appt.status != "PENDING":
            print(f"⚠️ Appointment #{appointment_id} already {appt.status}.")
            return
        if accept:
            appt.accept()
            print(f"✅ Appointment #{appointment_id} ACCEPTED by {appt.doctor}.")
        else:
            appt.decline()
            print(f"✅ Appointment #{appointment_id} DECLINED by {appt.doctor}. "
                  f"Slot {appt.slot['slot_id']} is free again.")

    # ---- helper ----
    def show_patient_appointments(self, patient_id):
        patient = self.patients.get(patient_id)
        if not patient:
            print(f"❌ Patient {patient_id} not found.")
            return
        print(f"📋 Appointments for {patient.name}:")
        if not patient.appointments:
            print("   (none)")
            return
        for a in patient.appointments:
            print(f"   {a}")


# ---------------------------------------------------------
# Demo / main flow
# ---------------------------------------------------------
def main():
    print("=" * 60)
    print(" Doctor Appointment Booking System")
    print(f" Max upcoming appointments per patient (N) = {N}")
    print("=" * 60)

    system = AppointmentSystem()

    # --- setup ---
    doc1 = Doctor(101, "Hassan", "Cardiology")
    doc1.add_slot(1, "2026-11-01 10:00")
    doc1.add_slot(2, "2026-11-01 11:00")
    doc1.add_slot(3, "2026-11-01 12:00")
    doc1.add_slot(4, "2026-11-02 09:00")
    system.add_doctor(doc1)

    pat1 = Patient(1, "Ali")
    pat2 = Patient(2, "Sara")
    system.add_patient(pat1)
    system.add_patient(pat2)

    # --- R1: patient views availability ---
    print("\n--- R1: View availability ---")
    system.view_doctor_availability(101)

    # --- R2: patient books ---
    print("\n--- R2: Book appointments ---")
    a1 = system.book_appointment(patient_id=1, doctor_id=101, slot_id=1)
    a2 = system.book_appointment(patient_id=1, doctor_id=101, slot_id=2)
    a3 = system.book_appointment(patient_id=1, doctor_id=101, slot_id=3)

    # --- R4: 4th booking by same patient must be rejected (N = 3) ---
    print("\n--- R4: Enforce N = 3 ---")
    system.book_appointment(patient_id=1, doctor_id=101, slot_id=4)

    # --- R3: doctor accepts / declines ---
    print("\n--- R3: Doctor responds ---")
    system.doctor_respond(a1.appt_id, accept=True)
    system.doctor_respond(a2.appt_id, accept=False)

    # --- show final state ---
    print("\n--- Final state ---")
    system.show_patient_appointments(1)
    print()
    system.view_doctor_availability(101)


if __name__ == "__main__":
    main()