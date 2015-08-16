'use strict';

/**
 * @ngdoc function
 * @name frontendApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the frontendApp
 */
angular.module('frontendApp')
  .controller('MainCtrl', function($scope, $upload, $location) {
    $scope.onFileSelect = function($files) {
		//$files: an array of files selected, each file has name, size, and type.
		$scope.selectedFiles = $files;
		$scope.progress = [];
		for (var i = 0; i < $files.length; i++) {
			var file = $files[i];
			$scope.upload = $upload.upload({
				url: '/api/uploadChat',
				method: 'POST',
				//headers: {'header-key': 'header-value'},
				//withCredentials: true,
				data: {},
				file: file
			}).progress(function(evt) {
				$scope.progress[i-1] = Math.min(100, parseInt(100.0 * evt.loaded / evt.total));
			}).success(function(data, status, headers, config) {
				// file is uploaded successfully
			}).then(function(){
				$scope.selectedFiles = null;
			});
		}
	}
});