'use strict';

(function () {
	
    var app = angular.module('dynamicFormsFrameworkAdmin', []);
    
    /*
     * This controller handles the logic to create, edit and save a form.
     */    
    app.controller('ResponsesCtrl', function ($scope, $http, $location) {

    	var responses = this;
    	responses.formId = ($location.search()).form;
        responses.versionNumber = ($location.search()).ver;
        responses.json = '';

        responses.getResponses = function(){
            $http.get(responses.formId+'/'+ responses.versionNumber+'/')
            .success(function(data){
                responses.json = data;
            })
            .error(function(data, status, headers, config){
                alert(data + status);
            });
        };

        // Calls the function getResponses
        responses.getResponses();
 		responses.isFile = function(field){
            var re = new RegExp('FileField');
            var infoFile =  /\[.*\].*:(.*)/g.exec(field);
            var res = '';
            res = re.exec(field);
            return res != null && infoFile[1] != ' ';
            
        };

        responses.fieldResponse=function(field){
        
             var infoFile =  /\[.*\](.*)/g.exec(field);
             return infoFile[1];
        };

        responses.downloadLink=function(field){
            var infoFile =  /.*,(\d*),(\d*)/g.exec(field);
            var field_id = infoFile[1];
            var entry = infoFile[2];
            return 'download/'+field_id+'/'+ entry+'/';
        };

    });

})();
