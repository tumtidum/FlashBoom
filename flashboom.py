"""flASh!..bOOm! v0.0.1 - Python 3.7 - by tumtidum.

Estimate the distance of lightning by measuring the time between
the 'flash' and the 'boom' during a thunderstorm (or any other
event you can see before you can hear because of the distance).

For increased accuracy, the air temperature can also be set in
order to fine-tune the speed of sound to the conditions.

"""

from tkinter import (ttk, Tk, Frame, N, W, E, S, StringVar, BitmapImage,
                     Listbox)
from tkinter.font import Font
from time import perf_counter
from math import sqrt


class App(Frame):
    """Main application (tkinter GUI)."""

    def __init__(self, root):
        """Summary here."""
        Frame.__init__(self, root)

        # Will be used for timing.
        time_start = 0

        # Used for feedback label.
        default_text = ". . ."
        V = StringVar()
        V.set(default_text)

        # Used for history box.
        history_list = []
        hist_compare_list = []
        history_var = StringVar()
        history_var.set(value=history_list)

        # Definitions used by the buttons.
        def flasher():
            """Actions for the flash button."""
            nonlocal time_start
            time_start = perf_counter()
            boom_button['state'] = 'normal'
            reset_button['state'] = 'normal'
            boom_button.focus_set()
            return time_start and V.set("Waiting for bOOm..")

        def boomer():
            """Actions for the boom button."""
            time_end = perf_counter()
            execution_time = float("%.2f" % (time_end - time_start))
            # Calculate speed of sound based on given air temperature.
            temp_celcius = int(temp_input.get())
            speed_sound_air = float("%.2f" % (331.3 * sqrt(1 +
                                              (temp_celcius / 273.15))))
            # Distance calculation.
            distance = int(execution_time * speed_sound_air)
            boom_button['state'] = 'disabled'
            flash_button.focus_set()
            # Add distance to history box.
            historyBoxer(distance)
            history_var.set(history_list)
            return V.set("± " + str(distance) + " metres")

        def resetter():
            """Actions for the reset button."""
            boom_button['state'] = 'disabled'
            reset_button['state'] = 'disabled'
            flash_button.focus_set()
            del history_list[:]
            del hist_compare_list[:]
            history_var.set(history_list)
            return V.set(default_text)

        def spacer(s, totalspace=14):
            """Fake TABs.

            To get around TAB display issue in listboxs on linux and
            probably Windows as well.

            """
            space = totalspace - len(s)
            return s + space * " "

        def historyBoxer(x):
            """Add latest measurement to history and compare to previous."""
            if history_list != []:
                a = hist_compare_list[0]
                hist_compare_list.insert(0, x)
                # Keep compare list small, only latest two values needed.
                if len(hist_compare_list) > 2:
                    hist_compare_list.pop(2)
                else:
                    pass
                b = hist_compare_list[0]
                if b > a:
                    history_list.insert(0, spacer(" " +
                                        str(hist_compare_list[0]) +
                                        " m") + ">")
                if b < a:
                    history_list.insert(0, spacer(" " +
                                        str(hist_compare_list[0]) +
                                        " m") + "<")
                if b is a:
                    history_list.insert(0, spacer(" " +
                                        str(hist_compare_list[0]) +
                                        " m") + "=")
            else:
                hist_compare_list.insert(0, x)
                history_list.insert(0, " " + str(hist_compare_list[0]) + " m")

        # Frames.
        # Rootframe.
        rootframe = ttk.Frame(
            root,
            padding='16 16 16 12',
            )
        rootframe.grid(
            column=0,
            row=0,
            sticky=(N, W, E, S)
            )
        # Frame one.
        frame_one = ttk.Frame(
            rootframe,
            padding='0 0 0 0'
            )
        frame_one.grid(
            column=0,
            row=0,
            sticky=(N, W, E, S)
            )
        # Inputframe.
        inputframe = ttk.Frame(
            frame_one,
            padding='8 0 8 0'
            )
        inputframe.grid(
            column=0,
            row=1,
            sticky=(N, W, E, S)
            )

        # Content.
        # Flash and boom images.
        image_1 = ttk.Label(
            frame_one,
            image=img_flash,
            padding='40 0 0 10'
            )
        image_1.grid(
            column=0,
            row=0,
            sticky=W
            )
        image_2 = ttk.Label(
            frame_one,
            image=img_boom,
            padding='0 0 28 10'
            )
        image_2.grid(
            column=0,
            row=0,
            sticky=E
            )

        # Flash button.
        flash_button = ttk.Button(
            inputframe,
            text='flASh!',
            command=lambda: flasher()
            )
        flash_button.grid(
            column=0,
            row=0,
            columnspan=1,
            rowspan=1,
            padx=1,
            pady=0,
            sticky=E
            )
        flash_button.focus_set()

        # Boom button.
        boom_button = ttk.Button(
            inputframe,
            text='bOOm!',
            state='disabled',
            command=lambda: boomer()
            )
        boom_button.grid(
            column=1,
            row=0,
            columnspan=1,
            rowspan=1,
            padx=1,
            pady=0,
            sticky=E
            )

        # Reset button.
        reset_button = ttk.Button(
            inputframe,
            text='Reset',
            state='disabled',
            command=lambda: resetter()
            )
        reset_button.grid(
            column=0,
            row=1,
            columnspan=1,
            rowspan=1,
            padx=2,
            pady=3,
            sticky=E
            )

        # Temperature input.
        temp_input = ttk.Spinbox(
            inputframe,
            width=3,
            from_=-80,
            to_=80,
            state='disabled',
            takefocus=False
            )
        temp_input.grid(
            column=1,
            row=1,
            columnspan=1,
            rowspan=1,
            padx=2,
            pady=3,
            sticky=W
            )
        temp_input.set(20)

        # °C text label.
        temp_txt = ttk.Label(
            inputframe,
            text="°C",
            padding='0 0 13 0'
            )
        temp_txt.grid(
            column=1,
            row=1,
            sticky=E
            )

        # Feedback/display label.
        feedback = ttk.Label(
            frame_one,
            text="Feedback..",
            textvariable=V,
            font=Font(weight='bold'),
            padding='0 12 0 8'
            )
        feedback.grid(
            column=0,
            row=2,
            sticky=S
            )

        # History box with scrollbar.
        history_scroll = ttk.Scrollbar(frame_one)
        history_scroll.grid(
            column=0,
            row=3,
            padx=0,
            pady=8,
            sticky=(N, S, E)
            )
        history_box = Listbox(
            frame_one,
            listvariable=history_var,
            font='courier',
            width=16,
            height=5,
            state='disabled',
            disabledforeground='black',
            # selectmode='extended',
            takefocus=0,
            yscrollcommand=history_scroll.set
            )
        history_box.grid(
            column=0,
            row=3,
            padx=8,
            pady=8,
            sticky=(N, S, W)
            )
        history_scroll.config(command=history_box.yview)


# Let's put this thing in motion!
if __name__ == '__main__':
    root = Tk()
    root.title('flASh!..bOOm!')
    # Load and assign images, odd it has to be here, but else won't work.
    img_flash = BitmapImage(file="img/flash.xbm", foreground='orange')
    img_boom = BitmapImage(file="img/boom.xbm", foreground='red')
    app = App(root)
    root.mainloop()
