import json
import requests

# Your Trello API Key and Token
# You can generate these by visiting https://trello.com/app-key
API_KEY = 'YOUR_TRELLO_API_KEY'
TOKEN = 'YOUR_TRELLO_TOKEN'

# Load your JSON configuration file
# Ensure this file exists in the same directory as the script
with open('trello-board-config.json', 'r', encoding='utf-8') as f:
    board_data = json.load(f)

base_url = "https://api.trello.com/1/"
auth_params = {'key': API_KEY, 'token': TOKEN}

# 1. Create the Board
print("Creating the board...")
board_name = board_data['name']
board_desc = board_data['desc']
board_prefs = board_data.get('prefs', {}) # Get preferences, default to empty dict if not present

create_board_url = f"{base_url}boards"
board_params = {
    'name': board_name,
    'desc': board_desc,
    'defaultLists': 'false', # Do not create Trello's default lists
    **auth_params
}

# Add preferences. Note that some preferences might not be directly supported
# during board creation and may require a separate PATCH call.
for pref_key, pref_value in board_prefs.items():
    # 'background' is often set separately via the Trello API
    if pref_key not in ['background']:
        board_params[pref_key] = pref_value

response = requests.post(create_board_url, params=board_params)
response.raise_for_status() # Raise an exception for HTTP errors
new_board = response.json()
board_id = new_board['id']
print(f"Board '{board_name}' created with ID: {board_id}")

# 2. Create Lists and map their IDs
print("Creating lists...")
list_name_to_id = {}
for list_item in board_data['lists']:
    list_name = list_item['name']
    list_pos = list_item['pos']
    create_list_url = f"{base_url}boards/{board_id}/lists"
    list_params = {
        'name': list_name,
        'pos': list_pos,
        **auth_params
    }
    response = requests.post(create_list_url, params=list_params)
    response.raise_for_status()
    new_list = response.json()
    list_name_to_id[list_name] = new_list['id']
    print(f"  List '{list_name}' created.")

# 3. Create Labels and map their IDs
print("Creating labels...")
label_name_to_id = {}
for label_item in board_data['labels']:
    label_name = label_item['name']
    label_color = label_item['color']
    create_label_url = f"{base_url}boards/{board_id}/labels"
    label_params = {
        'name': label_name,
        'color': label_color,
        **auth_params
    }
    response = requests.post(create_label_url, params=label_params)
    response.raise_for_status()
    new_label = response.json()
    label_name_to_id[label_name] = new_label['id']
    print(f"  Label '{label_name}' created.")


# 4. Create Cards
print("Creating cards...")
for card_item in board_data['cards']:
    card_name = card_item['name']
    card_desc = card_item.get('desc', '') # Get description, default to empty string
    original_list_name = card_item['idList']

    # Get the actual Trello list ID
    trello_list_id = list_name_to_id.get(original_list_name)
    if not trello_list_id:
        print(f"  Warning: List '{original_list_name}' not found for card '{card_name}'. Skipping card.")
        continue

    # Get the actual Trello label IDs
    trello_label_ids = []
    if 'labels' in card_item and card_item['labels']:
        for label_name in card_item['labels']:
            trello_label_id = label_name_to_id.get(label_name)
            if trello_label_id:
                trello_label_ids.append(trello_label_id)
            else:
                print(f"  Warning: Label '{label_name}' not found for card '{card_name}'.")

    create_card_url = f"{base_url}cards"
    card_params = {
        'idList': trello_list_id,
        'name': card_name,
        'desc': card_desc,
        'idLabels': ','.join(trello_label_ids), # Labels are passed as a comma-separated string of IDs
        **auth_params
    }
    response = requests.post(create_card_url, params=card_params)
    response.raise_for_status()
    print(f"  Card '{card_name}' created.")

print("\nImport completed!")
print(f"Your new board is accessible at: {new_board['url']}")