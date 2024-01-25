from ultra_cli.menus import Menu,StructuralMenu,Option,BACK_BUTTON,SEPARATOR




data_menu = Menu(title="Data and Storage")


def change_password_function():
    print("password can not be changed")
def change_name_function(new_name):
    print(f"your new name is: {new_name}")

privacy_menu = StructuralMenu(title="Privacy", structure=[
    "List of Available options:",
    Option(title="Change name", function=change_name_function, kwargs={"new_name":"MY_NEW_NAME"}),
    Option(title="Change password", function=change_password_function),
    BACK_BUTTON
])


main_menu = StructuralMenu(title="MainMenu", structure=[
    "List of Menus:",
    privacy_menu,
    data_menu,
    SEPARATOR,
    BACK_BUTTON
])

main_menu.execute()
