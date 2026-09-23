""" Travel Booking & Itinerary Planner """

# ---------------- DATA (nested lists/dictionaries) ----------------

DESTINATIONS = [

    {"city": "Paris", "country": "France", "hotel_price": 120.0, "transport_price": 300.0,
     "activities": [{"name": "Eiffel Tower", "price": 30.0}, {"name": "Louvre Museum", "price": 25.0}]},

    {"city": "Rome", "country": "Italy", "hotel_price": 100.0, "transport_price": 280.0,
     "activities": [{"name": "Colosseum", "price": 20.0}, {"name": "Vatican Museums", "price": 35.0}]},

    {"city": "Dubai", "country": "UAE", "hotel_price": 150.0, "transport_price": 350.0,
     "activities": [{"name": "Burj Khalifa", "price": 45.0}, {"name": "Desert Safari", "price": 60.0}]},

    {"city": "Istanbul", "country": "Turkey", "hotel_price": 70.0, "transport_price": 200.0,
     "activities": [{"name": "Hagia Sophia", "price": 15.0}, {"name": "Bosphorus Tour", "price": 25.0}]},

    {"city": "Cairo", "country": "Egypt", "hotel_price": 50.0, "transport_price": 150.0,
     "activities": [{"name": "Giza Pyramids", "price": 20.0}, {"name": "Egyptian Museum", "price": 15.0}]},

    {"city": "Kuala Lumpur", "country": "Malaysia", "hotel_price": 80.0, "transport_price": 320.0,
     "activities": [{"name": "Petronas Towers", "price": 28.0}, {"name": "Langkawi Trip", "price": 55.0}]},

]

TAX_RATE = 0.10              


# ---------------- VALIDATION HELPERS ----------------

def is_number(text):
    """Checks if a string represents a non-negative number (int or float)."""                  
    parts = text.split(".")
    if len(parts) > 2 or text == "":
        return False
    for part in parts:
        if part != "" and not part.isdigit():
            return False
    return True


def read_int(prompt, min_value, max_value):
    """Reads a validated whole number in [min_value, max_value]."""
    while True:
        text = input(prompt).strip()
        if text.isdigit() and min_value <= int(text) <= max_value:
            return int(text)
        print("Invalid number, try again.")


def read_price(prompt):
    """Reads a validated non-negative price/budget."""
    while True:
        text = input(prompt).strip()
        if is_number(text):
            return float(text)
        print("Invalid price, try again.")


def read_menu_choice(prompt, options):
    """Reads a choice that must be one of a tuple of valid strings."""
    while True:
        text = input(prompt).strip()
        if text in options:
            return text
        print("Invalid choice, try again.")


# ---------------- SEARCH / DISPLAY ----------------

def search_destinations():
    """Searches destinations by country, price range, or activity name."""
    print("\n1) By country  2) By price range  3) By activity  4) Show all")
    choice = read_menu_choice("Search option: ", ("1", "2", "3", "4"))
    results = []

    if choice == "1":
        country = input("Country: ").strip().lower()
        for dest in DESTINATIONS:
            if country in dest["country"].lower():
                results.append(dest)
    elif choice == "2":
        low = read_price("Min price: ")
        high = read_price("Max price: ")
        for dest in DESTINATIONS:
            if low <= dest["hotel_price"] <= high:
                results.append(dest)
    elif choice == "3":
        activity = input("Activity name: ").strip().lower()
        for dest in DESTINATIONS:
            found = False
            for act in dest["activities"]:
                if activity in act["name"].lower():
                    found = True
            if found:
                results.append(dest)
    else:
        results = DESTINATIONS

    if len(results) == 0:
        print("No destinations found.")
    else:
        index = 1
        for dest in results:
            print(f"{index}. {dest['city']}, {dest['country']} "
                  f"(Hotel ${dest['hotel_price']}, Transport ${dest['transport_price']})")
            index += 1
    return results


def show_destination(destination):
    """Prints full details of one destination."""
    print(f"\n{destination['city']}, {destination['country']}")
    print(f"Hotel/night: ${destination['hotel_price']}  Transport: ${destination['transport_price']}")
    print("Activities:")
    index = 1
    for act in destination["activities"]:
        print(f"  {index}. {act['name']} - ${act['price']}")
        index += 1


# ---------------- BOOKING ----------------

def select_destination():
    """Lets the user pick a destination from search results."""
    results = search_destinations()
    if len(results) == 0:
        return None
    index = read_int(f"Pick destination (1-{len(results)}): ", 1, len(results))
    chosen = results[index - 1]
    show_destination(chosen)
    return chosen


def add_activity(trip):
    """Adds an activity from the destination's list into the trip."""
    activities = trip["destination"]["activities"]
    index = 1
    for act in activities:
        print(f"  {index}. {act['name']} - ${act['price']}")
        index += 1
    pick = read_int(f"Add activity (1-{len(activities)}): ", 1, len(activities))
    trip["activities"].append(activities[pick - 1])
    print("Activity added.")


def remove_activity(trip):
    """Removes an activity the user already added to the trip."""
    if len(trip["activities"]) == 0:
        print("No activities to remove.")
        return
    index = 1
    for act in trip["activities"]:
        print(f"  {index}. {act['name']} - ${act['price']}")
        index += 1
    pick = read_int(f"Remove activity (1-{len(trip['activities'])}): ", 1, len(trip["activities"]))
    removed = trip["activities"].pop(pick - 1)
    print(f"Removed {removed['name']}.")


def change_nights(trip):
    """Changes the number of nights of the trip."""
    trip["nights"] = read_int("New number of nights: ", 1, 60)
    print("Nights updated.")


def change_travelers(trip):
    """Changes the number of travelers on the trip."""
    trip["travelers"] = read_int("New number of travelers: ", 1, 20)
    print("Travelers updated.")


# ---------------- CALCULATIONS ----------------

def calculate_trip_cost(trip):
    """Returns a dict with transport, accommodation, activities, taxes, total.
    Transport and activities are paid per traveler; accommodation is paid
    per night and multiplied by the number of travelers (one bed/spot each)."""
    travelers = trip["travelers"]

    transport = trip["destination"]["transport_price"] * travelers
    accommodation = trip["destination"]["hotel_price"] * trip["nights"] * travelers

    prices = []
    for act in trip["activities"]:
        prices.append(act["price"])
    activities_total = sum(prices) * travelers

    subtotal = transport + accommodation + activities_total
    taxes = subtotal * TAX_RATE
    total = subtotal + taxes

    costs = {"transport": transport, "accommodation": accommodation,
             "activities": activities_total, "taxes": taxes, "total": total}

    if trip["budget"] is not None and total > trip["budget"]:
        print(f"\nWARNING: total ${total:.2f} exceeds budget ${trip['budget']:.2f}!")

    return costs


# ---------------- ITINERARY ----------------

def build_itinerary(trip):
    """Builds a day-by-day list of activities (nested list: day -> activities)."""
    nights = trip["nights"]
    itinerary = []
    for day in range(nights):
        itinerary.append([])

    day = 0
    for act in trip["activities"]:
        itinerary[day].append(act["name"])
        day += 1
        if day == nights:
            day = 0

    print(f"\n--- Itinerary ({nights} nights) ---")
    for day in range(nights):
        if len(itinerary[day]) == 0:
            print(f"Day {day + 1}: free day")
        else:
            print(f"Day {day + 1}: " + ", ".join(itinerary[day]))
    return itinerary


# ---------------- SUMMARY ----------------

def booking_summary(trip, costs):
    """Prints the final booking summary."""
    print("\n===== BOOKING SUMMARY =====")
    print(f"{trip['destination']['city']}, {trip['destination']['country']} - "
          f"{trip['nights']} nights - {trip['travelers']} traveler(s)")
    for act in trip["activities"]:
        print(f"  - {act['name']} (${act['price']})")
    print(f"Transport: ${costs['transport']:.2f}")
    print(f"Accommodation: ${costs['accommodation']:.2f}")
    print(f"Activities: ${costs['activities']:.2f}")
    print(f"Taxes: ${costs['taxes']:.2f}")
    print(f"TOTAL: ${costs['total']:.2f}")
    if trip["budget"] is not None:
        if costs["total"] <= trip["budget"]:
            print("Status: within budget")
        else:
            print("Status: over budget")


# ---------------- MAIN MENU ----------------

def main():
    trip = None
    running = True
    while running:
        print("\n1) New trip  2) Add activity  3) Remove activity  4) Change nights"
              "\n5) Change travelers  6) Calculate cost  7) Build itinerary"
              "\n8) Final summary  9) Exit")
        choice = read_menu_choice("Choose: ", ("1", "2", "3", "4", "5", "6", "7", "8", "9"))

        if choice == "1":
            destination = select_destination()
            if destination is not None:
                nights = read_int("Nights: ", 1, 60)
                travelers = read_int("Number of travelers: ", 1, 20)
                has_budget = read_menu_choice("Set a budget? (y/n): ", ("y", "n"))
                if has_budget == "y":
                    budget = read_price("Budget: ")
                else:
                    budget = None
                trip = {"destination": destination, "nights": nights, "travelers": travelers,
                        "activities": [], "budget": budget}
                print("Trip created.")
        elif trip is None:
            print("Create a trip first (option 1).")
        elif choice == "2":
            add_activity(trip)
        elif choice == "3":
            remove_activity(trip)
        elif choice == "4":
            change_nights(trip)
        elif choice == "5":
            change_travelers(trip)
        elif choice == "6":
            costs = calculate_trip_cost(trip)
            print(f"Transport: ${costs['transport']:.2f}")
            print(f"Accommodation: ${costs['accommodation']:.2f}")
            print(f"Activities: ${costs['activities']:.2f}")
            print(f"Taxes: ${costs['taxes']:.2f}")
            print(f"Total: ${costs['total']:.2f}")
        elif choice == "7":
            build_itinerary(trip)
        elif choice == "8":
            costs = calculate_trip_cost(trip)
            build_itinerary(trip)
            booking_summary(trip, costs)
        else:
            running = False
            print("Goodbye!")


if __name__ == "__main__":
    main()