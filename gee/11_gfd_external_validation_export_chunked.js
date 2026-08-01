// Robust Flood-Risk Prioritisation in India
// Chunked Global Flood Database export for Earth Engine memory limits.
//
// Use this script if gee/11_gfd_external_validation_export.js exceeds Earth
// Engine memory. It exports:
//   1. gfd_india_adm2_boundaries.csv
//   2. gfd_india_event_inventory.csv
//   3. gfd_india_district_event_metrics_part_XX.csv batch files
//
// Place all downloaded CSV files in:
//   data/processed/gfd_external_validation/
//
// The Python notebooks aggregate the chunked district-event files into the
// district-level metrics required for the pilot.

var GFD = ee.ImageCollection('GLOBAL_FLOOD_DB/MODIS_EVENTS/V1');
var ADM2 = ee.FeatureCollection('WM/geoLab/geoBoundaries/600/ADM2');
var indiaAdm2 = ADM2.filter(ee.Filter.eq('shapeGroup', 'IND'));
var indiaGeometry = indiaAdm2.geometry();

var firstImage = ee.Image(GFD.first());
var analysisScale = firstImage.select('flooded').projection().nominalScale();

print('Indian ADM2 geometry count', indiaAdm2.size());
print('Sample ADM2 property names', ee.Feature(indiaAdm2.first()).propertyNames());
print('GFD total event count', GFD.size());
print('GFD first image band names', firstImage.bandNames());
print('GFD first image property names', firstImage.propertyNames());
print('GFD nominal scale: flooded', analysisScale);

var indiaByCountryCode = GFD.filter(ee.Filter.listContains('cc', 'IND'));
var indiaByCountryName = GFD.filter(ee.Filter.listContains('countries', 'India'));
var indiaByMetadata = indiaByCountryCode.merge(indiaByCountryName).distinct('id');
var indiaBySpatialIntersection = GFD.filterBounds(indiaGeometry);
var indiaEvents = indiaByMetadata.merge(indiaBySpatialIntersection).distinct('id')
  .sort('system:time_start');

print('India-filtered GFD event count by country code', indiaByCountryCode.size());
print('India-filtered GFD event count by country name', indiaByCountryName.size());
print('India-filtered GFD event count by metadata union', indiaByMetadata.size());
print('India-filtered GFD event count by spatial intersection', indiaBySpatialIntersection.size());
print('India-filtered GFD event count used', indiaEvents.size());
print('Earliest India-related event date',
  ee.Date(ee.Number(indiaEvents.aggregate_min('system:time_start'))).format('YYYY-MM-dd'));
print('Latest India-related event date',
  ee.Date(ee.Number(indiaEvents.aggregate_max('system:time_start'))).format('YYYY-MM-dd'));
print('India-related GFD event IDs', indiaEvents.aggregate_array('id'));

var boundaryExport = indiaAdm2.map(function(feat) {
  return ee.Feature(null, {
    boundary_shape_id: feat.get('shapeID'),
    boundary_district_name: feat.get('shapeName'),
    boundary_shape_type: feat.get('shapeType'),
    boundary_shape_group: feat.get('shapeGroup'),
    district_area_km2: feat.geometry().area(1).divide(1e6)
  });
});

var eventInventory = indiaEvents.map(function(img) {
  img = ee.Image(img);
  return ee.Feature(null)
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

function eventFloodMask(img) {
  img = ee.Image(img);
  return img.select('flooded').eq(1)
    .and(img.select('jrc_perm_water').neq(1))
    .selfMask()
    .rename('event_floodwater');
}

function numberOrZero(dict, key) {
  var value = ee.Dictionary(dict).get(key);
  return ee.Number(ee.Algorithms.If(value, value, 0));
}

function districtEventRows(img) {
  img = ee.Image(img);
  var floodMask = eventFloodMask(img);
  var eventAreaImage = floodMask.multiply(ee.Image.pixelArea()).rename('flooded_area_m2');
  var eventMeanImage = ee.Image.cat([
    img.select('duration').updateMask(floodMask).rename('duration'),
    img.select('clear_perc').updateMask(floodMask).rename('clear_perc')
  ]);

  return indiaAdm2.filterBounds(img.geometry()).map(function(feat) {
    var areaKm2 = feat.geometry().area(1).divide(1e6);
    var areaStats = eventAreaImage.reduceRegion({
      reducer: ee.Reducer.sum(),
      geometry: feat.geometry(),
      scale: analysisScale,
      maxPixels: 1e13,
      tileScale: 8
    });
    var meanStats = eventMeanImage.reduceRegion({
      reducer: ee.Reducer.mean(),
      geometry: feat.geometry(),
      scale: analysisScale,
      maxPixels: 1e13,
      tileScale: 8
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

function eventRowsForRange(startIndex, endIndex) {
  var eventList = indiaEvents.toList(indiaEvents.size()).slice(startIndex, endIndex);
  return ee.FeatureCollection(eventList.iterate(function(img, acc) {
    return ee.FeatureCollection(acc).merge(districtEventRows(ee.Image(img)));
  }, ee.FeatureCollection([])));
}

print('Boundary export sample', boundaryExport.limit(10));
print('Event inventory sample', eventInventory.limit(10));

Export.table.toDrive({
  collection: boundaryExport,
  description: 'gfd_india_adm2_boundaries',
  folder: 'gfd_external_validation',
  fileNamePrefix: 'gfd_india_adm2_boundaries',
  fileFormat: 'CSV'
});

Export.table.toDrive({
  collection: eventInventory,
  description: 'gfd_india_event_inventory',
  folder: 'gfd_external_validation',
  fileNamePrefix: 'gfd_india_event_inventory',
  fileFormat: 'CSV'
});

// Create twenty 10-event batches. Empty tail batches are harmless if the India
// event count is less than 200. Smaller batches are used to avoid Earth Engine
// memory errors during district-event reductions.

Export.table.toDrive({
  collection: eventRowsForRange(0, 10),
  description: 'gfd_india_district_event_metrics_part_00',
  folder: 'gfd_external_validation',
  fileNamePrefix: 'gfd_india_district_event_metrics_part_00',
  fileFormat: 'CSV'
});

Export.table.toDrive({
  collection: eventRowsForRange(10, 20),
  description: 'gfd_india_district_event_metrics_part_01',
  folder: 'gfd_external_validation',
  fileNamePrefix: 'gfd_india_district_event_metrics_part_01',
  fileFormat: 'CSV'
});

Export.table.toDrive({
  collection: eventRowsForRange(20, 30),
  description: 'gfd_india_district_event_metrics_part_02',
  folder: 'gfd_external_validation',
  fileNamePrefix: 'gfd_india_district_event_metrics_part_02',
  fileFormat: 'CSV'
});

Export.table.toDrive({
  collection: eventRowsForRange(30, 40),
  description: 'gfd_india_district_event_metrics_part_03',
  folder: 'gfd_external_validation',
  fileNamePrefix: 'gfd_india_district_event_metrics_part_03',
  fileFormat: 'CSV'
});

Export.table.toDrive({
  collection: eventRowsForRange(40, 50),
  description: 'gfd_india_district_event_metrics_part_04',
  folder: 'gfd_external_validation',
  fileNamePrefix: 'gfd_india_district_event_metrics_part_04',
  fileFormat: 'CSV'
});

Export.table.toDrive({
  collection: eventRowsForRange(50, 60),
  description: 'gfd_india_district_event_metrics_part_05',
  folder: 'gfd_external_validation',
  fileNamePrefix: 'gfd_india_district_event_metrics_part_05',
  fileFormat: 'CSV'
});

Export.table.toDrive({
  collection: eventRowsForRange(60, 70),
  description: 'gfd_india_district_event_metrics_part_06',
  folder: 'gfd_external_validation',
  fileNamePrefix: 'gfd_india_district_event_metrics_part_06',
  fileFormat: 'CSV'
});

Export.table.toDrive({
  collection: eventRowsForRange(70, 80),
  description: 'gfd_india_district_event_metrics_part_07',
  folder: 'gfd_external_validation',
  fileNamePrefix: 'gfd_india_district_event_metrics_part_07',
  fileFormat: 'CSV'
});

Export.table.toDrive({
  collection: eventRowsForRange(80, 90),
  description: 'gfd_india_district_event_metrics_part_08',
  folder: 'gfd_external_validation',
  fileNamePrefix: 'gfd_india_district_event_metrics_part_08',
  fileFormat: 'CSV'
});

Export.table.toDrive({
  collection: eventRowsForRange(90, 100),
  description: 'gfd_india_district_event_metrics_part_09',
  folder: 'gfd_external_validation',
  fileNamePrefix: 'gfd_india_district_event_metrics_part_09',
  fileFormat: 'CSV'
});

Export.table.toDrive({
  collection: eventRowsForRange(100, 110),
  description: 'gfd_india_district_event_metrics_part_10',
  folder: 'gfd_external_validation',
  fileNamePrefix: 'gfd_india_district_event_metrics_part_10',
  fileFormat: 'CSV'
});

Export.table.toDrive({
  collection: eventRowsForRange(110, 120),
  description: 'gfd_india_district_event_metrics_part_11',
  folder: 'gfd_external_validation',
  fileNamePrefix: 'gfd_india_district_event_metrics_part_11',
  fileFormat: 'CSV'
});

Export.table.toDrive({
  collection: eventRowsForRange(120, 130),
  description: 'gfd_india_district_event_metrics_part_12',
  folder: 'gfd_external_validation',
  fileNamePrefix: 'gfd_india_district_event_metrics_part_12',
  fileFormat: 'CSV'
});

Export.table.toDrive({
  collection: eventRowsForRange(130, 140),
  description: 'gfd_india_district_event_metrics_part_13',
  folder: 'gfd_external_validation',
  fileNamePrefix: 'gfd_india_district_event_metrics_part_13',
  fileFormat: 'CSV'
});

Export.table.toDrive({
  collection: eventRowsForRange(140, 150),
  description: 'gfd_india_district_event_metrics_part_14',
  folder: 'gfd_external_validation',
  fileNamePrefix: 'gfd_india_district_event_metrics_part_14',
  fileFormat: 'CSV'
});

Export.table.toDrive({
  collection: eventRowsForRange(150, 160),
  description: 'gfd_india_district_event_metrics_part_15',
  folder: 'gfd_external_validation',
  fileNamePrefix: 'gfd_india_district_event_metrics_part_15',
  fileFormat: 'CSV'
});

Export.table.toDrive({
  collection: eventRowsForRange(160, 170),
  description: 'gfd_india_district_event_metrics_part_16',
  folder: 'gfd_external_validation',
  fileNamePrefix: 'gfd_india_district_event_metrics_part_16',
  fileFormat: 'CSV'
});

Export.table.toDrive({
  collection: eventRowsForRange(170, 180),
  description: 'gfd_india_district_event_metrics_part_17',
  folder: 'gfd_external_validation',
  fileNamePrefix: 'gfd_india_district_event_metrics_part_17',
  fileFormat: 'CSV'
});

Export.table.toDrive({
  collection: eventRowsForRange(180, 190),
  description: 'gfd_india_district_event_metrics_part_18',
  folder: 'gfd_external_validation',
  fileNamePrefix: 'gfd_india_district_event_metrics_part_18',
  fileFormat: 'CSV'
});

Export.table.toDrive({
  collection: eventRowsForRange(190, 200),
  description: 'gfd_india_district_event_metrics_part_19',
  folder: 'gfd_external_validation',
  fileNamePrefix: 'gfd_india_district_event_metrics_part_19',
  fileFormat: 'CSV'
});
