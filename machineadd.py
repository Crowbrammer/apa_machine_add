# Get the unused machines screen done
import libs.apa_database
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock


class ScreenManagement(ScreenManager):
	pass

class MachineAddScreen(Screen):
	pass

class MachineAddLayout(BoxLayout):

	def __init__(self, **kwargs):
		super(MachineAddLayout, self).__init__(**kwargs)
		Clock.schedule_once(self.late_init, 0)

	def late_init(self, key, **largs):
		# print(dir(self.ids.num_positions))
		test = self.ids.machine_add_name.text
		# print('test: ',str(test))
		# create a dropdown with 10 buttons
		dropdown = DropDown()
		btn = Button(text='Up', size_hint_y=None, height=44)
		btn.bind(on_release=lambda btn, d=dropdown: d.select(btn.text))
		dropdown.add_widget(btn)

		btn = Button(text='Down', size_hint_y=None, height=44)
		btn.bind(on_release=lambda btn, d=dropdown: d.select(btn.text))
		dropdown.add_widget(btn)
			# then add the button inside the dropdown

		self.ids.status.bind(on_release=dropdown.open)
		dropdown.bind(on_select=lambda instance, x, e=self.ids.status: setattr(e, 'text', x))



	def record_new_model(self):
		machine_name = self.ids.machine_add_name.text
		status = self.ids.status.text
		print(machine_name)

		libs.apa_database.insert_data(tb='machineID_modelID_status', col1='machineID', \
			 		data1=machine_name, col2='modelID', data2=None, \
					col3='machine_status', data3=status)

class PrimaryOverlay(ScrollView):
	pass

class NavigationHUD(BoxLayout):
	pass

class MachineAddApp(App):
	pass

# A
if __name__ == '__main__':
	MachineAddApp().run()
