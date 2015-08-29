"use strict";function getChartConfig(a,b){b.post("/api/getconfig",{url_id:a.url_id}).success(function(b,c,d,e){a.data=b,a.fileUploaded=!0}).error(function(b,c,d,e){a.fileUploaded=!1,console.log(b)})}angular.module("frontendApp",["ngAnimate","ngCookies","ngResource","ngRoute","ngSanitize","ngTouch","angularFileUpload","highcharts-ng"]).config(["$routeProvider","$locationProvider",function(a,b){a.when("/",{templateUrl:"views/main.html",controller:"MainCtrl",controllerAs:"main"}).when("/:url_id",{templateUrl:"views/main.html",controller:"MainCtrl",controllerAs:"main"}).otherwise({redirectTo:"/"})}]),angular.module("frontendApp").controller("MainCtrl",["$scope","$upload","$routeParams","$location","$http",function(a,b,c,d,e){"undefined"!=typeof c.url_id?(a.url_id=c.url_id,getChartConfig(a,e)):(a.url_id=null,a.fileUploaded=!1),a.gotoBottom=function(){var a=d.hash();d.hash("help"),console.log("in scroll function"),$anchorScroll(),d.hash(a)},a.onFileSelect=function(c){a.selectedFiles=c,a.progress=[];for(var e=0;e<c.length;e++){var f=c[e];a.upload=b.upload({url:"/api/uploadChat",method:"POST",data:{url_id:a.url_id},file:f}).progress(function(b){a.progress[e-1]=Math.min(100,parseInt(100*b.loaded/b.total))}).success(function(b,c,e,f){a.data=b;var g="Nr. of Messages: "+a.data.number_of_messages+"; Nr. of People: "+a.data.number_of_users;ga("send","event","SuccesfullUpload","click",g),console.log("Success"),d.path("/"+b.url_id)}).then(function(){a.selectedFiles=null,a.fileUploaded=!0,setTimeout(function(){$(window).resize()},500)})}}}]),angular.module("frontendApp").run(["$templateCache",function(a){a.put("views/about.html","<p>This is the about view.</p>"),a.put("views/analysis.html","<p>This is the analysis view.</p>"),a.put("views/main.html",'<div class="container-fluid"> <div ng-if="fileUploaded == false"> <div class="row"> <div class="col-md-offset-3 col-md-6 text-center header"> <h1>#<b>group</b>Stats.io</h1> <div> <h4>Understand your friends. Use your Whatsapp chat history.</h4> </div> <div class="btn bg-primary btn-lg" ng-file-select="onFileSelect($files,$scope)">Upload your Chat </div> <div> <a ng-click="gotoBottom()">How it works</a> / <a href="/#/f3e2ccd8-2206-4d79-a1fb-4ec1eada0ebc">See an example</a> </div> </div> </div> <!-- Services --> <!-- The circle icons use Font Awesome\'s stacked icon classes. For more information, visit http://fontawesome.io/examples/ --> <section id="help"> <div class="row text-center"> <div class="col-md-12 text-center services bg-primary"> <h2>How it works</h2> <hr class="small"> <div class="row"> <div class="col-md-4 col-sm-12"> <div class="service-item"> <h4> <strong>Step 1: Export</strong> </h4> <p> Open the WhatsApp chat that you want to analyze. Find the "Email Chat" action and send it to you. </p> </div> </div> <div class="col-md-4 col-sm-12"> <div class="service-item"> <h4> <strong>Step 2: Save</strong> </h4> <p> Open the email that you sent in Step 1 and save the attached txt file. Note: We DON\'T save any of your uploaded data. </p> </div> </div> <div class="col-md-4 col-sm-12"> <div class="service-item"> <h4> <strong>Step 3: Upload</strong> </h4> <p> Upload the text file that you saved in Step 2 on this website. </p> </div> </div> </div> </div> </div> </section> </div> <!--<div ng-if="fileUploaded == true">--> <!--    <header id="top" class="header">--> <!--        <div class="row">--> <!--            <div class="col-md-12">--> <!--                #<b>group</b>Stats.io--> <!--                <div class="btn bg-primary btn-md" ng-file-select="onFileSelect($files,$scope)">Upload another Chat--> <!--                </div>--> <!--            </div>--> <!--        </div>--> <!--    </header>--> <!--</div>--> <!--   <div align="left">\n    <h2>#<b>Group</b>Dynamics</h2><p> Understand your friends using your Whatsapp chat history! </p>\n    <br>\n    <div class="btn btn-lg btn-primary" ng-file-select="onFileSelect($files,$scope)">Upload Chat File</div>\n  </div> --> <!-- <div class="jumbotron"> --> <!--   <div>\n    <div>\n      <h1>#<b>Group</b>Dynamics</h1>\n      <p class="lead">\n        <!-<img src="images/yeoman.8cb970fb.png" alt="I\'m Yeoman">--> <!-- <br>\n        Understand your friends using your Whatsapp chat history!\n      </p>\n      <p>\n        <div class="btn btn-lg btn-primary" ng-file-select="onFileSelect($files,$scope)">Upload Chat File</div>\n      </p>\n    </div>\n  </div> --> <div ng-if="fileUploaded == true"> <div class="row"> <div class="col-md-offset-3 col-md-6 text-center header2"> <h1>#<b>group</b>Stats.io</h1> <div> <h4>Understand your friends. Use your Whatsapp chat history.</h4> </div> <div class="btn bg-primary btn-lg" ng-file-select="onFileSelect($files,$scope)">Upload another Chat </div> </div> </div> <section> <div class="row"> <div class="col-md-offset-2 col-md-8 services2"> <div ng-repeat="chartConfig in data.charts"> <highchart config="data.charts[$index]"></highchart> <br> </div> </div> </div> <div class="row"> <div class="col-md-offset-2 col-md-8 services2 text-center"> <a href="whatsapp://send" data-text="Look at our chat analysis!" data-ng-href="http://groupstats.io/#/{{url_id}}" class="btn btn-success btn-lg"><i class="fa fa-whatsapp"></i> Share on Whatsapp</a> <div class="btn bg-primary btn-lg" ng-file-select="onFileSelect($files,$scope)">Analyze another Chat</div> </div> </div> </section> </div> </div>')}]);