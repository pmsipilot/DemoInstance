	// create the module and name it demoApp
	var demoApp = angular.module('demoApp', [
        'ngRoute', 'ngCookies','pascalprecht.translate',
        'ui.slider', 'ngTable', 'xeditable'
    ])
        .run(function($rootScope, favicoService, $http, $cookies, $location){
            $rootScope.$on('$routeChangeStart',function(){
                $rootScope.app_title = 'DemoInstance';
                favicoService.reset();
            });

            $rootScope.user = {};
            $rootScope.getUser = function(callback) {
                $http.get('/api/user').
                    success(function(data) {
                        $rootScope.user = data;
                    });
            };

            $rootScope.disconnect = function() {
                $cookies.token = undefined;
                $rootScope.user = {}
                $location.path('/');
            };
            $rootScope.getUser();
        });

	// configure our routes
	demoApp.config(function($routeProvider) {
		$routeProvider
			.when('/', {
				templateUrl : 'pages/image.html'
			})

            .when('/mail', {
                templateUrl : 'pages/login_mail.html'
            })

            .when('/auth', {
                templateUrl : 'pages/login_auth.html'
            })

            .when('/login/:token', {
                controller : function($routeParams, $cookies, $location, $rootScope){
                    $cookies.token = $routeParams.token;
                    $rootScope.getUser();
                },
                template : ''
            })

            .when('/list', {
                templateUrl : 'pages/list.html'
            })
        
            .when('/admin', {
                templateUrl : 'pages/admin.html'
            })

            .when('/instance/:image_name', {
                templateUrl : 'pages/instance.html'
            })

            .when('/instance/:image_name/:id', {
                templateUrl : 'pages/instance.html'
            })

			.when('/instance', {
				templateUrl : 'pages/instance.html'
			});
	});



    demoApp.config(function ($translateProvider, $httpProvider) {

        $httpProvider.interceptors.push(['$location','$q',function($location, $q) {
            return {
                'responseError': function(rejection) {
                    if ( rejection.status == 401 ){
                        if ( rejection.data.type == 'auth' )
                            $location.path('/auth');
                        else
                            $location.path('/mail');
                    }
                    return $q.reject(rejection);
                }
            };
        }]);

        $translateProvider.translations('en', {
            NEW_INSTANCE: 'Instances',
            CREATING_INSTANCE: 'Creating instance',
            DESTROYING_INSTANCE: 'Your instance will be permanently destroyed',
            STARTING_INSTANCE: 'Starting instance',
            STARTING_SYSTEM: 'Starting system',
            CREATE_INSTANCE_OF: 'Create instance of ',
            ABOUT: 'About',
            YOU_CAN_CONNECT: 'You can connect to',
            YOUR_INSTANCE_FINISH:'Your instance will be destroy in ',
            ARE_YOU_SURE:'Are you sure ?',
            FOR:'for',
            ERROR:'ERROR',
            USER:'User',

            TIME:'Time',
            ADD_TIME:'Extend lifetime (min.)',
            SUBMIT: 'Submit',
            CANCEL: 'Cancel',
            DESTROY: 'Destroy instance',

            LOGIN:'Please log in',
            DISCONNECT: 'disconnect',
            ADMINISTRATION:'Administration',
            LIST_INSTANCE:'History',
            EMAIL_SEND:'SEND',
            EMAIL_INFO:'An email will be send with your link',
            RETURN_HOME : 'Return Home',

            INSTANCE_LAUNCHED_AT: 'Startup time',
            INSTANCE_LIFE_TIME: 'Life time  (min.)',
            INSTANCE_DEAD_TIME: 'Time before remove (min.)',
            INSTANCE_ACTIONS: 'Actions',

            INSTANCE_TYPE : 'Type',
            INSTANCE_STATUS : 'Status',
            INSTANCE_DELETED: 'Deleted',
            INSTANCE_CREATED: 'Instance created',
            INSTANCE_DONE: 'Application running',
            INSTANCE_UP : 'Instance running',
            INSTANCE_POOL: 'Waiting'
        });
        $translateProvider.translations('fr', {
            NEW_INSTANCE: 'Instances',
            CREATING_INSTANCE: 'Cr&eacute;ation de votre environnement de d&eacute;monstration',
            DESTROYING_INSTANCE: 'Votre instance sera détruite pour toujours',
            STARTING_INSTANCE: 'D&eacute;marrage de votre environnement de d&eacute;monstration',
            STARTING_SYSTEM: 'Configuration de votre environnement de d&eacute;monstration',
            CREATE_INSTANCE_OF: 'Cr&eacute;ation de l\'instance ',
            ABOUT: 'A propos',
            YOU_CAN_CONNECT: 'Vous pouvez vous connecter à ',
            YOUR_INSTANCE_FINISH:'Votre instance se terminera dans ',
            ARE_YOU_SURE:'Etes vous sur ?',
            FOR:'pour',
            ERROR:'ERREUR',
            USER:'Utilisateur',

            TIME:'Temps',
            ADD_TIME: 'Prolonger (min.)',
            SUBMIT: 'Valider',
            CANCEL: 'Annuler',
            DESTROY: 'Détruire l\'instance',

            LOGIN:'Connectez vous',
            DISCONNECT: 'Déconnection',
            ADMINISTRATION:'Administration',
            LIST_INSTANCE:'Historique',
            EMAIL_SEND:'Envoyer',
            EMAIL_INFO:'Un email va vous être envoyé avec votre lien pour vous connecter',
            RETURN_HOME : 'Retourner à l\' accueil',

            INSTANCE_LAUNCHED_AT: 'Jour / heure de démarrage',
            INSTANCE_LIFE_TIME: 'Durée de vie (min.)',
            INSTANCE_DEAD_TIME: 'Durée avant destruction (min.)',
            INSTANCE_ACTIONS: 'Actions',

            INSTANCE_TYPE : 'Type',
            INSTANCE_STATUS : 'Etat',
            INSTANCE_DELETED: 'Supprimée',
            INSTANCE_CREATED: 'Instance démarrée',
            INSTANCE_DONE: 'Application démarrée',
            INSTANCE_UP : 'Instance en cours',
            INSTANCE_POOL: 'En attente'
        });
        $translateProvider.preferredLanguage('fr');
    });
