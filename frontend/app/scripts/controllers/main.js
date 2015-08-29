'use strict';

/**
 * @ngdoc function
 * @name frontendApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the frontendApp
 */
angular.module('frontendApp')
  .controller('MainCtrl', ['$scope', '$upload','$routeParams', '$location','$http', 
  	function($scope, $upload, $routeParams, $location, $http) {
  		if (typeof $routeParams.url_id !== 'undefined' ){
  			$scope.url_id = $routeParams.url_id;
  			getChartConfig($scope,$http);
  			$scope.encodedUrl = encodeURIComponent('Check our chat stats: ' + 'http://groupstats.io/#/' + $scope.url_id)
  		} else {
  			$scope.url_id = null;
  			$scope.fileUploaded = false;
  		}

  	
  	 	$scope.gotoBottom = function() {
      	// set the location.hash to the id of
      	// the element you wish to scroll to
      
	  	var old = $location.hash();

      $location.hash('help');
      console.log("in scroll function");

      // call $anchorScroll()
      $anchorScroll();
      
      //reset to old to keep any additional routing logic from kicking in
      $location.hash(old);

    };
    
    $scope.onFileSelect = function($files) {
    
   
     
		//$files: an array of files selected, each file has name, size, and type.
		$scope.selectedFiles = $files;
		$scope.progress = [];
		for (var i = 0; i < $files.length; i++) {
			var file = $files[i];
			$scope.upload = $upload.upload({
				url: '/api/uploadChat',
				method: 'POST',
				data: {'url_id': $scope.url_id},
				file: file
			}).progress(function(evt) {
				$scope.progress[i-1] = Math.min(100, parseInt(100.0 * evt.loaded / evt.total));
			}).success(function(data, status, headers, config) {
				$scope.data = data;

				var label = 'Nr. of Messages: ' + $scope.data.number_of_messages + '; Nr. of People: ' + $scope.data.number_of_users;
				//adding GoogleAnalytics Event
			     ga('send', 'event', 'SuccesfullUpload', 'click', label);
				 console.log("Success");
				 $location.path('/'+data.url_id);
			}).then(function(){
				//Not sure any of this gets executed.
				$scope.selectedFiles = null;
				$scope.fileUploaded = true;
				setTimeout(function(){ 	$(window).resize();}, 500);
			});
		}
	}
}]);

function getChartConfig($scope,$http){
	$http.post('/api/getconfig',{'url_id':$scope.url_id})
	.success(function(data,status,headers,config){
		$scope.data = data;
		$scope.fileUploaded = true;
	})
	.error(function(data,status,headers,config){
		$scope.fileUploaded = false;
		console.log(data);
	});
}