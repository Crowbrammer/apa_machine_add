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
from kivy.properties import ObjectProperty, StringProperty


global current_teammate


class ScreenManagement(ScreenManager):
	pass

class TeammateModifyScreen(Screen):
	def __init__(self, **kwargs):
		super(TeammateModifyScreen, self).__init__(**kwargs)
		print('tmS: ' + str(self.ids))

class TeammateModifyLayout(BoxLayout):

	def __init__(self, **kwargs):
		super(TeammateModifyLayout, self).__init__(**kwargs)
		current_teammate = 'Teammate Name'
		Clock.schedule_once(self.late_init, 0)


	def late_init(self, key, **kwargs):
		self.ids.teammate_name.text = App.get_running_app().teammate_name

		positions = libs.apa_database.get_data(table_name='modelID_positionnum')
		#teammate_name = teammate_name
		global lsm
		lsm = [] # Label-Switch Module
		for i in range(0, len(positions)):

			lsm.append(IsSheTrained())
			lsm[i].ids.position_label.text = '{}-{}'.format(positions[i][0], positions[i][1])
			self.add_widget(lsm[i])



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
			btn = SwitchScreensButton(text=each, id=id_name)

			self.add_widget(btn)

class ListTeammatesScreen(Screen):
	pass

class PrimaryOverlay(ScrollView):
	pass

class NavigationHUD(BoxLayout):
	pass

class SwitchScreensButton(Button):
	pass

class TeammateModifyApp(App):

	teammate_name = StringProperty()

	def build(self):
		return ScreenManagement()


if __name__ == '__main__':
	print(TeammateModifyApp().get_running_app())
	TeammateModifyApp().run()
