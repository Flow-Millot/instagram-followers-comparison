import json

# --- CONFIGURATION ---
# Rename if needed to match your downloaded files
FILE_FOLLOWERS = 'followers_1.json'
FILE_FOLLOWING = 'following.json'

def get_usernames(json_file, relation_type):
    """Extracts usernames handling different Instagram JSON structures."""
    users = set()
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            entry_list = []
            
            # 1. Get the relevant list based on structure
            if isinstance(data, list):
                entry_list = data
            elif isinstance(data, dict):
                if 'relationships_following' in data:
                    entry_list = data['relationships_following']
                elif 'relationships_followers' in data:
                    entry_list = data['relationships_followers']
                else:
                    # Fallback: Look for the first list in the dict
                    for val in data.values():
                        if isinstance(val, list):
                            entry_list = val
                            break

            # 2. Extract usernames
            for entry in entry_list:
                username = None
                
                # 1st try : Check 'string_list_data' (Followers case)
                try:
                    if 'string_list_data' in entry:
                        username = entry['string_list_data'][0].get('value')
                except (IndexError, AttributeError, TypeError):
                    pass

                # 2nd try : Check 'username' field
                if not username and 'title' in entry:
                    username = entry['title']

                if username:
                    users.add(username)
                    
    except FileNotFoundError:
        print(f"Error : '{json_file}' file is not found.")
        return set()
    
    return users

# --- RUN ---

# 1. Get the lists
my_followers = get_usernames(FILE_FOLLOWERS, 'followers')
my_following = get_usernames(FILE_FOLLOWING, 'following')

if not my_followers or not my_following:
    print("Error : Impossible to read lists. Verify the name of the files.")
else:
    # 2. Calculate the difference (Those I am - Those who follow me)
    not_following_back = my_following - my_followers
    
    print(f"\n--- Results ---")
    
    print("--- Liste of unfollowers ---")
    for user in sorted(not_following_back):
        print(f"Name: {user} | Link: https://www.instagram.com/{user}/")

    print(f"\nYou are following {len(my_following)} people.")
    print(f"{len(my_followers)} people are following you.")
    print(f"{len(not_following_back)} people do not follow you back.\n")
    
    # Save as a file
    with open('non_followers.txt', 'w', encoding='utf-8') as f:
        for user in sorted(not_following_back):
            f.write(f"https://www.instagram.com/{user}/\n")
    print("\nList saved to 'non_followers.txt'")