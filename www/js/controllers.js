angular.module('starter.controllers', [])

.controller('registrationCtrl', function ($state, requestManager) {
	/* jshint validthis: true */
	var vm = this;

	vm.activate = activate;
	vm.title = 'Sign Up';
	vm.student = {};

	activate();

	////////////////

	function activate() {
		vm.register = function(form){
			if (form.$valid) {
				delete vm.student.confirmPassword;
				console.log(vm.student);
				var url = 'http://hpl-fitnessapp-env.elasticbeanstalk.com/accounts/register/'
				requestManager.post(url, vm.student)
					.then(function (response) {
						console.log(response);
						$state.go("subscribe");
					})
					.catch(
					function (error) {
						vm.message = error.message;
					}
				);
			}
		};
	}
})

.controller('subscriptionCtrl', function ($state, $ionicLoading, requestManager) {
	/* jshint validthis: true */
	var vm = this;

	vm.activate = activate;
	vm.title = 'Subscription';
	vm.subscribe_data = {};
	vm.subscribe_data.plan = "Basic";

	activate();

	////////////////

	function stripeResponseHandler (status, response) {
		$ionicLoading.hide();
		if (response.error) {
			vm.message = response.error.message;
		} else {
			var token = response.id;
			console.log(token);

			$state.go('success');
		}
	}

	function activate() {
		vm.register = function(form){
			if (form.$valid) {
				console.log(vm.subscribe_data);
				console.log(form);
				Stripe.setPublishableKey('pk_test_6fdAKju4gJMWLdGuOYzI2i2j');
				$ionicLoading.show();
				Stripe.card.createToken(vm.subscribe_data, stripeResponseHandler);
			}
		};
	}
})

.controller('successCtrl', function () {
	/* jshint validthis: true */
	var vm = this;
	vm.title = 'Success';

	vm.close = function () {
		ionic.Platform.exitApp();
	}
});
