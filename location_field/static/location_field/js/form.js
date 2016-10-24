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
                draggable: true,
                zIndex: 1
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

            var image = {
                url: 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAABHNCSVQICAgIfAhkiAAAAF96VFh0UmF3IHByb2ZpbGUgdHlwZSBBUFAxAABo3uNKT81LLcpMVigoyk/LzEnlUgADYxMuE0sTS6NEAwMDCwMIMDQwMDYEkkZAtjlUKNEABZgamFmaGZsZmgMxiM8FAEi2FMnxHlGkAAADqElEQVRo3t1aTWgTQRQOiuDPQfHs38GDogc1BwVtQxM9xIMexIN4EWw9iAehuQdq0zb+IYhglFovClXQU+uhIuqh3hQll3iwpyjG38Zkt5uffc4XnHaSbpLZ3dnEZOBB2H3z3jeZN+9vx+fzYPgTtCoQpdVHrtA6EH7jme+/HFFawQBu6BnWNwdGjB2BWH5P32jeb0V4B54KL5uDuW3D7Y/S2uCwvrUR4GaEuZABWS0FHhhd2O4UdN3FMJneLoRtN7Y+GMvvUw2eE2RDh3LTOnCd1vQN5XZ5BXwZMV3QqQT84TFa3zuU39sy8P8IOqHb3T8fpY1emoyMSQGDI/Bwc+0ELy6i4nLtepp2mE0jc5L3UAhMsdxut0rPJfRDN2eMY1enF8Inbmj7XbtZhunkI1rZFD/cmFMlr1PFi1/nzSdGkT5RzcAzvAOPU/kVF9s0ujqw+9mP5QgDmCbJAV7McXIeGpqS3Qg7OVs4lTfMD1Yg9QLR518mZbImFcvWC8FcyLAbsev++3YETb0tn2XAvouAvjGwd14YdCahUTCWW6QQIzzDO/CIAzKm3pf77ei23AUkVbICHr8pnDZNynMQJfYPT7wyKBzPVQG3IvCAtyTsCmRBprQpMawWnkc+q2Rbn+TK/+gmRR7qTYHXEuZkdVM0p6SdLLYqX0LItnFgBxe3v0R04b5mGzwnzIUMPiBbFkdVmhGIa5tkJ4reZvyl4Rg8p3tMBh+FEqUduVRUSTKTnieL58UDG76cc70AyMgIBxs6pMyIYV5agKT9f/ltTnJFOIhuwXOCLD6gQ/oc8AJcdtuYb09xRQN3NWULgCwhfqSk3SkaBZViRTK3EYNUSBF4Hic0Y8mM+if0HhlMlaIHbQ8Z5lszxnGuIP2zrAw8J8jkA7pkMAG79AKuPTOOcgWZeVP5AsSDjAxWegGyJoSUWAj/FBpRa0JiviSbfldMqOMPcce7UVeBLK4gkMVVBLI2phLjKlIJm8lcxMNkLuIomXOTTmc1kwYf2E+nMQdzlaTTKgoaZJWyBQ141RY0DkrK6XflAQbih1geZnhJeXu5WeEZ3mVqSkrIgCzXJaXqoh65TUuLerdtFXgQ2bYKeD1pq6hobLE86SlztXMWvaA5vPO0sYWB9p2K1iJS4ra0Fju/udsN7fWu+MDRFZ+YuuIjX1d8Zu2OD92WC9G3ub1qABktBV7vssfBMX1L7yVjZ7PLHuABb9svezS7boNDyK/b4LdX123+Au+jOmNxrkG0AAAAAElFTkSuQmCC',
                scaledSize: new google.maps.Size(24, 24), // scaled size
                size: new google.maps.Size(24, 24),
                origin: new google.maps.Point(0, 0),
                anchor: new google.maps.Point(12, 12)
            };
            var current_position_marker = new google.maps.Marker({
                icon: image,
                zIndex: 0
            });

            // Try HTML5 geolocation.
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(function (position) {
                    var loc = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
                    if (!initial_position) {
                        if (!location_changed_by_user) {
                            current_location = loc;
                            new_loc_get(current_location);
                        }
                    }
                    current_position_marker.setMap(location_map);
                    current_position_marker.setPosition(loc);
                }, function () {
                });
            }

            searchBox.addListener('places_changed', function () {
                var places = searchBox.getPlaces();

                if (places.length == 0) {
                    return;
                }

                var p = places[0];
                placeMarker(p.geometry.location);
            });

            google.maps.event.addListener(marker, 'dragend', function (mouseEvent) {
                marker_change(mouseEvent.latLng);
            });


            google.maps.event.addListener(current_position_marker, 'click', function (mouseEvent) {
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
            for (var key in values) {
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