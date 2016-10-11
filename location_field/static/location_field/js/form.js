($ || django.jQuery)(function ($) {
    function location_field_load(map, address_field, zoom, suffix) {
        // var parent = map.parent().parent();

        var location_map;

        var location_coordinate = $('input[data-location-widget]');//parent.find('input[type=text]');

        var location_changed_by_user = false;
        var current_location;

        function savePosition(point) {
            if (point) {
                current_location = point;
                location_coordinate.val(point.lat().toFixed(6) + "," + point.lng().toFixed(6));
            }
        }

        function load() {
            var initial_position;

            if (location_coordinate.val()) {
                var l = location_coordinate.val().split(/,/);

                if (l.length > 1) {
                    initial_position = new google.maps.LatLng(l[0], l[1]);
                }
            }

            if (initial_position) {
                current_location = initial_position;
            } else {
                current_location = new google.maps.LatLng(-33.8688, 151.2195);
            }

            var options = {
                mapTypeId: google.maps.MapTypeId.ROADMAP,
                center: current_location,
                zoom: zoom
            };

            location_map = new google.maps.Map(map[0], options);

            var searchBox = new google.maps.places.SearchBox(address_field);

            var geocoder = new google.maps.Geocoder();

            // Bias the SearchBox results towards current map's viewport.
            location_map.addListener('bounds_changed', function () {
                searchBox.setBounds(location_map.getBounds());
            });

            var marker = new google.maps.Marker({
                map: location_map,
                position: initial_position,
                draggable: true
            });

            function placeMarker(location) {
                location_map.setZoom(zoom);
                marker.setPosition(location);
                location_map.setCenter(location);
                savePosition(location);
            }

            function update_address(location) {
                if (geocoder) {
                    geocoder.geocode({"latLng": location}, function (results, status) {
                        if (status == google.maps.GeocoderStatus.OK) {
                            $(address_field).val(results[0].formatted_address);
                        }
                    });
                }
            }

            function new_loc_get(location) {
                location_changed_by_user = true;
                placeMarker(location);

                update_address(location);
            }

            function marker_change(location) {
                location_changed_by_user = true;
                marker.setPosition(location);
                savePosition(location);

                update_address(location);
            }

            placeMarker(current_location);

            if (!initial_position) {
                // Try HTML5 geolocation.
                if (navigator.geolocation) {
                    navigator.geolocation.getCurrentPosition(function (position) {
                        if (!location_changed_by_user) {
                            current_location = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
                            new_loc_get(current_location);
                        }
                    }, function () {
                    });
                }
            }

            searchBox.addListener('places_changed', function () {
                var places = searchBox.getPlaces();

                if (places.length == 0) {
                    return;
                }

                p = places[0];
                placeMarker(p.geometry.location);
            });

            google.maps.event.addListener(marker, 'dragend', function (mouseEvent) {
                marker_change(mouseEvent.latLng);
            });

            google.maps.event.addListener(location_map, 'click', function (mouseEvent) {
                marker_change(mouseEvent.latLng);
            });
        }

        load();
    }


    $('input[data-location-widget]').livequery(function () {
        var $el = $(this), name = $el.attr('name'), pfx;

        try {
            pfx = name.match(/-(\d+)-/)[1];
        } catch (e) {
        }
        ;

        var values = {
            map: $el.attr('data-map'),
            zoom: $el.attr('data-zoom'),
            suffix: $el.attr('data-suffix'),
            address_field: $el.attr('data-address-field')
        }

        if (!/__prefix__/.test(name)) {
            for (key in values) {
                if (/__prefix__/.test(values[key])) {
                    values[key] = values[key].replace(/__prefix__/g, pfx);
                }
            }
        }

        var $map = $(values.map),
            $address_field = $(values.address_field)[0],
            zoom = parseInt(values.zoom),
            suffix = values.suffix;

        location_field_load($map, $address_field, zoom, suffix);
    });
});