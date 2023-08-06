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
            this.onleave = noop;
            this._users = {};
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
            var prev_handler = socket.onmessage;
            var self = this;
            socket.onmessage = function(e) {
                if (prev_handler) {
                    prev_handler(e);
                }
                if (e.data.substr(0, 9) === 'presence:') {
                    self.handle_message(e.data.substr(9));
                }
            };
        };

        _.prototype.handle_message = function(msg) {
            var self = this;
            msg.split(';').forEach(function(u) {
                var op = u.substr(0, 1), id = u.substr(1);
                if (op === '+' && typeof(self._users[id]) === 'undefined') {
                    self._users[id] = true;
                    debug('Presence: user #' + id + ' joined');
                    self.onjoin(id);
                } else if (op === '-' && typeof(self._users[id]) !== 'undefined') {
                    delete self._users[id];
                    debug('Presence: user #' + id + ' left');
                    self.onleave(id);
                }
            });
        };

        _.prototype.list_users = function() {
            return Object.keys(this._users);
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