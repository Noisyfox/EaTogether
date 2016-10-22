/** 
 * "PayPal Shoppign Cart" jQuery Plugin
 *
 * Author: flGravity
 * Created: 23/01/2012
 * Site: http://codecanyon.net/user/flGravity
 * Version: 2.3
 */
 
(function ($) {

    $.fn.paypalshop = function (s) {
    
        var shop = this;
        
        var settings = {
            /* application settings */
            groupAnimationTime: 500,
            groupAnimationStartDelay: 100,
            groupAnimationShift: 10,
            groupAnimationEasing: 'easeOutCubic',
            productsScrollTime: 500,
            productsScrollEasing: 'easeInOutCubic',
            cartItemsScrollTime: 400,
            cartItemsScrollEasing: 'easeInOutCubic',
            cartSlideDownTime: 300,
            cartSlideUpTime: 600,
            cartSlideEasing: 'easeOutQuint',
            currencySign: '$',
            numberPrecision: 2,
            productBuyLimit: 3,
            localStorage: true,
            localStorageName: 'ppshop',
            pageRows: 2,
            pageColumns: 3,
            buttonsOpacity: 0.7,
            priceHandler: function () {
                //default total price
                var p = this.price * this.quantity;
                //send new price to paypal ("amount")
                this.checkout_price = p / this.quantity;
                //return price
                return p;
            },
            /* paypal checkout settings */
            paypal: {
                'business': 'paypal@domain.com',
                'currency_code': 'USD',
                'lc': 'US',
                'return': 'http://www.domain.com/shop/',
                'cbt': 'Return to My Site',
                'cancel_return': 'http://www.domain.com/shop/',
                'no_shipping': 1
            }
        };

        //override settings 
        $.extend(settings, s);

        //shopping cart
        var cart = {};

        //DOM elements
        var active_group = null;
        var products = $('.shop-products > ul[id]', shop);
        
        //add groups
        var groups = $('<ul class="shop-groups"/>').appendTo(shop);
        
        //page scroll element
        var page_scroll = {
            prev: $('<a/>', {
                'class': 'page-prev',
                'title': 'Previous Page',
                'href': '#'
            }),
            next: $('<a/>', {
                'class': 'page-next',
                'title': 'Next Page',
                'href': '#'
            }),
            pn: $('<span class="page-number"/>')
        };
        
        //add to document
        $('<div class="page-scroll"/>').append(page_scroll.prev, page_scroll.pn, page_scroll.next).appendTo(shop);
        
        //shopping cart elements
        var shop_cart = {
            cart_header: $('<div/>', {
                'class': 'cart-header'
            }).html(
                '<p>Items: <span class="total-items"></span> ' +
                'Total: <span class="total-price"></span></p>'),
            cart_content: $('<div/>', {
                'class': 'cart-content'
            }),
            list_header: $('<div/>', {
                'class': 'list-header'
            }).html(
                '<span class="col-number">No.</span>' +
                '<span class="col-name">Name</span>' +
                '<span class="col-quantity">Quantity</span>' +
                '<span class="col-price">Price</span>' +
                '<span class="col-remove">Remove</span>'),
            list_content: $('<div/>', {
                'class': 'list-content'
            }),
            list_wrapper: $('<div/>', {
                'class': 'list-wrapper'
            }),
            list_scroll: $('<div/>', {
                'class': 'list-scroll'
            }).html(
                '<a class="scroll-down" href="#" title="Scroll down">down</a>' +
                '<a class="scroll-up" href="#" title="Scroll up">up</a>'),
            cart_footer: $('<div/>', {
                'class': 'cart-footer'
            }).html(
                '<p>Your total purchase is: <span class="total-items"></span> ' +
                'items (<span class="total-price"></span>)</p>' +
                '<a class="clear-button" href="#">Clear</a>' +
                '<a class="checkout-button" href="#">PayPal Checkout</a>')
        };
        
        //add to document
        shop_cart.list_wrapper.append(shop_cart.list_content);
        shop_cart.cart_content.append(shop_cart.list_header, shop_cart.list_wrapper, shop_cart.list_scroll);
        shop_cart.self = $('<div class="shop-cart"/>').
        append(shop_cart.cart_header).
        append(shop_cart.cart_content).
        append(shop_cart.cart_footer).
        appendTo(shop);


        //process product groups
        products.each(function (gid) {
        
            //create groups of products
            var gname = this.id.replace(/_/g, ' ');
            var gbutton = $('<a />', {
                'title': gname,
                'prod_id': this.id,
                'href': '#'
            }).text(gname);
            $('<li/>').append(gbutton).appendTo(groups);

            //click handler for product groups
            gbutton.click(function (e) {
            
                //make clicked group active
                groups.find('.active-group').removeClass('active-group');
                $(this).parent().addClass('active-group');
                
                //hide all groups 
                products.css('display', 'none');
                active_group = $('#' + $(this).attr('prod_id'), shop);
                
                //show only active group
                active_group.css({top:0, display:'block'});
                
                //animate products by shifting their top position and tweening opacity
                active_group.children('li').each(function (i) {
                    $(this).css({
                        'top': parseInt((i + settings.pageColumns) / settings.pageColumns) * settings.groupAnimationShift,
                        'opacity': 0
                    });
                    $(this).delay(i * settings.groupAnimationStartDelay).
                    animate({
                        'top': 0,
                        'opacity': 1
                    }, settings.groupAnimationTime, settings.groupAnimationEasing);
                });
                
                //update number of pages
                active_group.current_page = 1;
                active_group.pages = Math.ceil(active_group.children('li').length / (settings.pageRows * settings.pageColumns));
                
                //update page scroll
                resetPageScroll();
                e.preventDefault();
                
            }); // - gbutton.click()

            //process individual products in every group
            $(this).children('li').each(function (pid) {
                var product = $(this);
                
                //assign uniq id to every product within group
                product.attr('id', '_p0' + pid);
                
                //add "onclick" handler to product "Buy" button
                product.find('.product-buy').click(function (e) {
                
                    //check if option is set 	    	 		
                    var option = '';
                    if ($(this).attr('option')) {
                        var opt = $(this).attr('option');
                        if (isNaN(opt) && opt.length > 0) {
                            //look for select element by ID or Class within product
                            if (opt.charAt(0) == '#') {
                                option = $(this).closest('.product').find(opt).val() || '';
                            } else {
                                option = $(this).closest('.product').find('.' + opt).val() || '';
                            }
                        } else {
                            option = opt;
                        }
                    }
					
					// create product item
                    var item = {
                    	//general variables
                        group: product.parent().attr('id'),
                        id: product.attr('id'),
                        option: option || 'NA',
                        quantity: parseInt(product.attr('minimum' + option), 10) || 1,
                        minimum: parseInt(product.attr('minimum' + option), 10) || 1,
                        skip: parseInt(product.attr('skip' + option), 10) || 1,
                        //paypal variables
                        name: product.attr('name' + option),
                        price: parseFloat(product.attr('price' + option)),
                        shipping: product.attr('shipping' + option),
                        number: product.attr('number' + option),
                        handling: product.attr('handling' + option)
                    };
                    
                    // add item to the cart
                    addToCart(item, true);
                    e.preventDefault();
                    
                }).fadeTo(0, 0.7).hover(hoverHandler(300, 1), hoverHandler(300, settings.buttonsOpacity));
                
                //update currency sign 
                if (settings.currencySign) {
                    product.find('.product-currency').html(settings.currencySign);
                }
                
            });

            
            if (gid == 0) {
            
            	//first group is active
                groups.children('li:eq(0)').addClass('active-group');
                active_group = $(this);

                //update number of pages
                active_group.current_page = 1;
                active_group.pages = Math.ceil(active_group.children('li').length / (settings.pageRows * settings.pageColumns));
                resetPageScroll();
                updateCartTotals();
                
            } else {
            
                //hide all other product
                $(this).hide();
            
            }
            
        }); //end products.each()
        
        
        //restore cart if it was saved in localStorage
        if (settings.localStorage) {
            restoreCartLocally();
            // sync cart content among open pages every 3 sec
            window.setInterval(restoreCartLocally, 3000);
        }

        // add click listeners to page scroll prev button 
        page_scroll.prev.click(function (e) {
            if (active_group.current_page > 1) {
                active_group.animate({
                    'top': '+=' + products.parent().height()
                }, settings.productsScrollTime, settings.productsScrollEasing);
                active_group.current_page--;
                resetPageScroll();
            }
            e.preventDefault();
        });
		
		 // add click listeners to page scroll next button
        page_scroll.next.click(function (e) {
            if (active_group.current_page < active_group.pages) {
                active_group.animate({
                    'top': '-=' + products.parent().height()
                }, settings.productsScrollTime, settings.productsScrollEasing);
                active_group.current_page++;
                resetPageScroll();
            }
            e.preventDefault();
        });


        // add click listeners for cart "Clear" and "Checkout" buttons
        $('.clear-button', shop_cart.cart_footer).css('opacity', settings.buttonsOpacity).
        click(function (e) {
            cart = {};
            updateShoppingCart();
            saveCartLocally();
            $('.shop-cart .list-content', shop).css('top', 0);
            e.preventDefault();
        }).hover(hoverHandler(300, 1), hoverHandler(300, settings.buttonsOpacity));

        $('.checkout-button', shop_cart.cart_footer).css('opacity', settings.buttonsOpacity).
        click(function (e) {
            processCheckout();
            e.preventDefault();
        }).hover(hoverHandler(300, 1), hoverHandler(300, settings.buttonsOpacity));


        //slideup animation for cart on mousehover
        var shop_height = shop.height() + parseInt(shop.css('paddingBottom')) + parseInt(shop.css('paddingTop'));
        var cart_header_height = parseInt(shop_cart.cart_header.height());

        shop_cart.self.hover(function () {
            shop_cart.cart_header.css('visibility', 'hidden');
            $(this).stop().animate({
                'top': (shop_height - $(this).height()) + 'px'
            }, settings.cartSlideUpTime, settings.cartSlideEasing);
        }, function () {
            $(this).stop().animate({
                'top': (shop_height - cart_header_height) + 'px'
            }, settings.cartSlideDownTime, settings.cartSlideEasing, function () {
                shop_cart.cart_header.stop().css({
                    'visibility': 'visible',
                    'opacity': 0
                }).fadeTo('slow', 1);
            });
        }).css('top', (shop_height - cart_header_height) + 'px');


        //add click listeners for scroll buttons to scroll cart content
        $('.scroll-up, .scroll-down', shop_cart.list_scroll).click(function (e) {
            var w = shop_cart.list_wrapper; //wrapper div
            var p = shop_cart.list_content; //products in cart
            var pt = -parseInt(p.css('top')); //products "top"
            var d = p.height() - w.height(); //difference

            if (this.className == 'scroll-down' && pt < d) {
                if (d - pt > w.height()) {
                    pt += w.height();
                } else {
                    pt = d;
                }
            }

            if (this.className == 'scroll-up' && pt > 0) {
                if (pt > w.height()) {
                    pt -= w.height();
                } else {
                    pt = 0;
                }
            }

            p.animate({
                top: -pt
            }, settings.cartItemsScrollTime, settings.cartItemsScrollEasing);
            e.preventDefault();
        });



        /**  FUNCTION DEFINITIONS
         ************************************************************************************/


        /* 
         Hover handler shortcode
        */
        
        function hoverHandler(d, a) {
            return function () {
                $(this).stop().fadeTo(d, a);
            }
        }


        /* 
        * Function to add new items to cart
        */
        
        function addToCart(item, animate) {
        
            //check if group exists, otherwise create new group
            if (!(item.group in cart)) {
                cart[item.group] = new Object();
                cart[item.group].length = 0;
            }
            var g = cart[item.group];
            var p = item.id + '_' + item.option; //product id + option 
            
            //check if this product is already in cart 
            if (p in g) {
                if (g[p].quantity + g[p].skip <= settings.productBuyLimit) {
                    g[p].quantity = g[p].quantity + g[p].skip;
                } else {
                    animate = false;
                }
            } else {
                g[p] = item;
                g.length += 1;
            }
            
            // re-add items to cart
            updateShoppingCart();
            
            // save cart in localStorage
            saveCartLocally();
            
            //animate adding new item to cart
            if (animate) {
                var sch = shop_cart.cart_header.height();
                $('.shop-cart', shop).stop(false, true).animate({
                    'top': '+=' + sch
                }, 200).animate({
                    'top': '-=' + sch
                }, 200);
            }
            
        }


        /* 
        * Function to update quantity and price totals in shopping cart
        */
        
        function updateCartTotals() {
        
            // calculate total quantity and price for items
            var items = 0;
            var total = 0;
            for (var g in cart) {
                for (var i in cart[g]) {
                    
                    if (i == 'length') continue; //skip length property
                    
                    var v = cart[g][i];
                    items += v.quantity;
                    total += settings.priceHandler.call(v);
                }
            }
            
            //total price
            total = settings.currencySign + total.toFixed(settings.numberPrecision);
            $('.total-items', shop_cart.self).text(items);
            $('.total-price', shop_cart.self).html(total);
            
        }


        /* 
        * Function to generate shopping cart content from items in cart
        */
        
        function updateShoppingCart() {
        
            //update totals in cart
            updateCartTotals();
            
            //clear cart
            shop_cart.list_content.empty();
            
            // process groups in cart
            for (var g in cart) {
            
                //add header for group
                var index = 0;
                shop_cart.list_content.append('<div class="list-group">' + g.replace(/_/g, ' ') + '</div>');
                
                //process products in groups
                for (var i in cart[g]) {
                
                	//skip length property
                    if (i == 'length') continue; 
                    
                    var v = cart[g][i];
                    var p = $('<p />').attr({
                        'id': v.group + '::' + (v.id + '_' + v.option),
                        'class': (++index == cart[g].length) ? 'last-in-list' : ''
                    });
                    
                    p.append('<span class="col-number">' + index + '.</span>' +
                        '<span class="col-name">' + v.name + '</span>' +
                        '<span class="col-quantity">' +
                        '<a class="button-subtract" href="#" title="-1">-</a>' +
                        '<span class="item-quantity">' + v.quantity + '</span>' +
                        '<a class="button-add" href="#" title="+1">+</a></span>' +
                        '<span class="col-price">' +
                        '<span class="item-price">' + settings.priceHandler.call(v).toFixed(settings.numberPrecision) +
                        '</span></span>' +
                        '<span class="col-remove">' +
                        '<a class="button-delete" href="#" title="Remove">&times;</a></span>');

                    //add to cart
                    shop_cart.list_content.append(p);

                    //add click handlers for item buttons
                    p.bind('click', function (e) {
                        var p = this;
                        // handle buttons
                        if (/button-delete/.test(e.target.className)) {
                            itemRemoveHandler(p);
                        } else if (/button-(add|subtract)/.test(e.target.className)) {
                            itemQuantityHandler(p, e.target.className);
                        }
                        // save cart in localStorage
                        saveCartLocally();
                        e.preventDefault();
                    });
                    
                } // process products 
            
            } // process groups
            
        }


        /* 
        * Event handler for [+] & [-] buttons next to items in cart
        */
        
        function itemQuantityHandler(p, a) {
        
            //get current quantity from cart
            var filter = /(\w+)::(\w+)/.exec(p.id);
            var cart_item = cart[filter[1]][filter[2]];

            //add one
            if (a.indexOf('add') != -1) {
                if (cart_item.quantity + cart_item.skip <= settings.productBuyLimit) {
                    cart_item.quantity += cart_item.skip;
                }
            }
            
            //substract one
            if (a.indexOf('subtract') != -1) {
                if (cart_item.quantity - cart_item.skip >= cart_item.minimum) {
                    cart_item.quantity -= cart_item.skip;
                }
            }
            
            //update quantity in shopping cart
            $(p).find('.item-quantity').text(cart_item.quantity);
            
            //update price for item
            $(p).find('.item-price').text(settings.priceHandler.call(cart_item).toFixed(settings.numberPrecision));
            
            //update totals 
            updateCartTotals();
            
        }

        /* 
        * Handler for [x] button to remove item in cart
        */
        
        function itemRemoveHandler(p) {
            
            //look for item in cart
            var filter = /(\w+)::(\w+)/.exec(p.id);
            delete cart[filter[1]][filter[2]];
            cart[filter[1]].length--;
            
            //when length becomes 0 remove group itself
            if (cart[filter[1]].length == 0)
                delete cart[filter[1]];
            
            //re-add items to cart    
            updateShoppingCart();
            
        }
        
        
        /*
        * Function that handles page scroll for active product group
        */
        
        function resetPageScroll() {
        
            //page number / total pages
            var pages = active_group.current_page + '/' + active_group.pages;
            page_scroll.pn.text('Page: ' + pages);

            //make scroll arrows inactive when necessary
            
            if (active_group.current_page == 1) {
                page_scroll.prev.fadeTo(200, 0.2);
                page_scroll.prev.unbind('mouseleave mouseenter');
            } else {
                page_scroll.prev.fadeTo(200, settings.buttonsOpacity);
                page_scroll.prev.hover(hoverHandler(500, 1),
                    hoverHandler(500, settings.buttonsOpacity));
            }

            if (active_group.current_page == active_group.pages) {
                page_scroll.next.fadeTo(200, 0.2);
                page_scroll.next.unbind('mouseleave mouseenter');
            } else {
                page_scroll.next.fadeTo(200, settings.buttonsOpacity);
                page_scroll.next.hover(hoverHandler(500, 1),
                    hoverHandler(500, settings.buttonsOpacity));
            }
            
        }


        /* 
        * Function to submit request to PayPal with all items in cart
        */
        
        function processCheckout() {

            /*
            //static paypal request arguments
            var pp_settings = {
                cmd: '_cart',
                upload: 1,
                no_note: 0,
                bn: 'JQPayPalShop_ShoppingCart_EC_US',
                tax: 0,
                rm: 2,
                custom: ''
            };

            //copy settings.paypal to pp_settings 
            $.extend(pp_settings, settings.paypal);
            */

            //create form for POST request
            var form = $('<form />');
            form.attr('action', 'https://www.paypal.com/cgi-bin/webscr');
            form.attr('method', 'post');
            form.attr('target', '_blank');

            /*
            //add paypal variables
            var arg;
            for (var key in pp_settings) {
                arg = $('<input type="hidden" />');
                arg.attr('name', key);
                arg.attr('value', pp_settings[key]);
                //add to form
                form.append(arg);
            }
            */

            //now process items in cart
            var item_index = 0;
            
            //properties map for 'cart' to the paypal variables
            var map = {
                name: 'item_name',
                quantity: 'quantity',
                checkout_price: 'amount',
                shipping: 'shipping',
                number: 'item_number',
                handling: 'handling'
            };

            for (var g in cart) {
                //group
                for (var i in cart[g]) {
                    //item
                    if (i == 'length') continue;  //skip length property
                    item_index++;
                    //process item
                    for (var k in map) {
                        arg = $('<input type="text" />');
                        arg.attr('name', map[k] + '_' + item_index);
                        arg.attr('value', cart[g][i][k]);
                        form.append(arg);
                    }
                }
            }

            //add form to the document
            form.appendTo('body')
            //shop.append(form);
            form.submit();
            
            //remove form
            //form.remove();
        }


        /* 
        * Function to save cart content in localStorage
        */
        
        function saveCartLocally() {
            var can_store = false,
                can_json = false;
            // check if localStorage is supported 
            if (window.localStorage && window.localStorage.setItem)
                can_store = true;
            // check if JSON is supported
            if (window.JSON && window.JSON.stringify)
                can_json = true;
            // save cart
            if (settings.localStorage && can_store && can_json) {
                window.localStorage.setItem(settings.localStorageName, JSON.stringify(cart));
            }
        }


        /* 
        * Function restore saved cart from localStorage
        */
        
        function restoreCartLocally() {
            if (window.localStorage && window.localStorage.getItem) {
                var stored_cart = window.localStorage.getItem(settings.localStorageName);
                if (stored_cart) {
                	try {
                    	cart = JSON.parse(stored_cart);
                    } catch(e) {
                    	cart = {};
                    }
                    updateShoppingCart();
                }
            }
        }


		// return for chaining
        return this;
        
    } // $.fn.paypalshop end
    
    
})(jQuery);