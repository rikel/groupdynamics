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
				data: {},
				file: file
			}).progress(function(evt) {
				$scope.progress[i-1] = Math.min(100, parseInt(100.0 * evt.loaded / evt.total));
			}).success(function(data, status, headers, config) {
				$scope.data = data;
				// console.log("datasize: " + data.size);
				// console.log("length: " + data.length);
				// console.log(data);

				var label = 'Nr. of Messages: ' + $scope.data.number_of_messages + '; Nr. of People: ' + $scope.data.number_of_users;
				//adding GoogleAnalytics Event
			     ga('send', 'event', 'SuccesfullUpload', 'click', label);
				 console.log("Success");
			}).then(function(){
				$scope.selectedFiles = null;
				$scope.fileUploaded = true;
			});
		}
	}
}]);