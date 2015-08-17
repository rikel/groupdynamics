'use strict';

/**
 * @ngdoc function
 * @name frontendApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the frontendApp
 */
angular.module('frontendApp')
  .controller('MainCtrl', ['$scope', '$upload','$location', function($scope, $upload, $location) {
  	$scope.fileUploaded = false;
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
				$scope.data = data;
				var users = [];
				var messages = []
				for (var key in data) {
  					if (data.hasOwnProperty(key)) {
    					users.push(key);
    					messages.push(data[key])
  					}
				}
				$scope.highchartsNG = {
        			options: {
            			chart: {
                			type: 'bar'
            			},
            			xAxis: {
            				categories: users,
        				},
        			},
        			series: [{
            			data: messages
        			}],
        			title: {
            			text: 'Hello'
        			},
        			loading: false
    				}
			}).then(function(){
				$scope.selectedFiles = null;
				$scope.fileUploaded = true;
			});
		}
	}
}]);