(function () {
	'use strict';

	angular
		.module('services', [])
		.factory('requestManager', requestManager);

	requestManager.$inject = ['$http','$q','$ionicLoading'];

	/* @ngInject */
	function requestManager($http,$q,$ionicLoading,config) {
		return {
			post: post
		};

		////////////////

		function post(url, data) {
			$ionicLoading.show();
			var deferred = $q.defer();
			$http({	
				method: 'post',
				url: url,
				data: data
			}).success(function (data) {
				deferred.resolve(data);
				$ionicLoading.hide();
			}).error(function (data) {
				deferred.reject(data);
				$ionicLoading.hide();
			});
			return deferred.promise;
		}
	}
})();