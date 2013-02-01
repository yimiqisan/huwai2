// post
jQuery.postJSON = function(url, type, args, callback) {
    $.ajax({url: url, data: $.param(args), dataType: "text", type: type, async: false,
            success: function(response) {
                if (callback) callback(eval("(" + response + ")"));
            }, error: function(response) {
                console.log("ERROR:", response)
            }});
};

// cookie
(function($) {
    $.cookie = function(key, value, options) {
        // key and at least value given, set cookie...
        if (arguments.length > 1 && (!/Object/.test(Object.prototype.toString.call(value)) || value === null || value === undefined)) {
            options = $.extend({}, options);

            if (value === null || value === undefined) {
                options.expires = -1;
            }
            if (typeof options.expires === 'number') {
                var days = options.expires, t = options.expires = new Date();
                t.setDate(t.getDate() + days);
            }
            value = String(value);
            return (document.cookie = [
                encodeURIComponent(key), '=', options.raw ? value : encodeURIComponent(value),
                options.expires ? '; expires=' + options.expires.toUTCString() : '', // use expires attribute, max-age is not supported by IE
                options.path    ? '; path=' + options.path : '',
                options.domain  ? '; domain=' + options.domain : '',
                options.secure  ? '; secure' : ''
            ].join(''));
        }
        // key and possibly options given, get cookie...
        options = value || {};
        var decode = options.raw ? function(s) { return s; } : decodeURIComponent;

        var pairs = document.cookie.split('; ');
        for (var i = 0, pair; pair = pairs[i] && pairs[i].split('='); i++) {
            if (decode(pair[0]) === key) return decode(pair[1] || ''); // IE saves cookies with empty string as "c; ", e.g. without "=" as opposed to EOMB, thus pair[1] may be undefined
        }
        return null;
    };
})(jQuery);

// check
!function( $ ){
    "use strict"
/* CHECK CLASS DEFINITION */
var censor = '.censor'

,Check = function ( el ) {
    $(el).on('click', censor, this.censor)
}
Check.prototype = {
    constructor: Check
    
    , censor: function ( e ) {
        e && e.preventDefault();
        var $that = $(this)
        , form = $that.closest('form')
        , url = form.attr('action')
        , flag = true;
        form.find('.help-inline').each(function(i, e){
            var g = $(this).closest('.control-group')
            , n = $(this).closest('.controls').attr('for')
            , c = g.find('[name='+n+']');
            if (g.hasClass('info')) { flag=false;return true;}
            g.removeClass('error').removeClass('info').removeClass('success');
            if (g.hasClass('hide')) { return true; }
            if (!c.val()) {flag = false;g.addClass('error');return true;}
        })
        $that.trigger('censorn');
        if(flag){
            form.submit();
        }
        return false;
    }
}

/* CHECK PLUGIN DEFINITION */
$.fn.check = function ( option ) {
    return this.each(function () {
        var $this = $(this), data = $this.data('check')
        if (!data) $this.data('check', (data = new Check(this)))
        if (typeof option == 'string') data[option].call($this)
    })
}

$.fn.check.Constructor = Check

/* CHECK DATA-API */
    $(function () {
        $('body').on('click.check.data-api', censor, Check.prototype.censor)
    })

}( window.jQuery );

perdict = function(){
    $('.controls input').on('blur', function(){
		var that = $(this)
		, url = that.attr("check_url");
		if (url) {
			var args = {};
			args.key = that.attr("name");
			args.val = that.val();
			var g = that.closest('.control-group');
			if (g.hasClass('hide')) { return true; }
			g.removeClass('error').removeClass('info').removeClass('success');
			if (!args.val) {
				return false;
			}
			$.postJSON(url, 'GET', args, function(response){
			    if (response.error){
    			    g.addClass('info');
       				g.find('.predict-inline').html('<i class="icon-ban-circle"></i>&nbsp;'+response.error);
				    return false;
        	    } else if (response.ok) {
                    g.addClass('success');
				    g.find('.predict-inline').html('<i class="icon-ok-circle"></i>&nbsp;'+response.ok);
        	    }
			})
		}
	})
}


qq_login = function(){
    QC.Login({
        btnId:"qqLoginBtn",
		size:"B_M"
		}, function(reqData, opts){
	        var dom = document.getElementById(opts['btnId']),
			_logoutTemplate=[
		        '<span><img src="{figureurl}" class="{size_key}" style="height:20px;"/></span>',
			    '<span>{nickname}</span>',
    			'<span><a href="javascript:QC.Login.signOut();">退出</a></span>'	
     	    ].join("");
            dom && (dom.innerHTML = QC.String.format(_logoutTemplate, {
                nickname : QC.String.escHTML(reqData.nickname),
			    figureurl : reqData.figureurl
			}));
            var args = {};
            args.icode = window.prompt("请输入邀请码");
            args.nick = reqData.nickname;
            args.avatar = reqData.figureurl;
            args.gender = reqData.gender;
            QC.Login.getMe(function(openId, accessToken){
                args.openid = openId;
                args.token = accessToken;
                $.postJSON('/qq/reg/', 'POST', args, function(response){
				    if (response.error){
				        alert(response.error);
			            return false;
		            } else if (response.ok) {
				        alert(response.ok);
			            return true;
		            }
		        })
		    });
		}, function(opts){
            alert('QQ登录 注销成功');
	});
}