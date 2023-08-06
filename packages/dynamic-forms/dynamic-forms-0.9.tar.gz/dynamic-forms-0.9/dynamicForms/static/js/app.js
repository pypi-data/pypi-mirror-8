'use strict';

(function () {
    /*
    * Module dynamicFormsFramework
    * This module encapsulates the logic that will handle the form.
    */
    var app = angular.module('dynamicFormsFrameworkAdmin', ['ui.sortable','ui.bootstrap','checklist-model','angularCharts'])
    .config(['$locationProvider', '$httpProvider', function ($locationProvider, $httpProvider) {

        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
		$httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
     
    }]);
    
    app.directive('ngConfirmClick', [function(){
		return {
	  		priority: -1,
	  		restrict: 'A',
	  		link: function(scope, element, attrs){
	    		element.bind('click', function(e){
	      			var message = attrs.ngConfirmClick;
	      			if(message && !confirm(message)){
	        			e.stopImmediatePropagation();
	        			e.preventDefault();
	      			}
	    		});
	  		}
		}
	}]);

})();
