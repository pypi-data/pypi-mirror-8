// Generated by CoffeeScript 1.7.1
(function() {
  var $;

  $ = jQuery;

  $.fn.extend({
    serializeForm: function(options) {
      var data, field, form, settings, _i, _len, _ref;
      settings = {
        include_disabled: true
      };
      settings = $.extend(settings, options);
      data = {};
      form = $(this);
      _ref = form.find('input, select, textarea');
      for (_i = 0, _len = _ref.length; _i < _len; _i++) {
        field = _ref[_i];
        if ((!field.disabled || settings['include_disabled']) && (field.type !== "radio" || field.checked)) {
          data[field.name] = field.type !== 'checkbox' ? field.value : field.checked;
        }
      }
      return data;
    }
  });

}).call(this);
