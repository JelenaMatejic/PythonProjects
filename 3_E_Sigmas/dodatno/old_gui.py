from curses import window
import tkinter as tk

# GUI
# prozor za prikaz elemenata
window = tk.Tk()
window.geometry("800x500")

# dugme
button = tk.Button(window, text="Calculate", command=nk.nerode(), font=('Arial', 18))
button.pack()

window.mainloop()


window = tk.Tk() # kreiranje prozora
window.geometry("800x500") # zadavanje dimenzija prozoru
window.title("Nerodova konstrukcija") # naslov u prozoru

label = tk.Label(window, text="Hello world", font=('Arial', 18))
label.pack(padx=10, pady=10)

textbox = tk.Text(window, height=3, font=('Arial', 16))
textbox.pack(padx=10, pady=10)

button = tk.Button(window, text="Click me!", font=('Arial', 18))
button.pack()

window.mainloop()

 # for line in file.readlines():
        #     if "start" in line:
        #         line = file.next()
        #         print(line)
        #     elif "end" in line:
        #         line = file.next()
        #         print(line)
        #     else:
        #         print(line)

        # data = file.read()
        # data = data.split(",")

# with file:                
        #     l = [[float(num) for num in line.split(',')] for line in file]
        # print(l)


