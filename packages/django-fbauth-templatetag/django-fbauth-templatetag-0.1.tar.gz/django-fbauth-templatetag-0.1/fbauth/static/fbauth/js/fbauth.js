function FBAuthFacade() {}

FBAuthFacade.prototype = {
    get fbAuthTag() {
        var self = this;

        if (self._fbAuthTag == undefined) {
            self._fbAuthTag = document.getElementById('id_fbauth');
        }
        return self._fbAuthTag;
    },
    get fbApi() {
        var self = this;

        if (self._fbApi == undefined) {
            self._fbApi = self.fbAuthTag.getAttribute('facebook-api');
        }
        return self._fbApi;
    },
    get appId() {
        var self = this;
        
        if (self._appId == undefined) {
            self._appId = self.fbAuthTag.getAttribute('app-id');
        }
        return self._appId;
    },
    get channelUrl() {
        var self = this;

        if (self._channelUrl == undefined) {
            self._channelUrl = self.fbAuthTag.getAttribute('channel-url');
        }
        return self._channelUrl;
    },
    get redirectUrl() {
        var self = this;

        if (self._redirectUrl == undefined) {
            self._redirectUrl = self.fbAuthTag.getAttribute('redirect-url');
        }
        return self._redirectUrl;
    },
    isConnected: function(response) {
        return response.status == 'connected';
    },
    onLogin: function(response) {
        var self = this;

        if (self.isConnected(response)) {
            window.location.href = self.redirectUrl.format(
                response.authResponse.accessToken);
        }
    },
    getLoginStatus: function() {
        var self = this;

        FB.getLoginStatus(function(response) {
            if (self.isConnected(response)) {
                self.onLogin(response);
            }
            else {
                FB.login(function(response) {
                    self.onLogin(response)
                }, {scope: 'public_profile,email'});
            }
        });
    },
    init: function() {
        var self = this;

        $.ajaxSetup({ cache: true });

        // Loads Facebook SDK for Javacript
        $.ajax(self.fbApi, {
            async: false,
            cache: true,
            dataType: 'script',
            success: function(data, textStatus, jqXHR) {
                FB.init({
                    appId: self.appId,
                    status: true,
                    cookie: true,
                    xfml: true,
                    channelUrl: self.channelUrl,
                    version: 'v2.1'
                });
            }
        });
    }
};

fbauth_jquery.ready(function() {
    var facade = new FBAuthFacade();

    facade.init();

    $('button.facebook').click(function(e) {
        facade.getLoginStatus();
        e.preventDefault();
        e.stopPropagation();
    });
});
