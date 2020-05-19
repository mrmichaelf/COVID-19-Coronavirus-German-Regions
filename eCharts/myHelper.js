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
function formatValueToSentenceLike(value, separator) { // , TODO: language
  // if (language == 'de') {
  //   value.replace("Cases", "Infektionen");
  //   value.replace("Deaths", "Tote");
  //   value.replace("_New", "_Neu");
  //   value.replace("_Last_Week", "_Letzte_Woche");
  //   value.replace("_Per_Million", "_Pro_Millionen");
  // }
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
// type: Country or DeDistrict
// code: the code of the country e.g. "DE"
function getUrl(type, code) {
  if (type == 'Country') {
    return 'https://entorb.net/COVID-19-coronavirus/data/int/country-' + code + '.json';
  } else if (type == 'DeDistrict') {
    return 'https://entorb.net/COVID-19-coronavirus/data/de-districts/de-district_timeseries-' + code + '.json';
  }
}



// Fetches the data for one country code
// type: Country or DeDistrict
// code: the code of the country e.g. "DE"
// dataObject: the object which will contain all data about the Countries/DeDistricts
function fetchData(type, code, dataObject) {
  const url = getUrl(type, code);
  return $.getJSON(url, function () {
    // console.log(`success: ${code}`);
  })
    .done(function (data) {
      console.log('done: ' + code);
      dataObject[code] = data;
    })
    .fail(function () {
      console.log('fail:' + code);
    });
}


// Gets the series property of the chart object
// codes: the codes of the countries to display
// dataObject: the object which contains all data about the countries
// xAxis: the property displayed in the X axis
// yAxis: the property displayed in the Y axis
function getSeries(codes, dataObject, map_id_name, xAxis, yAxis) {
  const series = [];
  const dataSymbols = new Array('circle', 'rect', 'triangle', 'diamond'); // 'roundRect', 'pin', 'arrow'

  // sort codes by last value
  const lastValues2 = [];
  for (let i = 0; i < codes.length; i++) {
    const yValues = dataObject[codes[i]]; //[key][yAxis];
    const last_value = yValues[yValues.length - 1][yAxis]
    // console.log(codes[i] + " : " + last_value);
    lastValues2.push([codes[i], last_value]);
  }
  lastValues2.sort(function (a, b) {
    return a[1] - b[1];
  });
  codes_ordered = [];
  for (let i = 0; i < codes.length; i++) {
    codes_ordered.push(lastValues2[i][0]);
  }
  // reverse sorting, for all but the Doubling_Time series
  if (yAxis != "Cases_Doubling_Time" && yAxis != "Deaths_Doubling_Time") {
    // console.log("reversing")
    codes_ordered.reverse();
  }

  codes = codes_ordered;

  for (let i = 0; i < codes.length; i++) {
    const countryLine = [];
    // We filter the data to display here using the axis data
    $.each(dataObject[codes[i]], function (key, val) {
      countryLine.push([
        dataObject[codes[i]][key][xAxis],
        dataObject[codes[i]][key][yAxis],
      ]);
    });
    const modulo = i % dataSymbols.length;

    const seria = {
      data: countryLine, // the line of the country
      name: map_id_name[codes[i]],
      type: "line",
      symbolSize: 6,
      smooth: true,
      symbol: dataSymbols[modulo],
    };
    series.push(seria);
  }
  return series;
}

// when a country is selected for adding to the chart, this is called
function new_country_selected(countryCodes, country_code_to_add) { // , select_country, options_countries
  if (country_code_to_add != "placeholder123") {
    // var country_code_to_add = select_country.value;
    // console.log(country_code_to_add)

    // append to list of country codes
    countryCodes.push(country_code_to_add);

    // start fetching / download of data
    promises.push(fetchData('Country', country_code_to_add, countriesDataObject))

    // Version 1: pass select and its options as parameter
    // remove selected values from options_countries
    // arrayRemoveValueTextPairByValue(options_countries, country_code_to_add)
    // setOptionsToSelect(select_country, options_countries, "Choose");

    // Version 2: refresh all selects, as this is required when clicking in tabular instead of selecting via dropdown
    arrayRemoveValueTextPairByValue(options_countries_africa, country_code_to_add)
    arrayRemoveValueTextPairByValue(options_countries_asia, country_code_to_add)
    arrayRemoveValueTextPairByValue(options_countries_europe, country_code_to_add)
    arrayRemoveValueTextPairByValue(options_countries_north_america, country_code_to_add)
    arrayRemoveValueTextPairByValue(options_countries_south_america, country_code_to_add)
    arrayRemoveValueTextPairByValue(options_countries_oceania, country_code_to_add)
    setOptionsToSelect(select_countries_africa, options_countries_africa, "Choose");
    setOptionsToSelect(select_countries_asia, options_countries_asia, "Choose");
    setOptionsToSelect(select_countries_europe, options_countries_europe, "Choose");
    setOptionsToSelect(select_countries_north_america, options_countries_north_america, "Choose");
    setOptionsToSelect(select_countries_south_america, options_countries_south_america, "Choose");
    setOptionsToSelect(select_countries_oceania, options_countries_oceania, "Choose");

    // wait for fetching to complete, than update chart
    Promise.all(promises).then(function () {
      refreshCountryChartWrapper();
    });
  }
}

// when a DeDistrict is selected for adding to the chart, this is called
function new_deDistrict_selected(deDistrictCodes, deDistrict_code_to_add) {
  // append to list of codes
  deDistrictCodes.push(deDistrict_code_to_add);

  // start fetching / download of data
  promises.push(fetchData('DeDistrict', deDistrict_code_to_add, deDistrictDataObject))

  // wait for fetching to complete, than update chart
  Promise.all(promises).then(function () {
    refreshDeDistrictsChartWrapper();
  });
}

function resetDeDistrictsChart() {
  deDistrictCodes = [deDistrictCodesDefaultValue];
  refreshDeDistrictsChartWrapper();
}

// resets country selection to default
function resetCountryChart() {
  options_countries_africa = [];
  options_countries_asia = [];
  options_countries_europe = [];
  options_countries_north_america = [];
  options_countries_south_america = [];
  options_countries_oceania = [];
  countryCodes = ["DE"];
  populateCountrySelects();
  refreshCountryChartWrapper();
}

function populateCountrySelects() {
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



// Refreshes the country chart
// countryCodes: the codes of the countries to display
// countriesDataObject: the object which contains all data about the countries
// select_xAxisProperty: the select of the X axis
// select_yAxisProperty: the select of the Y axis
function refreshCountryChart(
  chart,
  countryCodes,
  countriesDataObject,
  select_xAxisProperty,
  select_yAxisProperty,
  select_xAxisTimeRange,
  select_xAxisScale,
  select_yAxisScale
) {

  // disable time selection for non-time series 
  if (select_xAxisProperty.value == "Date" || select_xAxisProperty.value == "Days_Past") {
    select_xAxisTimeRange.disabled = false;
  } else {
    select_xAxisTimeRange.disabled = true;
  }
  // disable logscale for time series
  if (select_xAxisProperty.value == "Date" || select_xAxisProperty.value == "Days_Past") {
    select_xAxisScale.disabled = true;
    select_xAxisScale.value = 'linscale';
  } else {
    select_xAxisScale.disabled = false;
  }
  // disable logscale for deaths_per_cases
  if (select_yAxisProperty.value == "Deaths_Per_Cases" || select_yAxisProperty.value == "Deaths_Per_Cases_Last_Week") {
    select_yAxisScale.disabled = true;
    select_yAxisScale.value = 'linscale';
  }


  option = {}
  // optionsAxisCommon = {
  //   // settings for both axis
  //   boundaryGap: false,
  //   nameTextStyle: { fontWeight: "bold" },
  //   minorTick: { show: true },
  //   minorSplitLine: {
  //     show: true
  //   },
  //   axisTick: { inside: true },
  //   axisLabel: { show: true },
  // }

  //  text: "COVID-19 Country Comparison Custom Chart",

  option = {
    title: {
      text: "COVID-19: " + formatValueToSentenceLike(select_yAxisProperty.value, "_"),
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
    xAxis: {
      // common settings for both axes
      type: 'value', // will be overwritten if needed below
      boundaryGap: false,
      nameTextStyle: { fontWeight: "bold" },
      minorTick: { show: true },
      minorSplitLine: {
        show: true
      },
      axisTick: { inside: true },
      axisLabel: { show: true },
      // for x only
      name: formatValueToSentenceLike(select_xAxisProperty.value, "_"),
      nameLocation: 'end',
    },
    // in type log : setting min is required
    yAxis: {
      // common settings for both axes
      type: 'value', // will be overwritten if needed below
      boundaryGap: false,
      nameTextStyle: { fontWeight: "bold" },
      minorTick: { show: true },
      minorSplitLine: {
        show: true
      },
      axisTick: { inside: true },
      axisLabel: { show: true },
      // for y only
      name: formatValueToSentenceLike(select_yAxisProperty.value, "_"),
      nameLocation: 'center',
      nameGap: 60,
    },
    series: getSeries(
      countryCodes,
      countriesDataObject,
      mapCountryNames,
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
        // restore: {},
        dataZoom: {},
        dataView: { readOnly: true },
        saveAsImage: {},
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

  if (select_xAxisProperty.value == "Date") {
    option.xAxis.type = "time";
    // trying to modify the date format
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

  // For doubling time: invert axis, only for Y
  if (select_yAxisProperty.value == "Cases_Doubling_Time" || select_yAxisProperty.value == "Deaths_Doubling_Time") {
    option.yAxis.inverse = true;
    option.yAxis.name = option.yAxis.name + " (days)";
    // option.yAxis.nameLocation = "start";
  }

  // Time restriction for X Axis only
  if (select_xAxisTimeRange.value == "4weeks") {
    const daysOffset = - 4 * 7;
    const daysInterval = 7;
    if (select_xAxisProperty.value == "Days_Past") {
      option.xAxis.min = daysOffset;
      option.xAxis.interval = daysInterval;
    }
    else if (select_xAxisProperty.value == "Date") {
      // fetch latest date of first data series as basis
      const s_data_last_date = option.series[0].data[option.series[0].data.length - 1][0];
      const ts_last_date = Date.parse(s_data_last_date);
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
      const s_data_last_date = option.series[0].data[option.series[0].data.length - 1][0];
      const ts_last_date = Date.parse(s_data_last_date);
      var minDate = new Date(ts_last_date);
      minDate.setDate(minDate.getDate() + daysOffset);
      option.xAxis.min = minDate;
      option.xAxis.interval = 3600 * 1000 * 24 * daysInterval;
    }
  }

  // Logscale for X Axis (eCharts allows either time axis or log axis)
  if (select_xAxisProperty.value != "Date") {
    if (select_xAxisScale.value == "linscale") {
      option.xAxis.type = "value";
    } else {
      option.xAxis.type = "log";
      // for logscale we need to set the min value to avoid 0 is not good ;-)
      if (select_xAxisProperty.value == "Deaths_New_Per_Million") {
        option.xAxis.min = 0.1;
      } else {
        option.xAxis.min = 1;
      }
    }
  }
  // Logscale for Y Axis (eCharts allows either time axis or log axis)
  if (select_yAxisScale.value == "linscale") {
    option.yAxis.type = "value";
  } else {
    option.yAxis.type = "log";
    // for logscale we need to set the min value to avoid 0 is not good ;-)
    if (select_yAxisProperty.value == "Deaths_New_Per_Million") {
      option.yAxis.min = 0.1;
    } else {
      option.yAxis.min = 1;
    }
  }

  // Marklines
  if (select_yAxisProperty.value == "Deaths_Per_Million") {
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
          name: 'US traffic 2018 and flu 2018/19',
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
          name: 'US traffic 2018 and flu 2018/19',
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
          name: 'US traffic 2018 and flu 2018/19',
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






function refreshDeDistrictsChart(
  chart,
  codes,
  dataObject,
  select_yAxisProperty
) {
  option = {
    title: {
      // text: "COVID-19: Landkreisvergleich 7-Tages-Neuinfektionen",
      text: "COVID-19: Landkreisvergleich " + formatValueToSentenceLike(select_yAxisProperty.value, "_"),
      left: 'center',
      subtext: "by Torben https://entorb.net based on RKI data",
      sublink: "https://entorb.net/COVID-19-coronavirus/",
    },
    legend: {
      type: 'scroll',
      orient: 'vertical',
      right: 0,
      top: 50,
      //          bottom: 20,
    },
    xAxis: {
      // common settings for both axes
      type: 'time', // will be overwritten if needed below
      boundaryGap: false,
      nameTextStyle: { fontWeight: "bold" },
      minorTick: { show: true },
      minorSplitLine: {
        show: true
      },
      axisTick: { inside: true },
      axisLabel: {
        show: true,
        formatter: function (value) {
          var date = new Date(value);
          return date.toLocaleDateString("de-DE")
        }
      },
      // for x only
      name: 'Datum',
      nameLocation: 'end',

    },
    yAxis: {
      // common settings for both axes
      type: 'value', // will be overwritten if needed below
      boundaryGap: false,
      nameTextStyle: { fontWeight: "bold" },
      minorTick: { show: true },
      minorSplitLine: {
        show: true
      },
      axisTick: { inside: true },
      axisLabel: { show: true },
      // for y only
      name: formatValueToSentenceLike(select_yAxisProperty.value, "_"),
      nameLocation: 'center',
      nameGap: 60,
    },
    series: getSeries(
      codes,
      dataObject,
      mapDeDistrictNames,
      'Date',
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
        // restore: {},
        dataZoom: {},
        dataView: { readOnly: true },
        saveAsImage: {},
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
      right: 250,
    },
  };

  if (select_yAxisProperty.value == "Cases_Last_Week_Per_Million") {
    option.series[0].markLine = {
      symbol: 'none',
      silent: true,
      animation: false,
      lineStyle: {
        color: "#0000ff"
        //type: 'solid'
      },
      data: [
        {
          yAxis: 500,
        },
      ]
    }
  }

  chart.clear(); // needed as setOption does not reliable remove all old data, see https://github.com/apache/incubator-echarts/issues/6202#issuecomment-460322781
  chart.setOption(option, true);
}