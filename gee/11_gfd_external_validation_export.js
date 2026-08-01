// Robust Flood-Risk Prioritisation in India
// External/convergent-validity pilot using the Global Flood Database (GFD).
//
// This script is intended for direct use in the Google Earth Engine Code Editor.
// It exports district-level satellite-observed flood metrics for India using:
//   - ee.ImageCollection('GLOBAL_FLOOD_DB/MODIS_EVENTS/V1')
//   - ee.FeatureCollection('WM/geoLab/geoBoundaries/600/ADM2')
//
// Scientific framing:
//   * GFD covers 2000-2018, while published DFSI reflects a longer historical
//     period. Treat this as partial temporal overlap.
//   * GFD is an independent satellite-observed sample of mapped flood events,
//     not a complete inventory of all Indian floods.
//   * GFD measures physical inundation. DFSI combines hazard, exposure and
//     human impacts. This is convergent validity, not definitive ground truth.
//
// After the exports finish in Google Drive, download the CSV files and place
// them in:
//   data/processed/gfd_external_validation/

var GFD = ee.ImageCollection('GLOBAL_FLOOD_DB/MODIS_EVENTS/V1');
var ADM2 = ee.FeatureCollection('WM/geoLab/geoBoundaries/600/ADM2');
var indiaAdm2 = ADM2.filter(ee.Filter.eq('shapeGroup', 'IND'));
var indiaGeometry = indiaAdm2.geometry();

// Use a scale close to the MODIS/GFD native product. We print actual nominal
// scales below and then use the flooded-band nominal scale as analysisScale.
var firstImage = ee.Image(GFD.first());
var floodedScale = firstImage.select('flooded').projection().nominalScale();
var durationScale = firstImage.select('duration').projection().nominalScale();
var clearScale = firstImage.select('clear_perc').projection().nominalScale();
var permWaterScale = firstImage.select('jrc_perm_water').projection().nominalScale();
var analysisScale = floodedScale;

print('Indian ADM2 geometry count', indiaAdm2.size());
print('Sample Indian ADM2 first feature property names',
  ee.Feature(indiaAdm2.first()).propertyNames());
print('Sample Indian ADM2 first raw feature', indiaAdm2.first());
print('Sample Indian ADM2 properties', indiaAdm2.limit(10).select(['shapeName', 'shapeID', 'shapeType', 'shapeGroup']));
print('GFD total event count', GFD.size());
print('GFD first image band names', firstImage.bandNames());
print('GFD first image property names', firstImage.propertyNames());
print('GFD first raw image', firstImage);
print('GFD nominal scale: flooded', floodedScale);
print('GFD nominal scale: duration', durationScale);
print('GFD nominal scale: clear_perc', clearScale);
print('GFD nominal scale: jrc_perm_water', permWaterScale);
print('Selected analysis scale (m)', analysisScale);

// Metadata filter where possible. GFD images include country metadata, but
// property structure can be inconsistent across examples. We therefore combine
// documented country-code/name filtering with a spatial-intersection filter.
var indiaByCountryCode = GFD.filter(ee.Filter.listContains('cc', 'IND'));
var indiaByCountryName = GFD.filter(ee.Filter.listContains('countries', 'India'));
var indiaByMetadata = indiaByCountryCode.merge(indiaByCountryName).distinct('id');
var indiaBySpatialIntersection = GFD.filterBounds(indiaGeometry);
var indiaEvents = indiaByMetadata.merge(indiaBySpatialIntersection).distinct('id');

print('India-filtered GFD event count by country code', indiaByCountryCode.size());
print('India-filtered GFD event count by country name', indiaByCountryName.size());
print('India-filtered GFD event count by metadata union', indiaByMetadata.size());
print('India-filtered GFD event count by spatial intersection', indiaBySpatialIntersection.size());
print('India-filtered GFD event count used', indiaEvents.size());
print('First India-related GFD event property names',
  ee.Image(indiaEvents.first()).propertyNames());
print('First India-related raw GFD event', indiaEvents.first());
print('Sample India-related GFD event properties',
  indiaEvents.limit(10).map(function(img) {
    img = ee.Image(img);
    return ee.Feature(null, {
      id: img.get('id'),
      cc: img.get('cc'),
      countries: img.get('countries'),
      system_time_start: img.get('system:time_start'),
      event_date: ee.Date(img.get('system:time_start')).format('YYYY-MM-dd'),
      dfo_main_cause: img.get('dfo_main_cause'),
      dfo_severity: img.get('dfo_severity')
    });
  })
);
print('India-related GFD event IDs', indiaEvents.aggregate_array('id'));
print('Earliest India-related event date',
  ee.Date(ee.Number(indiaEvents.aggregate_min('system:time_start'))).format('YYYY-MM-dd'));
print('Latest India-related event date',
  ee.Date(ee.Number(indiaEvents.aggregate_max('system:time_start'))).format('YYYY-MM-dd'));

// Export an event inventory table for audit and reproducibility.
var eventInventory = indiaEvents.map(function(img) {
  img = ee.Image(img);
  return ee.Feature(null)
  // Preserve all original image properties exposed by Earth Engine, because
  // GFD metadata names can differ from examples in documentation.
  .copyProperties(img)
  .set({
    gfd_event_id: img.get('id'),
    cc: img.get('cc'),
    countries: img.get('countries'),
    system_time_start: img.get('system:time_start'),
    event_date: ee.Date(img.get('system:time_start')).format('YYYY-MM-dd'),
    dfo_main_cause: img.get('dfo_main_cause'),
    dfo_severity: img.get('dfo_severity'),
    india_filter_method: 'metadata_union_or_spatial_intersection',
    india_filter_note: 'Country metadata filters may be empty; spatial intersection with India boundary was also used.'
  });
});

// For every event:
//   event floodwater = flooded == 1 AND jrc_perm_water != 1
// Non-flood pixels are masked, not treated as observed floodwater.
// clear_perc is retained only over observed, non-permanent flood pixels.
function eventFloodMask(img) {
  img = ee.Image(img);
  return img.select('flooded').eq(1)
    .and(img.select('jrc_perm_water').neq(1))
    .selfMask()
    .rename('event_floodwater');
}

function eventFloodAreaM2(img) {
  return eventFloodMask(img).multiply(ee.Image.pixelArea())
    .rename('flooded_area_event_m2');
}

function eventDurationAreaDays(img) {
  img = ee.Image(img);
  return img.select('duration')
    .updateMask(eventFloodMask(img))
    .multiply(ee.Image.pixelArea())
    .rename('inundation_area_days_m2_days');
}

function eventClearPct(img) {
  img = ee.Image(img);
  return img.select('clear_perc')
    .updateMask(eventFloodMask(img))
    .rename('clear_perc_over_flood');
}

var floodMaskCollection = ee.ImageCollection(indiaEvents.map(eventFloodMask));
var floodAreaCollection = ee.ImageCollection(indiaEvents.map(eventFloodAreaM2));
var durationAreaCollection = ee.ImageCollection(indiaEvents.map(eventDurationAreaDays));
var clearPctCollection = ee.ImageCollection(indiaEvents.map(eventClearPct));

// District-level definitions:
//   district_area_km2: boundary area in square kilometres.
//   gfd_event_collection_count: number of India-related GFD events in the
//     filtered image collection.
//   ever_flooded_area_km2: area flooded at least once, excluding permanent water.
//   ever_flooded_fraction_pct: ever_flooded_area_km2 / district_area_km2 * 100.
//   cumulative_flooded_area_event_km2: sum over events of flooded area in km2;
//     repeated flooding of the same pixel in different events is counted once
//     per event.
//   cumulative_flooded_area_event_fraction: cumulative event-area divided by
//     district area.
//   cumulative_inundation_area_days_km2_days: sum over events of flooded
//     pixel area multiplied by inundation duration in days.
//   cumulative_inundation_area_days_per_km2: area-days divided by district area.
//   mean_flooded_pixel_event_count: mean number of detected flood events per
//     district pixel.
//   maximum_flooded_pixel_event_count: maximum number of detected flood events
//     for any district pixel.
//   mean_clear_perc_over_observed_flood_pixels: mean clear-observation percent
//     over pixels where non-permanent floodwater was detected.
var everFlooded = floodMaskCollection.max().rename('ever_flooded');
var floodedPixelEventCount = floodMaskCollection.sum().rename('flooded_pixel_event_count');
var districtSumMetricImage = ee.Image.cat([
  everFlooded.multiply(ee.Image.pixelArea()).rename('ever_flooded_area_m2'),
  floodAreaCollection.sum().rename('cumulative_flooded_area_event_m2'),
  durationAreaCollection.sum().rename('cumulative_inundation_area_days_m2_days')
]);
var districtMeanMetricImage = ee.Image.cat([
  floodedPixelEventCount.rename('flooded_pixel_event_count'),
  clearPctCollection.mean().rename('mean_clear_perc_over_observed_flood_pixels')
]);
var districtMaxMetricImage = floodedPixelEventCount.rename('flooded_pixel_event_count');

function numberOrZero(dict, key) {
  var value = ee.Dictionary(dict).get(key);
  return ee.Number(ee.Algorithms.If(value, value, 0));
}

var eventCount = indiaEvents.size();
var firstDate = ee.Date(ee.Number(indiaEvents.aggregate_min('system:time_start'))).format('YYYY-MM-dd');
var lastDate = ee.Date(ee.Number(indiaEvents.aggregate_max('system:time_start'))).format('YYYY-MM-dd');

var districtMetrics = indiaAdm2.map(function(feat) {
  var areaKm2 = feat.geometry().area(1).divide(1e6);
  var sumStats = districtSumMetricImage.reduceRegion({
    reducer: ee.Reducer.sum(),
    geometry: feat.geometry(),
    scale: analysisScale,
    maxPixels: 1e13,
    tileScale: 4
  });
  var meanStats = districtMeanMetricImage.reduceRegion({
    reducer: ee.Reducer.mean(),
    geometry: feat.geometry(),
    scale: analysisScale,
    maxPixels: 1e13,
    tileScale: 4
  });
  var maxStats = districtMaxMetricImage.reduceRegion({
    reducer: ee.Reducer.max(),
    geometry: feat.geometry(),
    scale: analysisScale,
    maxPixels: 1e13,
    tileScale: 4
  });
  var everKm2 = numberOrZero(sumStats, 'ever_flooded_area_m2').divide(1e6);
  var cumulativeKm2 = numberOrZero(sumStats, 'cumulative_flooded_area_event_m2').divide(1e6);
  var areaDaysKm2 = numberOrZero(sumStats, 'cumulative_inundation_area_days_m2_days').divide(1e6);
  return ee.Feature(null, {
    boundary_shape_id: feat.get('shapeID'),
    boundary_district_name: feat.get('shapeName'),
    boundary_shape_type: feat.get('shapeType'),
    boundary_shape_group: feat.get('shapeGroup'),
    district_area_km2: areaKm2,
    gfd_event_collection_count: eventCount,
    ever_flooded_area_km2: everKm2,
    ever_flooded_fraction_pct: everKm2.divide(areaKm2).multiply(100),
    cumulative_flooded_area_event_km2: cumulativeKm2,
    cumulative_flooded_area_event_fraction: cumulativeKm2.divide(areaKm2),
    cumulative_inundation_area_days_km2_days: areaDaysKm2,
    cumulative_inundation_area_days_per_km2: areaDaysKm2.divide(areaKm2),
    mean_flooded_pixel_event_count: meanStats.get('flooded_pixel_event_count'),
    maximum_flooded_pixel_event_count: maxStats.get('flooded_pixel_event_count'),
    mean_clear_perc_over_observed_flood_pixels: meanStats.get('mean_clear_perc_over_observed_flood_pixels'),
    first_observed_event_date: firstDate,
    last_observed_event_date: lastDate
  });
});

// District-event table definitions:
// One row is emitted only when non-permanent floodwater is actually detected
// within the district. An event footprint intersection alone is not counted.
function districtEventRows(img) {
  img = ee.Image(img);
  var floodMask = eventFloodMask(img);
  var eventAreaImage = floodMask.multiply(ee.Image.pixelArea()).rename('flooded_area_m2');
  var eventMeanImage = ee.Image.cat([
    img.select('duration').updateMask(floodMask).rename('duration'),
    img.select('clear_perc').updateMask(floodMask).rename('clear_perc')
  ]);

  return indiaAdm2.map(function(feat) {
    var areaKm2 = feat.geometry().area(1).divide(1e6);
    var areaStats = eventAreaImage.reduceRegion({
      reducer: ee.Reducer.sum(),
      geometry: feat.geometry(),
      scale: analysisScale,
      maxPixels: 1e13,
      tileScale: 4
    });
    var meanStats = eventMeanImage.reduceRegion({
      reducer: ee.Reducer.mean(),
      geometry: feat.geometry(),
      scale: analysisScale,
      maxPixels: 1e13,
      tileScale: 4
    });
    var floodedKm2 = numberOrZero(areaStats, 'flooded_area_m2').divide(1e6);
    return ee.Feature(null, {
      boundary_shape_id: feat.get('shapeID'),
      boundary_district_name: feat.get('shapeName'),
      gfd_event_id: img.get('id'),
      event_date: ee.Date(img.get('system:time_start')).format('YYYY-MM-dd'),
      flooded_area_km2: floodedKm2,
      flooded_fraction_of_district: floodedKm2.divide(areaKm2),
      mean_inundation_duration: meanStats.get('duration'),
      mean_clear_percentage: meanStats.get('clear_perc')
    });
  }).filter(ee.Filter.gt('flooded_area_km2', 0));
}

var districtEventMetrics = ee.FeatureCollection(indiaEvents.iterate(function(img, acc) {
  return ee.FeatureCollection(acc).merge(districtEventRows(img));
}, ee.FeatureCollection([])));
print('District metrics sample', districtMetrics.limit(10));
print('District-event metrics sample', districtEventMetrics.limit(10));

Export.table.toDrive({
  collection: districtMetrics,
  description: 'gfd_india_adm2_metrics',
  folder: 'gfd_external_validation',
  fileNamePrefix: 'gfd_india_adm2_metrics',
  fileFormat: 'CSV'
});

Export.table.toDrive({
  collection: districtEventMetrics,
  description: 'gfd_india_district_event_metrics',
  folder: 'gfd_external_validation',
  fileNamePrefix: 'gfd_india_district_event_metrics',
  fileFormat: 'CSV'
});

Export.table.toDrive({
  collection: eventInventory,
  description: 'gfd_india_event_inventory',
  folder: 'gfd_external_validation',
  fileNamePrefix: 'gfd_india_event_inventory',
  fileFormat: 'CSV'
});
