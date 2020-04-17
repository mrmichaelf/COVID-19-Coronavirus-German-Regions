// Adds options to the select
// select: The select object
// optionsArray: the options to add
// if optionsArray item consists of key, values pairs, than use the value for display, 
// else format the key to sentenceLike
function setOptionsToSelect(select, optionsArray, placeholdertext) {
  removeAllOptionsFromSelect(select);
  if (placeholdertext != "") {
    // add a placeholder as first element, important for onchange event on first selection
    const option = document.createElement("option");
    option.value = "placeholder123";
    option.innerText = placeholdertext;
    select.add(option);
  }
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

// remove all options of a select
// from https://stackoverflow.com/posts/3364546/timeline
function removeAllOptionsFromSelect(select) {
  var i, L = select.options.length - 1;
  for (i = L; i >= 0; i--) {
    select.remove(i);
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
  console.log(url);
  // I like using "() => {}" lambda expressions instead of "function () {}" as parameters
  return $.getJSON(url, () => {
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
      name: mapCountryNames[countryCodes[i]],
      type: "line",
      symbolSize: 5,
    };
    series.push(seria);
  }
  return series;
}



// from https://love2dev.com/blog/javascript-remove-from-array/
function arrayRemove(arr, value) {
  return arr.filter(function (ele) { return ele != value; });
}


function arrayRemoveValueTextPairByValue(arr, key) {
  for (let i = 0; i < arr.length; i++) {
    if (arr[i].value == key) { arr.splice(i, 1); }
  }
  //return arr;
}

// Refreshes the chart
// countryCodes: the codes of the countries to display
// countriesDataObject: the object which contains all data about the countries
// select_xAxisProperty: the select of the X axis
// select_yAxisProperty: the select of the Y axis
function refreshChart(
  chart,
  countryCodes,
  countriesDataObject,
  select_xAxisProperty,
  select_yAxisProperty,
  select_yAxisScale
) {
  option = {}
  option = {
    title: {
      text: "COVID-19 Country Custom Plot",
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
      name: formatValueToSentenceLike(select_xAxisProperty.value, "_"),
      type: "value", // value, time  ; will be overwritten if field "Date" is selected
      nameTextStyle: { fontWeight: "bold" },
      nameLocation: "center",
      minorTick: { show: true },
      minorSplitLine: {
        show: true
      }
    },
    // in type log : setting min is required
    yAxis: {
      // name: "Cases",
      name: formatValueToSentenceLike(select_yAxisProperty.value, "_"),
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
      select_xAxisProperty.value,
      select_yAxisProperty.value
    ),
    tooltip: {
      trigger: 'axis', // item or axis
      axisPointer: {
        type: 'shadow',
        snap: true
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
    },
    grid: {
      containLabel: false,
      left: '5%',
      bottom: '5%',
      right: '15%',
    },
  };

  if (select_xAxisProperty.value == "Date") {
    option.xAxis.type = "time";
  }

  if (select_yAxisScale.value == "linscale") {
    option.yAxis.type = "value";
  } else {
    option.yAxis.type = "log";
    // for logscale we need to set the min value as 0 is not good ;-)
    option.yAxis.min = 1;
  }


  chart.clear(); // needed as setOption does not reliable remove all old data, see https://github.com/apache/incubator-echarts/issues/6202#issuecomment-460322781
  chart.setOption(option, true);
}

