from tkinter import *
import os
from PIL import Image, ImageTk
from tkinter import messagebox
import time
import requests

start_time = time.time()

API_KEY = os.environ["API_KEY"]

class WeatherApp(Frame):

    def __init__(self,root):
        self.root = root
        self.root.geometry("500x500")
        self.photo = PhotoImage(file="Images/weathericon.png")
        self.root.iconphoto(False, self.photo)
        self.root.title("Weather Forecast")
        self.root.resizable(height=0,width=0)
        self.display_screen()

    def display_screen(self):
        self.background_image = PhotoImage(file="Images/tagicon.png")
        self.background_label = Label(self.root, background="green")
        self.city_label = Label(text="Enter a city: ",font=60,background="yellow",border=15)
        self.city_entry = Entry(self.root,bd="1",font=60)
        self.city_btn = Button(text="Search",font=60,command=self.display_data,background="lightgreen",border=3)
        self.city_label.place(x=50,y=20,relwidth=0.23,relheight=0.1)
        self.city_entry.place(x=175,y=20,relwidth=0.55,relheight=0.1)
        self.city_btn.place(x=50,y=80,relwidth=0.8,relheight=0.05)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.result_frame = Frame(self.root,background="lightblue")
        self.result_frame.place(x=50,y=120,relwidth=0.8,relheight=0.7)

    def display_data(self):
        try:
            self.city = self.city_entry.get()
            self.city = self.city.capitalize()
            self.response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={self.city}&units=metric&appid={API_KEY}")
            self.data = self.response.json()
            self.result_frame.destroy()
            self.result_frame = Frame(self.root,background="lightblue")
            self.result_frame.place(x=50, y=120, relwidth=0.8, relheight=0.7)
            self.min_temp, self.max_temp = self.data["main"]["temp_min"],self.data["main"]["temp_max"]
            self.country = self.data["sys"]["country"]
            self.first_display = self.city + ", " + self.country
            self.temp = self.data["main"]["temp"]
            self.forecast = self.data["weather"][0]["main"]
            self.felt = self.data["main"]["feels_like"]
            self.feels_like = Label(self.result_frame,text=f"Feels like: {self.felt}°C",background="lightblue")
            self.min_max = Label(self.result_frame,text=f"Daily (min-max): {self.min_temp}°C - {self.max_temp}°C",background="lightblue")
            self.city_name = Label(self.result_frame,text=self.first_display,background="lightblue")
            self.temp_label = Label(self.result_frame,text=f"Temperature: {self.temp}°C",background="lightblue")
            self.forecast_label = Label(self.result_frame,text=f"Weather: {self.forecast}",background="lightblue")
            self.city_name.pack()
            self.temp_label.pack()
            self.min_max.pack()
            self.feels_like.pack()
            self.forecast_label.pack()

        except KeyError or NameError:
            if self.city_entry.get() == "":
                error_box = messagebox.showwarning(title="Enter a city name",
                                                   message="You haven't entered a city name")
                self.city_entry = Entry(self.root, bd="1", font=60)
                self.city_entry.place(x=175, y=20, relwidth=0.55, relheight=0.1)
            else:
                error_box = messagebox.showwarning(title="Not a valid city",
                                                   message="The city you've entered isn't a valid city")
                self.city_entry = Entry(self.root, bd="1", font=60)
                self.city_entry.place(x=175, y=20, relwidth=0.55, relheight=0.1)
        except ConnectionError:
            warning_box = messagebox.showwarning(title="No internet",
                                                 message="Please check your internet connection")
            self.city_entry = Entry(self.root, bd="1", font=60)
            self.city_entry.place(x=175, y=20, relwidth=0.55, relheight=0.1)

if __name__ == '__main__':
    root = Tk()
    app = WeatherApp(root)
    root.mainloop()
    end_time = time.time()
    print(end_time - start_time)
