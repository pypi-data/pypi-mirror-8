"""Reference chat client for hangups."""

import appdirs
import argparse
import asyncio
import datetime
import logging
import os
import sys
import urwid

import hangups
from hangups.ui.notify import Notifier
from hangups.ui.utils import get_conv_name


LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
COL_SCHEMES = {
    # Very basic scheme with no colour
    'default': {
        ('active_tab', '', ''),
        ('inactive_tab', 'standout', ''),
        ('msg_date', '', ''),
        ('msg_sender', '', ''),
        ('msg_text', '', ''),
        ('status_line', 'standout', ''),
        ('tab_background', 'standout', ''),
    },
    'solarized-dark': {
        ('active_tab', 'light gray', 'light blue'),
        ('inactive_tab', 'underline', 'light green'),
        ('msg_date', 'dark cyan', ''),
        ('msg_sender', 'dark blue', ''),
        ('msg_text', '', ''),
        ('status_line', 'standout', ''),
        ('tab_background', 'underline', 'black'),
    },
}


class ChatUI(object):
    """User interface for hangups."""

    def __init__(self, cookies_path, keybindings, palette):
        """Start the user interface."""
        self._keys = keybindings

        # These are populated by on_connect when it's called.
        self._conv_widgets = {} # {conversation_id: ConversationWidget}
        self._tabbed_window = None # TabbedWindowWidget
        self._conv_list = None # hangups.ConversationList
        self._user_list = None # hangups.UserList
        self._notifier = None # hangups.notify.Notifier

        # TODO Add urwid widget for getting auth.
        try:
            cookies = hangups.auth.get_auth_stdin(cookies_path)
        except hangups.GoogleAuthError as e:
            sys.exit('Login failed ({})'.format(e))

        self._client = hangups.Client(cookies)
        self._client.on_connect.add_observer(self._on_connect)

        loop = asyncio.get_event_loop()
        self._urwid_loop = urwid.MainLoop(
            LoadingWidget(), palette, handle_mouse=False,
            event_loop=urwid.AsyncioEventLoop(loop=loop)
        )

        self._urwid_loop.start()
        try:
            # Returns when the connection is closed.
            loop.run_until_complete(self._client.connect())
        finally:
            # Ensure urwid cleans up properly and doesn't wreck the terminal.
            self._urwid_loop.stop()

    def get_conv_widget(self, conv_id):
        """Return an existing or new ConversationWidget."""
        if conv_id not in self._conv_widgets:
            set_title_cb = (lambda widget, title:
                            self._tabbed_window.set_tab(widget, title=title))
            widget = ConversationWidget(self._client,
                                        self._conv_list.get(conv_id),
                                        set_title_cb)
            self._conv_widgets[conv_id] = widget
        return self._conv_widgets[conv_id]

    def add_conversation_tab(self, conv_id, switch=False):
        """Add conversation tab if not present, and optionally switch to it."""
        conv_widget = self.get_conv_widget(conv_id)
        self._tabbed_window.set_tab(conv_widget, switch=switch)

    def on_select_conversation(self, conv_id):
        """Called when the user selects a new conversation to listen to."""
        # switch to new or existing tab for the conversation
        self.add_conversation_tab(conv_id, switch=True)

    def _on_connect(self, initial_data):
        """Handle connecting for the first time."""
        self._user_list = hangups.UserList(
            self._client, initial_data.self_entity, initial_data.entities,
            initial_data.conversation_participants
        )
        self._conv_list = hangups.ConversationList(
            self._client, initial_data.conversation_states, self._user_list,
            initial_data.sync_timestamp
        )
        self._conv_list.on_event.add_observer(self._on_event)
        self._notifier = Notifier(self._conv_list)
        # show the conversation menu
        conv_picker = ConversationPickerWidget(self._conv_list,
                                               self.on_select_conversation)
        self._tabbed_window = TabbedWindowWidget(self._keys, self._on_quit)
        self._tabbed_window.set_tab(conv_picker, switch=True,
                                    title='Conversations')
        self._urwid_loop.widget = self._tabbed_window

    def _on_event(self, conv_event):
        """Open conversation tab for new messages when they arrive."""
        if isinstance(conv_event, hangups.ChatMessageEvent):
            self.add_conversation_tab(conv_event.conversation_id)

    def _on_quit(self):
        """Handle the user quitting the application."""
        future = asyncio.async(self._client.disconnect())
        future.add_done_callback(lambda future: future.result())


class LoadingWidget(urwid.WidgetWrap):
    """Widget that shows a loading indicator."""

    def __init__(self):
        # show message in the center of the screen
        super().__init__(urwid.Filler(
            urwid.Text('Connecting...', align='center')
        ))


class ConversationPickerWidget(urwid.WidgetWrap):
    """Widget for picking a conversation."""

    def __init__(self, conversation_list, on_select):
        # Build buttons for selecting conversations ordered by most recently
        # modified first.
        convs = sorted(conversation_list.get_all(), reverse=True,
                       key=lambda c: c.last_modified)
        on_press = lambda button, conv_id: on_select(conv_id)
        buttons = [urwid.Button(get_conv_name(conv), on_press=on_press,
                                user_data=conv.id_)
                   for conv in convs]
        listbox = urwid.ListBox(urwid.SimpleFocusListWalker(buttons))
        widget = urwid.Padding(listbox, left=2, right=2)
        super().__init__(widget)


class ReturnableEdit(urwid.Edit):
    """Edit widget that clears itself and calls a function on return."""

    def __init__(self, on_return, caption=None):
        super().__init__(caption=caption)
        self._on_return = on_return

    def keypress(self, size, key):
        key = super().keypress(size, key)
        if key == 'enter':
            self._on_return(self.get_edit_text())
            self.set_edit_text('')
        else:
            return key


class StatusLineWidget(urwid.WidgetWrap):
    """Widget for showing typing status."""

    def __init__(self, conversation):
        self._typing_statuses = {}
        self._conversation = conversation
        self._conversation.on_event.add_observer(self._on_event)
        self._conversation.on_typing.add_observer(self._on_typing)
        self._widget = urwid.Text('', align='center')
        super().__init__(urwid.AttrWrap(self._widget, 'status_line'))

    def _on_event(self, conv_event):
        """Make users stop typing when they send a message."""
        if isinstance(conv_event, hangups.ChatMessageEvent):
            self._typing_statuses[conv_event.user_id] = (
                hangups.TypingStatus.STOPPED
            )
            self._update()

    def _on_typing(self, typing_message):
        """Handle typing updates."""
        self._typing_statuses[typing_message.user_id] = typing_message.status
        self._update()

    def _update(self):
        """Update list of typers."""
        typers = [self._conversation.get_user(user_id).first_name
                  for user_id, status in self._typing_statuses.items()
                  if status == hangups.TypingStatus.TYPING]
        if len(typers) > 0:
            msg = '{} {} typing...'.format(
                ', '.join(sorted(typers)),
                'is' if len(typers) == 1 else 'are'
            )
        else:
            msg = ''
        self._widget.set_text(msg)


class MessageWidget(urwid.WidgetWrap):

    """Widget for displaying a single message in a conversation."""

    def __init__(self, timestamp, text, user=None):
        # Save the timestamp as an attribute for sorting.
        self.timestamp = timestamp
        text = [
            ('msg_date', '(' + self._get_date_str(timestamp) + ') '),
            ('msg_text', text)
        ]
        if user is not None:
            text.insert(1, ('msg_sender', user.first_name + ': '))
        self._widget = urwid.Text(text)
        super().__init__(self._widget)

    @staticmethod
    def _get_date_str(timestamp):
        """Convert UTC datetime into user interface string."""
        return timestamp.astimezone(tz=None).strftime('%I:%M:%S %p')

    def __lt__(self, other):
        return self.timestamp < other.timestamp


class ConversationWidget(urwid.WidgetWrap):
    """Widget for interacting with a conversation."""

    def __init__(self, client, conversation, set_title_cb):
        client.on_disconnect.add_observer(lambda: self._show_info_message(
            'Disconnected.'
        ))
        client.on_reconnect.add_observer(lambda: self._show_info_message(
            'Connected.'
        ))
        self._client = client
        self._conversation = conversation
        self._conversation.on_event.add_observer(self._on_event)

        self._num_unread = 0
        self._set_title_cb = set_title_cb
        self._set_title()

        self._list_walker = urwid.SimpleFocusListWalker([])
        self._list_box = urwid.ListBox(self._list_walker)
        self._status_widget = StatusLineWidget(conversation)
        self._widget = urwid.Pile([
            ('weight', 1, self._list_box),
            ('pack', self._status_widget),
            ('pack', ReturnableEdit(self._on_return, caption='Send message: ')),
        ])
        # focus the edit widget by default
        self._widget.focus_position = 2

        # Display any old ConversationEvents already attached to the
        # conversation.
        for event in self._conversation.events:
            self._on_event(event)
        self._num_unread = 0
        self._set_title()

        super().__init__(self._widget)

    def keypress(self, size, key):
        """Handle marking messages as read and keeping client active."""
        # Set the client as active.
        future = asyncio.async(self._client.set_active())
        future.add_done_callback(lambda future: future.result())

        # Mark the newest event as read.
        future = asyncio.async(self._conversation.update_read_timestamp())
        future.add_done_callback(lambda future: future.result())

        # Mark messages as read.
        self._num_unread = 0
        self._set_title()
        return super().keypress(size, key)

    def _set_title(self):
        """Update this conversation's tab title."""
        title = get_conv_name(self._conversation, truncate=True)
        if self._num_unread > 0:
            title += ' ({})'.format(self._num_unread)
        self._set_title_cb(self, title)

    def _on_return(self, text):
        """Called when the user presses return on the send message widget."""
        # Ignore if the user hasn't typed a message.
        if len(text) == 0:
            return
        # XXX: Exception handling here is still a bit broken. Uncaught
        # exceptions in _on_message_sent will only be logged.
        segments = [hangups.ChatMessageSegment(text)]
        asyncio.async(
            self._conversation.send_message(segments)
        ).add_done_callback(self._on_message_sent)

    def _on_message_sent(self, future):
        """Handle showing an error if a message fails to send."""
        try:
            future.result()
        except hangups.NetworkError:
            self._show_info_message('Failed to send message.')

    def _add_message_widget(self, message_widget):
        """Add MessageWidget to the ConversationWidget.

        Automatically scroll down to show the new text if the bottom is showing
        (the last widget is focused). This allows the user to scroll up to read
        previous messages while new messages are arriving.
        """
        try:
            bottom_visible = (self._list_box.focus_position ==
                              len(self._list_walker) - 1)
        except IndexError:
            bottom_visible = True  # ListBox is empty
        self._list_walker.append(message_widget)
        self._list_walker.sort()
        if bottom_visible:
            # set_focus_valign is necessary so the last message is always shown
            # completely.
            self._list_box.set_focus(len(self._list_walker) - 1)
            self._list_box.set_focus_valign('bottom')

    def _show_info_message(self, text):
        """Display an informational message with timestamp."""
        timestamp = datetime.datetime.now(tz=datetime.timezone.utc)
        self._add_message_widget(MessageWidget(timestamp, text, None))

    def _on_event(self, conv_event):
        """Display a new conversation message."""
        user = self._conversation.get_user(conv_event.user_id)

        # XXX: If the ConversationWidget is created by a ConversationEvent, the
        # ConversationEvent will be duplicated in the list of messages.

        if isinstance(conv_event, hangups.ChatMessageEvent):
            self._add_message_widget(MessageWidget(
                conv_event.timestamp, conv_event.text, user
            ))
            # Update the count of unread messages.
            if not user.is_self:
                self._num_unread += 1

        elif isinstance(conv_event, hangups.RenameEvent):
            if conv_event.new_name == '':
                text = ('{} cleared the conversation name'
                        .format(user.first_name))
            else:
                text = ('{} renamed the conversation to {}'
                        .format(user.first_name, conv_event.new_name))
            self._add_message_widget(MessageWidget(conv_event.timestamp, text))

        elif isinstance(conv_event, hangups.MembershipChangeEvent):
            event_users = [self._conversation.get_user(user_id) for user_id
                           in conv_event.participant_ids]
            names = ', '.join([user.full_name for user in event_users])
            if conv_event.type_ == hangups.MembershipChangeType.JOIN:
                text = ('{} added {} to the conversation'
                        .format(user.first_name, names))
            else:  # LEAVE
                text = ('{} left the conversation'.format(names))
            self._add_message_widget(MessageWidget(conv_event.timestamp, text))

        # Update the title in case unread count or conversation name changed.
        self._set_title()


class TabbedWindowWidget(urwid.WidgetWrap):

    """A widget that displays a list of widgets via a tab bar."""

    def __init__(self, keybindings, quit_f):
        self._widgets = [] # [urwid.Widget]
        self._widget_title = {} # {urwid.Widget: str}
        self._tab_index = None # int
        self._quit_f = quit_f
        self._keys = keybindings
        self._tabs = urwid.Text('')
        self._frame = urwid.Frame(None)
        super().__init__(urwid.Pile([
            ('pack', urwid.AttrWrap(self._tabs, 'tab_background')),
            ('weight', 1, self._frame),
        ]))

    def _update_tabs(self):
        """Update tab display."""
        text = []
        for num, widget in enumerate(self._widgets):
            palette = ('active_tab' if num == self._tab_index
                       else 'inactive_tab')
            text += [
                (palette, ' {} '.format(self._widget_title[widget]).encode()),
                ('tab_background', b' '),
            ]
        self._tabs.set_text(text)
        self._frame.contents['body'] = (self._widgets[self._tab_index], None)

    def keypress(self, size, key):
        """Handle keypresses for changing tabs."""
        key = super().keypress(size, key)
        num_tabs = len(self._widgets)
        if key == self._keys['prev_tab']:
            self._tab_index = (self._tab_index - 1) % num_tabs
            self._update_tabs()
        elif key == self._keys['next_tab']:
            self._tab_index = (self._tab_index + 1) % num_tabs
            self._update_tabs()
        elif key == self._keys['quit']:
            self._quit_f()
        else:
            return key

    def set_tab(self, widget, switch=False, title=None):
        """Add or modify a tab.

        If widget is not a tab, it will be added. If switch is True, switch to
        this tab. If title is given, set the tab's title.
        """
        if widget not in self._widgets:
            self._widgets.append(widget)
            self._widget_title[widget] = ''
        if switch:
            self._tab_index = self._widgets.index(widget)
        if title:
            self._widget_title[widget] = title
        self._update_tabs()


def main():
    """Main entry point."""
    # Build default paths for files.
    dirs = appdirs.AppDirs('hangups', 'hangups')
    default_log_path = os.path.join(dirs.user_log_dir, 'hangups.log')
    default_cookies_path = os.path.join(dirs.user_cache_dir, 'cookies.json')

    parser = argparse.ArgumentParser(
        prog='hangups', formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    dirs = appdirs.AppDirs('hangups', 'hangups')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='log detailed debugging messages')
    parser.add_argument('--log', default=default_log_path,
                        help='log file path')
    parser.add_argument('--cookies', default=default_cookies_path,
                        help='cookie storage path')
    parser.add_argument('--key-next-tab', default='ctrl d',
                        help='keybinding for next tab')
    parser.add_argument('--key-prev-tab', default='ctrl u',
                        help='keybinding for previous tab')
    parser.add_argument('--key-quit', default='ctrl e',
                        help='keybinding for quitting')
    parser.add_argument('--col-scheme', choices=COL_SCHEMES.keys(),
                        default='default', help='colour scheme to use')
    args = parser.parse_args()

    # Create all necessary directories.
    for path in [args.log, args.cookies]:
        directory = os.path.dirname(path)
        if directory != '' and not os.path.isdir(directory):
            try:
                os.makedirs(directory)
            except OSError as e:
                sys.exit('Failed to create directory: {}'.format(e))

    log_level = logging.DEBUG if args.debug else logging.WARNING
    logging.basicConfig(filename=args.log, level=log_level, format=LOG_FORMAT)
    # urwid makes asyncio's debugging logs VERY noisy, so adjust the log level:
    logging.getLogger('asyncio').setLevel(logging.WARNING)

    try:
        ChatUI(args.cookies, {
            'next_tab': args.key_next_tab,
            'prev_tab': args.key_prev_tab,
            'quit': args.key_quit,
        }, COL_SCHEMES[args.col_scheme])
    except KeyboardInterrupt:
        sys.exit('Caught KeyboardInterrupt, exiting abnormally')
    except:
        # urwid will prevent some exceptions from being printed unless we use
        # print a newline first.
        print('')
        raise


if __name__ == '__main__':
    main()
