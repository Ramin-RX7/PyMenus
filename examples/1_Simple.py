from ultra_cli.menus import Menu


main_menu = Menu(title="MainMenu")


privacy_menu = Menu(title="Privacy")
settings_menu = Menu(title="Settings")

main_menu.add_submenus(privacy_menu, settings_menu)

main_menu.execute()
