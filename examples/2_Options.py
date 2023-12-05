from ultra_cli import Menu,Option


main_menu = Menu(title="MainMenu")


privacy_menu = Menu(title="Privacy")
data_menu = Menu(title="Data and Storage")


def change_password_function():
    print("password can not be changed")
def change_name_function(new_name):
    print(f"your new name is: {new_name}")

change_password = Option(title="Change password", function=change_password_function)
change_name = Option(title="Change name", function=change_name_function, kwargs={"new_name":"MY_NEW_NAME"})

privacy_menu.add_options(
    change_name,
    change_password,
)

main_menu.add_submenus(privacy_menu, data_menu)

main_menu.execute()
