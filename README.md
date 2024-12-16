# Eve - Your Therapeutic Chatbot

Eve is a friendly and supportive chatbot designed to interact with users on Discord. She listens and offers advice on anything from school to personal stuff, keeping the conversation casual but helpful.

## Features

- Listens to messages in multiple channels across multiple Discord servers.
- Maintains a message history for each channel to provide context-aware responses.
- Generates responses using a generative AI model.
- Provides a friendly and conversational experience, slightly Gen Z in tone.

## Setup

### Prerequisites

- Python 3.7+
- Discord API Token
- Gemini API Key
- `.env` file with the following variables:
  - `GEMINI_API`
  - `TOKEN`

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/eve.git
   cd eve
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a 

.env

 file in the root directory and add your API keys:
   ```env
   GEMINI_API=your_gemini_api_key
   TOKEN=your_discord_token
   ```

4. Run the bot:
   ```bash
   python index.py
   ```

## Usage

1. Add Eve to your Discord server by clicking the "Add to Server" button on the [webpage](https://yourwebsite.com).
2. Eve will start listening to messages in the channels she has access to.
3. You can also DM Eve if you prefer talking in private.


## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes.

## License

This project is licensed under the MIT License.
