from tkinter import *
from tkinter import ttk as tk

class ComboText(tk.Frame):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent)
        self.parent = parent
        self._job = None
        self.data = []
        self['background'] = 'white'
        self.text = tk.Text(self, **kwargs)
        self.text.pack(side=tk.LEFT, expand=tk.YES, fill='x')
        symbol = u"\u25BC"
        self.button = tk.Button(self,width = 2,text=symbol, background='white',relief = 'flat', command = self.showOptions)
        self.button.pack(side=tk.RIGHT)

        #pass bindings from parent frame widget to the inner Text widget
        #This is so you can bind to the main ComboText and have those bindings
        #apply to things done within the Text widget.
        #This could also be applied to the inner button widget, but since
        #ComboText is intended to behave "like" a Text widget, I didn't do that
        bindtags = list(self.text.bindtags())
        bindtags.insert(0,self)
        self.text.bindtags(tuple(bindtags))

    def showOptions(self):

        #Get the coordinates of the parent Frame, and the dimensions of the Text widget
        x,y,width,height = [self.winfo_rootx(), self.winfo_rooty(), self.text.winfo_width(), self.text.winfo_height()]

        self.toplevel = tk.Toplevel()
        self.toplevel.overrideredirect(True) #Use this to get rid of the menubar

        self.listbox = tk.Listbox(self.toplevel,width=width, height =len(self.data))
        self.listbox.pack()

        #Populate the options in the listbox based on self.data
        for s in self.data:
            self.listbox.insert(tk.END,s)


        #Position the Toplevel so that it aligns well with the Text widget
        list_height = self.listbox.winfo_reqheight()
        self.toplevel.geometry("%dx%d+%d+%d" % (width, list_height, x, y+height))

        self.listbox.focus_force()
        self.listbox.bind("<Enter>", self.ListboxHighlight)
        self.listbox.bind("<Leave>",self.stopListboxHighlight)
        self.listbox.bind("<Button-1>",self.selectOption)
        self.toplevel.bind("<Escape>", self.onCancel)
        self.toplevel.bind("<FocusOut>", self.onCancel)


    def ListboxHighlight(self,*ignore):
        #While the mouse is moving within the listbox,
        #Highlight the option the mouse is over
        x,y = self.toplevel.winfo_pointerxy()
        widget = self.toplevel.winfo_containing(x,y)

        idx = self.listbox.index("@%s,%s" % (x-self.listbox.winfo_rootx(),y-self.listbox.winfo_rooty()))
        self.listbox.selection_clear(0,100) #very sloppy "Clear all"
        self.listbox.selection_set(idx)
        self.listbox.activate(idx)
        self._job = self.after(25,self.ListboxHighlight)

    def stopListboxHighlight(self,*ignore):
        #Stop the recurring highlight function.
        if self._job:
            self.after_cancel(self._job)
            self._job = None

    def onCancel(self,*ignore):
        #Stop callback function to avoid error once listbox destroyed.
        self.stopListboxHighlight()

        #Destroy the popup Toplevel
        self.toplevel.destroy()

    def selectOption(self,event):
        x,y = [event.x,event.y]
        idx = self.listbox.index("@%s,%s" % (x,y))

        if self.data:
            self.text.delete('1.0','end')
            self.text.insert('end',self.data[idx])

        self.stopListboxHighlight()
        self.toplevel.destroy()
        self.text.focus_force()

    def setOptions(self,optionList):
        self.data = optionList

    #Map the Text methods onto the ComboText class so that
    #the ComboText can be treated like a regular Text widget
    #with some other options added in.
    #This was necessary because ComboText is a subclass of Frame, not Text
    def __getattr__(self,name):
        def textMethod(*args, **kwargs):
            return getattr(self.text,name)(*args, **kwargs)
        return textMethod

if __name__ == '__main__':
    root = tk.Tk()
    ct = ComboText(root, width = 50, height = 3)
    ct.pack()
    ct.setOptions(['Option %d' % i for i in range (0,5)])
    root.mainloop()