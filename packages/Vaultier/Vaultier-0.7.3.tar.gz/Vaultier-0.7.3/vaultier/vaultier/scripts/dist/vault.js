Vaultier.VaultColorView = Ember.View.extend({
    layoutName: 'Vault/VaultColor',
    init: function () {
        if (this.get('value') == null) {
            this.set('value', 'blue');
        }
        this.prepareColorPicker();

        this._super();
    },
    prepareColorPicker: function () {
        var colorsAndSelected = [];
        Vaultier.Color.proto().colors.forEach(function (color) {
            colorsAndSelected.addObject({
                'value': color,
                'selected': color == this.get('value'),
                'css': (color == this.get('value')
                    ? 'color-picker-base vlt-background-' + color
                    : 'color-picker-base vlt-background-' + color + '-light')
            });
        }.bind(this));
        this.set('colors', colorsAndSelected);
    },
    actions: {
        changeColor: function (color) {
            this.set('value', Ember.get(color, 'value'));
            this.get('colors').forEach(function (color) {
                if (Ember.get(color, 'value') == this.get('value')) {
                    Ember.set(color, 'selected', 'selected');
                    Ember.set(color, 'css', 'color-picker-base vlt-background-' + color.value)
                } else {
                    Ember.set(color, 'selected', null);
                    Ember.set(color, 'css', 'color-picker-base vlt-background-' + color.value + '-light')
                }
            }.bind(this));
        }
    }
});


Vaultier.VaultsIndexRoute = Ember.Route.extend(
    Vaultier.WorkspaceKeysMixin,
    {

        beforeModel: function () {
            this.checkWorkspaceKeys();
        },

        model: function (params, queryParams) {
            var workspace = this.modelFor('Workspace');
            var store = this.get('store');

            // retrieve vaults
            var vaults = store.find('Vault', {workspace: workspace.get('id')});

            // load memberships
            var memberships = store
                .find('Role', {to_workspace: workspace.get('id') })
                .then(function (memberships) {
                    return memberships.toArray()
                });

            // return promise for all requests
            return Ember.RSVP.hash({
                vaults: vaults,
                memberships: memberships
            });
        },

        setupController: function (ctrl, model) {
            // set model
            ctrl.set('content', model.vaults);
            ctrl.set('memberships', model.memberships);

            // retrieve workspace
            var workspace = this.modelFor('Workspace');
            this.set('workspace', workspace);
            ctrl.set('workspace', workspace);

            // set breadcrumbs
            ctrl.set('breadcrumbs',
                Vaultier.Breadcrumbs.create({router: this.get('router'), environment: this.get('environment')})
                    .addHome()
                    .addWorkspace()
            );
        }

    });

Vaultier.VaultsIndexController = Ember.ArrayController.extend({
    breadcrumbs: null
});


Vaultier.VaultsIndexView = Ember.View.extend({
    templateName: 'Vault/VaultsIndex',
    layoutName: 'Layout/LayoutStandard'
});


Vaultier.VaultIndexItemView = Ember.View.extend({
    templateName: 'Vault/VaultsIndexItem',
    classNameBindings: ['selected:selected'],
    mouseEnter: function() {
        this.set('selected', 'selected');
    },
    mouseLeave: function() {
        this.set('selected', null);
    }
});


Vaultier.VaultsCreateRoute = Ember.Route.extend(
    Vaultier.WorkspaceKeysMixin,
    {

        beforeModel: function () {
            this.checkWorkspaceKeys();
        },

        model: function (params, transition) {

            var store = this.get('store');
            var workspace = this.modelFor('Workspace');

            if (!this.get('auth').checkPermissions(transition, function () {
                return workspace.get('perms.create')
            }.bind(this), true)) {
                return;
            }

            // create record
            var vault = store.createRecord('Vault');

                    // load memberships
            var memberships = store
                .find('Role', {to_workspace: workspace.get('id') })
                .then(function (memberships) {
                    return memberships.toArray()
                });

            // return promise for all requests
            return Ember.RSVP.hash({
                vault: vault,
                memberships: memberships
            });

        },

        actions: {
            save: function () {
                var workspace = this.get('workspace');
                var record = this.get('controller.content');
                record.set('workspace', this.get('workspace.id'));

                var promise = record
                    .saveRecord()
                    .then(function () {
                        $.notify('Your vault has been created successfully.', 'success');
                        this.transitionTo('Vault.index', record);
                    }.bind(this))
                    .catch(function (error) {
                        $.notify('Ooops! Something went wrong.', 'error');
                        this.get('errors').logError(error);
                    }.bind(this));

                ApplicationLoader.promise(promise);
            }
        },

        setupController: function (ctrl, model) {
             // set model
            ctrl.set('content', model.vault);
            ctrl.set('memberships', model.memberships);

            // retrieve workspace
            var workspace = this.modelFor('Workspace');
            this.set('workspace', workspace);
            this.get('controller').set('workspace', workspace);

            // set breadcrumbs
            ctrl.set('breadcrumbs',
                Vaultier.Breadcrumbs.create({router: this.get('router'), environment: this.get('environment')})
                    .addHome()
                    .addWorkspace()
                    .addText('Create new vault')
            );

        }
    });

Vaultier.VaultsCreateController = Ember.ObjectController.extend({
    workspace: null,
    breadcrumbs: null,
    env: null
});

Vaultier.VaultsCreateView = Ember.View.extend({
    templateName: 'Vault/VaultsCreate',
    layoutName: 'Layout/LayoutStandard'
});


Vaultier.VaultRoute = Ember.Route.extend(
    Vaultier.WorkspaceKeysMixin,
    {
        model: function (params, transition) {
            workspace = this.modelFor('Workspace');
            model = this.get('store')
                .find('Vault', params.vault)
                .then(function (model) {
                    if (model.get('workspace') != workspace.get('id')) {
                        var error = new Error();
                        error.status = 404;
                        throw error;
                    }
                    return model;
                });
            return model;
        },

        afterModel: function (vault) {
            var environment = this.get('environment');
            environment.set('vault', vault);
            this.checkWorkspaceKeys();
        },

        serialize: function (model) {
            // primitives
            if (typeof model == 'string' || typeof model == 'number') {
                return model;
            }

            return {
                vault: model.get('slug')
            };
        },

        actions: {
            deleteVault: function (vault) {
                Vaultier.confirmModal(this, 'Are you sure?', function () {
                    var promise = vault
                        .deleteRecord()
                        .then(
                            function () {
                                $.notify('Your vault has been deleted successfully.', 'success');
                                this.transitionTo('Workspace.index');
                            }.bind(this),
                            function (error) {
                                $.notify('Ooops! Something went wrong.', 'error');
                            }.bind(this)
                        );
                    ApplicationLoader.promise(promise);

                }.bind(this));

            }

        }

    });

Vaultier.VaultIndexRoute = Ember.Route.extend(
    Vaultier.WorkspaceKeysMixin,
    {
        beforeModel: function () {
            if (this.checkWorkspaceKeys()) {
                this.transitionTo('Cards.index');
            }
        }
    });


Vaultier.VaultEditRoute = Ember.Route.extend(
    Vaultier.WorkspaceKeysMixin,
    {

        beforeModel: function() {
            this.checkWorkspaceKeys();
        },

        model: function (params, transition) {
            var vault = this.modelFor('Vault');

            if (!this.get('auth').checkPermissions(transition, function () {
                return vault.get('perms.update');
            }.bind(this), true)) {
                return;
            }

            return vault
        },

        setupController: function (ctrl, model) {
            this._super(ctrl, model);

            var environment = this.get('environment');
            environment.set('vault', model);
            // set breadcrumbs
            ctrl.set('breadcrumbs',
                Vaultier.Breadcrumbs.create({router: this.get('router'), environment: environment})
                    .addHome()
                    .addWorkspace()
                    .addVault()
                    .addText('Edit vault')
            )
        },

        actions: {
            save: function () {
                var record = this.get('controller.content');
                var promise = record
                    .saveRecord()
                    .then(function () {
                        $.notify('Your changes has been saved successfully.', 'success');
                        history.go(-1);
                    }.bind(this))
                    .catch(function (error) {
                        $.notify('Ooops! Something went wrong.', 'error');
                        this.get('errors').logError(error)
                    }.bind(this))

                 ApplicationLoader.promise(promise);
            }
        }

    });

Vaultier.VaultEditController = Ember.ObjectController.extend({
    breadcrumbs: null
});

Vaultier.VaultEditView = Ember.View.extend({
    templateName: 'Vault/VaultEdit',
    layoutName: 'Layout/LayoutStandard'
});


Vaultier.VaultRolesAdminIndexRoute = Vaultier.RolesAdminIndexRoute.extend(
    Vaultier.WorkspaceKeysMixin,
    {
        beforeModel: function () {
            this.checkWorkspaceKeys();
        },

        setupInviteData: function (params) {
            var vault = this.modelFor('Vault');
            return {
                inviteObject: vault
            }
        },

        setupBlocks: function () {
            return {workspace: true, vault: true}
        },

        setupBreadcrumbs: function () {
            return Vaultier.Breadcrumbs.create({router: this.get('router'), environment: this.get('environment')})
                .addHome()
                .addWorkspace()
                .addVault()
                .addRolesAdminIndex('Vault.rolesAdminIndex');
        },

        setupInviteRoute: function (models) {
            return {
                inviteRouteName: 'Vault.rolesAdminInvite'
            };
        }

    });


Vaultier.VaultRolesAdminIndexController = Vaultier.RolesAdminIndexController.extend({
});


Vaultier.VaultRolesAdminInviteRoute = Vaultier.RolesAdminInviteRoute.extend(
    Vaultier.WorkspaceKeysMixin,
    {

        beforeModel: function () {
            this.checkWorkspaceKeys();
        },

        /**
         * override this to setup invite workspace and invite to object
         */
        setupInviteData: function (params) {
            var vault = this.modelFor('Vault');
            var workspace = this.modelFor('Workspace');
            return {
                inviteObject: vault,
                inviteParams: { to_vault: vault},
                inviteWorkspace: workspace
            }
        },

        setupBreadcrumbs: function () {
            return Vaultier.Breadcrumbs.create({router: this.get('router'), environment: this.get('environment')})
                .addHome()
                .addWorkspace()
                .addVault()
                .addRolesAdminIndex('Vault.rolesAdminIndex')
                .addRolesAdminInvite('Vault.rolesAdminInvite');
        }

    });

Vaultier.VaultRolesAdminInviteController = Vaultier.RolesAdminInviteController.extend({
});


//# sourceMappingURL=vault.js.map