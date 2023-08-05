(function() {
  var __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  define(["underscore", "backbone", "timezone", "sprintf", "common/has_properties"], function(_, Backbone, tz, sprintf, HasProperties) {
    var AbstractTicker, AdaptiveTicker, CompositeTicker, DEFAULT_DESIRED_N_TICKS, DaysTicker, MonthsTicker, ONE_DAY, ONE_HOUR, ONE_MILLI, ONE_MINUTE, ONE_MONTH, ONE_SECOND, ONE_YEAR, SingleIntervalTicker, arange, argmin, clamp, copy_date, date_range_by_month, date_range_by_year, indices, last_month_no_later_than, last_year_no_later_than, log, repr, _ref, _ref1, _ref2, _ref3, _ref4, _ref5;
    ONE_MILLI = 1.0;
    ONE_SECOND = 1000.0;
    ONE_MINUTE = 60.0 * ONE_SECOND;
    ONE_HOUR = 60 * ONE_MINUTE;
    ONE_DAY = 24 * ONE_HOUR;
    ONE_MONTH = 30 * ONE_DAY;
    ONE_YEAR = 365 * ONE_DAY;
    arange = function(start, end, step) {
      var i, ret_arr;
      if (end == null) {
        end = false;
      }
      if (step == null) {
        step = false;
      }
      if (!end) {
        end = start;
        start = 0;
      }
      if (start > end) {
        if (step === false) {
          step = -1;
        } else if (step > 0) {
          "the loop will never terminate";
          1 / 0;
        }
      } else if (step < 0) {
        "the loop will never terminate";
        1 / 0;
      }
      if (!step) {
        step = 1;
      }
      ret_arr = [];
      i = start;
      if (start < end) {
        while (i < end) {
          ret_arr.push(i);
          i += step;
        }
      } else {
        while (i > end) {
          ret_arr.push(i);
          i += step;
        }
      }
      return ret_arr;
    };
    repr = function(obj) {
      var elem, elems_str, key, obj_as_string, props_str;
      if (obj === null) {
        return "null";
      } else if (obj.constructor === Array) {
        elems_str = ((function() {
          var _i, _len, _results;
          _results = [];
          for (_i = 0, _len = obj.length; _i < _len; _i++) {
            elem = obj[_i];
            _results.push(repr(elem));
          }
          return _results;
        })()).join(", ");
        return "[" + elems_str + "]";
      } else if (obj.constructor === Object) {
        props_str = ((function() {
          var _results;
          _results = [];
          for (key in obj) {
            _results.push("" + key + ": " + (repr(obj[key])));
          }
          return _results;
        })()).join(", ");
        return "{" + props_str + "}";
      } else if (obj.constructor === String) {
        return "\"" + obj + "\"";
      } else if (obj.constructor === Function) {
        return "<Function: " + obj.name + ">";
      } else {
        obj_as_string = obj.toString();
        if (obj_as_string === "[object Object]") {
          return "<" + obj.constructor.name + ">";
        } else {
          return obj_as_string;
        }
      }
    };
    indices = function(arr) {
      return _.range(arr.length);
    };
    argmin = function(arr) {
      var ret;
      ret = _.min(indices(arr), (function(i) {
        return arr[i];
      }));
      return ret;
    };
    clamp = function(x, min_val, max_val) {
      return Math.max(min_val, Math.min(max_val, x));
    };
    log = function(x, base) {
      if (base == null) {
        base = Math.E;
      }
      return Math.log(x) / Math.log(base);
    };
    copy_date = function(date) {
      return new Date(date.getTime());
    };
    last_month_no_later_than = function(date) {
      date = copy_date(date);
      date.setUTCDate(1);
      date.setUTCHours(0);
      date.setUTCMinutes(0);
      date.setUTCSeconds(0);
      date.setUTCMilliseconds(0);
      return date;
    };
    last_year_no_later_than = function(date) {
      date = last_month_no_later_than(date);
      date.setUTCMonth(0);
      return date;
    };
    date_range_by_year = function(start_time, end_time) {
      var date, dates, end_date, start_date;
      start_date = last_year_no_later_than(new Date(start_time));
      end_date = last_year_no_later_than(new Date(end_time));
      end_date.setUTCFullYear(end_date.getUTCFullYear() + 1);
      dates = [];
      date = start_date;
      while (true) {
        dates.push(copy_date(date));
        date.setUTCFullYear(date.getUTCFullYear() + 1);
        if (date > end_date) {
          break;
        }
      }
      return dates;
    };
    date_range_by_month = function(start_time, end_time) {
      var date, dates, end_date, prev_end_date, start_date;
      start_date = last_month_no_later_than(new Date(start_time));
      end_date = last_month_no_later_than(new Date(end_time));
      prev_end_date = copy_date(end_date);
      end_date.setUTCMonth(end_date.getUTCMonth() + 1);
      dates = [];
      date = start_date;
      while (true) {
        dates.push(copy_date(date));
        date.setUTCMonth(date.getUTCMonth() + 1);
        if (date > end_date) {
          break;
        }
      }
      return dates;
    };
    DEFAULT_DESIRED_N_TICKS = 6;
    AbstractTicker = (function(_super) {
      __extends(AbstractTicker, _super);

      function AbstractTicker() {
        _ref = AbstractTicker.__super__.constructor.apply(this, arguments);
        return _ref;
      }

      AbstractTicker.prototype.initialize = function(attrs, options) {
        return AbstractTicker.__super__.initialize.call(this, attrs, options);
      };

      AbstractTicker.prototype.get_ticks = function(data_low, data_high, range, _arg) {
        var desired_n_ticks;
        desired_n_ticks = _arg.desired_n_ticks;
        if (desired_n_ticks == null) {
          desired_n_ticks = DEFAULT_DESIRED_N_TICKS;
        }
        return this.get_ticks_no_defaults(data_low, data_high, desired_n_ticks);
      };

      AbstractTicker.prototype.get_ticks_no_defaults = function(data_low, data_high, desired_n_ticks) {
        var end_factor, factor, factors, interval, start_factor, ticks;
        interval = this.get_interval(data_low, data_high, desired_n_ticks);
        start_factor = Math.floor(data_low / interval);
        end_factor = Math.ceil(data_high / interval);
        factors = arange(start_factor, end_factor + 1);
        ticks = (function() {
          var _i, _len, _results;
          _results = [];
          for (_i = 0, _len = factors.length; _i < _len; _i++) {
            factor = factors[_i];
            _results.push(factor * interval);
          }
          return _results;
        })();
        return ticks;
      };

      AbstractTicker.prototype.get_interval = void 0;

      AbstractTicker.prototype.get_min_interval = function() {
        return this.get('min_interval');
      };

      AbstractTicker.prototype.get_max_interval = function() {
        return this.get('max_interval');
      };

      AbstractTicker.prototype.min_interval = void 0;

      AbstractTicker.prototype.max_interval = void 0;

      AbstractTicker.prototype.toString = function() {
        var class_name, key, params_str, props;
        class_name = typeof this;
        props = this.get('toString_properties');
        params_str = ((function() {
          var _i, _len, _results;
          _results = [];
          for (_i = 0, _len = props.length; _i < _len; _i++) {
            key = props[_i];
            _results.push("" + key + "=" + (repr(this[key])));
          }
          return _results;
        }).call(this)).join(", ");
        return "" + class_name + "(" + params_str + ")";
      };

      AbstractTicker.prototype.get_ideal_interval = function(data_low, data_high, desired_n_ticks) {
        var data_range;
        data_range = data_high - data_low;
        return data_range / desired_n_ticks;
      };

      AbstractTicker.prototype.defaults = function() {
        return _.extend(AbstractTicker.__super__.defaults.call(this), {
          toString_properties: []
        });
      };

      return AbstractTicker;

    })(HasProperties);
    SingleIntervalTicker = (function(_super) {
      __extends(SingleIntervalTicker, _super);

      function SingleIntervalTicker() {
        _ref1 = SingleIntervalTicker.__super__.constructor.apply(this, arguments);
        return _ref1;
      }

      SingleIntervalTicker.prototype.initialize = function(attrs, options) {
        SingleIntervalTicker.__super__.initialize.call(this, attrs, options);
        this.register_property('min_interval', function() {
          return this.get('interval');
        }, true);
        this.add_dependencies('min_interval', this, ['interval']);
        this.register_property('max_interval', function() {
          return this.get('interval');
        }, true);
        return this.add_dependencies('max_interval', this, ['interval']);
      };

      SingleIntervalTicker.prototype.get_interval = function(data_low, data_high, n_desired_ticks) {
        return this.get('interval');
      };

      SingleIntervalTicker.prototype.defaults = function() {
        return _.extend(SingleIntervalTicker.__super__.defaults.call(this), {
          toString_properties: ['interval']
        });
      };

      return SingleIntervalTicker;

    })(AbstractTicker);
    CompositeTicker = (function(_super) {
      __extends(CompositeTicker, _super);

      function CompositeTicker() {
        _ref2 = CompositeTicker.__super__.constructor.apply(this, arguments);
        return _ref2;
      }

      CompositeTicker.prototype.initialize = function(attrs, options) {
        var tickers;
        CompositeTicker.__super__.initialize.call(this, attrs, options);
        tickers = this.get('tickers');
        this.register_property('min_intervals', function() {
          return _.invoke(tickers, 'get_min_interval');
        }, true);
        this.add_dependencies('min_intervals', this, ['tickers']);
        this.register_property('max_intervals', function() {
          return _.invoke(tickers, 'get_max_interval');
        }, true);
        this.add_dependencies('max_intervals', this, ['tickers']);
        this.register_property('min_interval', function() {
          return _.first(this.get('min_intervals'));
        }, true);
        this.add_dependencies('min_interval', this, ['min_intervals']);
        this.register_property('max_interval', function() {
          return _.first(this.get('max_intervals'));
        }, true);
        return this.add_dependencies('max_interval', this, ['max_interval']);
      };

      CompositeTicker.prototype.get_best_ticker = function(data_low, data_high, desired_n_ticks) {
        var best_ticker, best_ticker_ndx, data_range, errors, ideal_interval, intervals, ticker_ndxs;
        data_range = data_high - data_low;
        ideal_interval = this.get_ideal_interval(data_low, data_high, desired_n_ticks);
        ticker_ndxs = [_.sortedIndex(this.get('min_intervals'), ideal_interval) - 1, _.sortedIndex(this.get('max_intervals'), ideal_interval)];
        intervals = [this.get('min_intervals')[ticker_ndxs[0]], this.get('max_intervals')[ticker_ndxs[1]]];
        errors = intervals.map(function(interval) {
          return Math.abs(desired_n_ticks - (data_range / interval));
        });
        best_ticker_ndx = ticker_ndxs[argmin(errors)];
        best_ticker = this.get('tickers')[best_ticker_ndx];
        return best_ticker;
      };

      CompositeTicker.prototype.get_interval = function(data_low, data_high, desired_n_ticks) {
        var best_ticker;
        best_ticker = this.get_best_ticker(data_low, data_high, desired_n_ticks);
        return best_ticker.get_interval(data_low, data_high, desired_n_ticks);
      };

      CompositeTicker.prototype.get_ticks_no_defaults = function(data_low, data_high, desired_n_ticks) {
        var best_ticker;
        best_ticker = this.get_best_ticker(data_low, data_high, desired_n_ticks);
        return best_ticker.get_ticks_no_defaults(data_low, data_high, desired_n_ticks);
      };

      CompositeTicker.prototype.defaults = function() {
        return CompositeTicker.__super__.defaults.call(this);
      };

      return CompositeTicker;

    })(AbstractTicker);
    AdaptiveTicker = (function(_super) {
      __extends(AdaptiveTicker, _super);

      function AdaptiveTicker() {
        _ref3 = AdaptiveTicker.__super__.constructor.apply(this, arguments);
        return _ref3;
      }

      AdaptiveTicker.prototype.initialize = function(attrs, options) {
        var prefix_mantissa, suffix_mantissa;
        AdaptiveTicker.__super__.initialize.call(this, attrs, options);
        prefix_mantissa = _.last(this.get('mantissas')) / this.base;
        suffix_mantissa = _.first(this.get('mantissas')) * this.base;
        this.extended_mantissas = _.flatten([prefix_mantissa, this.get('mantissas'), suffix_mantissa]);
        return this.base_factor = this.get('min_interval') === 0.0 ? 1.0 : this.get('min_interval');
      };

      AdaptiveTicker.prototype.get_interval = function(data_low, data_high, desired_n_ticks) {
        var best_mantissa, candidate_mantissas, data_range, errors, ideal_interval, ideal_magnitude, ideal_mantissa, interval, interval_exponent;
        data_range = data_high - data_low;
        ideal_interval = this.get_ideal_interval(data_low, data_high, desired_n_ticks);
        interval_exponent = Math.floor(log(ideal_interval / this.base_factor, this.get('base')));
        ideal_magnitude = Math.pow(this.get('base'), interval_exponent) * this.base_factor;
        ideal_mantissa = ideal_interval / ideal_magnitude;
        candidate_mantissas = this.extended_mantissas;
        errors = candidate_mantissas.map(function(mantissa) {
          return Math.abs(desired_n_ticks - (data_range / (mantissa * ideal_magnitude)));
        });
        best_mantissa = candidate_mantissas[argmin(errors)];
        interval = best_mantissa * ideal_magnitude;
        return clamp(interval, this.get('min_interval'), this.get('max_interval'));
      };

      AdaptiveTicker.prototype.defaults = function() {
        return _.extend(AdaptiveTicker.__super__.defaults.call(this), {
          toString_properties: ['mantissas', 'base', 'min_magnitude', 'max_magnitude'],
          base: 10.0,
          min_interval: 0.0,
          max_interval: Infinity
        });
      };

      return AdaptiveTicker;

    })(AbstractTicker);
    MonthsTicker = (function(_super) {
      __extends(MonthsTicker, _super);

      function MonthsTicker() {
        _ref4 = MonthsTicker.__super__.constructor.apply(this, arguments);
        return _ref4;
      }

      MonthsTicker.prototype.initialize = function(attrs, options) {
        var interval, months;
        MonthsTicker.__super__.initialize.call(this, attrs, options);
        months = this.get('months');
        interval = months.length > 1 ? (months[1] - months[0]) * ONE_MONTH : 12 * ONE_MONTH;
        return this.set('interval', interval);
      };

      MonthsTicker.prototype.get_ticks_no_defaults = function(data_low, data_high, desired_n_ticks) {
        var all_ticks, date, month_dates, months, months_of_year, ticks_in_range, year_dates;
        year_dates = date_range_by_year(data_low, data_high);
        months = this.get('months');
        months_of_year = function(year_date) {
          return months.map(function(month) {
            var month_date;
            month_date = copy_date(year_date);
            month_date.setUTCMonth(month);
            return month_date;
          });
        };
        month_dates = _.flatten((function() {
          var _i, _len, _results;
          _results = [];
          for (_i = 0, _len = year_dates.length; _i < _len; _i++) {
            date = year_dates[_i];
            _results.push(months_of_year(date));
          }
          return _results;
        })());
        all_ticks = _.invoke(month_dates, 'getTime');
        ticks_in_range = _.filter(all_ticks, (function(tick) {
          return (data_low <= tick && tick <= data_high);
        }));
        return ticks_in_range;
      };

      MonthsTicker.prototype.defaults = function() {
        return _.extend(MonthsTicker.__super__.defaults.call(this), {
          toString_properties: ['months']
        });
      };

      return MonthsTicker;

    })(SingleIntervalTicker);
    DaysTicker = (function(_super) {
      __extends(DaysTicker, _super);

      function DaysTicker() {
        _ref5 = DaysTicker.__super__.constructor.apply(this, arguments);
        return _ref5;
      }

      DaysTicker.prototype.initialize = function(attrs, options) {
        var days, interval;
        DaysTicker.__super__.initialize.call(this, attrs, options);
        days = this.get('days');
        interval = days.length > 1 ? (days[1] - days[0]) * ONE_DAY : 31 * ONE_DAY;
        return this.set('interval', interval);
      };

      DaysTicker.prototype.get_ticks_no_defaults = function(data_low, data_high, desired_n_ticks) {
        var all_ticks, date, day_dates, days, days_of_month, interval, month_dates, ticks_in_range,
          _this = this;
        month_dates = date_range_by_month(data_low, data_high);
        days = this.get('days');
        days_of_month = function(month_date, interval) {
          var dates, day, day_date, future_date, _i, _len;
          dates = [];
          for (_i = 0, _len = days.length; _i < _len; _i++) {
            day = days[_i];
            day_date = copy_date(month_date);
            day_date.setUTCDate(day);
            future_date = new Date(day_date.getTime() + (interval / 2));
            if (future_date.getUTCMonth() === month_date.getUTCMonth()) {
              dates.push(day_date);
            }
          }
          return dates;
        };
        interval = this.get('interval');
        day_dates = _.flatten((function() {
          var _i, _len, _results;
          _results = [];
          for (_i = 0, _len = month_dates.length; _i < _len; _i++) {
            date = month_dates[_i];
            _results.push(days_of_month(date, interval));
          }
          return _results;
        })());
        all_ticks = _.invoke(day_dates, 'getTime');
        ticks_in_range = _.filter(all_ticks, (function(tick) {
          return (data_low <= tick && tick <= data_high);
        }));
        return ticks_in_range;
      };

      DaysTicker.prototype.defaults = function() {
        return _.extend(DaysTicker.__super__.defaults.call(this), {
          toString_properties: ['days']
        });
      };

      return DaysTicker;

    })(SingleIntervalTicker);
    return {
      "arange": arange,
      "ONE_MILLI": ONE_MILLI,
      "ONE_SECOND": ONE_SECOND,
      "ONE_MINUTE": ONE_MINUTE,
      "ONE_HOUR": ONE_HOUR,
      "ONE_DAY": ONE_DAY,
      "ONE_MONTH": ONE_MONTH,
      "ONE_YEAR": ONE_YEAR,
      "AbstractTicker": AbstractTicker,
      "AdaptiveTicker": AdaptiveTicker,
      "CompositeTicker": CompositeTicker,
      "DaysTicker": DaysTicker,
      "MonthsTicker": MonthsTicker,
      "SingleIntervalTicker": SingleIntervalTicker
    };
  });

}).call(this);

/*
//@ sourceMappingURL=tickers.js.map
*/