(function() {
  var __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  define(["underscore", "backbone", "kiwi", "./has_properties", "range/range1d"], function(_, Backbone, kiwi, HasProperties, Range1d) {
    var Constraint, EQ, Expr, GE, LE, Panel, Panels, Var, _ref, _ref1;
    Var = kiwi.Variable;
    Expr = kiwi.Expression;
    Constraint = kiwi.Constraint;
    EQ = kiwi.Operator.Eq;
    LE = kiwi.Operator.Le;
    GE = kiwi.Operator.Ge;
    Panel = (function(_super) {
      __extends(Panel, _super);

      function Panel() {
        _ref = Panel.__super__.constructor.apply(this, arguments);
        return _ref;
      }

      Panel.prototype.type = 'Panel';

      Panel.prototype.initialize = function(attrs, options) {
        var name, v, vars, _i, _len,
          _this = this;
        Panel.__super__.initialize.call(this, attrs, options);
        this.solver = this.get('solver');
        this.var_constraints = {};
        vars = ['top', 'bottom', 'left', 'right', 'width', 'height'];
        for (_i = 0, _len = vars.length; _i < _len; _i++) {
          v = vars[_i];
          name = '_' + v;
          this[name] = new Var(v);
          this.register_property(v, this._get_var, false);
          this.register_setter(v, this._set_var);
          this.solver.add_edit_variable(this[name], kiwi.Strength.weak);
        }
        this.solver.add_constraint(new Constraint(new Expr(this._top), GE));
        this.solver.add_constraint(new Constraint(new Expr(this._bottom), GE));
        this.solver.add_constraint(new Constraint(new Expr(this._left), GE));
        this.solver.add_constraint(new Constraint(new Expr(this._right), GE));
        this.solver.add_constraint(new Constraint(new Expr(this._width), GE));
        this.solver.add_constraint(new Constraint(new Expr(this._height), GE));
        this.solver.add_constraint(new Constraint(new Expr(this._left, this._width, [-1, this._right]), EQ));
        this.solver.add_constraint(new Constraint(new Expr(this._bottom, this._height, [-1, this._top]), EQ));
        this.solver.update_variables(false);
        this._h_range = new Range1d.Model({
          start: this.get('left'),
          end: this.get('left') + this.get('width')
        });
        this.register_property('inner_range_horizontal', function() {
          _this._h_range.set('start', _this.get('left'));
          _this._h_range.set('end', _this.get('left') + _this.get('width'));
          return _this._h_range;
        }, false);
        this.add_dependencies('inner_range_horizontal', this, ['left', 'width']);
        this._v_range = new Range1d.Model({
          start: this.get('bottom'),
          end: this.get('bottom') + this.get('height')
        });
        this.register_property('inner_range_vertical', function() {
          _this._v_range.set('start', _this.get('bottom'));
          _this._v_range.set('end', _this.get('bottom') + _this.get('height'));
          return _this._v_range;
        }, false);
        this.add_dependencies('inner_range_vertical', this, ['bottom', 'height']);
        window.foo = this;
        this._aspect_constraint = null;
        this.register_property('aspect', function() {
          return _this.get('width') / _this.get('height');
        }, true);
        this.register_setter('aspect', this._set_aspect);
        return this.add_dependencies('aspect', this, ['width', 'height']);
      };

      Panel.prototype._set_var = function(value, prop_name) {
        var c, v;
        v = this['_' + prop_name];
        if (typeof value === 'number') {
          this.solver.suggest_value(v, value);
        } else if (typeof value === 'string') {

        } else {
          c = new Constraint(new Expr(v, [-1, value]), EQ);
          if (this.var_constraints[prop_name] == null) {
            this.var_constraints[prop_name] = [];
          }
          this.var_constraints[prop_name].push(c);
          this.solver.add_constraint(c);
        }
        return this.solver.update_variables();
      };

      Panel.prototype._get_var = function(prop_name) {
        return this['_' + prop_name].value();
      };

      Panel.prototype._set_aspect = function(aspect) {
        var c;
        if (this._aspect_constraint != null) {
          this.solver.remove_constraint(this.aspect_constraint);
          c = new Constraint(new Expr([aspect, this._height], [-1, this._width]), EQ);
          this._aspect_constraint = c;
          this.solver.add_constraint(c);
          return this.solver.update_variables();
        }
      };

      Panel.prototype.defaults = function() {
        return {
          'top_strength': kiwi.Strength.strong,
          'bottom_strength': kiwi.Strength.strong,
          'left_strength': kiwi.Strength.strong,
          'right_strength': kiwi.Strength.strong,
          'width_strength': kiwi.Strength.strong,
          'height_strength': kiwi.Strength.strong
        };
      };

      return Panel;

    })(HasProperties);
    Panels = (function(_super) {
      __extends(Panels, _super);

      function Panels() {
        _ref1 = Panels.__super__.constructor.apply(this, arguments);
        return _ref1;
      }

      Panels.prototype.model = Panel;

      return Panels;

    })(Backbone.Collection);
    return {
      "Model": Panel,
      "Collection": new Panels()
    };
  });

}).call(this);

/*
//@ sourceMappingURL=panel.js.map
*/