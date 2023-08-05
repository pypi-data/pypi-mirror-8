function FBAuthCheckjQuery() {}

FBAuthCheckjQuery.prototype = {
    get jqueryVersion() {
        return Number(window.jQuery.fn.jquery[0]);
    },
    get checkjQueryTag() {
        var self = this;

        if (self._checkjQueryTag == undefined) {
            self._checkjQueryTag = document.getElementById(
                'id_fbauth_check_jquery');
        }
        return self._checkjQueryTag;
    },
    get jqueryRequiredVersion() {
        var self = this;

        if (self._jqueryRequiredVersion == undefined) {
            self._jqueryRequiredVersion = self.checkjQueryTag.getAttribute(
                'jquery-required-version');
        }
        return Number(self._jqueryRequiredVersion[0]);
    },
    get jqueryCdn() {
        var self = this;

        if (self._jqueryCdn == undefined) {
            self._jqueryCdn = self.checkjQueryTag.getAttribute('jquery-cdn');
        }
        return self._jqueryCdn;
    },
    init: function() {
        var checker = new FBAuthCheckjQuery();

        if (!(window.jQuery && checker.jqueryVersion 
                < checker.jqueryRequiredVersion)) {
            $ = undefined;
            jQuery = undefined;

            var jqueryTag = document.createElement('script');

            jqueryTag.src = checker.jqueryCdn;
            jqueryTag.type = 'text/javascript';
            jqueryTag.async = true;
            document.getElementsByTagName('head')[0].appendChild(jqueryTag);
        }
    },
    ready: function(callback) {
        var interval = window.setInterval(function() {
            if (window.$ != undefined) {
                callback();
                window.clearInterval(interval);
            }
        }, 10.);
    }
};

var fbauth_jquery = new FBAuthCheckjQuery();

fbauth_jquery.init();
