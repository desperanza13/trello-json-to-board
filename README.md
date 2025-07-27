# trello-json-to-board

This Python script allows you to create a Trello board, including its lists, labels, and cards, from a JSON configuration file. This is useful for quickly setting up new projects with predefined structures or migrating board data.

## Features

* Creates a Trello board with a specified name and description.
* Adds custom lists to the newly created board.
* Adds custom labels with specified names and colors.
* Populates the board with cards, associating them with the correct lists and labels based on your JSON configuration.

## Prerequisites

Before running the script, ensure you have the following:

1.  **Python 3.x**: The script is written in Python 3.
2.  **`requests` library**: This library is used for making HTTP requests to the Trello API.
    You can install it using pip:
    ```bash
    pip install requests
    ```
3.  **Trello API Key and Token**: You'll need your personal Trello API Key and a Token. You can generate these by visiting [https://trello.com/app-key](https://trello.com/app-key).
    * Your API Key is listed directly.
    * To get a Token, click on "Generate a new Token" at the top of the API Key page.

## Setup

1.  **Clone this repository** (or download `script.py` and create `trello-board-config.json` manually).

2.  **Create your JSON configuration file**:
    The script expects a JSON file containing the structure of your Trello board. An example file named `trello-find-my-family-sunless-completo.json` is provided. You can adapt this file or create your own. The structure should be as follows:

    ```json
    {
      "name": "Your Board Name",
      "desc": "Description of your board.",
      "prefs": {
        "permissionLevel": "private",
        "voting": "disabled",
        "comments": "members",
        "invitations": "members",
        "selfJoin": false,
        "cardCovers": true,
        "background": "blue",
        "cardAging": "regular"
      },
      "lists": [
        {
          "name": "List 1 Name",
          "pos": "top"
        },
        {
          "name": "List 2 Name",
          "pos": "bottom"
        }
      ],
      "labels": [
        {
          "name": "Label 1 Name",
          "color": "green"
        },
        {
          "name": "Label 2 Name",
          "color": "blue"
        }
      ],
      "cards": [
        {
          "name": "Card 1 Name",
          "desc": "Description for Card 1.",
          "idList": "List 1 Name",
          "labels": ["Label 1 Name"]
        },
        {
          "name": "Card 2 Name",
          "desc": "Description for Card 2.",
          "idList": "List 2 Name",
          "labels": ["Label 2 Name", "Label 1 Name"]
        }
      ]
    }
    ```
    * `name`: The name of your Trello board.
    * `desc`: The description of your Trello board.
    * `prefs`: (Optional) Board preferences. Note that some preferences might not be fully supported by the Trello API during board creation and may require manual adjustment or a separate `PATCH` call. The `background` preference is often set separately.
    * `lists`: An array of list objects.
        * `name`: The name of the list.
        * `pos`: The position of the list (e.g., "top", "bottom", or a float value).
    * `labels`: An array of label objects.
        * `name`: The name of the label.
        * `color`: The color of the label (e.g., "green", "blue", "orange", "red", "purple", "yellow").
    * `cards`: An array of card objects.
        * `name`: The name of the card.
        * `desc`: The description of the card.
        * `idList`: **Important**: This should be the *name* of the list as defined in your `lists` array in the JSON, *not* a Trello ID. The script will map this name to the correct Trello List ID.
        * `labels`: (Optional) An array of label names that you want to associate with the card. These names must match the `name` of the labels defined in your `labels` array.

3.  **Update `script.py` with your Trello Credentials**:
    Open `script.py` and replace the placeholder values for `API_KEY` and `TOKEN` with your actual Trello API Key and Token:

    ```python
    API_KEY = 'YOUR_TRELLO_API_KEY'
    TOKEN = 'YOUR_TRELLO_TOKEN'
    ```

4.  **Ensure the JSON file name matches**:
    The script currently expects the JSON file to be named `trello-find-my-family-sunless-completo.json`. If your JSON file has a different name, update this line in `script.py`:

    ```python
    with open('your-json-file-name.json', 'r', encoding='utf-8') as f:
        board_data = json.load(f)
    ```

## Usage

Once you have set up the prerequisites and configured the script, run it from your terminal:

```bash
python script.py
