# NOMADO BOOKING AGENT

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)


## Overview
This project is a FasrAPI-based booking agebt designed to assist users in searching for and booking travel options, including flights, hotels and destinations. It integrates with the Travelpayouts API to fetch real-time data on flight prices, hotel availability, popular destinations, and more. The agent acts as an intermediary, querying the Travelpayouts endpoints to retrieve options and presenting them to the user for selection. For bookings, the API generates affiliate booking links.

**Key Features:**
- Search for flights by origin, destination, dates, and filters (e.g., cheapest tickets, non-stop).
- Search for hotels by location, check-in/out dates, and guest details.
- Retrieve popular destinations and travel insights.
- Generate booking links for selected options to earn affiliate commissions.

## Prerequisites
- Python 3.10 or higher.
- A Travelpayouts API token: Sign up at [Travelpayouts](https://www.travelpayouts.com/) and obtain your token from the developer dashboard.
- Familiarity with FastAPI and HTTP requests.


## Installation

1. Clone the repository:
   ```bash
   git clone git@github.com:blaxpyda/nomado-bot.git
   cd nomado-bot
   ```

2. Create a virtual environment:
   ```bash
  uv venv .venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   uv add -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the root directory with your Travelpayouts token:
   ```bash
   TRAVELPAYOUTS_TOKEN=your_api_token_here


## Usage

Run the FastAPI server:
```bash
uvicorn main:app --reload
```
The API will be available at `http://127.0.0.1:8000`. Access the interactive docs at `http://127.0.0.1:8000/docs` for Swagger UI.


### Example Workflow
1. User queries the chatbot about travel plans.
2. Bot intuitively asks a user various questions about his travel plans as it builds a perfect json payload to query the API.
3. Bot sends payload through a GET request and is returned data about a travel option
4. Bot receives data and renders to the user some of the options
5. User chooses among the travel options returned
6. Bot confirms if it can continue with the booking 
7. Bot returns a link to book the chosen travel option
8. User clicks on the link and books the travel option

## API Endpoints

## Configurations
- **API Token**: Loaded from `.env`. All requests to Travelpayouts include `X-Access-Token` header.
- **Rate Limits**: Travelpayouts enforces limits (e.g., 200 searches/hour per IP for flight searches). Handle errors gracefully in production.
- **Currencies & Locales**: Defaults to USD and English.


## Project Structure

## Contributing
1. Fork the repo.
2. Create a feature branch: `git checkout -b feature/new-endpoint`.
3. Commit changes: `git commit -m 'Add new endpoint'`.
4. Push: `git push origin feature/new-endpoint`.
5. Open a Pull Request.

We welcome improvements, such as adding error handling, caching, or support for more Travelpayouts endpoints.

## License
MIT License. See [LICENSE](LICENSE) for details.

## Resources

- [Travelpayouts API Docs](https://travelpayouts.github.io/slate/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- For questions, open an issue or contact support@travelpayouts.com.