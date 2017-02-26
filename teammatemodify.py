# Get the unused machines screen done
import libs.apa_database
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.properties import ObjectProperty


global current_teammate
current_teammate = 'Fuck you.'

class ScreenManagement(ScreenManager):
	pass

class TeammateModifyScreen(Screen):
	pass

class TeammateModifyLayout(BoxLayout):

	def __init__(self, **kwargs):
		super(TeammateModifyLayout, self).__init__(**kwargs)
		#teammate_name = ''
		Clock.schedule_once(self.late_init, 0)


	def late_init(self, key, **kwargs):
		self.ids.teammate_name.text = current_teammate

		positions = libs.apa_database.get_data(table_name='modelID_positionnum')
		#teammate_name = teammate_name
		global lsm
		lsm = [] # Label-Switch Module
		for i in range(0, len(positions)):

			lsm.append(IsSheTrained())
			lsm[i].ids.position_label.text = '{}-{}'.format(positions[i][0], positions[i][1])
			self.add_widget(lsm[i])
			# Needs to pick each item apart and analyze it for its model name.
			# Should move onto the item immediately if the item doesn't have the model



	def record_that_shit(self):
		pass


class IsSheTrained(BoxLayout):
	pass

# # # # # # # # # # # # # # # # # # # #

# Teammates List

# # # # # # # # # # # # # # # # # # # #

class ListTeammatesLayout(BoxLayout):

	teammate_button_id = ''

	def __init__(self, **kwargs):
		super(ListTeammatesLayout, self).__init__(**kwargs)
		global current_teammate
		teammates_training = libs.apa_database.get_data(table_name='teammate_modelID_positionnum')
		teammates = {x[0] for x in teammates_training}
		for each in teammates:

			id_name = 'teammate{}'.format(each)
			btn = SwitchScreensButton(text=each, id=id_name,\
				on_press=lambda x=each: self.update_label(x))

			self.add_widget(btn)

	def update_label(self, text):
		print(App.get_running_app().root.ids)

class ListTeammatesScreen(Screen):
	pass

class PrimaryOverlay(ScrollView):
	pass

class NavigationHUD(BoxLayout):
	pass

class SwitchScreensButton(Button):
	pass

class TeammateModifyApp(App):
	def build(self):
		return ScreenManagement()


if __name__ == '__main__':
	print(TeammateModifyApp().get_running_app())
	TeammateModifyApp().run()

print(app.get_running_app())
