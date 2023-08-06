'use strict';


(function () {
	
    var app = angular.module('dynamicFormsFrameworkAdmin');
    
    /*
     * This controller handles the logic to create, edit and save a form.
     */    
    app.controller('statisticsCtrl', function ($scope, $http, $location, $window, $filter) {
    	
        var separator = '/';
        var stat = this;
    	stat.formId = ($location.search()).form;
        stat.versionNumber = ($location.search()).ver;
        stat.versionNumber = ($location.search()).ver;
        stat.versionNumber = ($location.search()).ver;
        stat.versionNumber = ($location.search()).ver;
        stat.json = '';

        stat.config = {
            title: '',
            tooltips: true,
            labels: false,
            mouseover: function() {},
            mouseout: function() {},
            click: function() {},
            legend: {
                display: true,
                // Could be 'left, right'
                position: 'right'
            }
        };

        stat.data = {
            series: [],
            data: [{
                x: '',
                y: []
            }]
        };
        
        stat.values = {};
        stat.filter_id = '';
        stat.filter_type = '';
        stat.filter_value = '';
        stat.path = '';

        stat.getStatistics = function(){
            if(stat.filter_id != '' && stat.filter_type != '' && stat.filter_value != ''){
                stat.path = stat.filter_id +'/' +stat.filter_type +'/'+ stat.filter_value;
            }else {
                stat.path = '';
            }
            $http.get('../statistics/'+stat.formId+'/'+stat.versionNumber+'/'+stat.path)
                .success(function(data){
                    stat.json = JSON.parse(JSON.stringify(data));
                    for(var field_id in stat.json){
                        var field = $.extend({}, stat.json[field_id]);
                        if (field.field_type == 'NumberField'){
                            var conf = angular.copy(stat.config);
                            conf.title = field.field_text;
                            var d = angular.copy(stat.data);
                            for(var i = 0; i < 5; i++){
                                d.data[i] = {
                                    'x': field.quintilesX[i],
                                    'y': [field.quintilesY[i]]
                                };
                            }
                            stat.values[field_id] = {
                                'id': field_id,
                                'chart': 'pie',
                                'field_type': 'NumberField',  
                                'conf': conf,
                                'data': d,
                                'm' : field.mean,
                                'mt' : field.total_mean,
                                'sd' : field.standard_deviation,
                                'sdt' : field.total_standard_deviation,
                                'tf' : field.total_filled,
                                'tnf': field.total_not_filled,
                                'req': field.required,
                                'type': 'Number'
                            };
                        } else if (field.field_type == 'SelectField'){
                            var conf = angular.copy(stat.config);
                            conf.title = field.field_text;
                            var d = angular.copy(stat.data);
                            for(var i = 0; i < field.total_per_option.length; i++){
                                d.data[i] = {
                                    'x': field.options[i],
                                    'y': [field.total_per_option[i]]
                                };
                            }
                            stat.values[field_id] = {
                                'id': field_id,
                                'chart': 'pie',
                                'field_type': 'SelectField',  
                                'conf': conf,
                                'data': d,
                                'tf' : field.total_filled,
                                'tnf': field.total_not_filled,
                                'req': field.required,
                                'type': 'Combobox'
                            };
                        } else if (field.field_type == 'CheckboxField'){
                            var conf = angular.copy(stat.config);
                            conf.title = field.field_text;
                            var d = angular.copy(stat.data);
                            for(var i = 0; i < field.total_per_option.length; i++){
                                d.data[i] = {
                                    'x': field.options[i],
                                    'y': [field.total_per_option[i]]
                                };
                            }
                            stat.values[field_id] = {
                                'id': field_id,
                                'chart': 'pie',
                                'field_type': 'CheckboxField',  
                                'conf': conf,
                                'data': d,
                                'tf' : field.total_filled,
                                'tnf': field.total_not_filled,
                                'req': field.required,
                                'type': 'Checkbox'
                            };
                        }
                                        
                    }
                })
                .error(function(data, status, headers, config){
                    alert('error loading statistics: ' + data);
                });
        };
     
        stat.getStatistics();
     
        stat.Discard = function(){
            stat.filter_id = '';
            stat.filter_type = '';
            stat.filter_value = '';
            stat.path = '';
            stat.getStatistics();
        };

        
        $scope.chart_types = [
            'pie',
            'bar',
        ];    

    });
})();
