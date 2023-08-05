define(['underscore', 'highcharts'], function(_, Highcharts) {
  var dateRegexp, getColor, getSeries, parseDate, processResponse;
  getColor = function(idx) {
    var colors;
    colors = Highcharts.getOptions().colors;
    return colors[idx % colors.length];
  };
  dateRegexp = /\d{4}-\d{2]-\d{2]/;
  parseDate = function(str) {
    var day, month, year;
    year = parseInt(str.substr(0, 4));
    month = parseInt(str.substr(5, 2)) - 1;
    day = parseInt(str.substr(8, 2));
    return Date.UTC(year, month, day);
  };
  processResponse = function(resp, fields, seriesIdx) {
    var avg, chartType, clustered, color, formatterFunc, i, idx, max, name, norm, options, p, point, series, seriesData, seriesList, seriesNo, svalue, x, xEnum, xField, xLabels, xName, xType, xlen, y, yEnum, yField, yLabels, yName, yType, ylen, _i, _j, _len, _len1, _ref, _ref1;
    if (fields.length > 2) {
      throw new Error('3-dimensional charts are not supported. Specify which field the series applies to.');
    } else if (!fields) {
      throw new Error('The field instances must be supplied');
    }
    xLabels = [];
    yLabels = [];
    xField = fields[0], yField = fields[1];
    xName = xField.get('name');
    xEnum = xField.get('enumerable') || xField.get('simple_type') === 'boolean';
    xType = xField.get('simple_type') === 'date' ? 'datetime' : 'linear';
    if (yField) {
      yName = yField.get('name');
      yEnum = yField.get('enumerable') || yField.get('simple_type') === 'boolean';
      yType = yField.get('simple_type') === 'date' ? 'datetime' : 'linear';
    } else {
      yName = 'Frequency';
      yEnum = false;
      yType = 'linear';
    }
    if (xEnum && yEnum) {
      chartType = 'scatter';
      xLabels.push(' ');
      yLabels.push(' ');
    } else if (yField && !xEnum && !yEnum) {
      chartType = 'scatter';
    } else if (yEnum) {
      chartType = 'scatter';
    } else {
      chartType = 'column';
    }
    seriesData = {};
    clustered = resp.clustered;
    _ref = resp.data;
    for (i = _i = 0, _len = _ref.length; _i < _len; i = ++_i) {
      point = _ref[i];
      if (seriesIdx != null) {
        svalue = point.values.slice(seriesIdx, seriesIdx + 1)[0];
      } else {
        svalue = '';
      }
      if (!(series = seriesData[svalue])) {
        series = seriesData[svalue] = {
          name: svalue,
          stats: {
            min: point.count,
            max: point.count,
            sum: point.count
          }
        };
        if (xEnum && yEnum) {
          series.data = [
            {
              x: 0,
              y: 0,
              radius: 0,
              sentinel: true
            }, point
          ];
        } else {
          series.data = [point];
        }
      } else {
        series.data.push(point);
        series.stats.min = Math.min(series.stats.min, point.count);
        series.stats.max = Math.max(series.stats.max, point.count);
        series.stats.sum += point.count;
      }
      x = point.values[0];
      if (x === null) {
        x = '(no data)';
      }
      if (xEnum) {
        if ((idx = xLabels.indexOf(x.toString())) === -1) {
          idx = xLabels.push(x.toString()) - 1;
        }
        x = idx;
      } else {
        if (xType === 'datetime') {
          x = parseDate(x);
        }
      }
      if (yField) {
        y = point.values[1];
        if (y === null) {
          y = '(no data)';
        }
        if (yEnum) {
          if ((idx = yLabels.indexOf(y.toString())) === -1) {
            idx = yLabels.push(y.toString()) - 1;
          }
          y = idx;
        } else {
          if (yType === 'datetime') {
            y = parseDate(y);
          }
        }
      } else {
        y = point.count;
      }
      point.x = x;
      point.y = y;
    }
    seriesList = [];
    if (xEnum && yEnum) {
      xlen = xLabels.push(' ') - 1;
      ylen = yLabels.push(' ') - 1;
    }
    seriesNo = 0;
    for (name in seriesData) {
      series = seriesData[name];
      if (xEnum && yEnum) {
        series.data.push({
          x: 0,
          y: ylen,
          radius: 0,
          sentinel: true
        });
        series.data.push({
          x: xlen,
          y: ylen,
          radius: 0,
          sentinel: true
        });
        series.data.push({
          x: xlen,
          y: ylen,
          radius: 0,
          sentinel: true
        });
      }
      seriesList.push(series);
      avg = series.stats.avg = series.stats.sum / parseFloat(series.data.length, 10);
      max = series.stats.max;
      if (chartType === 'scatter') {
        _ref1 = series.data;
        for (_j = 0, _len1 = _ref1.length; _j < _len1; _j++) {
          p = _ref1[_j];
          if (p.sentinel) {
            continue;
          }
          norm = Math.min(Math.max(parseInt(parseFloat(p.count, 10) / avg * 5) / 10, 0.05), 1);
          color = Highcharts.Color(getColor(seriesNo)).setOpacity(norm);
          p.marker = {
            fillColor: color.get()
          };
          if (xEnum) {
            p.marker.radius = 7;
          }
        }
      }
      seriesNo++;
    }
    if (chartType === 'scatter' && xEnum) {
      if (seriesList[1]) {
        formatterFunc = function() {
          return "<h5>" + this.series.name + "</h5><br /><b>" + xName + ":</b> " + this.series.xAxis.categories[this.point.x] + "<br /><b>" + yName + ":</b> " + this.series.yAxis.categories[this.point.y];
        };
      } else {
        formatterFunc = function() {
          return "<b>" + xName + ":</b> " + this.series.xAxis.categories[this.point.x] + "<br /><b>" + yName + ":</b> " + this.series.yAxis.categories[this.point.y];
        };
      }
    } else if (chartType === 'column' && xEnum) {
      if (seriesList[1]) {
        formatterFunc = function() {
          return "<h5>" + this.series.name + "</h5><br /><b>" + xName + ":</b> " + this.series.xAxis.categories[this.point.x] + "<br /><b>" + yName + ":</b> " + (Highcharts.numberFormat(parseFloat(this.y)));
        };
      } else {
        formatterFunc = function() {
          return "<b>" + xName + ":</b> " + this.series.xAxis.categories[this.point.x] + "<br /><b>" + yName + ":</b> " + (Highcharts.numberFormat(parseFloat(this.y)));
        };
      }
    } else {
      if (seriesList[1]) {
        formatterFunc = function() {
          return "<h5>" + this.series.name + "</h5><br /><b>" + xName + ":</b> " + (Highcharts.numberFormat(parseFloat(this.x))) + "<br /><b>" + yName + ":</b> " + (Highcharts.numberFormat(parseFloat(this.y)));
        };
      } else {
        formatterFunc = function() {
          return "<b>" + xName + ":</b> " + (Highcharts.numberFormat(parseFloat(this.x))) + "<br /><b>" + yName + ":</b> " + (Highcharts.numberFormat(parseFloat(this.y)));
        };
      }
    }
    options = {
      clustered: clustered,
      chart: {
        type: chartType
      },
      title: {
        text: yField ? "" + xName + " vs. " + yName : "" + xName + " " + yName
      },
      series: seriesList,
      xAxis: {
        title: {
          text: xName
        },
        type: xType
      },
      yAxis: {
        title: {
          text: yName
        },
        type: yType
      },
      tooltip: {
        formatter: formatterFunc
      }
    };
    if (xLabels.length) {
      options.xAxis.categories = xLabels;
    }
    if (yLabels.length) {
      options.yAxis.categories = yLabels;
    }
    if (!seriesList[1]) {
      options.legend = {
        enabled: false
      };
    }
    if (chartType === 'scatter') {
      options.yAxis.gridLineWidth = 0;
      if (!xEnum) {
        options.chart.zoomType = 'xy';
      }
    }
    return options;
  };
  getSeries = function(data) {
    var datum, point, points, _i, _len;
    points = [];
    for (_i = 0, _len = data.length; _i < _len; _i++) {
      datum = data[_i];
      point = _.clone(datum);
      point.x = datum.values[0];
      if (datum.values[1] != null) {
        point.y = datum.values[1];
      } else {
        point.y = datum.count;
      }
      points.push(point);
    }
    return {
      data: _.sortBy(points, 'x')
    };
  };
  return {
    processResponse: processResponse,
    getSeries: getSeries
  };
});
