Nodeshot.addRegions({
    body: '#body'
});

// localStorage check
Nodeshot.addInitializer(function () {
    Nodeshot.preferences = window.localStorage || {};
});

// init layout
Nodeshot.addInitializer(function () {
    Nodeshot.notifications = new NotificationCollection();
    Nodeshot.notificationView = new NotificationCollectionView({
        collection: Nodeshot.notifications
    }).render();

    Nodeshot.accountMenu = new AccountMenuView({
        model: Nodeshot.currentUser
    });
    Nodeshot.accountMenu.render();

    Nodeshot.mainMenu = new MainMenuView(); // renders automatically

    Nodeshot.generalSearch = new SearchView(); // renders automatically

    Nodeshot.onNodeClose = '#/map';
});

// init pages
Nodeshot.addInitializer(function () {
    MapView.prototype.resetDataContainers();
    MapView.prototype.loadMapData();

    Nodeshot.page = new Page();

    Nodeshot.page.on('sync', function () {
        Nodeshot.body.close();
        Nodeshot.body.show(new PageView({
            model: Nodeshot.page
        }));
    });

    Nodeshot.page.on('error', function (model, http) {
        if (http.status === 404) {
            createModal({
                message: 'the requested page was not found'
            });
        } else {
            createModal({
                message: 'there was an error while retrieving the page'
            });
        }
    });

    Backbone.history.start();
});

var NodeshotController = {
    // index
    index: function () {
        Backbone.history.navigate('#pages/home', {
            trigger: true
        });
    },

    // page details
    getPage: function (slug) {
        toggleLoading('show');

        Nodeshot.page.set('slug', slug);
        Nodeshot.page.fetch();

        var link = $('#nav-bar a[href="#/pages/' + slug + '"]');

        // ensure no duplicate active links
        $('#nav-bar li').removeClass('active');

        if (link.length && link.parents('.dropdown').length) {
            link.parents('.dropdown').addClass('active');
        } else {
            link.trigger('click');
        }
    },

    // node list
    getNodeList: function() {
        new NodeCollection().fetch({
            success: function(collection){
                Nodeshot.body.close();
                Nodeshot.body.show(new NodeListView({
                    model: new Backbone.Model({ total: collection.count }),
                    collection: collection
                }));
            }
        });
    },

    // node details
    getNode: function (slug) {
        var node = new Node(Nodeshot.nodesNamed[slug].feature.properties);
        Nodeshot.body.close();
        Nodeshot.body.show(new NodeDetailsView({
            model: node
        }));
    },

    // map view
    getMap: function () {
        Nodeshot.body.close();
        Nodeshot.body.show(new MapView());
        $('#nav-bar a[href="#/map"]').trigger('click');
    },

    // map node popup
    getMapNode: function (slug) {
        if (typeof (Nodeshot.body.currentView) === "undefined" || Nodeshot.body.currentView.name != 'MapView') {
            this.getMap();
        }
        Nodeshot.nodesNamed[slug].openPopup();
    },

    // user profile view
    getUser: function (username) {
        var user = new User({ username: username });

        user.fetch()
        .done(function(){
            Nodeshot.body.close();
            Nodeshot.body.show(new UserDetailsView({
                model: user
            }));
        })
        .error(function(http){
            // TODO: D.R.Y.
            if (http.status === 404) {
                createModal({
                    message: 'the requested page was not found'
                });
            } else {
                createModal({
                    message: 'there was an error while retrieving the page'
                });
            }
        });
    }
}

var NodeshotRouter = new Marionette.AppRouter({
    controller: NodeshotController,
    appRoutes: {
        "": "index",
        "_=_": "index", // facebook redirects here
        "pages/:slug": "getPage",
        "map": "getMap",
        "map/:slug": "getMapNode",
        "nodes": "getNodeList",
        "nodes/:slug": "getNode",
        "users/:username": "getUser"
    }
});

$(document).ready(function ($) {
    Nodeshot.start();

    // login / sign in
    $('#js-signin-form').submit(function (e) {
        e.preventDefault();
        var data = $(this).serializeJSON();
        // data.remember is true if "on", false otherwise
        data.remember = data.hasOwnProperty('remember') ? true : false;
        // remember choice
        Nodeshot.preferences.staySignedIn = data.remember;

        Nodeshot.currentUser.login(data);
    });

    // sign up
    $('#js-signup-form').submit(function (e) {
        e.preventDefault();
        var form = $(this),
            data = form.serialize();

        // remove eventual errors
        form.find('.error').removeClass('error');

        $.post('/api/v1/profiles/', data).error(function (http) {
            // TODO improve
            // signup validation
            var json = http.responseJSON;

            for (key in json) {
                var input = $('#js-signup-' + key);
                if (input.length) {
                    var container = input.parent();
                    container.attr('data-original-title', json[key]);
                    container.addClass('error');
                }
            }

            form.find('.error').tooltip('show');
            form.find('.hastip:not(.error)').tooltip('hide');

        }).done(function (response) {
            $('#signup-modal').modal('hide');
            createModal({
                message: 'sent confirmation mail'
            });
        });
    });

    // signup link in sign in overlay
    $('#js-signup-link').click(function (e) {
        e.preventDefault();
        $('#signin-modal').modal('hide');
        $('#signup-modal').modal('show');
    });


    // signin link in signup overlay
    $('#js-signin-link').click(function (e) {
        e.preventDefault();
        $('#signup-modal').modal('hide');
        $('#signin-modal').modal('show');
    });

    // dismiss modal links
    $('.js-dismiss').click(function (e) {
        $(this).parents('.modal').modal('hide');
    });

    // enable tooltips
    $('.hastip').tooltip();

    // load full user profile
    if(Nodeshot.currentUser.isAuthenticated()){
        Nodeshot.currentUser.fetch();
    }

    // create status CSS classes
    css = _.template($('#status-css-template').html(), {});
    $('head').append(css);
});

var createModal = function (opts) {
    var template_html = $('#modal-template').html(),
        close = function () {
            $('#tmp-modal').modal('hide')
        },
        options = $.extend({
            message: '',
            successMessage: 'ok',
            successAction: function () {},
            defaultMessage: null,
            defaultAction: function () {}
        }, opts);

    $('body').append(_.template(template_html, options));

    $('#tmp-modal').modal('show');

    $('#tmp-modal .btn-success').one('click', function (e) {
        close();
        options.successAction()
    });

    $('#tmp-modal .btn-default').one('click', function (e) {
        close();
        options.defaultAction()
    });

    $('#tmp-modal').one('hidden.bs.modal', function (e) {
        $('#tmp-modal').remove();
    })
};

var toggleLoading = function (operation) {
    var loading = $('#loading');

    if (!loading.length) {
        $('body').append(_.template($('#loading-template').html(), {}));
        loading = $('#loading');

        var dimensions = loading.getHiddenDimensions();
        loading.outerWidth(dimensions.width);
        loading.css({
            left: 0,
            margin: '0 auto'
        });

        // close loading
        $('#loading .icon-close').click(function (e) {
            toggleLoading();
            if (Nodeshot.currentXHR) {
                Nodeshot.currentXHR.abort();
            }
        });
    }

    if (operation == 'show') {
        loading.fadeIn(255);
    } else if (operation == 'hide') {
        loading.fadeOut(255);
    } else {
        loading.fadeToggle(255);
    }
};

$(document).ajaxSend(function (event, xhr, settings) {
    if(settings.url.indexOf('notifications') > -1){
        return;
    }
    toggleLoading('show');
    Nodeshot.currentXHR = xhr;
});

$(document).ajaxStop(function () {
    toggleLoading('hide');
});

// extend underscore with formatDateTime shortcut
_.formatDateTime = function(dateString){
    // TODO: format configurable
    return $.format.date(dateString, "dd MMMM yyyy, HH:mm");
};

// extend underscore with formatDate shortcut
_.formatDate = function(dateString){
    // TODO: format configurable
    return $.format.date(dateString, "dd MMMM yyyy");
};
