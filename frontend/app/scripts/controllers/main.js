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
				var messages = [];
				
				//abs.NrOfMsg needed for PieChart
				var absNrOfMsg = 0;
				//get data for pie chart
				var pieData =  [];
				
				
				for (var key in data) {
  					if (data.hasOwnProperty(key)) {
    					users.push(key);	
    					messages.push(data[key]);
    					absNrOfMsg += data[key];
  					}
				}
			
				
				for (var key in data) {
  					if (data.hasOwnProperty(key)) {
  						var percentage = data[key]/absNrOfMsg*100;
  						var n = percentage.toFixed(2);
  						var percentageFixed = parseFloat(n);
						
  						var pieUser = 
  						
  						{
			                name: key,
			                y: percentageFixed
        				 }
    					pieData.push(pieUser);
  					}
				}
				console.log(data);
				console.log(messages);
				console.log(pieData);

				
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
    			
    			
    			$scope.highchartsNG2 = {
        			
            			chart: {
            				plotBackgroundColor: null,
				            plotBorderWidth: null,
				            plotShadow: false,
				            type: 'pie'
            			},
            			title: {
        					text: 'Absolute message share per user'
            			},
            			
            			tooltip: {
				            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
				        },
				        plotOptions: {
				            pie: {
				                allowPointSelect: true,
				                cursor: 'pointer',
				                dataLabels: {
				                    enabled: true,
				                    format: '<b>{point.name}</b>: {point.percentage:.1f} %',
				                    style: {
				                        color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
				                    }
				                }
				            }
				        },
				        
				        series: [{
				        	name: "% of messages",
				            colorByPoint: true,
            				data: pieData
            			
        				}]
        			
    			}
    				
    				
    				
			}).then(function(){
				$scope.selectedFiles = null;
				$scope.fileUploaded = true;
			});
		}
	}
}]);