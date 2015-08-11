demoApp.factory('favicoService', function() {
        var favico = new Favico({
            animation : 'pop'
        });

        var badge = function(num, opts) {
            opts = opts || {};
            favico.badge(num,opts);
        };
        var reset = function() {
            favico.reset();
        };

        return {
            badge : badge,
            reset : reset
        };
});