from tkinter import *
import bluetooth
# GUI
root = Tk()
root.title("Chatbot")

BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

# Send function
def send():
	send = "You -> " + e.get()
	txt.insert(END, "\n" + send)
	user = e.get().lower()
	e.delete(0, END)

def search():
    print("Looking for nearby devices .... ")
    send = "Looking for nearby devices"
    txt.insert(END, "\n" + send)
    nearby_devices = bluetooth.discover_devices(
        duration=6, lookup_names=True, flush_cache=True, lookup_class=False)

    send = ("found %d device(s)" % len(nearby_devices))
    txt.insert(END, "\n" + send)
    
    my_list = []
    i = 1
    for addr, name in nearby_devices:    
        try:
            #print("  %s - %s" % (addr, name))
            my_list.append(["INDEX: " + str(i), "NAME: " + name,  addr])
            i += 1
        except UnicodeEncodeError:
            #print("  %s - %s" % (addr, name.encode('utf-8', 'replace')))
            my_list.append(["INDEX: " + str(i) , "NAME: " + name.encode('utf-8', 'replace'), addr])
            i += 1

    for element in my_list:
        send = str(element)
        txt.insert(END, "\n" + send)


lable1 = Label(root, bg=BG_COLOR, fg=TEXT_COLOR, text="Welcome", font=FONT_BOLD, pady=10, width=20, height=1).grid(
	row=0)

txt = Text(root, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, width=60)
txt.grid(row=1, column=0, columnspan=2)

scrollbar = Scrollbar(txt)
scrollbar.place(relheight=1, relx=0.974)

e = Entry(root, bg="#2C3E50", fg=TEXT_COLOR, font=FONT, width=55)
e.grid(row=2, column=0)

send = Button(root, text="Send", font=FONT_BOLD, bg=BG_GRAY,
			command=send).grid(row=2, column=1)

search = Button(root, text="Search", font=FONT_BOLD, bg=BG_GRAY,
			command=search).grid(row=1, column=1)

root.mainloop()
