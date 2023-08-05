var mail = mail || {};

mail.Admin = {

    frame: undefined,
    cke: undefined,

    init: function () {
        this.frame = window.frames['html'];
        django.jQuery(this.frame).on('load', this.onFrameLoad(this));
        django.jQuery('form').on('submit', this.onSubmit(this));
    },

    onSubmit: function (self) {
        return function (e) {
            self.extractData();
        }
    },

    onFrameLoad: function (self) {
        return function (e) {
            self.ajdustFrameHeight();

            self.cke = self.frame.contentWindow.CKEDITOR;
            self.cke.on('instanceReady', self.onCKEReady(self));

            for (var i in self.cke.instances) {
                self.cke.instances[i].on('change', self.onCKEInstanceChange(self));
            }
        }
    },

    onCKEReady: function(self){
        return function(e){
            self.ajdustFrameHeight();
        }
    },

    onCKEInstanceChange: function(self){
        return function(e){
            self.ajdustFrameHeight();
        }
    },

    extractData: function () {
        var data = {};
        django.jQuery.each(this.frame.contentWindow.CKEDITOR.instances, function (k, v) {
            var d = v.getData();
            if (d && d.length > 0) {
                data[k] = v.getData();
            }
        });
        if (data && data !== {}) {
            django.jQuery('input[name=html]').val(JSON.stringify(data));
        }
    },

    ajdustFrameHeight: function () {
        var h = this.frame.contentWindow.document.body.offsetHeight
        django.jQuery('iframe').height(h);
    }

};

django.jQuery(document).ready(function () {
    mail.Admin.init();
});