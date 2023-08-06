if (typeof(tornadopush) === 'undefined') {
    var tornadopush = {};
}

(function(tp) {

    var debug = function(o) {
        if (tp.DEBUG) {
            console.log(o);
        }
    };

    tp.Presence = (function() {
        var noop = function() {};

        var _ = function(socket) {
            this.onjoin = noop;
            this.onmeta = noop;
            this.onleave = noop;
            this.onmessage = noop;
            this._users = {};
            this.user_meta = {};
            this._send_buffer = [];
            this._first_connect = true;
            if (socket) {
                this.listen(socket);
            }
        };

        _.from_url = function(url) {
            var ws = ReconnectingWebSocket ? ReconnectingWebSocket : WebSocket;
            return new _(new ws(url));
        };

        _.prototype.listen = function(socket) {
            this.socket = socket;
            var prev_onmessage = socket.onmessage,
                prev_onopen = socket.onopen,
                self = this;
            socket.onopen = function(e) {
                if (prev_onopen) {
                    prev_onopen(e);
                }
                self._flush_send_buffer();
            };
            socket.onmessage = function(e) {
                if (prev_onmessage) {
                    prev_onmessage(e);
                }
                if (e.data.substr(0, 9) === 'presence:') {
                    self.handle_message(e.data.substr(9));
                } else if (e.data.substr(0, 15) === 'presence_bcast:') {
                    self.handle_broadcast(e.data.substr(15));
                }
            };
        };

        _.prototype.handle_message = function(msg) {
            var op = msg.substr(0, 1),
                id = msg.substr(1, msg.indexOf(';') - 1),
                meta = msg.substr(msg.indexOf(';') + 1);
            if (op === '+') {
                var is_new = typeof(this._users[id]) === 'undefined';
                this._users[id] = JSON.parse(meta);
                if (is_new) {
                    debug('Presence: user #' + id + ' joined');
                    this.onjoin(id);
                } else {
                    debug('Presence: updated meta for user #' + id);
                }
                this.onmeta(id, meta);
            } else if (op === '-' && typeof(this._users[id]) !== 'undefined') {
                delete this._users[id];
                debug('Presence: user #' + id + ' left');
                this.onleave(id);
            }
        };

        _.prototype.handle_broadcast = function(data) {
            var from_id = data.substr(0, data.indexOf(';')),
                msg = data.substr(data.indexOf(';') + 1);
            debug('Recieved broadcasted message from #' + from_id + ': ' + msg);
            this.onmessage(from_id, msg);
        };

        _.prototype._send = function(msg) {
            if (!this.socket) {
                throw Error('No sockets for presence broadcast (this can happen if you are using presence through SSE)');
            } else if (this.socket.readyState === WebSocket.CONNECTING) {
                this._send_buffer.push(msg);
            } else if (this.socket.readyState === WebSocket.OPEN) {
                this.socket.send(msg);
            }
        };

        _.prototype._flush_send_buffer = function() {
            for (var i in this._send_buffer) {
                this.socket.send(this._send_buffer[i]);
            }
            this._send_buffer = [];
        };

        _.prototype.set_meta = function(meta) {
            this.user_meta = meta;
            this._send_meta();
        };

        _.prototype.set_meta_prop = function(name, value) {
            this.user_meta[name] = value;
            this._send_meta();
        };

        _.prototype._send_meta = function() {
            var data = JSON.stringify(this.user_meta);
            this._send('presence:meta:' + data);
            debug('Set presence meta: ' + data);
        };

        _.prototype.users = function() {
            return this._users;
        };

        _.prototype.user_ids = function() {
            return Object.keys(this._users);
        };

        _.prototype.get_user_meta = function(id) {
            return this._users[id];
        };

        _.prototype.broadcast = function(message) {
            this._send('presence:bcast:' + message);
            debug('Message broadcasted: ' + message);
        };

        return _;
    })();

    tp.join = function(channel) {
        if (!tp.ws_support) {
            throw Error('Presence notification requires WebSocket support');
        }
        var path = '/presence' + (channel ? '/' + channel : '');
        tp.presence = tp.Presence.from_url(tp.url(path));
        return tp.presence;
    };

})(tornadopush);