/*global window, jQuery, google, dojo, esri, dijit*/

(function() {

  jQuery.geoevents = {
    select_point: 'geo-event-select-point',
    select_marker: 'geo-event-select-marker',
    map_loaded: 'geo-events-map-loaded',
    basket_loaded: 'geo-events-basket-loaded',
    basket_delete: 'geo-events-basket-delete',
    basket_save: 'geo-events-basket-save',
    basket_update: 'geo-events-basket-update',
    basket_cancel: 'geo-events-basket-cancel',
    ajax_start: 'geo-events-ajax-start',
    ajax_stop: 'geo-events-ajax-stop'
  };

// Convert google geocoder to geojson
  jQuery.google2geojson = function(googlejson) {
    var feature = {
      type: 'Feature',
      bbox: [],
      geometry: {
        type: 'Point',
        coordinates: []
      },
      properties: {
        name: '',
        title: '',
        description: '',
        tags: '',
        center: [],
        other: googlejson
      }
    };
    feature.properties.title = googlejson.address_components[0].long_name;
    feature.properties.description = googlejson.formatted_address;
    feature.properties.tags = googlejson.types;

    // Geometry
    feature.properties.center = [
      googlejson.geometry.location.lat(),
      googlejson.geometry.location.lng()
    ];

    var bounds = googlejson.geometry.bounds;
    var type = 'Point';
    if (bounds) {
      type = 'Polygon';
    } else {
      bounds = googlejson.geometry.viewport;
    }
    feature.geometry.type = type;

    var ne = bounds.getNorthEast();
    var sw = bounds.getSouthWest();
    if (type === 'Polygon') {
      feature.geometry.coordinates = [
        [sw.lat(), sw.lng()],
        [sw.lat(), ne.lng()],
        [ne.lat(), ne.lng()],
        [ne.lat(), sw.lng()]
      ];
    } else {
      feature.geometry.type = 'Point';
      feature.geometry.coordinates = [
        googlejson.geometry.location.lat(),
        googlejson.geometry.location.lng()
      ];
    }

    feature.bbox = [sw.lat(), sw.lng(), ne.lat(), ne.lng()];
    return feature;
  };

  /* Geolocator dialog jQuery plugin */
  jQuery.fn.geodialog = function(settings) {
    var self = this;
    self.initialized = false;
    self.events = {
      initialize: 'geo-dialog-initialize',
      save: 'geo-dialog-save',
      cancel: 'geo-dialog-cancel'
    };

    self.options = {
      template: '',
      width: jQuery(window).width() * 0.85,
      height: jQuery(window).height() * 0.95,

      sidebar: {
        json: '',
        template: '',
        suggestions: '',
        fieldName: self.attr('id'),
        tabs: {
          search: {},
          advanced: {}
        }
      },

      map: {
        json: '',
        fieldName: self.attr('id')
      },

      basket: {
        json: '',
        template: '',
        fieldName: self.attr('id'),
        geojson: {
          type: 'FeatureCollection',
          features: []
        }
      },

      // Handlers
      handle_leftbutton_dblclick: function(button, area) {
        var width = self.leftarea.width();
        var max_width = 300;
        var min_width = 0;
        if (width < 20) {
          area.trigger('resize', [max_width]);
          jQuery('a', self.leftbutton).html('&laquo;');
        } else {
          area.trigger('resize', [min_width]);
          jQuery('a', self.leftbutton).html('&raquo;');
        }
      },

      handle_rightbutton_dblclick: function(button, area) {
        var width = self.rightarea.width();
        var min_width = area.width();
        var max_width = parseInt(3 * area.width() / 4, 10);

        if (width < 20) {
          area.trigger('resize', [max_width]);
          jQuery('a', self.rightbutton).html('&raquo;');
        } else {
          area.trigger('resize', [min_width]);
          jQuery('a', self.rightbutton).html('&laquo;');
        }
      },

      handle_initialize: function() {
        if (self.initialized) {
          // Already initialized
          return;
        }

        // Splitter
        jQuery.get(self.options.template, function(data) {
          var $data = jQuery(data);
          self.empty();
          self.append($data);

          // Left splitter
          var left = jQuery('.geo-leftside', self);
          left.splitter({
            type: 'v',
            outline: true,
            accessKey: "L"
          });

          self.leftarea = jQuery('.geo-left', left);
          self.leftbutton = jQuery('.vsplitbar', left);
          jQuery('a', self.leftbutton).html('&raquo;');

          jQuery('a', self.leftbutton).click(function() {
            self.options.handle_leftbutton_dblclick(self.leftbutton, left);
          });

          self.leftbutton.dblclick(function() {
            self.options.handle_leftbutton_dblclick(self.leftbutton, left);
          });

          // Right splitter
          var right = jQuery('.geo-splitter', self);
          right.splitter({
            type: 'v',
            outline: true,
            sizeRight: 0,
            accessKey: "R"
          });

          self.rightarea = jQuery('.geo-right', right);
          self.rightbutton = jQuery(jQuery('.vsplitbar', right)[1]);
          jQuery('a', self.rightbutton).html('&laquo;');

          jQuery('a', self.rightbutton).click(function() {
            self.options.handle_rightbutton_dblclick(self.rightbutton, right);
          });

          self.rightbutton.dblclick(function() {
            self.options.handle_rightbutton_dblclick(self.rightbutton, right);
          });

          // Sidebar
          self.sidebar = jQuery('.geo-sidebar', self);
          self.sidebar.geosidebar(self.options.sidebar);

          // Map
          self.mapcanvas = jQuery('.geo-map', self);
          self.mapcanvas.geomap(self.options.map);

          // Basket
          self.basket = jQuery('.geo-basket', self);
          self.options.basket.origJSON = jQuery.extend({}, self.options.basket.geojson);
          self.basket.geobasket(self.options.basket);

        });

        // Plugin initialized
        self.initialized = true;
      },

      handle_map_loaded: function() {
        jQuery('a', self.leftbutton).click();
        jQuery('a', self.rightbutton).click();
      },

      handle_save: function() {
        var fieldName = self.attr('id');
        var json = self.basket.options.geojson;
        // sort the geotags by name before sending it to object annotation
        json.features = json.features.sort(function(a, b) {
          var aName = a.properties.title.toLowerCase();
          var bName = b.properties.title.toLowerCase();
          return ((aName < bName) ? -1 : ((aName > bName) ? 1 : 0));
        });

        self.trigger(jQuery.geoevents.basket_save, {json: json});
        self.trigger(jQuery.geoevents.basket_update, {json: json});
        json = JSON.stringify(json);
        jQuery('[name=' + fieldName + ']').text(json);
      },

      initialize: function() {
        self.dialog({
          bgiframe: true,
          modal: true,
          closeOnEscape: false,
          autoOpen: false,
          width: self.options.width,
          height: self.options.height,
          resize: true,
          dialogClass: 'eea-geotags-popup',
          buttons: {
            'Save geotags': function() {
              self.dialog('close');
              self.trigger(self.events.save);
            },
            'Cancel': function() {
              self.dialog('close');
              self.trigger(self.events.cancel);
            }
          },
          close: function(e) {
            if (e.currentTarget) {
              self.trigger(self.events.cancel);
            }
          },
          open: function() {
            self.trigger(self.events.initialize);
          }
        });

        // Bind events
        self.bind(self.events.initialize, function(evt, data) {
          self.options.handle_initialize(data);
        });

        self.bind(self.events.save, function(evt, data) {
          self.options.handle_save(data);
        });

        self.bind(self.events.cancel, function() {
          jQuery(self).trigger(jQuery.geoevents.basket_cancel);
        });

        jQuery(self).bind(jQuery.geoevents.map_loaded, function(data) {
          self.options.handle_map_loaded(data);
        });
      }
    };

    // Update settings
    if (settings) {
      jQuery.extend(self.options, settings);
    }

    self.options.initialize();
    return this;
  };

  /* Geo Map Canvas jQuery plugin */
  jQuery.fn.geomap = function(settings) {
    var self = this;

    self.options = {
      json: '',
      fieldName: '',
      map_options: {
        latitude: 55,
        longitude: 35,
        center: null,
        zoom: 4,
        navigationControl: true,
        navigationControlOptions: {
          style: google.maps.NavigationControlStyle.ZOOM_PAN,
          position: google.maps.ControlPosition.RIGHT
        },
        mapTypeControl: true,
        mapTypeControlOptions: {
          position: google.maps.ControlPosition.TOP_RIGHT,
          style: google.maps.MapTypeControlStyle.DEFAULT
        },
        mapTypeId: google.maps.MapTypeId.TERRAIN
      },

      // Handlers
      handle_select: function(data, autoclick) {
        if (!data) {
          return;
        }

        if (data.bbox.length) {
          var lat = data.bbox[0];
          var lng = data.bbox[1];
          var sw = new google.maps.LatLng(lat, lng);

          lat = data.bbox[2];
          lng = data.bbox[3];
          var ne = new google.maps.LatLng(lat, lng);

          var viewport = new google.maps.LatLngBounds(sw, ne);
          self.Map.fitBounds(viewport);
        } else {
          self.Map.setZoom(4);
        }

        // Marker
        jQuery.geomarker({
          fieldName: self.options.fieldName,
          map: self.Map,
          points: [data],
          center: data.properties.center,
          autoclick: autoclick
        });
      },

      handle_rightclick: function(data, center) {
        // Markers
        jQuery.geomarker({
          fieldName: self.options.fieldName,
          map: self.Map,
          points: data.features,
          center: center
        });
      },

      initialize: function() {
        self.initialized = false;
        self.addClass('geo-mapcanvas');
        var options = self.options.map_options;
        if (!options.latlng) {
          options.center = new google.maps.LatLng(
            options.latitude,
            options.longitude
          );
        }

        self.Map = new google.maps.Map(self[0], options);

        self.Geocoder = new google.maps.Geocoder();

        // Handle events
        var context = jQuery('#' + self.options.fieldName);
        jQuery(context).bind(jQuery.geoevents.select_point, function(evt, data) {
          data.target.effect('transfer', {to: self}, 'slow', function() {
            self.options.handle_select(data.point, data.autoclick);
          });
        });

        // Map initialized
        google.maps.event.addListener(self.Map, 'tilesloaded', function() {
          if (self.initialized) {
            return;
          }
          self.initialized = true;
          jQuery(context).trigger(jQuery.geoevents.map_loaded);
        });

        // Right click
        google.maps.event.addListener(self.Map, 'rightclick', function(data) {
          var latlng = data.latLng;
          var center = [latlng.lat(), latlng.lng()];

          // Empty marker to clear map
          jQuery.geomarker({
            fieldName: self.options.fieldName,
            map: self.Map,
            center: center,
            points: []
          });

          jQuery(context).trigger(jQuery.geoevents.ajax_start);
          self.Geocoder.geocode({location: latlng}, function(results) {
            var features = [];
            jQuery.each(results, function() {
              features.push(jQuery.google2geojson(this));
            });

            var results_obj = {
              type: 'FeatureCollection',
              features: features
            };

            self.options.handle_rightclick(results_obj, center);
            jQuery(context).trigger(jQuery.geoevents.ajax_stop);
          });
        });
      }
    };

    if (settings) {
      jQuery.extend(self.options, settings);
    }

    // Return
    self.options.initialize();
    return this;
  };

  jQuery.geomarker = function(settings) {
    var self = this;

    self.options = {
      fieldName: '',
      template: '<div class="geo-marker">' +
        '<h3 class="title"></h3>' +
        '<h4 class="subtitle"></h4>' +
        '<h5 class="tags"></h5>' +
        '</div>',
      map: null,
      points: [],
      center: [0, 0],
      autoclick: false,

      initialize: function() {
        self.options.clear();
        self.mappoints = {};

        // Marker
        var center = self.options.center;
        var latlng = new google.maps.LatLng(center[0], center[1]);
        self.marker = new google.maps.Marker({
          position: latlng
        });
        self.marker.setMap(self.options.map);

        // InfoWindow
        var template = jQuery('<div>');
        jQuery.each(self.options.points, function() {
          var point = this;
          var uid = point.properties.center[0] + '-' + point.properties.center[1];
          self.mappoints[uid] = point;

          var title = this.properties.title;
          var subtitle = this.properties.description;
          var tags = '';
          if (typeof(this.properties.tags) === 'string') {
            tags = this.properties.tags;
          } else {
            jQuery.each(this.properties.tags, function() {
              tags += this + ', ';
            });
          }

          var itemplate = jQuery(self.options.template);
          itemplate.attr('id', uid).attr('title', 'Add');
          var icon = jQuery('<div>')
            .addClass('ui-icon')
            .addClass('ui-icon-extlink')
            .text('+');
          itemplate.prepend(icon);
          jQuery('.title', itemplate).text(title);
          jQuery('.subtitle', itemplate).text(subtitle);
          jQuery('.tags', itemplate).text(tags);

          template.append(itemplate);
        });

        var context = jQuery('#' + self.options.fieldName);
        if (self.options.points.length) {
          // Add info window
          self.info = new google.maps.InfoWindow({
            content: template.html()
          });

          self.info.open(self.options.map, self.marker);
          google.maps.event.addListener(self.info, 'domready', function() {
            var $geo_marker = jQuery('.geo-marker');
            $geo_marker.click(function() {
              var _self = jQuery(this);
              jQuery(context).trigger(jQuery.geoevents.select_marker, {
                point: self.mappoints[_self.attr('id')],
                button: _self
              });
            });

            // Autoclick
            if (self.options.autoclick) {
              $geo_marker.click();
            }
          });

          // Google event handlers
          google.maps.event.addListener(self.marker, 'click', function() {
            self.info.open(self.options.map, self.marker);
          });
        }
      },

      clear: function() {
        if (self.marker) {
          self.marker.setMap(null);
        }
        if (self.info) {
          self.info.close();
        }
      }
    };

    if (settings) {
      jQuery.extend(self.options, settings);
    }

    self.options.initialize();
    return this;
  };

  /* Geo basket jQuery plugin */
  jQuery.fn.geobasket = function(settings) {
    var self = this;

    self.options = {
      json: '',
      template: '',
      fieldName: '',
      multiline: 1,
      geojson: {
        type: 'FeatureCollection',
        features: []
      },

      initialize: function() {
        var query = {};
        query.fieldName = self.options.fieldName;
        jQuery.get(self.options.template, query, function(data) {
          self.html(data);
          self.options.redraw(false);
          jQuery(context).trigger(jQuery.geoevents.basket_loaded, self);

        });

        var context = jQuery('#' + self.options.fieldName);
        jQuery(context).bind(jQuery.geoevents.select_marker, function(evt, data) {
          data.button.effect('transfer', {to: self}, 'slow', function() {
            self.options.handle_select(data.point);
          });
        });

        jQuery(context).bind(jQuery.geoevents.basket_loaded, function(evt) {
          self.options.handle_loaded(evt);
        });

        jQuery(context).bind(jQuery.geoevents.basket_cancel, function(evt) {
          self.options.handle_cancel(evt);
        });

        jQuery(context).bind(jQuery.geoevents.basket_update, function(evt, data) {
          self.options.handle_update(data);
        });

        jQuery(context).bind(jQuery.geoevents.basket_delete, function(evt, data) {
          data.element.slideUp(function() {
            jQuery(this).remove();
            self.options.handle_delete(data.point);
          });
        });
      },

      handle_loaded: function() {
        var geobasket_clear = jQuery('.geo-basket-clear', self);
        geobasket_clear.find('.ui-icon-trash').click(function() {
          var items = jQuery('.geo-basket-items', self);
          items.find('.ui-icon-trash').click();
        });
      },

      handle_delete: function(point) {
        var pcenter = point.properties.center;
        pcenter = pcenter[0] + '-' + pcenter[1];
        self.options.geojson.features = jQuery.map(self.options.geojson.features,
          function(feature) {
            var center = feature.properties.center;
            center = center[0] + '-' + center[1];
            if (pcenter !== center) {
              return feature;
            }
          });
      },

      handle_cancel: function() {
        if (self.options.origJSON.features) {
          self.options.geojson = jQuery.extend({}, self.options.origJSON);
          self.options.redraw();
        }
        else {
          self.options.geojson.features = [];
          self.options.redraw();
        }
      },

      handle_update: function(data) {
        self.options.origJSON = jQuery.extend({}, data.json);
      },

      handle_select: function(point) {
        var i, eea_geotags = window.EEAGeotags,
          initialData = eea_geotags.initialCountryData,
          initialData_length, names, features_length;
        if (!self.options.multiline) {
          self.options.geojson.features = [];
        } else {
          self.options.handle_delete(point);
        }

        if (point.properties.countries && eea_geotags.shouldExpandCountryGroups) {
          names = [];
          // add also the individual countries that are part of this country group
          initialData_length = initialData.features.length;

          features_length = self.options.geojson.features.length;
          // collect the names so that we can have a property to check upon for
          // points that are already added
          for (i = 0; i < features_length; i += 1) {
            names.push(self.options.geojson.features[i].properties.name);
          }
          for (i = 0; i < initialData_length; i += 1) {
            // add only the countries that are not already in the list by checking
            // their geotags name
            if (jQuery.inArray(initialData.features[i].properties.name, names) === -1) {
              self.options.geojson.features.unshift(initialData.features[i]);
            }
          }
        }
        else {
          self.options.geojson.features.unshift(point);
        }
        self.options.redraw(true);
      },

      redraw: function(highlight) {
        var items = jQuery('.geo-basket-items', self);
        items.empty();

        jQuery.each(self.options.geojson.features, function() {
          var div = jQuery('<div>');
          items.append(div);
          div.geobasketitem({
            fieldName: self.options.fieldName,
            point: this
          });
        });

        if (highlight) {
          var first = jQuery('.geo-point-view:first', items);
          first.addClass('ui-pulsate-item');
          first.effect('pulsate', {}, 200, function() {
            first.removeClass('ui-pulsate-item');
          });
        }
      }
    };

    if (settings) {
      jQuery.extend(self.options, settings);
    }

    // Return
    self.options.initialize();
    return this;
  };

  /* Geo basket item */
  jQuery.fn.geobasketitem = function(settings) {
    var self = this;
    self.options = {
      fieldName: '',
      template: '<div>' +
        '<h3 class="title"></h3>' +
        '<h4 class="subtitle"></h4>' +
        '<h5 class="tags"></h5>' +
        '</div>',
      point: {},

      // Methods
      initialize: function() {
        self.addClass('geo-point-view');
        self.delbutton = jQuery('<div>')
          .addClass('ui-icon')
          .addClass(' ui-icon-trash')
          .text('X')
          .attr('title', 'Delete');
        self.prepend(self.delbutton);

        var context = jQuery('#' + self.options.fieldName);
        self.delbutton.click(function() {
          jQuery(context).trigger(jQuery.geoevents.basket_delete, {
            point: self.options.point,
            element: self
          });
        });

        var title = self.options.point.properties.title;
        var subtitle = self.options.point.properties.description;
        var tags = '';
        if (typeof(self.options.point.properties.tags) === 'string') {
          tags = self.options.point.properties.tags;
        } else {
          jQuery.each(self.options.point.properties.tags, function() {
            tags += this + ', ';
          });
        }

        var template = jQuery(self.options.template);
        jQuery('.title', template).text(title);
        jQuery('.subtitle', template).text(subtitle);
        jQuery('.tags', template).text(tags);

        self.append(template);
      }
    };

    if (settings) {
      jQuery.extend(self.options, settings);
    }

    self.options.initialize();
    return this;
  };

  /* Geo Side bar jQuery plugin */
  jQuery.fn.geosidebar = function(settings) {
    var self = this;
    self.options = {
      json: '',
      template: '',
      suggestions: '',
      fieldName: '',
      tabs: {
        search: {},
        advanced: {}
      },

      // Methods
      initialize: function() {
        var query = {};
        query.fieldName = self.options.fieldName;
        jQuery.get(self.options.template, query, function(data) {
          self.sidebararea = jQuery(data);

          self.loading = jQuery('<div>');
          self.sidebararea.append(self.loading);
          self.loading.geoloader({
            fieldName: self.options.fieldName
          });

          self.append(self.sidebararea);

          var options = self.options.tabs;
          options.json = self.options.json;
          options.fieldName = self.options.fieldName;
          options.suggestions = self.options.suggestions;
          self.sidebararea.geotabs(options);
        });
      }

    };

    if (settings) {
      jQuery.extend(self.options, settings);
    }

    self.options.initialize();
    return this;
  };

  jQuery.fn.geoloader = function(settings) {
    var self = this;
    self.working = 0;

    self.options = {
      fieldName: '',

      initialize: function() {
        self.addClass('geo-loading');
        self.hide();

        var context = jQuery('#' + self.options.fieldName);
        self.ajaxStart(function() {
          jQuery(context).trigger(jQuery.geoevents.ajax_start);
        });

        self.ajaxStop(function() {
          jQuery(context).trigger(jQuery.geoevents.ajax_stop);

        });

        jQuery(context).bind(jQuery.geoevents.ajax_start, function() {
          self.show();
        });

        jQuery(context).bind(jQuery.geoevents.ajax_stop, function() {
          self.hide();
        });
      },

      show: function() {
        self.working += 1;
        if (self.working > 0) {
          self.show();
        }
      },

      hide: function() {
        self.working -= 1;
        if (!self.working) {
          self.hide();
        }
      }
    };


    if (settings) {
      jQuery.extend(self.options, settings);
    }

    self.options.initialize();
    return this;
  };

  /* Geo tabs jQuery plugin */
  jQuery.fn.geotabs = function(settings) {
    var self = this;

    self.options = {
      json: '',
      fieldName: '',
      suggestions: '',
      search: {},
      advanced: {},

      // Methods
      initialize: function() {
        var $geo_panes, $icons;
        if (window.EEA) {
          if (window.EEA.eea_accordion) {
            window.EEA.eea_accordion(jQuery('.eea-accordion-panels', self));
          }
        }
        else {
          $geo_panes = jQuery('.geo-panes', self);
          $icons = $geo_panes.find('.eea-icon').addClass('ui-icon ui-icon-carat-1-e');
          $icons.eq(0).removeClass('ui-icon-carat-1-e')
            .addClass('ui-icon-carat-1-s');
          $geo_panes.find('h2').click(function() {
            var $this = $(this);
            $icons.removeClass('ui-icon-carat-1-s ui-icon-carat-1-e')
              .addClass('ui-icon-carat-1-e');
            $this.find('.eea-icon')
              .removeClass('ui-icon-carat-1-e')
              .addClass('ui-icon-carat-1-s');
          });
          $geo_panes.tabs('.geo-pane', {tabs: 'h2', effect: 'slide'});
        }
        var options = self.options.search;
        options.json = self.options.json;
        options.fieldName = self.options.fieldName;
        options.suggestions = self.options.suggestions;
        jQuery('.geo-results', self).geosearchtab(options);

        options = self.options.advanced;
        options.json = self.options.json;
        options.fieldName = self.options.fieldName;
        jQuery('.geo-advanced', self).geoadvancedtab(options);

      }
    };

    if (settings) {
      jQuery.extend(self.options, settings);
    }

    self.options.initialize();
    return this;
  };

  /* Geo search tab jQuery plugin */
  jQuery.fn.geosearchtab = function(settings) {
    var self = this;

    // Default settings
    self.options = {
      // Settings
      fieldName: '',
      json: '',
      suggestions: '',
      query: {
        address: '',
        q: '',
        country: '',
        featureClass: '',
        continentCode: '',
        maxRows: 10
      },

      handle_suggestions: function(data) {
        var suggestions = data.suggestions;

        if (!suggestions.length) {
          return;
        }

        var htitle = jQuery('<h5>').text('Suggestions').addClass('geo-suggestions');
        self.resultsarea.append(htitle);

        var context = jQuery('#' + self.options.fieldName);

        jQuery.each(suggestions, function() {
          self.options.query.address = this.text;
          jQuery(context).trigger(jQuery.geoevents.ajax_start);
          var xquery = {'address': this.text};
          self.Geocoder.geocode(xquery, function(data) {
            var features = [];
            jQuery.each(data, function() {
              features.push(jQuery.google2geojson(this));
            });

            var geojson = {
              type: 'FeatureCollection',
              features: features
            };

            self.options.handle_query(geojson, false);
            jQuery(context).trigger(jQuery.geoevents.ajax_stop);
          });
        });
      },

      // Handlers
      handle_submit: function() {
        self.searchbutton.removeClass('submitting');

        var value = self.searchtext.val();
        if (!value) {
          return;
        }
        self.options.query.address = value;
        self.options.query.q = value;
        self.options.query.country = self.search_country.val();
        self.options.query.featureClass = self.search_feature_class.val();
        self.options.query.continentCode = self.search_continent_code.val();
        var query = self.options.query;

        var context = jQuery('#' + self.options.fieldName);
        jQuery(context).trigger(jQuery.geoevents.ajax_start);

        // Search with geonames.org
        jQuery.getJSON(self.options.json, query, function(data) {
          if (data.features.length) {
            self.options.handle_query(data, true);
            jQuery(context).trigger(jQuery.geoevents.ajax_stop);
            jQuery(".missing-geonames-results").addClass('visualHidden');
          } else {
            // Search with Google
            var xquery = {address: query.address};
            self.Geocoder.geocode(xquery, function(data) {
              var features = [];
              jQuery.each(data, function() {
                features.push(jQuery.google2geojson(this));
              });

              var data_obj = {
                type: 'FeatureCollection',
                features: features
              };

              self.options.handle_query(data_obj, true);
              jQuery(context).trigger(jQuery.geoevents.ajax_stop);
              jQuery(".missing-geonames-results").removeClass('visualHidden');
            });
          }
        });
      },

      handle_query: function(data, reset) {
        self.results = data;
        self.fclasses = [
          ['All', 'all feature classes']
        ];
        if (reset) {
          self.resultsarea.empty();
          self.filters_ctl.empty();

          if (!self.results.features.length) {
            var div = jQuery('<div>').addClass('geo-hints');
            div.text('We could not find a match for this location anywhere. ' +
              'Please check your spelling or try looking for a different location.');
            self.resultsarea.append(div);
            return;
          }
        }

        jQuery.each(self.results.features, function() {
          var div = jQuery('<div>', {'data-fclass': this.properties.other.fcl});
          div.geopointview({
            fieldName: self.options.fieldName,
            point: this
          });
          self.resultsarea.append(div);

          var fcl = this.properties.other.fcl;
          var fclName = this.properties.other.fclName;
          var filter = [fcl, fclName];
          var unique = true;

          for (var i = 0; i < self.fclasses.length; i++) {
            if (self.fclasses[i].toString() === filter.toString()) {
              unique = false;
            }
          }

          // the results are from google and we don't have any fcl or fclName property
          if (!fcl || !fclName) {
            unique = false;
          }

          if (unique === true) {
            self.fclasses.push(filter);
          }
        });

        self.resultsarea.geo_points_divs = self.resultsarea.find(".geo-point-view");
        jQuery.each(self.fclasses, function() {
          self.options.addFilters(this);
        });
        self.options.toggle_filters_area_visibility();
      },

      toggle_filters_area_visibility: function() {

        self.fcl_filters.toggle(function() {
          self.filters_ctl.slideDown('fast');
          self.slide_ui_icons("down");
        }, function() {
          self.filters_ctl.slideUp('fast');
          self.slide_ui_icons("up");
        });
        self.fcl_filters.show();
      },

      // Add filter checkbox
      addFilters: function(filter) {
        var parent_container = self.filters_ctl;
        var container = jQuery('<p></p>');
        var checkbox = jQuery('<input />', {
          type: 'radio', id: 'fcl-' + filter[0],
          value: filter[1],
          name: 'feature-class',
          checked: 'checked' ? filter[0] === 'All' : ''
        }).appendTo(container);
        jQuery('<label />', {'for': 'fcl-' + filter[0], text: filter[1]}).appendTo(container);
        container.appendTo(parent_container);

        checkbox.on('change', function() {
          self.resultsarea.geo_points_divs.hide();

          var fcl_id = this.id;
          var fcl = fcl_id.substr(4);
          if (fcl === 'All') {
            self.resultsarea.geo_points_divs.show();
          } else {
            self.resultsarea.geo_points_divs.filter(function() {
              return this.getAttribute('data-fclass') === fcl;
            }).show();
          }

        });
      },

      init_ui_icons: function(context) {
        var icon_right, icon_down;
        var slide_icon = $(context).find('.eea-icon');

        if (window.EEA) {
          icon_right = 'eea-icon eea-icon-chevron-right';
          icon_down = 'eea-icon eea-icon-chevron-down';
        }
        else {
          icon_right = 'ui-icon ui-icon-carat-1-e';
          icon_down = 'ui-icon ui-icon-carat-1-s';
          slide_icon.addClass(icon_right);
        }

        return function(direction) {
          if (direction === "down") {
            slide_icon.removeClass(icon_right).addClass(icon_down);
          }
          else {
            slide_icon.removeClass(icon_down).addClass(icon_right);
          }
        };
      },
      // Initialize
      initialize: function() {
        self.searchform = jQuery('form', self);
        self.searchbutton = jQuery('input[type=submit]', self.searchform);
        self.searchtext = jQuery('input[type=text]', self.searchform);
        self.search_country = jQuery('[name="country"]', self.searchform);
        self.search_feature_class = jQuery('[name="featureClass"]', self.searchform);
        self.search_continent_code = jQuery('[name="continentCode"]', self.searchform);
        self.resultsarea = jQuery('.geo-results-area', self);
        self.filters_area = jQuery('.filters-area', self);
        self.filters_ctl = self.filters_area.find('.filters-ctl');
        self.fcl_filters = self.filters_area.find('#toggle-fcl-filters');
        self.slide_ui_icons = self.options.init_ui_icons(self.filters_area);
        self.Geocoder = new google.maps.Geocoder();

        // Handle suggestions
        if (self.options.suggestions.length) {
          jQuery.getJSON(self.options.suggestions, {}, function(data) {
            self.options.handle_suggestions(data);
          });
        }

        self.searchform.submit(function(ev) {
          self.options.handle_submit();
          ev.preventDefault();
        });

      }
    };

    // Update settings
    if (settings) {
      jQuery.extend(self.options, settings);
    }

    self.options.initialize();
    return this;
  };

  /* Geo point view jQuery plugin */
  jQuery.fn.geopointview = function(settings) {
    var self = this;
    self.options = {
      fieldName: '',
      template: '<div>' +
        '<h3 class="title"></h3>' +
        '<h4 class="subtitle"></h4>' +
        '<h5 class="tags"></h5>' +
        '</div>',
      point: {},

      // Methods
      initialize: function() {
        self.addClass('geo-point-view').attr('title', 'See on map');
        var icon = jQuery('<div>')
          .addClass('ui-icon')
          .addClass('ui-icon-extlink')
          .text('+');
        self.prepend(icon);

        var title = self.options.point.properties.title;
        var subtitle = self.options.point.properties.description;
        var tags = '';
        if (typeof(self.options.point.properties.tags) === 'string') {
          tags = self.options.point.properties.tags;
        } else {
          jQuery.each(self.options.point.properties.tags, function() {
            tags += this + ', ';
          });
        }

        var template = jQuery(self.options.template);
        jQuery('.title', template).text(title);
        jQuery('.subtitle', template).text(subtitle);
        jQuery('.tags', template).text(tags);

        self.append(template);

        var context = jQuery('#' + self.options.fieldName);
        self.click(function() {
          jQuery(context).trigger(jQuery.geoevents.select_point, {
            point: self.options.point,
            target: self,
            autoclick: true
          });
        });
      }

    };

    if (settings) {
      jQuery.extend(self.options, settings);
    }

    // Return
    self.options.initialize();
    return this;
  };

  /* Geo advanced tab jQuery plugin */
  jQuery.fn.geoadvancedtab = function(settings) {
    var self = this;
    self.options = {
      fieldName: '',
      json: '',

      // Methods
      handle_biogroups_change: function() {
        var value = self.biogroups.val();

        if (!value) {
          return;
        }

        var value_json = {};
        jQuery.each(self.biogroups.geojson.features, function() {
          if (this.properties.name === value) {
            value_json = this;
            return false;
          }
          return true;
        });

        var context = jQuery('#' + self.options.fieldName);
        jQuery(context).trigger(jQuery.geoevents.select_point, {
          point: value_json,
          target: self.biogroups
        });
      },

      handle_groups_change_reset: function() {
        self.countries.empty().parent().hide();
        self.nuts.empty().parent().hide();
        self.cities.empty().parent().hide();
        self.naturalfeatures.empty().parent().hide();
      },

      handle_groups_change: function() {
        self.options.handle_groups_change_reset();

        var value = self.groups.val();
        if (!value) {
          return;
        }

        var value_json = {};
        jQuery.each(self.data.features, function() {
          if (this.properties.name === value) {
            value_json = this;
            return false;
          }
          return true;
        });

        var context = jQuery('#' + self.options.fieldName);

        // Get countries
        jQuery.getJSON(self.options.json, {
          type: 'countries', group: value}, function(data) {
          // save initial country data to be used when adding country groups
          window.EEAGeotags.initialCountryData = data;

          self.countries.empty();
          var option = jQuery('<option>').val('').text('');
          self.countries.append(option);

          jQuery.each(data.features, function(index) {
            // Center map on second country in group
            if (index === 1) {
              value_json.properties.center = this.properties.center;
              jQuery(context).trigger(jQuery.geoevents.select_point, {
                point: value_json,
                target: self.groups
              });
            }
            // Add countries to datamodel
            if (value_json.properties.countries === undefined) {
              value_json.properties.countries = [];
            }
            value_json.properties.countries.push(this.properties.title);

            option = jQuery('<option>')
              .val(this.properties.name)
              .text(this.properties.title)
              .data('geojson', this);
            self.countries.append(option);
          });

          self.countries.parent().show();
        });
      },

      handle_countries_change_reset: function() {
        self.nuts.empty().parent().hide();
        self.cities.empty().parent().hide();
        self.naturalfeatures.empty().parent().hide();
      },

      handle_countries_change: function() {
        self.options.handle_countries_change_reset();

        var country = jQuery('option:selected', self.countries);

        if (!country.length) {
          return;
        }

        // Center map
        var query = {
          address: country.data('geojson').properties.title,
          region: country.data('geojson').properties.country
        };

        var context = jQuery('#' + self.options.fieldName);
        self.Geocoder.geocode(query, function(data) {
          if (!data.length) {
            return;
          }

          var data_point = jQuery.google2geojson(data[0]);
          jQuery(context).trigger(jQuery.geoevents.select_point, {
            point: data_point,
            target: self.countries
          });
        });
        // Get nut regions
        jQuery.getJSON(self.options.json, {
          type: 'nuts', country: query.region}, function(data) {
          self.nuts.empty();
          var option = jQuery('<option>').val('').text('');
          self.nuts.append(option);
          jQuery.each(data.features, function() {
            option = jQuery('<option>')
              .val(this.properties.name)
              .text(this.properties.title)
              .data('geojson', this);
            self.nuts.append(option);
          });
          self.nuts.parent().show();
        });

        // Get natural features
        jQuery.getJSON(self.options.json, {
          type: 'natural', country: query.region}, function(data) {
          self.naturalfeatures.empty();
          var option = jQuery('<option>').val('').text('');
          self.naturalfeatures.append(option);
          jQuery.each(data.features, function() {
            option = jQuery('<option>')
              .val(this.properties.name)
              .text(this.properties.title)
              .data('geojson', this);
            self.naturalfeatures.append(option);
          });
          self.naturalfeatures.parent().show();
        });

      },

      handle_nuts_change_reset: function() {
        self.cities.empty().parent().hide();
      },

      handle_nuts_change: function() {
        self.options.handle_nuts_change_reset();

        var nut = jQuery('option:selected', self.nuts);
        if (!nut.length) {
          return;
        }
        var geoinfo = nut.data('geojson').properties;
        var query = {
          address: geoinfo.adminName1,
          region: geoinfo.country,
          // #19495 we need to set a component restriction
          // to the country of the point otherwise google
          // maps will select Capital Region from Canada
          // when we had Denmark selected
          componentRestrictions: {
            country: geoinfo.country
          }
        };

        var context = jQuery('#' + self.options.fieldName);
        // Center map
        self.Geocoder.geocode(query, function(data) {
          if (!data.length) {
            return;
          }

          var data_point = jQuery.google2geojson(data[0]);
          jQuery(context).trigger(jQuery.geoevents.select_point, {
            point: data_point,
            target: self.nuts
          });
        });

        // Get cities
        var req = {
          type: 'cities',
          country: query.region,
          adminCode1: nut.data('geojson').properties.adminCode1
        };

        jQuery.getJSON(self.options.json, req, function(data) {
          self.cities.empty();
          var option = jQuery('<option>').val('').text('');
          self.cities.append(option);
          jQuery.each(data.features, function() {
            option = jQuery('<option>')
              .val(this.properties.name)
              .text(this.properties.title)
              .data('geojson', this);
            self.cities.append(option);
          });
          self.cities.parent().show();
        });

        //. Get natural features
        var req_natural = {
          type: 'natural',
          country: req.country,
          adminCode1: req.adminCode1
        };

        jQuery.getJSON(self.options.json, req_natural, function(data) {
          self.naturalfeatures.empty();
          var option = jQuery('<option>').val('').text('');
          self.naturalfeatures.append(option);
          jQuery.each(data.features, function() {
            option = jQuery('<option>')
              .val(this.properties.name)
              .text(this.properties.title)
              .data('geojson', this);
            self.naturalfeatures.append(option);
          });
          self.naturalfeatures.parent().show();
        });

      },

      handle_cities_change: function() {
        var city = jQuery('option:selected', self.cities);
        if (!city.length) {
          return;
        }

        // Center map
        var query = {
          address: city.data('geojson').properties.title + ', ' +
            city.data('geojson').properties.adminName1,
          region: city.data('geojson').properties.country
        };

        var context = jQuery('#' + self.options.fieldName);
        self.Geocoder.geocode(query, function(data) {
          if (!data.length) {
            return;
          }

          var data_point = jQuery.google2geojson(data[0]);
          jQuery(context).trigger(jQuery.geoevents.select_point, {
            point: data_point,
            target: self.cities
          });
        });
      },

      handle_naturalfeatures_change: function() {
        var natural = jQuery('option:selected', self.naturalfeatures);
        if (!natural.length) {
          return;
        }

        // Center map
        var query = {
          address: natural.data('geojson').properties.title + ', ' +
            natural.data('geojson').properties.adminName1,
          region: natural.data('geojson').properties.country
        };

        var context = jQuery('#' + self.options.fieldName);
        self.Geocoder.geocode(query, function(data) {
          if (!data.length) {
            return;
          }

          var data_point = jQuery.google2geojson(data[0]);
          jQuery(context).trigger(jQuery.geoevents.select_point, {
            point: data_point,
            target: self.naturalfeatures
          });
        });
      },

      // Initialize
      initialize: function() {
        self.biogroups = jQuery('select[name=biogroups]', self);
        self.groups = jQuery('select[name=groups]', self);
        self.countries_expand = jQuery('#expand_countries', self);
        // by default expand country checkbox is selected so we set
        // the expand property to true by default
        window.EEAGeotags.shouldExpandCountryGroups = true;
        self.countries = jQuery('select[name=countries]', self);
        self.nuts = jQuery('select[name=nuts]', self);
        self.cities = jQuery('select[name=cities]', self);
        self.naturalfeatures = jQuery('select[name=naturalfeature]', self);
        self.data = {};

        self.Geocoder = new google.maps.Geocoder();

        // Hide
        self.countries.parent().hide();
        self.nuts.parent().hide();
        self.cities.parent().hide();
        self.naturalfeatures.parent().hide();

        // Fill biogeographical regions
        jQuery.getJSON(self.options.json, {type: 'biogroups'}, function(data) {
          self.biogroups.empty();
          var option = jQuery('<option>').val('').text('');
          self.biogroups.append(option);
          jQuery.each(data.features, function() {
            self.biogroups.geojson = data;
            option = jQuery('<option>')
              .val(this.properties.name)
              .text(this.properties.title);
            self.biogroups.append(option);
          });
        });

        // Fill groups
        jQuery.getJSON(self.options.json, {type: 'groups'}, function(data) {
          self.data = data;
          self.groups.empty();
          var option = jQuery('<option>').val('').text('');
          self.groups.append(option);
          jQuery.each(self.data.features, function() {
            option = jQuery('<option>')
              .val(this.properties.name)
              .text(this.properties.title);
            self.groups.append(option);
          });
        });

        // Events
        self.biogroups.change(function() {
          self.options.handle_biogroups_change();
        });

        self.groups.change(function() {
          self.options.handle_groups_change();
        });

        self.countries.change(function() {
          self.options.handle_countries_change();
        });
        self.countries_expand.change(function() {
          window.EEAGeotags.shouldExpandCountryGroups = $(this).is(':checked') ? true : false;
        });


        self.nuts.change(function() {
          self.options.handle_nuts_change();
        });

        self.cities.change(function() {
          self.options.handle_cities_change();
        });

        self.naturalfeatures.change(function() {
          self.options.handle_naturalfeatures_change();
        });
      }
    };

    if (settings) {
      jQuery.extend(self.options, settings);
    }

    // Return
    self.options.initialize();
    return this;
  };

  jQuery.fn.geopreview = function(settings) {
    var self = this;
    self.options = {
      json: {},
      fieldName: '',
      template: '<div><div class="geo-preview-marker">' +
        '<h3 class="title"></h3>' +
        '<h4 class="subtitle"></h4>' +
        '<h5 class="tags"></h5>' +
        '</div></div>',
      map_options: {
        latitude: 0,
        longitude: 0,
        center: null,
        zoom: 3,
        navigationControl: true,
        navigationControlOptions: {
          style: google.maps.NavigationControlStyle.ZOOM_PAN
//        position: google.maps.ControlPosition.RIGHT // this generated a javascript error in IE
        },
        mapTypeControl: true,
        mapTypeControlOptions: {
          position: google.maps.ControlPosition.TOP_RIGHT,
          style: google.maps.MapTypeControlStyle.DEFAULT
        },
        mapTypeId: google.maps.MapTypeId.TERRAIN
      },

      handle_points: function(json) {
        self.options.handle_cleanup();
        if (!json.features) {
          return;
        }

        jQuery.each(json.features, function() {
          var center = this.properties.center;
          var latlng = new google.maps.LatLng(center[0], center[1]);
          var marker = new google.maps.Marker({
            position: latlng
          });
          marker.setMap(self.Map);
          self.markers.push(marker);

          var title = this.properties.title;
          var subtitle = this.properties.description;
          var tags = '';
          if (typeof(this.properties.tags) === 'string') {
            tags = this.properties.tags;
          } else {
            jQuery.each(this.properties.tags, function() {
              tags += this + ', ';
            });
          }

          var itemplate = jQuery(self.options.template);
          jQuery('.title', itemplate).text(title);
          jQuery('.subtitle', itemplate).text(subtitle);
          jQuery('.tags', itemplate).text(tags);

          // Google event handlers
          google.maps.event.addListener(marker, 'click', function() {
            self.info.setContent(itemplate.html());
            self.info.open(self.Map, marker);
          });
        });
      },

      handle_cleanup: function() {
        jQuery.each(self.markers, function() {
          this.setMap(null);
        });
        self.markers.length = 0;

        if (self.info) {
          self.info.close();
        }
      },

      set_map_bounds: function(markers) {
        if (!markers.length) {
          return;
        }
        var latlngbounds = new google.maps.LatLngBounds();
        var markers_length = markers.length;
        for (var i = 0, length = markers_length; i < length; i++) {
          latlngbounds.extend(markers[i].position);
        }
        self.options.map_options.center = latlngbounds.getCenter();
        return latlngbounds;
      },

      fit_map_bounds: function(map_bounds) {
        // fit bounds if we have markers otherwise center map on Europe
        if (map_bounds && self.markers.length > 1) {
          self.Map.fitBounds(map_bounds);
        }
        else {
          self.Map.setCenter(self.options.map_options.center);
        }

      },
      initialize: function() {
        self.markers = [];
        self.info = new google.maps.InfoWindow({
          content: ''
        });

        self.addClass('geo-preview-mapcanvas');
        var options = self.options.map_options;
        if (!options.latlng) {
          options.center = new google.maps.LatLng(
            options.latitude,
            options.longitude
          );
        }

        self.Map = new google.maps.Map(self[0], options);
        self.Geocoder = new google.maps.Geocoder();

        self.options.handle_points(self.options.json);
        var context = jQuery('#' + self.options.fieldName);
        var latlngbounds;
        var markers_length = self.markers.length;

        if (markers_length > 1) {
          latlngbounds = self.options.set_map_bounds(self.markers);
        }
        else {
          latlngbounds = null;
          options.center = new google.maps.LatLng(55, 35);
        }
        options.latlngbounds = latlngbounds;

        context.bind(jQuery.geoevents.basket_save, function(evt, data) {
          var options = self.options;
          var map_options =  options.map_options;

          options.handle_points(data.json);

          map_options.latlngbounds = self.options.set_map_bounds(self.markers);
          options.fit_map_bounds(map_options.latlngbounds);
        });

        // Fix preview map
        jQuery('form[name=edit_form] .formTab, .wizard-left, .wizard-right').click(function() {
          // #5339 fix preview map also when using eea.forms
          if (jQuery(this).closest('form').find('.formPanel:visible').find('#location-geopreview').length) {
            google.maps.event.trigger(self.Map, 'resize');
            self.options.fit_map_bounds(options.latlngbounds);
          }
        });
      }
    };

    if (settings) {
      jQuery.extend(self.options, settings);
    }

    // Return
    self.options.initialize();
    return this;
  };

// End namespace
}());


if (window.EEAGeotags === undefined) {
  var EEAGeotags = {'version': '1.0'};
}

// EEA Geotags view widget on map
EEAGeotags.View = function(context, options) {
  var self = this;
  self.map = '';
  self.context = context;
  self.context.parent().addClass('eea-geotags-view');
  self.settings = {};
  if (!self.context.attr('id')) {
    self.context.attr({id: self.context.attr('id') + self.id});
    self.id = '#' + self.context.attr('id') + self.count;
  }
  else {
    self.id = '#' + self.context.attr('id');
  }
  if (options) {
    jQuery.extend(self.settings, options);
  }
  EEAGeotags.settings = self.settings;
  self.initialize();
};

EEAGeotags.View.prototype = {

  initialize: function() {
    var self = this;
    dojo.require('dijit.layout.BorderContainer');
    dojo.require('dijit.layout.ContentPane');
    dojo.require('esri.map');
    dojo.require('esri.dijit.Scalebar');
    dojo.require("esri.layers.FeatureLayer");
    dojo.require("esri.dijit.Popup");
    self.init();
  },

  init: function() {
    var self = this,
      eea_location = jQuery('.eea-location-listing'),
      eea_location_links = eea_location.find('a'),
      eea_location_links_length = eea_location_links.length,
      eea_location_data = eea_location.data();
    self.modal = eea_location_links_length ? eea_location_data.modal : "Events";
    self.map_div = jQuery(self.id);
    if ((self.modal !== "False" && self.modal !== "Events") || (eea_location_links_length < 4 && (self.modal !== "Events" && self.modal !== "False"))) {
      var dialogBox,
        ui_dialog,
        eea_location_offset = eea_location.is(':visible') ? eea_location.offset() : eea_location.closest(':visible').offset(),
        pos_top = eea_location_offset.top + eea_location.height(),
        pos_left = eea_location_offset.left;
      // CREATE MAP
      self.map_div.show();
      self.initMap(eea_location_links);
      self.map_div.hide();
      eea_location_links.click(function(e) {
        if (!dialogBox) {
          // ie bug which fails if we have open and width and height in
          // the dialog options so we add them with plain jquery instead
          // of using dialog with open parameter
          dialogBox = self.map_div.dialog({
            closeOnEscape: true,
            autoOpen: false,
            resize: true
          });
          ui_dialog = dialogBox.closest('.ui-dialog');
          ui_dialog.css({left: pos_left, top: pos_top,
            width: eea_location_data.modal_dimensions[0],
            height: eea_location_data.modal_dimensions[1]}).show();
          // register our own close since dialog.open isn't triggered
          ui_dialog.find('.ui-dialog-titlebar-close').click(function(e) {
            ui_dialog.hide();
            e.preventDefault();
          });
          // resize map root to fit the designated space of #content
          // without scrollbars
          self.map_div.find(self.id + '_root').css({width: '100%', height: '100%'});

        }
        else {
          ui_dialog.css({left: pos_left, top: pos_top}).show();
        }
        e.preventDefault();
      });
    }
    else {
      self.map_div.show();
      self.initMap(eea_location_links);
    }
  },
  // Show loading image
  showLoading: function() {
    var loading;
    var self = this;
    loading = jQuery('#' + self.id + 'LoadingImg')[0];
    esri.show(loading);
    self.disableMapNavigation();
    self.hideZoomSlider();
  },

  // Hide loading image
  hideLoading: function() {
    var loading;
    var self = this;
    loading = jQuery('#' + self.id + 'LoadingImg')[0];
    esri.hide(loading);
    self.enableMapNavigation();
    self.showZoomSlider();
  },

  // Draw points on map
  drawPoints: function(eea_location_links) {
    var self = this,
      context_url, infoTemplate, map_points, locationTags, locationTagsLen;
    map_points = jQuery('#map_points');
    locationTags = eea_location_links;
    locationTagsLen = locationTags ? locationTags.length : 0;

    context_url = $("base").attr('href');
    //    remove /view if page is called with it
    if (context_url.endswith('/view')) {
      context_url = context_url.replace(/\/view$/g, '');
    }

    var infotemplate = map_points.length ? '${Title}<img src="${Url}/image_thumb" class="esriInfoImg" />' : '${Addr}';
    infoTemplate = new esri.InfoTemplate('${Name}', infotemplate);
    EEAGeotags.map.infoWindow.hide();
    var featureCollection = {
      "layerDefinition": null,
      "featureSet": {
        "features": [],
        "geometryType": "esriGeometryPoint"
      }
    };
    var renderer;
    var portal = EEAGeotags.settings.portal_url ? EEAGeotags.settings.portal_url + "/" : "/";
    if (self.modal === "Events") {
      renderer =
      {
        "type": "simple",
        "symbol": {
          "type": "esriPMS",
          "url": portal + EEAGeotags.settings.infoWindowImgName,
          "width": 15,
          "height": 15
        }
      };
    }
    featureCollection.layerDefinition = {
      "geometryType": "esriGeometryPoint",
      "objectIdField": "ObjectID",
      "drawingInfo": {
        "renderer": EEAGeotags.settings.featureCollectionRenderer || renderer
      },
      "fields": [
        {
          "name": "ObjectID",
          "alias": "ObjectID",
          "type": "esriFieldTypeOID"
        },
        {
          "name": "description",
          "alias": "Description",
          "type": "esriFieldTypeString"
        },
        {
          "name": "title",
          "alias": "Title",
          "type": "esriFieldTypeString"
        }
      ]
    };

    // remove previous graphics before adding new ones with faceted navigation
    // queries
    if (EEAGeotags.featureLayer) {
      EEAGeotags.featureLayer.clear();
    }
    var setPoints = function(res, results) {
      //define a popup template
      var popup = new esri.dijit.Popup(null, dojo.create("div"));
      EEAGeotags.map.setInfoWindow(popup);
      var popupTemplate = new esri.dijit.PopupTemplate({
        title: "{title}",
        description: "{description}"
      });
      //create a feature layer based on the feature collection
      var featureLayer = new esri.layers.FeatureLayer(res, {
        id: 'geotagsLayer',
        infoTemplate: popupTemplate
      });


      // add or change read more link for pop-up
      dojo.connect(popup, "onSelectionChange", function() {
        var feature = popup.getSelectedFeature();
        var readmeLink = dojo.query(".readmore", EEAGeotags.map.infoWindow.domNode)[0];
        if (feature && feature.attributes.Url) {
          if (!readmeLink) {
            dojo.create("a", {
              "class": "action readmore",
              "innerHTML": "Read More",
              "href": feature.attributes.Url
            }, dojo.query(".actionList", EEAGeotags.map.infoWindow.domNode)[0]);
          }
          else {
            readmeLink.href = feature.attributes.Url;
          }
        }
      });

      //associate the features with the popup on click
      dojo.connect(featureLayer, "onClick", function(evt) {
        var features = [];
        dojo.forEach(featureLayer.graphics, function(item) {
          if (evt.graphic.geometry.x === item.geometry.x &&
            evt.graphic.geometry.y === item.geometry.y) {
            features.push(item);
          }
        });
        popup.hide();
        EEAGeotags.map.infoWindow.setFeatures(features);
      });

      var features = [];
      var initialTemplate = infoTemplate.content,
        tempTemplate = "";
      var wgs = new esri.SpatialReference({ "wkid": 102100 });
      jQuery.each(results, function(i, item) {
        var geometry, mapPoint;
        geometry = new esri.geometry.Point(parseFloat(item.properties.center[1]), parseFloat(item.properties.center[0]), wgs);
        geometry = esri.geometry.geographicToWebMercator(geometry);
        var name = item.itemType || 'Location',
          itemUrl = item.itemUrl || context_url,
          icon = item.itemIcon || context_url + "/red_pin.png",
          addr = decodeURIComponent(item.properties.title) || decodeURIComponent(item.properties.description),
          addrDescription = decodeURIComponent(item.properties.description) || decodeURIComponent(item.properties.title),
          itemDate = item.itemDate,
          itemDescription = item.itemDescription,
          itemTitle = item.itemTitle ? '<h3>' + decodeURIComponent(item.itemTitle) + '</h3>' : '',
          mapOptions = {'Name': name,
            'Url': itemUrl,
            'Title': itemTitle};

        // add extra template information only if it's available from the catalog search
        tempTemplate = initialTemplate;

        if (addr) {
          mapOptions.Addr = addr;
        }

        if (addrDescription) {
          tempTemplate += '<p><strong>Location: </strong>${AddrDesc}</p>';
          mapOptions.AddrDesc = addrDescription;
        }

        if (itemDate && parseInt(itemDate, 10)) {
          tempTemplate += '<p><strong>Period: </strong>${Period}</p>';
          mapOptions.Period = itemDate;
        }
        if (itemDescription && itemDescription.length > 5) {
          tempTemplate += '<p><strong>Description: </strong>${Desc}</p>';
          mapOptions.Desc = decodeURIComponent(itemDescription);
        }
        // we need to recreate the infoTemplate otherwise all features will use the
        // same infoTemplate which will have it's content changed along the way
        infoTemplate = new esri.InfoTemplate('${Name}', tempTemplate);
        mapPoint = new esri.Graphic({'geometry': geometry, 'attributes': mapOptions });
        mapPoint.setInfoTemplate(infoTemplate);
        if (!EEAGeotags.settings.generalIcon) {
          mapPoint.setSymbol(new esri.symbol.PictureMarkerSymbol(icon, 30, 30));
        }
        features.push(mapPoint);
        // set latitude and longitude on each tag as data attribute
        if (locationTagsLen) {
          jQuery(locationTags[i]).data('latitude', item.properties.center[1]);
          jQuery(locationTags[i]).data('longitude', item.properties.center[0]);
        }
      });
      // first is add, second is update, third is delete parameter
      featureLayer.applyEdits(features, null, null);

      EEAGeotags.map.addLayers([featureLayer]);
      EEAGeotags.featureLayer = featureLayer;

      var enableClusterLayer = function() {
        // cluster points
        var cluster = dojo.map(features, function(item) {
          return { "x": item.geometry.x, "y": item.geometry.y, "attributes": item.attributes, 'template': item.infoTemplate };
        });

        var clusterLayer = new window.EEAGeotags.GeotagsClusterLayer({
          "data": cluster,
          "distance": 100,
          "id": "clusters",
          "labelColor": "#fff",
          "labelOffset": 10,
          "resolution": EEAGeotags.map.extent.getWidth() / EEAGeotags.map.width,
          "singleColor": "#888"
        });
        var defaultSym = new esri.symbol.SimpleMarkerSymbol().setSize(4);
        var renderer = new esri.renderer.ClassBreaksRenderer(
          defaultSym,
          "clusterCount"
        );
        var greenSymbol = new esri.symbol.PictureMarkerSymbol("http://static.arcgis.com/images/Symbols/Shapes/GreenPin1LargeB.png", 64, 64).setOffset(0, 15);
        var redSymbol = new esri.symbol.PictureMarkerSymbol("http://static.arcgis.com/images/Symbols/Shapes/RedPin1LargeB.png", 72, 72).setOffset(0, 15);
        renderer.addBreak(2, 200, greenSymbol);
        renderer.addBreak(200, 1001, redSymbol);

        clusterLayer.setRenderer(renderer);
        EEAGeotags.map.addLayer(clusterLayer);
      };
      if (window.EEAGeotags.GeotagsClusterLayer) {
        enableClusterLayer();
      }

    };

    if (map_points.length && map_points.html() !== "None") {
      var results = map_points.html();
      results = results.replace(/'/g, "");

      results = jQuery.parseJSON(results);
      setPoints(featureCollection, results);
    }
    else {
      jQuery.getJSON(context_url + '/eea.geotags.jsondata', {}, function(res) {
        setPoints(featureCollection, res.features);
        //center map and display infoWindow when clicking on a geotag
        locationTags.click(function(e) {
          var geometryClick;
          geometryClick = new esri.geometry.Point(jQuery(this).data('latitude'), jQuery(this).data('longitude'));
          geometryClick = esri.geometry.geographicToWebMercator(geometryClick);
          // show infoWindow after clicking on tag name
          var location = jQuery.grep(EEAGeotags.featureLayer.graphics, function(i) {
            return i.geometry.x === geometryClick.x && i.geometry.y === geometryClick.y;
          })[0];
          var point = location.geometry;
          EEAGeotags.map.infoWindow.setFeatures([location]);
          EEAGeotags.map.infoWindow.show(point, self.map.getInfoWindowAnchor(point));
          self.map.infoWindow.resize(250, 150);
          EEAGeotags.map.centerAndZoom(point, 6);
          EEAGeotags.map.resize();
          e.preventDefault();
        });

        if (self.modal === "Events") {
          locationTags.eq(0).trigger('click');
        }
      });
    }
  },

  // Create map
  initMap: function(eea_location_links) {
    // To get initial coordinates, zoom to default location and run in debugger: dojo.toJson(EEAGeotags.map.extent.toJson());
    var self = this;
    var initExtent, basemap, geometricExtent;
    initExtent = new esri.geometry.Extent({"xmin": -171, "ymin": -330, "xmax": 240, "ymax": 140, "spatialReference": {"wkid": 102100}});
    geometricExtent = esri.geometry.geographicToWebMercator(initExtent);
    // load a different map service if the #eeaEsriMap div has a data property called map_service
    var map_service = self.map_div.data('map_service') || 'http://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer';
    basemap = new esri.layers.ArcGISTiledMapServiceLayer(map_service);
    var map_id = self.id.substr(1, self.id.length);
    self.map = new esri.Map(map_id, {'extent': geometricExtent,
      'wrapAround180': true,
      'fadeOnZoom': true,
      'force3DTransforms': true,
      'isScrollWheelZoom': false,
      'navigationMode': 'css-transforms'});
    self.map.addLayer(basemap);
    EEAGeotags.map = self.map;
    // Loading images
    dojo.connect(self.map, 'onUpdateStart', self.showLoading);
    dojo.connect(self.map, 'onUpdateEnd', self.hideLoading);

    dojo.connect(self.map, 'onLoad', function() {
      // Resize the map when the browser resizes
      // zoom in by a factor of 2 in order to avoid having map smaller than container
      EEAGeotags.map.centerAndZoom(EEAGeotags.map.extent.getCenter(), 2);

      dojo.ready(function() {
        dojo.connect(dijit.byId(self.id), 'resize', self.map, self.map.resize);
        var resize = self.settings.infoWindowSize;
        resize = resize || [140, 100];
        self.map.infoWindow.resize(resize[0], resize[1]);

        // Draw a point on map
        self.drawPoints(eea_location_links);

        // Scalebar
        self.scalebar = new esri.dijit.Scalebar({ map: self.map,
          scalebarUnit: 'metric', // Use 'english' for miles
          attachTo: 'bottom-left' });

        // Hack to disable scroll wheel zooming, as map.disableScrollWheelZoom() has no effect
        self.map.onMouseWheel = function() {
        };
      });

      jQuery('body').trigger('EEAGeotags.MapLoaded');
    });
  }
};

// jQuery plugin for EEAGeotags.View
jQuery.fn.EEAGeotagsView = function(options) {
  return this.each(function(i) {
    var context = jQuery(this).addClass('eea-ajax');
    context.count = i;
    var geoview = new EEAGeotags.View(context, options);
    context.data('EEAGeotagsView', geoview);
  });
};

