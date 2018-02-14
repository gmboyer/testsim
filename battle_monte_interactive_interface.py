from ipywidgets import interact, interactive, fixed, interact_manual, IntSlider, Accordion, Tab, HBox, VBox, Output
import ipywidgets as widgets
from IPython.display import display, clear_output
from battle_monte import *



def main():
    c1_name = widgets.Text(value = 'Rhonda', placeholder = 'Type something', description = 'Name 1:', disabled = False)
    c1_sex = widgets.Dropdown(options = ['male', 'female'], value = 'female', description = 'Sex:', disabled = False)
    c1_str = IntSlider(min = 4, max = 12, step = 2, description = 'STR', value = 6)
    c1_dex = IntSlider(min = 4, max = 12, step = 2, description = 'DEX', value = 6)
    c1_con = IntSlider(min = 4, max = 12, step = 2, description = 'CON', value = 6)
    c1_wis = IntSlider(min = 4, max = 12, step = 2, description = 'WIS', value = 6)
    c1_int = IntSlider(min = 4, max = 12, step = 2, description = 'INT', value = 6)
    c1_cha = IntSlider(min = 4, max = 12, step = 2, description = 'CHA', value = 6)
    c1_lck = IntSlider(min = 0, max = 4, step = 4, description = 'LCK', value = 0)
    c1_SpAbil = widgets.SelectMultiple(
        options = ['armor training', 'berserk', 'combat dicipline', 'sneak attack'],
        # value = ['none'],
        #rows=10,
        description = 'Special Abilities',
        disabled = False
    )
    c1_fightstyle = widgets.Dropdown(
        value = 'none',
        options = ['none', 'well-rounded', 'powerful', 'finesse', 'dual-weapon', 'defensive'],
        description = 'Fightstyle:',
        disabled = False,
        button_style = '', # 'success', 'info', 'warning', 'danger' or ''
        # tooltips=['Description of slow', 'Description of regular', 'Description of fast'],
    #     icons=['check'] * 3
    )
    c1_armor = widgets.Dropdown(
        value = 'none',
        options = ['none', 'padded', 'chainmail', 'platemail'],
        description = 'Armor:',
        disabled = False,
        button_style = '', # 'success', 'info', 'warning', 'danger' or ''
        # tooltips=['Description of slow', 'Description of regular', 'Description of fast'],
    #     icons=['check'] * 3
    )
    c1_dualw = widgets.Checkbox(
        value = False,
        description = 'Dual-Wield?',
        disabled = False
    )

    c2_name = widgets.Text(value = 'Rufus', placeholder = 'Type something', description = 'Name 1:', disabled = False)
    c2_sex = widgets.Dropdown(options = ['male', 'female'], value = 'male', description = 'Sex:', disabled = False)
    c2_str = IntSlider(min = 4, max = 12, step = 2, description = 'STR', value = 6)
    c2_dex = IntSlider(min = 4, max = 12, step = 2, description = 'DEX', value = 6)
    c2_con = IntSlider(min = 4, max = 12, step = 2, description = 'CON', value = 6)
    c2_wis = IntSlider(min = 4, max = 12, step = 2, description = 'WIS', value = 6)
    c2_int = IntSlider(min = 4, max = 12, step = 2, description = 'INT', value = 6)
    c2_cha = IntSlider(min = 4, max = 12, step = 2, description = 'CHA', value = 6)
    c2_lck = IntSlider(min = 0, max = 4, step = 4, description = 'LCK', value = 0)
    c2_SpAbil = widgets.SelectMultiple(
        options = ['armor training', 'berserk', 'combat dicipline', 'sneak attack'],
        # value = ['none'],
        #rows=10,
        description = 'Special Abilities',
        disabled = False
    )
    c2_fightstyle = widgets.Dropdown(
        value = 'none',
        options = ['none', 'well-rounded', 'powerful', 'finesse', 'dual-weapon', 'defensive'],
        description = 'Fightstyle:',
        disabled = False,
        button_style = '', # 'success', 'info', 'warning', 'danger' or ''
        # tooltips=['Description of slow', 'Description of regular', 'Description of fast'],
    #     icons=['check'] * 3
    )
    c2_armor = widgets.Dropdown(
        value = 'none',
        options = ['none', 'padded', 'chainmail', 'platemail'],
        description = 'Armor:',
        disabled = False,
        button_style = '', # 'success', 'info', 'warning', 'danger' or ''
        # tooltips=['Description of slow', 'Description of regular', 'Description of fast'],
    #     icons=['check'] * 3
    )
    c2_dualw = widgets.Checkbox(
        value = False,
        description = 'Dual-Wield?',
        disabled = False
    )

    iterations = IntSlider(min = 2, max = 9999, step = 1, description = '# of battles:')
    dis = IntSlider(min = 0, max = 20, step = 1, description = 'Start distance:')


    c1_namesex = widgets.HBox([c1_name, c1_sex])
    c1_stat_block = widgets.VBox([c1_str, c1_dex, c1_con, c1_wis, c1_int, c1_cha, c1_lck])
    c1_SpAbil_fightstyle_armor = widgets.VBox([c1_SpAbil, c1_fightstyle, c1_armor, c1_dualw])
    c1_stat_abil = widgets.HBox([c1_stat_block, c1_SpAbil_fightstyle_armor])
    c1_tab_contents = widgets.VBox([c1_namesex, c1_stat_abil])

    c2_namesex = widgets.HBox([c2_name, c2_sex])
    c2_stat_block = widgets.VBox([c2_str, c2_dex, c2_con, c2_wis, c2_int, c2_cha, c2_lck])
    c2_SpAbil_fightstyle_armor = widgets.VBox([c2_SpAbil, c2_fightstyle, c2_armor, c2_dualw])
    c2_stat_abil = widgets.HBox([c2_stat_block, c2_SpAbil_fightstyle_armor])
    c2_tab_contents = widgets.VBox([c2_namesex, c2_stat_abil])

    tab_contents = ['Combatant 1', 'Combatant 2',]
    children = [c1_tab_contents, c2_tab_contents]
    tab = widgets.Tab()
    tab.children = children
    tab.set_title(0, 'Combatant 1')
    tab.set_title(1, 'Combatant 2')

    button = widgets.Button(description="Battle!")


    def on_button_clicked(b):
        clear_output(True)
        display(this)
        battle_monte(c1_name = c1_name.value,
                c1_sex = c1_sex.value,
                c1_str = c1_str.value,
                c1_dex = c1_dex.value,
                c1_con = c1_con.value,
                c1_wis = c1_wis.value,
                c1_int = c1_int.value,
                c1_cha = c1_cha.value,
                c1_lck = c1_lck.value,
                c1_SpAbil = c1_SpAbil.value,
                c1_fightstyle = c1_fightstyle.value,
                c1_armor = c1_armor.value,
                c1_dualw = c1_dualw.value,
                c2_name = c2_name.value,
                c2_sex = c2_sex.value,
                c2_str = c2_str.value,
                c2_dex = c2_dex.value,
                c2_con = c2_con.value,
                c2_wis = c2_wis.value,
                c2_int = c2_int.value,
                c2_cha = c2_cha.value,
                c2_lck = c2_lck.value,
                c2_SpAbil = c2_SpAbil.value,
                c2_fightstyle = c2_fightstyle.value,
                c2_armor = c2_armor.value,
                c2_dualw = c2_dualw.value,
                it = iterations.value,
                dis = dis.value)
        plt.show()

    button.on_click(on_button_clicked)

    this = widgets.VBox([
        tab,
        iterations,
        dis,
        button,
    ])

    display(this)


if __name__ == '__main__':
    main()
