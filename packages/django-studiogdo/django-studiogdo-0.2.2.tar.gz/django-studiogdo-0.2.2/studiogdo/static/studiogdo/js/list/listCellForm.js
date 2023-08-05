// Generated by CoffeeScript 1.7.1
(function() {
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

  define(function() {
    var ListeEditForm;
    return ListeEditForm = (function() {
      function ListeEditForm(list, value, form) {
        this.list = list;
        this.value = value;
        this.form = form;
        this.hideForm = __bind(this.hideForm, this);
        this.showForm = __bind(this.showForm, this);
        this.close = __bind(this.close, this);
        this.firstFocus = __bind(this.firstFocus, this);
        this.enter = __bind(this.enter, this);
        this.removeEventListenerOnInputs = __bind(this.removeEventListenerOnInputs, this);
        this.addEventListenerOnInputs = __bind(this.addEventListenerOnInputs, this);
        this.changed = __bind(this.changed, this);
        this.cancelChange = __bind(this.cancelChange, this);
        this.commitChange = __bind(this.commitChange, this);
        this.cancel = __bind(this.cancel, this);
        this.commit = __bind(this.commit, this);
        this.inputs = this.form.querySelectorAll("input");
        this.selects = this.form.querySelectorAll("select");
        this.editionMode = true;
        this.showForm();
      }

      ListeEditForm.prototype.commit = function(evt, list) {
        return alert('edition committing to be done');
      };

      ListeEditForm.prototype.cancel = function(evt, list) {
        return list.editForm = null;
      };

      ListeEditForm.prototype.commitChange = function(evt) {
        if (!this.editionMode) {
          return;
        }
        if (evt != null) {
          evt.preventDefault();
        }
        this.close();
        if (this.changed()) {
          return this.commit(evt, this.list);
        } else {
          return this.cancel(evt, this.list);
        }
      };

      ListeEditForm.prototype.cancelChange = function(evt) {
        if (evt != null) {
          evt.preventDefault();
        }
        this.close();
        return this.cancel(evt, this.list);
      };

      ListeEditForm.prototype.changed = function() {
        var input, new_value, old_value, select, _i, _j, _len, _len1, _ref, _ref1;
        _ref = this.inputs;
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          input = _ref[_i];
          if (input.type === "checkbox") {
            return true;
          }
          new_value = input.value;
          old_value = input.getAttribute("value");
          if (new_value !== old_value) {
            return true;
          }
        }
        _ref1 = this.selects;
        for (_j = 0, _len1 = _ref1.length; _j < _len1; _j++) {
          select = _ref1[_j];
          new_value = select.value;
          old_value = select.getAttribute("value");
          if (new_value !== old_value) {
            return true;
          }
        }
        return false;
      };

      ListeEditForm.prototype.addEventListenerOnInputs = function() {
        var input, select, _i, _j, _len, _len1, _ref, _ref1;
        _ref = this.inputs;
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          input = _ref[_i];
          if (input.type === "checkbox") {
            input.addEventListener("click", this.commitChange);
            input.addEventListener("keydown", this.enter);
          } else {
            input.addEventListener("blur", this.commitChange);
            input.addEventListener("keydown", this.enter);
          }
        }
        _ref1 = this.selects;
        for (_j = 0, _len1 = _ref1.length; _j < _len1; _j++) {
          select = _ref1[_j];
          select.addEventListener("change", this.commitChange);
          select.addEventListener("keydown", this.enter);
        }
        return this.form.addEventListener("submit", this.commitChange);
      };

      ListeEditForm.prototype.removeEventListenerOnInputs = function() {
        var input, select, _i, _j, _len, _len1, _ref, _ref1;
        _ref = this.inputs;
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          input = _ref[_i];
          if (input.type === "checkbox") {
            input.removeEventListener("click", this.commitChange);
            input.removeEventListener("keydown", this.enter);
          } else {
            input.removeEventListener("blur", this.commitChange);
            input.removeEventListener("keydown", this.enter);
          }
        }
        _ref1 = this.selects;
        for (_j = 0, _len1 = _ref1.length; _j < _len1; _j++) {
          select = _ref1[_j];
          select.removeEventListener("change", this.commitChange);
          select.removeEventListener("keydown", this.enter);
        }
        return this.form.removeEventListener("submit", this.commitChange);
      };

      ListeEditForm.prototype.enter = function(evt) {
        if (evt.keyCode === 27) {
          evt.preventDefault();
          return this.cancelChange();
        }
      };

      ListeEditForm.prototype.firstFocus = function() {
        var input;
        input = this.form.querySelector("input");
        if (input) {
          input.focus();
          if (input.type !== "checkbox") {
            return input.select();
          }
        }
      };

      ListeEditForm.prototype.close = function() {
        this.hideForm();
        return this.editionMode = false;
      };

      ListeEditForm.prototype.showForm = function() {
        addClassName(this.value, 'hidden');
        removeClassName(this.form, 'hidden');
        return this.addEventListenerOnInputs();
      };

      ListeEditForm.prototype.hideForm = function() {
        this.removeEventListenerOnInputs();
        removeClassName(this.value, 'hidden');
        return addClassName(this.form, 'hidden');
      };

      return ListeEditForm;

    })();
  });

}).call(this);
