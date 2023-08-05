(function() {
  var __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  define(["backbone", "common/has_parent"], function(Backbone, HasParent) {
    var TestParent, TestParents, _ref, _ref1;
    TestParent = (function(_super) {
      __extends(TestParent, _super);

      function TestParent() {
        _ref = TestParent.__super__.constructor.apply(this, arguments);
        return _ref;
      }

      TestParent.prototype.type = 'TestParent';

      TestParent.prototype.parent_properties = ['testprop'];

      TestParent.prototype.display_defaults = {
        testprop: 'defaulttestprop'
      };

      return TestParent;

    })(HasParent);
    TestParents = (function(_super) {
      __extends(TestParents, _super);

      function TestParents() {
        _ref1 = TestParents.__super__.constructor.apply(this, arguments);
        return _ref1;
      }

      TestParents.prototype.model = TestParent;

      return TestParents;

    })(Backbone.Collection);
    return {
      "Model": TestParent,
      "Collection": new TestParents()
    };
  });

}).call(this);

/*
//@ sourceMappingURL=test_parent.js.map
*/