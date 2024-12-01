from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from arduino_controller import ArduinoController

# Main controller for the wellness lamp app
class WellnessLampController(BoxLayout):
    def __init__(self, **kwargs):
        """
        Initialize the main UI and connect to the Arduino.
        """
        super().__init__(**kwargs)
        self.orientation = "vertical"  #Arrange widgets vertically
        self.padding = 20  #Add padding around the layout
        self.spacing = 15  #Add spacing between widgets

        # Initialize Arduino communication
        self.arduino = ArduinoController(port='COM3')  #Adjust port 
        self.connected = self.arduino.connect()  #Check if connection is successful

        # Add title
        self.title = Label(
            text="Wellness Lamp Controller",  # App title
            font_size='24sp',  # Font size
            size_hint=(1, 0.2),  # Title height
            bold=True,  # Bold text
            halign="center",  # Center alignment
            valign="middle"  # Vertical alignment
        )
        self.title.bind(size=self.title.setter('text_size'))  #Center-align text
        self.add_widget(self.title)

        # Brightness Slider Section
        slider_layout = BoxLayout(orientation="vertical", spacing=15, size_hint=(1, 1))
        slider_layout.add_widget(Label(text="Adjust Brightness", font_size='18sp'))
        self.dimness_slider = Slider(min=0, max=255, value=128)  #Slider for brightness control (0-255)
        self.dimness_slider.bind(value=self.on_dimness_change)  #Attach function for slider changes
        slider_layout.add_widget(self.dimness_slider)
        self.label = Label(text="Dimness: 128", font_size='16sp', halign="center")  #Label to display brightness value
        slider_layout.add_widget(self.label)
        self.add_widget(slider_layout)

        #Color Picker Section
        picker_layout = BoxLayout(orientation="vertical", spacing=10, size_hint=(1, 3))
        picker_layout.add_widget(Label(text="Choose a Color", font_size='15sp'))  #Section title
        self.color_picker = ColorPicker(size_hint=(1, 1))  #Widget for selecting color
        self.color_picker.bind(color=self.on_color_change)  #Add function for color changes
        picker_layout.add_widget(self.color_picker)
        self.add_widget(picker_layout)

        # Send Button
        self.send_button = Button(
            text="Send Settings",  #Button label
            font_size='20sp',  #Font size for better visibility
            size_hint=(1, 0.15),  #Adjust button size
            background_color=(0.2, 0.6, 0.8, 1),  #Light blue background
            color=(1, 1, 1, 1)  #White text
        )
        self.send_button.bind(on_press=self.send_to_arduino)  #Attach function for button press
        self.add_widget(self.send_button)

    #Function for dimness slider value changes
    def on_dimness_change(self, instance, value):
    
        #Handle brightness slider changes and send the value to Arduino.
        dimness_value = int(value)  #Convert slider value to an integer
        self.label.text = f"Dimness: {dimness_value}"  #Update label with the new value
        if self.connected:
            self.arduino.send_dimness(dimness_value)  #Send dimness value to Arduino

    #Function for color picker changes
    def on_color_change(self, instance, color):
       
        #Handle color picker changes and send RGB values to Arduino.
        r, g, b = [int(c * 255) for c in color[:3]]  #Convert normalized color values (0-1) to RGB (0-255)
        print(f"Color set to RGB({r}, {g}, {b})")  #Print selected color
        if self.connected:
            self.arduino.send_color(r, g, b)  #Send RGB values to Arduino

    #Function for sending settings via the button
    def send_to_arduino(self, instance):
     
        #Resend the current brightness and color settings to Arduino.
        self.on_dimness_change(None, self.dimness_slider.value)  #Resend dimness value
        r, g, b = [int(c * 255) for c in self.color_picker.color[:3]]  #Get current color values
        self.on_color_change(None, (r / 255, g / 255, b / 255))  #Resend RGB values

#Main app class
class WellnessLampApp(App):
    def build(self):
       
        #Build and return the main UI.
       
        return WellnessLampController()

#Entry point to run the app
if __name__ == "__main__":
    WellnessLampApp().run()
