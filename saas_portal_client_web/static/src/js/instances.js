odoo.define('saas_portal_client_web.instances', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');
    var core = require('web.core');
    var rpc = require('web.rpc');

    var _t = core._t;

    publicWidget.registry.SaasInstances = publicWidget.Widget.extend({
        selector: '.saas-instances-container',
        events: {
            'click .load-more': '_onLoadMore',
            'click .reload-instances': '_onReload',
        },

        /**
         * @override
         */
        start: function () {
            this.page = 1;
            this.limit = 20;
            this.loading = false;
            this.loadInstances();
            return this._super.apply(this, arguments);
        },

        loadInstances: function () {
            var self = this;
            
            if (this.loading) {
                return;
            }
            
            this.loading = true;
            this._showLoader();
            
            rpc.query({
                route: '/saas_portal/api/instances',
                params: {
                    page: this.page,
                    limit: this.limit,
                }
            }).then(function (data) {
                self.loading = false;
                self._hideLoader();
                
                if (self.page === 1) {
                    self._renderInstances(data.instances);
                } else {
                    self._appendInstances(data.instances);
                }
                
                self._updatePager(data);
                self._updateLoadMore(data);
            }).catch(function (error) {
                self.loading = false;
                self._hideLoader();
                self._showError(_t('Erreur lors du chargement des instances'));
            });
        },

        _renderInstances: function (instances) {
            var $container = this.$('.instances-list');
            if (!$container.length) {
                return;
            }
            
            $container.empty();
            
            if (instances.length === 0) {
                $container.html('<p>' + _t('Aucune instance disponible') + '</p>');
                return;
            }
            
            var html = '';
            instances.forEach(function (instance) {
                var expiredClass = instance.expired ? 'text-danger' : '';
                var expiredBadge = instance.expired 
                    ? '<span class="badge badge-danger"><i class="fa fa-clock-o"></i> Expiré</span>' 
                    : '';
                
                html += '<tr class="' + expiredClass + '">';
                html += '<td><a href="/my/domain/' + instance.id + '">' + instance.name + '</a></td>';
                html += '<td>' + (instance.plan_name || '') + '</td>';
                html += '<td>' + (instance.expiration_datetime ? new Date(instance.expiration_datetime).toLocaleDateString() : '') + '</td>';
                html += '<td>' + expiredBadge + '</td>';
                html += '</tr>';
            });
            
            $container.html(html);
        },

        _appendInstances: function (instances) {
            var $container = this.$('.instances-list');
            instances.forEach(function (instance) {
                var expiredClass = instance.expired ? 'text-danger' : '';
                var expiredBadge = instance.expired 
                    ? '<span class="badge badge-danger"><i class="fa fa-clock-o"></i> Expiré</span>' 
                    : '';
                
                var html = '<tr class="' + expiredClass + '">';
                html += '<td><a href="/my/domain/' + instance.id + '">' + instance.name + '</a></td>';
                html += '<td>' + (instance.plan_name || '') + '</td>';
                html += '<td>' + (instance.expiration_datetime ? new Date(instance.expiration_datetime).toLocaleDateString() : '') + '</td>';
                html += '<td>' + expiredBadge + '</td>';
                html += '</tr>';
                $container.append(html);
            });
        },

        _updatePager: function (data) {
            var $pager = this.$('.instances-pager');
            if (!$pager.length) {
                return;
            }
            
            var html = '';
            if (data.pages > 1) {
                html += '<nav aria-label="Pagination">';
                html += '<ul class="pagination">';
                
                // Bouton précédent
                if (data.page > 1) {
                    html += '<li class="page-item"><a class="page-link" href="#" data-page="' + (data.page - 1) + '">Précédent</a></li>';
                }
                
                // Pages
                for (var i = 1; i <= data.pages; i++) {
                    var active = i === data.page ? 'active' : '';
                    html += '<li class="page-item ' + active + '"><a class="page-link" href="#" data-page="' + i + '">' + i + '</a></li>';
                }
                
                // Bouton suivant
                if (data.page < data.pages) {
                    html += '<li class="page-item"><a class="page-link" href="#" data-page="' + (data.page + 1) + '">Suivant</a></li>';
                }
                
                html += '</ul>';
                html += '</nav>';
            }
            
            $pager.html(html);
            
            // Gérer les clics sur les pages
            var self = this;
            $pager.on('click', '.page-link', function (e) {
                e.preventDefault();
                var page = parseInt($(this).data('page'));
                if (page && page !== self.page) {
                    self.page = page;
                    self.loadInstances();
                    // Scroll vers le haut
                    $('html, body').animate({scrollTop: 0}, 300);
                }
            });
        },

        _updateLoadMore: function (data) {
            var $loadMore = this.$('.load-more-container');
            if (!$loadMore.length) {
                return;
            }
            
            if (data.page < data.pages) {
                $loadMore.show();
            } else {
                $loadMore.hide();
            }
        },

        _showLoader: function () {
            var $loader = this.$('.instances-loader');
            if ($loader.length) {
                $loader.show();
            } else {
                this.$('.instances-list').before('<div class="instances-loader text-center"><i class="fa fa-spinner fa-spin"></i> Chargement...</div>');
            }
        },

        _hideLoader: function () {
            this.$('.instances-loader').hide();
        },

        _showError: function (message) {
            var $error = this.$('.instances-error');
            if ($error.length) {
                $error.text(message).show();
            } else {
                this.$('.instances-list').before('<div class="instances-error alert alert-danger">' + message + '</div>');
            }
        },

        _onLoadMore: function (e) {
            e.preventDefault();
            this.page++;
            this.loadInstances();
        },

        _onReload: function (e) {
            e.preventDefault();
            this.page = 1;
            this.loadInstances();
        },
    });

    return publicWidget.registry.SaasInstances;
});

