// клиентская сторона socket-соединения

var pushMeConnection = {

    conn: undefined,

    reconnectTimeout: 5000,

    listenerIdSeq: 1,

    listeners: {},
    callbacks: {},

    MAGIC_TOPIC: '-<*>-', // id топика, на который "подписываются"
                          // слушатели, для которых топик не указан.
                          // Такие слушетели будут получать все сообщения.

    connect: function(host, port, uid) {
        var pushme = this;
        // создает SockJS-соединение с указанным хостом/портом,
        // идентифицируемое на серверной стороне по uid
        if (!this.conn) {
            var conn = new SockJS(host + ':' + port + '/pull');

            conn.onopen = function() { conn.send(uid); };

            conn.onmessage = function(msg) {
                pushme.processMessage(msg);
            };

            conn.onclose = function() {
                delete pushme.conn;
                var tOut = setTimeout(
                    function() {
                        clearTimeout(tOut);
                        pushme.connect(host, port, uid);
                    },
                    pushme.reconnectTimeout
                );
            };

            this.conn = conn;

        } else {
            console.error('Already connected!');
        };
    },

    processMessage: function(e) {
        var msg = JSON.parse(e.data),
            topic = msg.topic,
            fanouts = this.callbacks[this.MAGIC_TOPIC],
            handlers = this.callbacks[topic];

        for (var key in fanouts) {
            fanouts[key](msg.data, topic);
        };

        for (var key in handlers) {
            handlers[key](msg.data, topic);
        };
    },

    subscribe: function(callback, topic) {
        // добавляет callback к подписчикам, возвращает id,
        // с помощью которого callback может быть отписан
        // если topic не указан - подписчик будет получать все
        this.listenerIdSeq += 1;
        var id = this.listenerIdSeq,
            topic = topic || this.MAGIC_TOPIC;
        if (!this.callbacks[topic]) {
            this.callbacks[topic] = {}
        };
        this.callbacks[topic][id] = callback;
        this.listeners[id] = topic;
        return id;
    },

    unsubscribe: function(id) {
        // отписывает callback по идентификатору id,
        // который ранее вернул метод subscribe
        if (this.listeners[id]) {
            delete this.callbacks[this.listeners[id]][id];
            delete this.listeners[id];
        } else {
            console.error('Wrong listener id:', id);
        };
    },
};
