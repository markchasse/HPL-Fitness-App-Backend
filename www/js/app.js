angular.module('starter', ['ionic', 'starter.controllers', 'services'])

.run(function($ionicPlatform) {
	$ionicPlatform.ready(function() {
		if (window.cordova && window.cordova.plugins && window.cordova.plugins.Keyboard) {
			cordova.plugins.Keyboard.hideKeyboardAccessoryBar(true);
			cordova.plugins.Keyboard.disableScroll(true);
		}
		if (window.StatusBar) {
			StatusBar.styleLightContent();
		}
	});
})

.config(function($stateProvider, $urlRouterProvider) {
	$stateProvider
	.state('register', {
		url: '/',
		templateUrl: 'templates/registeration.html',
		controller: 'registrationCtrl as vm'
	})
	.state('subscribe', {
		url: '/subscribe',
		templateUrl: 'templates/subscription.html',
		controller: 'subscriptionCtrl as vm'
	})
	.state('success', {
		url: '/success',
		templateUrl: 'templates/success.html',
		controller: 'successCtrl as vm'
	});
	$urlRouterProvider.otherwise('/');
});
