# Booking Agent Bot Use Cases
Below are use cases for the Booking Agent API implemented as a conversational bot, designed to interact with users in a natural, chat-like manner. The bot leverages the FastAPI backend to query the Travelpayouts API for flights, hotels, and destinations, guiding users through their travel planning.

<details>
<summary><b>Use Case 1: Searching for lfights to a destination</b></summary>

**Description**: A user wants to find flights to a specific destination and interacts with the bot to get options.

**Conversation**:
```
User: Hey, I want to go to Phuket!
Bot: Sure thing, let's narrow down some options! Where are you flying from?
User: I'm in New York.
Bot: Awesome! When do you want to travel to Phuket? For example, give me a departure date or a month.
User: How about next month, around October 10th?
Bot: Got it! Any return date, or is this one-way?
User: Let's make it a return trip, maybe October 17th.
Bot: Perfect. I'm searching for flights from New York (NYC) to Phuket (HKT) for October 10th to 17th. One moment...
Bot: Here are some options:
  - Cheapest: $650, one stop, 18h 30m (Thai Airways)
  - Fastest: $820, one stop, 16h 10m (Qatar Airways)
Want more details on any of these or other filters like non-stop only?
```

**Bot Workflow**:
1. User initiates with a destination ("Phuket").
2. Bot prompts for origin and travel dates to complete the query.
3. Bot sends a GET request to `/search-flights` with parameters: `origin=NYC`, `destination=HKT`, `depart_date=2025-10-10`, `return_date=2025-10-17`.
4. API queries Travelpayouts (e.g., GET `/v1/prices/cheap` or POST `/v1/flight_search`).
5. Bot formats the response into a user-friendly list of flight options with prices and airlines.
6. Bot offers to refine results or proceed to booking.

</details>

<details>
<summary><b>Use Case 2: Finding hotels near a location</b></summary>

**Description**: A user seeks hotel recommendations based on a city name and budget range.

**Conversation**:
```
User: I need a hotel in Paris for next weekend.
Bot: Nice choice, Paris is amazing! Can you tell me the exact dates? Like, check-in and check-out?
User: Check-in on October 3rd, check-out on October 5th.
Bot: Got it. How many adults are staying?
User: Just two of us.
Bot: Alright, searching for hotels in Paris for October 3rd to 5th, for 2 adults...
Bot: Here are some options:
  - Hotel Eiffel: $120/night, 4 stars, near Eiffel Tower
  - Le Cozy Inn: $85/night, 3 stars, central location
Want to know more about any of these or book one?
User: Tell me more about Hotel Eiffel.
Bot: Hotel Eiffel: 4-star, 0.5 miles from Eiffel Tower, free Wi-Fi, breakfast included. Total for 2 nights: $240. Ready to get a booking link?
```

**Bot Workflow**:
1. User specifies a location ("Paris") and time frame ("next weekend").
2. Bot clarifies exact dates and number of guests.
3. Bot sends a GET request to `/search-hotels` with parameters: `location=Paris`, `check_in=2025-10-03`, `check_out=2025-10-05`, `adults=2`.
4. API queries Travelpayouts (e.g., GET `/v2/hotel/lookup`).
5. Bot presents hotel options with key details (name, price, rating).
6. On user request, bot provides more details or generates a booking link via POST to `/book`.

</details>

<details>
<summary><b>Use Case 3: Exploring Popular Destinations</b></summary>

**Description**: A user asks for popular destinations and receives suggestions along with brief descriptions.

**Conversation**:
```
User: I want to go somewhere fun but I’m not sure where.
Bot: No problem, I can suggest some hot destinations! Where are you traveling from?
User: London.
Bot: Cool! Let me check some popular spots from London...
Bot: Here are some trending destinations:
  - Barcelona: from $80 round-trip, vibrant culture
  - Amsterdam: from $95 round-trip, scenic canals
  - Rome: from $110 round-trip, historic sites
Any of these sound exciting, or want more ideas?
User: Barcelona sounds great! What’s the cheapest flight there?
Bot: Let’s find you a deal to Barcelona! When do you want to go?
```

**Bot Workflow**:
1. User expresses interest in travel without a specific destination.
2. Bot asks for the origin to tailor suggestions.
3. Bot sends a GET request to `/get-destinations` with `origin=LON`.
4. API queries Travelpayouts (e.g., GET `/v1/city-directions` or `/v1/prices/popular`).
5. Bot presents a list of destinations with indicative prices.
6. On user selection, bot transitions to a flight search.

</details>

<details>
<summary><b>Use Case 4: Completing a Booking</b></summary>

**Description**: A user completes a booking process by selecting an option and confirming details.

**Conversation**:
```
User: I like that $650 flight to Phuket you mentioned earlier. Can you book it?
Bot: Awesome choice! I can get you a booking link for that flight. Just confirm: it’s the Thai Airways flight from NYC to Phuket, departing October 10th, returning October 17th, right?
User: Yep, that’s the one!
Bot: Great! Here’s your booking link: [Book Now](https://travelpayouts.com/redirect?search_id=abc123&option_id=xyz456). Click to finalize on the partner site. Safe travels!
```

**Bot Workflow**:
1. User selects a flight from previous search results.
2. Bot confirms the selection to avoid errors.
3. Bot sends a POST request to `/book` with `search_id` and `option_id` from the flight search.
4. API queries Travelpayouts to generate an affiliate booking URL.
5. Bot returns the URL in a user-friendly format.

</details>