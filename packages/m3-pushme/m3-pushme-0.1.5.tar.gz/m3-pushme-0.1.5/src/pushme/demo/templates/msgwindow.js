var inp = Ext.getCmp('{{ component.inp.client_id }}');
var out = Ext.getCmp('{{ component.out.client_id }}');

var callbackId = pushMeConnection.subscribe(
    function(msg) {
        out.setValue(out.value + '\n' + msg);
    },
	'echo' // конкретный топик
);

// этот слушатель будет получать все сообщения, вне зависимости от их топика
var fanout = pushMeConnection.subscribe(
	function(msg, topic) {
		console.log(topic, ':', msg)
	}
);

win.on('close', function() {
    pushMeConnection.unsubscribe(callbackId);
    pushMeConnection.unsubscribe(fanout);
});

function sendMessage() {
    Ext.Ajax.request({
        url: '{{ component.send_url }}',
        params: { message: inp.getValue() },
        method: 'POST'
    });
};
