import requests

# Function to get a random cat fact
def get_cat_fact():
    try:
        response = requests.get("https://catfact.ninja/fact")
        if response.status_code == 200:
            fact = response.json()["fact"]
            print(f"🐱 Here's your cat fact:\n\n{fact}")
        else:
            print("😿 Oops! Failed to fetch a fact. Please try again.")
    except Exception as e:
        print(f"😿 Something went wrong: {e}")

def main():
    print("Welcome to the Cat Fact Generator! 🐱")
    while True:
        user_input = input("\nPress Enter to get a fact, or type 'q' to quit: ")
        if user_input.lower() == 'q':
            print("Goodbye! Come back for more cat facts! 😊")
            break
        get_cat_fact()

# Run the program
if __name__ == '__main__':
    main()