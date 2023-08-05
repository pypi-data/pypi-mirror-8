/*
 * wq.app 0.6.2 - spinner.js
 * Wrapper for jQuery Mobile's spinner
 * (c) 2012-2014, S. Andrew Sheppard
 * http://wq.io/license
 */

define(['jquery.mobile', './console'],
function(jqm, console) {

// Exported module object
var spin = {};

spin.start = function(msg, duration, opts) {
    if (!jqm.loaderWidget) {
        console.warn('Not ready to spin!');
        return;
    }

    if (!opts) opts = {};
    if (msg) {
        opts.text = msg;
        opts.textVisible = true;
    }
    jqm.loading('show', opts);

    if (duration)
        setTimeout(spin.stop, duration * 1000);
};

spin.stop = function() {
    if (!jqm.loaderWidget)
        return;
    jqm.loading('hide');
};

return spin;

});
