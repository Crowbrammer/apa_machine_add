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
from kivy.core.window import Window

global current_teammate


class ScreenManagement(ScreenManager):
	pass

class TeammateModifyScreen(Screen):
	def on_enter(self):

		# On screen load

		# Store the list of essential data into local variables
		all_label_switches = self.ids.primary_overlay.ids.teammate_modify_layout.lsm
		teammate_name = App.get_running_app().teammate_name
		all_training = libs.apa_database.get_data(table_name='teammate_modelID_positionnum', specific_data=teammate_name, column_name='teammate', model=None,
						order_by_column=None)
		teammates_with_training = {x[0] for x in all_training}

		# Check if she's even in the training table.
		if teammate_name in teammates_with_training:
			# Go through each lsm widget.
			for each in all_label_switches:
				# For each, check each training entry...
				for each_entry in all_training:
					# until we find one with her name in it that...
					if each_entry[0] == teammate_name:
						# matches the label containing the position, then...
						if each.ids.position_label.text == '{}-{}'.format(each_entry[1], each_entry[2]):
							# Update the switch to on and stop the loop if found
							each.ids.position_training_switch.active = True
							break
						else:
							# Update the switch to False and finish the loop if not found
							each.ids.position_training_switch.active = False

class TeammateModifyLayout(BoxLayout):



	def __init__(self, **kwargs):
		super(TeammateModifyLayout, self).__init__(**kwargs)
		current_teammate = 'Teammate Name'
		Clock.schedule_once(self.late_init, 0)


	def late_init(self, key, **kwargs):
		print(self.parent.parent.ids)
		teammate_name = App.get_running_app().teammate_name
		self.ids.teammate_name.text = teammate_name

		self.positions = libs.apa_database.get_data(table_name='modelID_position')


		#teammate_name = teammate_name
		# Label-Switch Module
		global lsm
		self.lsm = []

		for i in range(0, len(self.positions)):

			self.lsm.append(IsSheTrained())
			self.lsm[i].ids.position_label.text = '{}-{}'.format(self.positions[i][0], self.positions[i][1])
			# When a switch is flipped on, add the name and position from the index
			# of the current lsm.
			self.lsm[i].ids.position_training_switch.num = i
			self.lsm[i].ids.position_training_switch.bind(active=self.record_that_shit)


		#	if positions
			self.add_widget(self.lsm[i])

		[print('{}'.format(x)) for x in self.positions]
		#self.record_that_shit()
		# If there's too few lsm's to take up the whole screen, create a BoxLayout
		# to take up the remaining space

	def record_that_shit(self, instance=None, value=None):
		'''
		When a switch is flipped on, add the name and position from the index
		of the current lsm.
		'''

		print('instance.text:', instance)
		print('value:', value)

		# Open db connection, get required teammate_training data, close conn.

		teammates_training = libs.apa_database.get_data(table_name='teammate_modelID_positionnum', specific_data=False, column_name=None, model=None,
						order_by_column=None)

		print('tt',teammates_training)

		print('But let us try instance.parent.ids.position_label.text:', \
				instance.parent.ids.position_label.text)

		## Get the entry of the position chart associated with the IsSheTrained()
		## parent of the switch

		# self.lsm.find(instance.parent)
		index = self.lsm.index(instance.parent)

		# Use that position to call the entry from self.positions
		current_position = self.positions[index]

		# Test it
		# print(current_position)


		teammate_name = App.get_running_app().teammate_name
		print(teammate_name)


		#for each

		# if switch == Active
		if value == True:
			print('# if switch == Active')
			# Check if entry of (teammate_name, modelID, and position_num) are there
			# by concatenating tuples of (teammate_name,) + the current value of
			# position chart and comparing that to each entry in the fetchall
			if (teammate_name,) + current_position in teammates_training:
				# if it exists, leave it there
				print('# if it exists, leave it there')
				print(True, "The entry's already there. Leave it.")

			else:

				# Testing the data
				print('Pre-entry\n\n', {print('{}'.format(x)) for x in teammates_training})

				# elif it doesn't exist, add it
				print("## elif it doesn't exist, add it")
				libs.apa_database.insert_data(tb='teammate_modelID_positionnum', \
				col1='teammate', data1=teammate_name, col2='modelID', \
				data2=current_position[0], col3='positionNum', data3=current_position[1], \
				col4=None, data4=None, col5=None, data5=None)

				teammates_training_after = libs.apa_database.get_data(table_name='teammate_modelID_positionnum', specific_data=False, column_name=None, model=None,
								order_by_column=None)

				# Testing the data--print only the item that's in one set, but not the other
				#print('Post-entry:\n\n', {print('{}'.format(x)) for x in teammates_training_after})
				#print('Difference:', set(teammates_training_after) - set(teammates_training))

		# elif switch == Inactive
		else:
			print('# elif switch == Inactive')
			print('teammate_name:', teammate_name)
			print('current_position[0]:', current_position[0])
			print('current_position[1]:', current_position[1])
			if (teammate_name,) + current_position in teammates_training:

				# Testing the data
				#print('Pre-entry\n\n', {print('{}'.format(x)) for x in teammates_training})

				# # if it exists, remove it
				libs.apa_database.delete_training_entry(self, teammate=teammate_name, \
					modelID=current_position[0], positionNum=current_position[1])

				teammates_training_after = libs.apa_database.get_data(table_name='teammate_modelID_positionnum', specific_data=False, column_name=None, model=None,
								order_by_column=None)

				# Testing the data--print only the item that's in one set, but not the other
				#print('Post-entry:\n\n', {print('{}'.format(x)) for x in teammates_training_after})
				#print('Difference:', set(teammates_training_after) - set(teammates_training))

			else:

				# elif it doesn't exist, leave it
				print(True, "The entry doesn't exist. Leave it.")

		# Close connection

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
