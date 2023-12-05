# Ultra CLI

`ultra-cli` is python module/library that generates flexible cli menus.

The approach that is considered of an app using `ultra-cli` is as defined below:

- The app have a `main menu`
- This `main menu` might have some sub-menus
- As each sub-menu can also have multiple sub-menus
- An end point for each menu where user can select what should happen next (excluding sub-menus), is called `Option`
- `Option` is a function that will be called when the user selects it in a menu.

## Demonstration of how this works

    MainMenu/
    ├─── SubMenu_1/
    │   ├─── anotherSubMenu/
    │   └─── myoption_1
    └─── SubMenu_2/
        ├─── myoption_2
        └─── myoption_3

In the example above, as you can see, App starts with a menu called `MainMenu`.\
This contains 2 sub-menus called `SubMenu_1` and `SubMenu_2`. This means you can navigate to one of these menus when you are in `MainMenu`.\
Now if you navigate to `SubMenu_1`, you have 2 choices:
- `anotherSubMenu` which is a sub-menu (empty)
- `myoption_1` which is an `Option` object that which will call a specified function when you navigate to it.

```python
from ultra_cli import Menu,Option

# Creating main menu
main_menu = Menu(title="MainMenu")
# Creating other menus
privacy_menu = Menu(title="Privacy")
data_menu = Menu(title="Data and Storage")
```

```python
# functions of our Options
def change_password_function():
    print("password can not be changed")
def change_name_function(new_name):
    print(f"your new name is: {new_name}")

# Defining the Options
change_password = Option(title="Change password", function=change_password_function)
change_name = Option(title="Change name", function=change_name_function, kwargs={"new_name":"MY_NEW_NAME"})

# Adding declared options to the privacy_menu options
privacy_menu.add_options(
    change_name,
    change_password
)
```

```python
# Adding privacy_menu and data_menu to main_menu
main_menu.add_submenus(privacy_menu, data_menu)

# Start of the app
main_menu.execute()
```

<!-- ## API docs -->
