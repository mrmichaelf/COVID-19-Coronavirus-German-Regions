// -------------
// 1. Small helpers
// -------------

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



// from https://love2dev.com/blog/javascript-remove-from-array/
function arrayRemove(arr, value) {
  return arr.filter(function (ele) { return ele != value; });
}

// modifies array of objects by removing if value == keys
function arrayRemoveValueTextPairByValue(arr, key) {
  for (let i = arr.length - 1; i >= 0; i--) {
    if (arr[i].value == key) { arr.splice(i, 1); }
  }
}



// Adds options to the select, after removing all existing options
// select: The select object
// optionsArray: the options to add
// if optionsArray item consists of key, values pairs, than use the value for display, 
// else format the key to sentenceLike style
// if placeholdertext != "" than add this word as first dummy entry (for example "Choose"), important for onchange event on first selection
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


// -------------
// 2. My data specific functions
// -------------




// Gets the url of the given country
// countryCode: the code of the country e.g. "DE"
function getUrl(country_code) {
  // `words${variable}words` syntax is more readable than "words" + variable + "words"
  return `https://entorb.net/COVID-19-coronavirus/data/int/country-${country_code}.json`;
}



// Fetches the data for one country code
// countryCode: the code of the country e.g. "DE"
// countriesDataObject: the object which will contain all data about the countries
function fetchData(countryCode, countriesDataObject) {
  const url = getUrl(countryCode);
  // AAN: I like using "() => {}" lambda expressions instead of "function () {}" as parameters
  return $.getJSON(url, () => {
    // console.log(`success: ${countryCode}`);
  })
    .done((data) => {
      console.log(`done: ${countryCode}`);
      countriesDataObject[countryCode] = data;
    })
    .fail(() => {
      console.log(`fail: ${countryCode}`);
    });
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
      smooth: true,
    };
    series.push(seria);
  }
  return series;
}

// when a country is selected for adding to the chart, this is called
function new_country_selected(countryCodes, select_country, options_countries) {
  if (select_country.value != "placeholder123") {
    var country_code_to_add = select_country.value;
    // console.log(country_code_to_add)

    // append to list of country codes
    countryCodes.push(country_code_to_add);

    // start fetching / download of data
    promises.push(fetchData(country_code_to_add, countriesDataObject))

    // remove selected values from options_countries
    arrayRemoveValueTextPairByValue(options_countries, country_code_to_add)
    setOptionsToSelect(select_country, options_countries, "Choose");

    // wait for fetching to complete, than update chart
    Promise.all(promises).then(() => {
      refreshChartWrapper();
    });
  }
}

// resets country selection to default
function resetChart() {
  // TODO: This is not working properly: dropdowns are not refilled.
  // options_countries_africa = [];
  // options_countries_asia = [];
  // options_countries_europe = [];
  // options_countries_north_america = [];
  // options_countries_south_america = [];
  // options_countries_oceania = [];
  console.log(countryCodes);
  // countryCodes = ["DE"];
  console.log(countryCodes);
  populate_country_selects();
  refreshChartWrapper();
}

function populate_country_selects() {
  // Africa
  for (let i = 0; i < mapContinentCountries['Africa'].length; i++) {
    const code = mapContinentCountries['Africa'][i][0];
    const name = mapContinentCountries['Africa'][i][1]
    if (!(countryCodes.includes(code))) {
      options_countries_africa.push(
        { value: code, text: name }
      );
    }
  }
  setOptionsToSelect(select_countries_africa, options_countries_africa, "Choose");
  // Asia
  for (let i = 0; i < mapContinentCountries['Asia'].length; i++) {
    const code = mapContinentCountries['Asia'][i][0];
    const name = mapContinentCountries['Asia'][i][1]
    if (!(countryCodes.includes(code))) {
      options_countries_asia.push(
        { value: code, text: name }
      );
    }
  }
  setOptionsToSelect(select_countries_asia, options_countries_asia, "Choose");
  // Europe
  for (let i = 0; i < mapContinentCountries['Europe'].length; i++) {
    const code = mapContinentCountries['Europe'][i][0];
    const name = mapContinentCountries['Europe'][i][1]
    if (!(countryCodes.includes(code))) {
      options_countries_europe.push(
        { value: code, text: name }
      );
    }
  }
  setOptionsToSelect(select_countries_europe, options_countries_europe, "Choose");
  // North America
  for (let i = 0; i < mapContinentCountries['North America'].length; i++) {
    const code = mapContinentCountries['North America'][i][0];
    const name = mapContinentCountries['North America'][i][1]
    if (!(countryCodes.includes(code))) {
      options_countries_north_america.push(
        { value: code, text: name }
      );
    }
  }
  setOptionsToSelect(select_countries_north_america, options_countries_north_america, "Choose");
  // South America
  for (let i = 0; i < mapContinentCountries['South America'].length; i++) {
    const code = mapContinentCountries['South America'][i][0];
    const name = mapContinentCountries['South America'][i][1]
    if (!(countryCodes.includes(code))) {
      options_countries_south_america.push(
        { value: code, text: name }
      );
    }
  }
  setOptionsToSelect(select_countries_south_america, options_countries_south_america, "Choose");
  // Oceania
  for (let i = 0; i < mapContinentCountries['Oceania'].length; i++) {
    const code = mapContinentCountries['Oceania'][i][0];
    const name = mapContinentCountries['Oceania'][i][1]
    if (!(countryCodes.includes(code))) {
      options_countries_oceania.push(
        { value: code, text: name }
      );
    }
  }
  setOptionsToSelect(select_countries_oceania, options_countries_oceania, "Choose");
}



// -------------
// 3. eCharts
// -------------



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
  optionsAxisCommon = {
    // settings for both axis
    boundaryGap: false,
    nameTextStyle: { fontWeight: "bold" },
    minorTick: { show: true },
    minorSplitLine: {
      show: true
    },
    axisTick: { inside: true },
    axisLabel: { show: true },
  }
  option = {
    title: {
      text: "COVID-19 Country Comparison Custom Chart",
      left: 'center',
      subtext: "by Torben https://entorb.net based on JHU data",
      sublink: "https://entorb.net/COVID-19-coronavirus/",
    },
    legend: {
      type: 'scroll',
      orient: 'vertical',
      right: 0,
      top: 50,
      //          bottom: 20,
    },
    xAxis: { ...optionsAxisCommon }, // copy of object
    // in type log : setting min is required
    yAxis: { ...optionsAxisCommon }, // copy of object
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
      left: 75,
      bottom: 40,
      right: 180,
    },
  };

  option.xAxis.type = "value"; // value, time, log  ; will be overwritten if field "Date" is selected
  option.xAxis.name = formatValueToSentenceLike(select_xAxisProperty.value, "_");
  option.xAxis.nameLocation = "end";
  option.yAxis.type = "value"; // value, time, log  ; will be overwritten if field "Date" is selected
  option.yAxis.name = formatValueToSentenceLike(select_yAxisProperty.value, "_");
  option.yAxis.nameLocation = "center";
  option.yAxis.nameGap = 60;

  if (select_xAxisProperty.value == "Date") {
    option.xAxis.type = "time";
    // option.xAxis.axisLabel.formatter = function (value, index) {
    //   // Formatted to be month/day; display year only in the first label
    //   var date = new Date(value);
    //   var texts = [(date.getMonth() + 1), date.getDate()];
    //   if (index === 0) {
    //     texts.unshift(date.getYear());
    //   }
    //   return texts.join('-');
    // }
  }

  if (select_yAxisProperty.value == "Cases_Doubling_Time" || select_yAxisProperty.value == "Deaths_Doubling_Time") {
    option.yAxis.inverse = true;
    option.yAxis.name = option.yAxis.name + " (days)";
    // option.yAxis.nameLocation = "start";
  }



  if (select_xAxisTimeRange.value == "4weeks") {
    const daysOffset = - 4 * 7;
    const daysInterval = 7;
    if (select_xAxisProperty.value == "Days_Past") {
      option.xAxis.min = daysOffset;
      option.xAxis.interval = daysInterval;
    }
    else if (select_xAxisProperty.value == "Date") {
      // fetch latest date of first data series as basis
      const s_data_last_date = option.series[0].data[option.series[0].data.length - 1][0]
      const ts_last_date = Date.parse(s_data_last_date)
      var minDate = new Date(ts_last_date);
      minDate.setDate(minDate.getDate() + daysOffset);
      option.xAxis.min = minDate;
      option.xAxis.interval = 3600 * 1000 * 24 * daysInterval;
    }
  } else if (select_xAxisTimeRange.value == "12weeks") {
    const daysOffset = - 12 * 7;
    const daysInterval = 14;
    if (select_xAxisProperty.value == "Days_Past") {
      option.xAxis.min = daysOffset;
      option.xAxis.interval = daysInterval;
    }
    else if (select_xAxisProperty.value == "Date") {
      // fetch latest date of first data series as basis
      const s_data_last_date = option.series[0].data[option.series[0].data.length - 1][0]
      const ts_last_date = Date.parse(s_data_last_date)
      var minDate = new Date(ts_last_date);
      minDate.setDate(minDate.getDate() + daysOffset);
      option.xAxis.min = minDate;
      option.xAxis.interval = 3600 * 1000 * 24 * daysInterval;
    }
  }


  if (select_yAxisScale.value == "linscale") {
    option.yAxis.type = "value";
  } else {
    option.yAxis.type = "log";
    // for logscale we need to set the min value as 0 is not good ;-)
    option.yAxis.min = 1;
    if (select_yAxisProperty.value == "Deaths_New_Per_Million") {
      option.yAxis.min = 0.1;
    }
  }

  if (select_yAxisProperty.value == "Deaths_Per_Million") {
    console.log('male')
    option.series[0].markLine = {
      symbol: 'none',
      silent: true,
      animation: false,
      lineStyle: {
        color: "#0000ff"
        //type: 'solid'
      },
      data: [
        // { type: 'average', name: '123' },
        {
          yAxis: 9,
          name: 'US 9/11',
          // value: 'value',
          label: {
            position: 'insideStartTop',
            formatter: '{b}' // b -> name
          },
        },
        {
          yAxis: 44,
          name: 'US guns 2017',
          // value: 'value',
          label: {
            position: 'insideStartTop',
            formatter: '{b}' // b -> name
          },
        },
        {
          yAxis: 104,
          name: 'US traffic 2018 and\nflu 2018/19',
          // value: 'value',
          label: {
            position: 'insideStartTop',
            formatter: '{b}' // b -> name
          },
        },
        {
          yAxis: 205,
          name: 'US drugs 2018',
          // value: 'value',
          label: {
            position: 'insideStartTop',
            formatter: '{b}' // b -> name
          },
        },
        {
          yAxis: 1857,
          name: 'US cancer 2018',
          // value: 'value',
          label: {
            position: 'insideStartTop',
            formatter: '{b}' // b -> name
          },
        },
      ]
    }
  }


  if (select_yAxisProperty.value == "Deaths_New_Per_Million") {
    console.log('male')
    option.series[0].markLine = {
      symbol: 'none',
      animation: false,
      lineStyle: {
        color: "#0000ff"
        //type: 'solid'
      },
      data: [
        {
          yAxis: 44 / 365,
          name: 'US guns 2017',
          // value: 'value',
          label: {
            position: 'insideStartTop',
            formatter: '{b}' // b -> name
          },
        },
        {
          yAxis: 104 / 365,
          name: 'US traffic 2018 and\nflu 2018/19',
          // value: 'value',
          label: {
            position: 'insideStartTop',
            formatter: '{b}' // b -> name
          },
        },
        {
          yAxis: 205 / 365,
          name: 'US drugs 2018',
          // value: 'value',
          label: {
            position: 'insideStartTop',
            formatter: '{b}' // b -> name
          },
        },
        {
          yAxis: 1857 / 365,
          name: 'US cancer 2018',
          // value: 'value',
          label: {
            position: 'insideStartTop',
            formatter: '{b}' // b -> name
          },
        },
        {
          yAxis: 8638 / 365,
          name: 'US total mortality 2017',
          // value: 'value',
          label: {
            position: 'insideStartTop',
            formatter: '{b}' // b -> name
          },
        },
      ]
    }
  }

  if (select_yAxisProperty.value == "Deaths_Last_Week_Per_Million") {
    console.log('male')
    option.series[0].markLine = {
      symbol: 'none',
      animation: false,
      lineStyle: {
        color: "#0000ff"
        //type: 'solid'
      },
      data: [
        {
          yAxis: 44 / 52.14,
          name: 'US guns 2017',
          // value: 'value',
          label: {
            position: 'insideStartTop',
            formatter: '{b}' // b -> name
          },
        },
        {
          yAxis: 104 / 52.14,
          name: 'US traffic 2018 and\nflu 2018/19',
          // value: 'value',
          label: {
            position: 'insideStartTop',
            formatter: '{b}' // b -> name
          },
        },
        {
          yAxis: 205 / 52.14,
          name: 'US drugs 2018',
          // value: 'value',
          label: {
            position: 'insideStartTop',
            formatter: '{b}' // b -> name
          },
        },
        {
          yAxis: 1857 / 52.14,
          name: 'US cancer 2018',
          // value: 'value',
          label: {
            position: 'insideStartTop',
            formatter: '{b}' // b -> name
          },
        },
        {
          yAxis: 8638 / 52.14,
          name: 'US total mortality 2017',
          // value: 'value',
          label: {
            position: 'insideStartTop',
            formatter: '{b}' // b -> name
          },
        },
      ]
    }
  }


  chart.clear(); // needed as setOption does not reliable remove all old data, see https://github.com/apache/incubator-echarts/issues/6202#issuecomment-460322781
  chart.setOption(option, true);
}

