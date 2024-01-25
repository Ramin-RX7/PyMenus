from ultra_cli.menus import Menu


def new_chat():
    print("New chat section")
    print("(Options are functions that start each section of your program)")


def show_contacts(starts_with:str):
    for contact in ["Anne","Bob","Peter","Anthony"]:
        if contact.lower().startswith(starts_with):
            print(contact)



main_menu_tree = {
    "title" : "MainMenu",
    "sub_menus" : [
        {
            "title" : "Settings",
            "sub_menus" : [
                {
                    "title":"profile"
                },
                {
                    "title":"privacy"
                }
            ]
        },
        {
            "title" : "chats",
            "sub_menus" : [
                {
                    "title":"previous chats"
                }
            ],
            "options" : [
                {
                    "title": "New chat",
                    "function": new_chat
                },
                {
                    "title": "Show Contacts",
                    "function": show_contacts,
                    "kwargs" : {"starts_with":"a"}
                }
            ]
        },
    ],
    "options": [
        {
            "title": "About us",
            "function": lambda: print("This is about us page.")
        }
    ]

}



main_menu = Menu.parse_dict(main_menu_tree)
main_menu.execute()
