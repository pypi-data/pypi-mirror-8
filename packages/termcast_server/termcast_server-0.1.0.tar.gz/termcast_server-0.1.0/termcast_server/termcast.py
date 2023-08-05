import time
import json
import re

import vt100

auth_re = re.compile(b'^hello ([^ ]+) ([^ ]+)$')
extra_data_re = re.compile(b'\033\]499;([^\007]*)\007')

clear_patterns = [
    b"\033[H\033[J",
    b"\033[H\033[2J",
    b"\033[2J\033[H",
    # this one is from tmux - can't possibly imagine why it would choose to do
    # things this way, but i'm sure there's some kind of reason
    # it's not perfect (it's not always followed by a \e[H, sometimes it just
    # moves the cursor to wherever else directly), but it helps a bit
    lambda handler: b"\033[H\033[K\r\n\033[K" + b"".join([b"\033[1B\033[K" for i in range(handler.rows - 2)]) + b"\033[H",
]

class Handler(object):
    def __init__(self, rows, cols):
        self.created_at = time.time()
        self.idle_since = time.time()
        self.rows = rows
        self.cols = cols
        self.buf = b''
        self.prev_read = b''
        self.vt = vt100.vt100(rows, cols)

    def process(self, data):
        to_process = self.prev_read + data
        processed = self.vt.process(to_process)
        self.prev_read = to_process[processed:]

        self.buf += data

        extra_data = {}
        while True:
            m = extra_data_re.search(self.buf)
            if m is None:
                break
            try:
                extra_data_json = m.group(1).decode('utf-8')
                extra_data = json.loads(extra_data_json)
            except Exception as e:
                print("failed to parse metadata: %s" % e, file=sys.stderr)
                pass
            self.buf = self.buf[:m.start(0)] + self.buf[m.end(0):]
        if "geometry" in extra_data:
            self.rows = extra_data["geometry"][1]
            self.cols = extra_data["geometry"][0]
            self.vt.set_window_size(self.rows, self.cols)

        for pattern in clear_patterns:
            if type(pattern) == type(lambda x: x):
                pattern = pattern(self)
            clear = self.buf.rfind(pattern)
            if clear != -1:
                print("found a clear")
                self.buf = self.buf[clear + len(pattern):]

        self.idle_since = time.time()

    def get_term(self):
        term = ''
        for i in range(0, self.rows):
            for j in range(0, self.cols):
                term += self.vt.cell(i, j).contents()
            term += "\n"

        return term[:-1]

    def total_time(self):
        return self._human_readable_duration(time.time() - self.created_at)

    def idle_time(self):
        return self._human_readable_duration(time.time() - self.idle_since)

    def _human_readable_duration(self, duration):
        days = 0
        hours = 0
        minutes = 0
        seconds = 0

        if duration > 60*60*24:
            days = duration // (60*60*24)
            duration -= days * 60*60*24
        if duration > 60*60:
            hours = duration // (60*60)
            duration -= hours * 60*60
        if duration > 60:
            minutes = duration // 60
            duration -= minutes * 60
        seconds = duration

        ret = "%02ds" % seconds
        if minutes > 0 or hours > 0 or days > 0:
            ret = ("%02dm" % minutes) + ret
        if hours > 0 or days > 0:
            ret = ("%02dh" % hours) + ret
        if days > 0:
            ret = ("%dd" % days) + ret

        return ret

class Connection(object):
    def __init__(self, client, connection_id, publisher):
        self.client = client
        self.connection_id = connection_id
        self.publisher = publisher
        self.viewers = 0

    def run(self):
        buf = b''
        while len(buf) < 1024 and b"\n" not in buf:
            buf += self.client.recv(1024)

        pos = buf.find(b"\n")
        if pos == -1:
            print("no authentication found")
            return

        auth = buf[:pos]
        if auth[-1:] == b"\r":
            auth = auth[:-1]

        buf = buf[pos+1:]

        m = auth_re.match(auth)
        if m is None:
            print("no authentication found (%s)" % auth)
            return

        print(b"got auth: " + auth)
        self.name = m.group(1)
        self.client.send(b"hello, " + self.name + b"\n")

        extra_data = {}
        m = extra_data_re.match(buf)
        if m is not None:
            try:
                extra_data_json = m.group(1).decode('utf-8')
                extra_data = json.loads(extra_data_json)
            except Exception as e:
                print("failed to parse metadata: %s" % e, file=sys.stderr)
                pass
            buf = buf[len(m.group(0)):]

        if "geometry" in extra_data:
            self.handler = Handler(
                extra_data["geometry"][1], extra_data["geometry"][0]
            )
        else:
            self.handler = Handler(24, 80)

        self.handler.process(buf)
        while True:
            buf = b''
            try:
                buf = self.client.recv(1024)
            except Exception as e:
                print('*** recv failed: ' + str(e))

            if len(buf) > 0:
                self.publisher.notify(
                    "new_data", self.connection_id, self.handler.buf, buf
                )
                self.handler.process(buf)
            else:
                self.publisher.notify("streamer_disconnect", self.connection_id)
                return

    def msg_new_viewer(self, connection_id):
        if connection_id != self.connection_id:
            return
        self.viewers += 1
        self.publisher.notify(
            "new_data", self.connection_id, self.handler.buf, b''
        )
        self.client.send(b"msg watcher connected\n")

    def msg_viewer_disconnect(self, connection_id):
        if connection_id != self.connection_id:
            return
        self.client.send(b"msg watcher disconnected\n")
        self.viewers -= 1

    def request_get_streamers(self):
        return {
            "name": self.name,
            "id": self.connection_id,
            "rows": self.handler.rows,
            "cols": self.handler.cols,
            "idle_time": self.handler.idle_time(),
            "total_time": self.handler.total_time(),
            "viewers": self.viewers,
        }
