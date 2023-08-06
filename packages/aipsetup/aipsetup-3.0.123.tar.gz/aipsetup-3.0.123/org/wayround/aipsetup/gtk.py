
import os.path
import logging

import org.wayround.utils.gtk

_gtk_session = None


def start_session():
    """
    Start GTK session
    """

    from gi.repository import Gtk

    global _gtk_session

    import signal

    if not _gtk_session:
        logging.debug("start_session")

        signal.signal(signal.SIGINT, signal.SIG_DFL)

        _gtk_session = True

        MainWindow()

        try:
            Gtk.main()
        except:
            logging.exception("Exception while running Gtk.main()")
            stop_session()

        _gtk_session = None


def stop_session():
    """
    Stop GTK session
    """

    global _gtk_session

    if _gtk_session:
        logging.debug("stop_session")
        from gi.repository import Gtk

        Gtk.main_quit()


class MainWindow:
    """
    Overall aipsetup system window

    Exists ensure everything is Ok

    This window created and shown on :func:`start_session`
    """

    def __init__(self):

        from gi.repository import Gtk

        self.currently_opened = None

        ui_file = os.path.join(
            os.path.dirname(__file__), 'gui', 'main_loop.glade'
            )

        ui = Gtk.Builder()
        ui.add_from_file(ui_file)

        self.ui = org.wayround.utils.gtk.widget_dict(ui)

        self.ui['window1'].connect("delete-event", Gtk.main_quit)

        self.ui['button1'].connect(
            'clicked',
            self.onExitClicked
            )

        self.ui['button2'].connect(
            'clicked',
            self.onEditInfoClicked
            )

        self.ui['button3'].connect(
            'clicked',
            self.onEditLatestButtonActivated
            )
        self.ui['window1'].iconify()

        self.ui['window1'].show_all()

    def onExitClicked(self, toggle):

        from gi.repository import Gtk

        Gtk.main_quit()

    def onEditLatestButtonActivated(self, toggle):

        import org.wayround.aipsetup.latesteditor

        org.wayround.aipsetup.latesteditor.main()

    def onEditInfoClicked(self, toggle):

        import org.wayround.aipsetup.infoeditor

        org.wayround.aipsetup.infoeditor.main()
