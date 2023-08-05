var __hasProp = {}.hasOwnProperty,
  __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

define(['underscore', 'marionette'], function(_, Marionette) {
  var Welcome;
  Welcome = (function(_super) {
    __extends(Welcome, _super);

    function Welcome() {
      return Welcome.__super__.constructor.apply(this, arguments);
    }

    Welcome.prototype.className = 'welcome';

    Welcome.prototype.template = 'welcome';

    return Welcome;

  })(Marionette.ItemView);
  return {
    Welcome: Welcome
  };
});
