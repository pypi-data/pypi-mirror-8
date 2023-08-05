(function() {
  require(['main'], function(Bokeh) {
    var options, plot1, scatter1, scatter2, scatter3, source, x, xdr, xs, ydr1, ydr2, ys1, ys2, ys3;
    xs = (function() {
      var _i, _len, _ref, _results;
      _ref = _.range(630);
      _results = [];
      for (_i = 0, _len = _ref.length; _i < _len; _i++) {
        x = _ref[_i];
        _results.push(x / 50);
      }
      return _results;
    })();
    ys1 = (function() {
      var _i, _len, _results;
      _results = [];
      for (_i = 0, _len = xs.length; _i < _len; _i++) {
        x = xs[_i];
        _results.push(Math.sin(x));
      }
      return _results;
    })();
    ys2 = (function() {
      var _i, _len, _results;
      _results = [];
      for (_i = 0, _len = xs.length; _i < _len; _i++) {
        x = xs[_i];
        _results.push(Math.cos(x));
      }
      return _results;
    })();
    ys3 = (function() {
      var _i, _len, _results;
      _results = [];
      for (_i = 0, _len = xs.length; _i < _len; _i++) {
        x = xs[_i];
        _results.push(Math.tan(x));
      }
      return _results;
    })();
    source = Bokeh.Collections('ColumnDataSource').create({
      data: {
        x: xs,
        y1: ys1,
        y2: ys2,
        y3: ys3
      }
    });
    xdr = Bokeh.Collections('DataRange1d').create({
      sources: [
        {
          ref: source.ref(),
          columns: ['x']
        }
      ]
    });
    ydr1 = Bokeh.Collections('DataRange1d').create({
      sources: [
        {
          ref: source.ref(),
          columns: ['y1']
        }
      ]
    });
    ydr2 = Bokeh.Collections('DataRange1d').create({
      sources: [
        {
          ref: source.ref(),
          columns: ['y2']
        }
      ]
    });
    scatter1 = {
      type: 'circle',
      x: 'x',
      y: 'y1',
      radius: 8,
      radius_units: 'screen',
      fill_color: 'red',
      line_color: 'black'
    };
    scatter2 = {
      type: 'rect',
      x: 'x',
      y: 'y2',
      width: 5,
      width_units: 'screen',
      height: 5,
      height_units: 'screen',
      fill_color: 'blue'
    };
    scatter3 = {
      type: 'rect',
      x: 'x',
      y: 'y3',
      width: 5,
      width_units: 'screen',
      height: 5,
      height_units: 'screen',
      fill_color: 'blue'
    };
    options = {
      title: "Scatter Demo",
      dims: [600, 600],
      xrange: xdr,
      xaxes: "min",
      yaxes: "min",
      tools: false,
      legend: false
    };
    plot1 = Bokeh.Plotting.make_plot(scatter1, source, _.extend({
      title: "Plot 1",
      yrange: ydr1
    }, options));
    console.log("plot1 created");
    _.delay((function() {
      var g, glyphs;
      console.log("adding another renderer scatter2");
      glyphs = Bokeh.Plotting.create_glyphs(plot1, [scatter2], [source]);
      return plot1.add_renderers((function() {
        var _i, _len, _results;
        _results = [];
        for (_i = 0, _len = glyphs.length; _i < _len; _i++) {
          g = glyphs[_i];
          _results.push(g.ref());
        }
        return _results;
      })());
    }), 500);
    _.delay((function() {
      var g, glyphs, p1;
      console.log("adding another renderer scatter3");
      glyphs = Bokeh.Plotting.create_glyphs(plot1, [scatter3], [source]);
      p1 = plot1;
      return plot1.add_renderers((function() {
        var _i, _len, _results;
        _results = [];
        for (_i = 0, _len = glyphs.length; _i < _len; _i++) {
          g = glyphs[_i];
          _results.push(g.ref());
        }
        return _results;
      })());
    }), 1000);
    _.delay((function() {
      console.log("clear renderers");
      return plot1.set('renderers', []);
    }), 1500);
    _.delay((function() {
      var g, glyphs, p1;
      glyphs = Bokeh.Plotting.create_glyphs(plot1, [scatter1, scatter3], [source]);
      p1 = plot1;
      return plot1.add_renderers((function() {
        var _i, _len, _results;
        _results = [];
        for (_i = 0, _len = glyphs.length; _i < _len; _i++) {
          g = glyphs[_i];
          _results.push(g.ref());
        }
        return _results;
      })());
    }), 3000);
    return Bokeh.Plotting.show(plot1);
  });

}).call(this);

/*
//@ sourceMappingURL=column_select.js.map
*/