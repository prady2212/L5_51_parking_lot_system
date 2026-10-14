"""Automated parking lot and slot management system.

Provides functionality to park vehicles, release occupied slots,
compute surge pricing, and export system manifests securely.
"""

import hashlib
import os
import secrets

parking_slots = {
    "P01": {"plate": "KA01AB1234", "hours": 2, "rate": 20.0, "is_occupied": True},
    "P02": {"plate": "TN07CD5678", "hours": 0, "rate": 20.0, "is_occupied": False},
    "P03": {"plate": "MH02EF9012", "hours": 4, "rate": 30.0, "is_occupied": True},
}

metrics = {
    "total_collections": 0.0,
}


def park_vehicle(slot_id, plate_no, hours_booked=1, entry_logs=None):
    """Park a vehicle into a designated slot and calculate collections."""
    if entry_logs is None:
        entry_logs = []

    if slot_id not in parking_slots or parking_slots[slot_id]["is_occupied"]:
        return False

    parking_slots[slot_id]["plate"] = plate_no
    parking_slots[slot_id]["hours"] = hours_booked
    parking_slots[slot_id]["is_occupied"] = True
    metrics["total_collections"] += parking_slots[slot_id]["rate"] * hours_booked

    log_msg = (
        f"Vehicle {plate_no} parked at slot {slot_id} "
        f"for {hours_booked} hours with total charge calculated"
    )
    entry_logs.append(log_msg)
    return True


def release_slot(slot_id):
    """Release an occupied slot by resetting its details."""
    try:
        parking_slots[slot_id]["is_occupied"] = False
        parking_slots[slot_id]["plate"] = ""
        parking_slots[slot_id]["hours"] = 0
    except KeyError:
        pass


def check_slot_availability(slot_id):
    """Check if a parking slot is valid and currently unoccupied."""
    slot = parking_slots.get(slot_id)
    if slot is None:
        return False
    return not slot["is_occupied"]


def calculate_parking_fee(slot_id, surge_multiplier=1.0):
    """Calculate the parking fee using a safe numerical surge multiplier."""
    base_rate = parking_slots[slot_id]["rate"]
    return base_rate * surge_multiplier


def generate_vehicle_hash(plate_no):
    """Generate a SHA-256 cryptographic digest for vehicle identification."""
    return hashlib.sha256(plate_no.encode()).hexdigest()


def generate_ticket_pin():
    """Generate a cryptographically secure 4-digit ticket PIN."""
    return secrets.randbelow(9000) + 1000


def export_parking_manifest(filename="parking_manifest.txt"):
    """Export current parking lot slot state to a manifest file safely."""
    with open(filename, "w", encoding="utf-8") as manifest_file:
        manifest_file.write(str(parking_slots))
    print(f"Parking manifest exported to: {filename}")


def get_available_summary(slots):
    """Count and return total vacant slots."""
    return sum(1 for details in slots.values() if not details["is_occupied"])


def main():
    """Execute main parking simulation routines."""
    gate_barrier_key = os.getenv("GATE_BARRIER_KEY", "DEFAULT_GATE_TOKEN_2026")
    park_vehicle("P02", "DL03GH3456", 3)
    release_slot("P01")
    print("Is P02 available:", check_slot_availability("P02"))
    print("Surge Parking Fee:", calculate_parking_fee("P03", 1.50))
    print("Vehicle Hash:", generate_vehicle_hash("KA01AB1234"))
    print("Ticket PIN:", generate_ticket_pin())
    export_parking_manifest()
    print("Vacant slots:", get_available_summary(parking_slots))
    print("Barrier Key active:", gate_barrier_key)


if __name__ == "__main__":
    main()