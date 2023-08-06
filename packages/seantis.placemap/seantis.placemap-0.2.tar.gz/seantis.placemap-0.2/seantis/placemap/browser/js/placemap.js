this.seantis = this.seantis || {};

this.seantis.placemap = (function() {

    var self = this;
    var layers = [];

    self.create_kml_layer = function(url, title, color) {

        var defaultStyle = new OpenLayers.Style({
            'pointRadius': 8,
            'fillColor': color,
            'fillOpacity': 1.0,
            'strokeColor': '#fff',
            'strokeWidth': 2
        });

        var selectStyle = new OpenLayers.Style({
            'pointRadius': 8,
            'fillColor': '#fff',
            'fillOpacity': 1.0,
            'strokeColor': color,
            'strokeWidth': 2
        });

        var style = new OpenLayers.StyleMap({
            'default': defaultStyle,
            'select': selectStyle
        });

        var layer = new OpenLayers.Layer.Vector(title, {
            protocol: new OpenLayers.Protocol.HTTP({
                url: url,
                format: new OpenLayers.Format.KML({
                    extractStyles: false,
                    extractAttributes: true
                })
            }),
            strategies: [new OpenLayers.Strategy.Fixed()],
            projection: new OpenLayers.Projection('EPSG:4326'),
            styleMap: style
        });

        layer.is_popup_layer = true;

        return layer;
    };

    self.get_popup_layers = function(map) {
        var popup_layers = [];
        for (var i=0; i<map.layers.length; i++) {
            if (map.layers[i].is_popup_layer === true) {
                popup_layers.push(map.layers[i]);
            }
        }
        return popup_layers;
    };

    self.enable_popups = function(map) {

        var on_popup_close = function(event) {
            select.unselectAll();
        };

        var on_feature_select = function(event) {
            var feature = event.feature;
            var content = "<h2>" + feature.attributes.name + "</h2>" + feature.attributes.description;

            var popup = new OpenLayers.Popup.FramedCloud(
                "chicken",
                feature.geometry.getBounds().getCenterLonLat(),
                new OpenLayers.Size(100,100),
                content,
                null,
                true,
                on_popup_close
            );

            feature.popup = popup;
            map.addPopup(popup);
        };

        var on_feature_unselect = function(event) {
            var feature = event.feature;

            if (feature.popup) {
                map.removePopup(feature.popup);
                feature.popup.destroy();
                delete feature.popup;
            }
        };

        var layers = self.get_popup_layers(map);
        var select = new OpenLayers.Control.SelectFeature(layers);

        for (var i=0; i<layers.length; i++) {
            layers[i].events.on({
                "featureselected": on_feature_select,
                "featureunselected": on_feature_unselect
            });
        }

        map.addControl(select);
        select.activate();
    };

    self.enable_source_filters = function(map, legend) {
        $(legend).find('.source').click(function(e) {
            var source = $(this);

            if ($(e.target).is('a')) {
                return;
            }

            var name = source.find('.placemap-title').text();
            var layers = map.getLayersByName(name);

            if (layers.length != 1){
                return;
            }

            var visibility = ! layers[0].getVisibility();

            layers[0].setVisibility(visibility);
            source.toggleClass('is-hidden', !visibility);
        });
    };

    return self;
})();
