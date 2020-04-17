// Adds options to the select
// select: The select object
// optionsArray: the options to add
// if optionsArray item consists of key, values pairs, than use the value for display, 
// else format the key to sentenceLike
function addOptionsToSelect(select, optionsArray) {
  for (let i = 0; i < optionsArray.length; i++) {
    const option = document.createElement("option");
    if (optionsArray[i].value && optionsArray[i].text) {
      option.value = optionsArray[i].value;
      option.innerText = optionsArray[i].text;
    } else {
      option.value = optionsArray[i];
      option.innerText = formatValueToSentenceLike(optionsArray[i], "_");
    }
    select.add(option);
  }
}

// Formats value "Something_Is_HERE" to "Something is here" like sentence
// value: The value to format
// separator: the separator string between words
function formatValueToSentenceLike(value, separator) {
  const allLowerCaseValue = value.split(separator).join(" ").toLowerCase();
  return allLowerCaseValue[0].toUpperCase() + allLowerCaseValue.substr(1);
}

// Fetches the data for one country code
// countryCode: the code of the country e.g. "DE"
// countriesDataObject: the object which will contain all data about the countries
function fetchData(countryCode, countriesDataObject) {
  const url = getUrl(countryCode);
  // I like using "() => {}" lambda expressions instead of "function () {}" as parameters
  return $.getJSON(url, (data) => {
    console.log(`success: ${countryCode}`);
  })
    .done((data) => {
      console.log(`done: ${countryCode}`);
      countriesDataObject[countryCode] = data;
    })
    .fail(() => {
      console.log(`fail: ${countryCode}`);
    });
}

// Gets the url of the given country
// countryCode: the code of the country e.g. "DE"
function getUrl(country_code) {
  // `words${variable}words` syntax is more readable than "words" + variable + "words"
  return `https://entorb.net/COVID-19-coronavirus/data/int/country-${country_code}.json`;
}

// Gets the series property of the chart object
// countryCodes: the codes of the countries to display
// countriesDataObject: the object which contains all data about the countries
// xAxis: the property displayed in the X axis
// yAxis: the property displayed in the Y axis
function getSeries(countryCodes, countriesDataObject, xAxis, yAxis) {
  const series = [];
  for (let i = 0; i < countryCodes.length; i++) {
    const countryLine = [];
    // We filter the data to display here using the axis data
    $.each(countriesDataObject[countryCodes[i]], function (key, val) {
      countryLine.push([
        countriesDataObject[countryCodes[i]][key][xAxis],
        countriesDataObject[countryCodes[i]][key][yAxis],
      ]);
    });
    const seria = {
      data: countryLine, // the line of the country
      name: countryNames[countryCodes[i]],
      type: "line",
      symbolSize: 5,
    };
    series.push(seria);
  }
  return series;
}

// Refreshes the chart
// countryCodes: the codes of the countries to display
// countriesDataObject: the object which contains all data about the countries
// xAxisPropertySelect: the select of the X axis
// yAxisPropertySelect: the select of the Y axis
function refreshChart(
  chart,
  countryCodes,
  countriesDataObject,
  xAxisPropertySelect,
  yAxisPropertySelect,
  yAxisScaleSelect
) {
  option = {}
  option = {
    title: {
      text: "COVID-19 Country Plot",
      subtext: "by Torben https://entorb.net based on JHU data",
      sublink: "https://entorb.net/COVID-19-coronavirus/"
    },
    legend: {
      type: 'scroll',
      orient: 'vertical',
      right: 0,
      top: 50,
      //          bottom: 20,
    },
    xAxis: {
      name: formatValueToSentenceLike(xAxisPropertySelect.value, "_"),
      type: "value",
      nameTextStyle: { fontWeight: "bold" },
      nameLocation: "middle",
      minorTick: { show: true },
      minorSplitLine: {
        show: true
      }
    },
    // in type log : setting min is required
    yAxis: {
      // name: "Cases",
      name: formatValueToSentenceLike(yAxisPropertySelect.value, "_"),
      type: "value", //value or log
      // min: 1,
      // max: 10000,
      nameTextStyle: { fontWeight: "bold" },
      nameLocation: "center",
      minorTick: { show: true },
      minorSplitLine: {
        show: true
      }
    }, //max: "dataMax"
    series: getSeries(
      countryCodes,
      countriesDataObject,
      xAxisPropertySelect.value,
      yAxisPropertySelect.value
    ),
    tooltip: {
      trigger: 'item', // item or axis
      axisPointer: {
        type: 'shadow'
      }
    },
    toolbox: {
      show: true,
      showTitle: true,
      feature: {
        saveAsImage: {},
        // restore: {},
        dataZoom: {},
        dataView: { readOnly: true },
        // magicType: {
        //  type: ['line', 'bar', 'stack', 'tiled']
        //},
        //brush: {},
      },
    }
  };

  if (yAxisScaleSelect.value == "linscale") {
    console.log("lin");
    option.yAxis.type = "value";
  } else {
    console.log("log");
    option.yAxis.type = "log";
    // for logscale we need to set the min value as 0 is not good ;-)
    option.yAxis.min = 1;
  }


  chart.clear(); // needed as setOption does not reliable remove all old data, see https://github.com/apache/incubator-echarts/issues/6202#issuecomment-460322781
  chart.setOption(option, true);
}
