module.exports = function(grunt) {
    require('load-grunt-tasks')(grunt);

    grunt.initConfig({
        clean: ['public'],
        concat: {
            js_application: {
                src: [
                    'script.js',
                    'js/service/*.js',
                    'js/controller/*.js'
                ],
                dest: 'public/js/app.js',
                options: {
                    banner: ";(function(window, undefined){\n",
                    footer: "\n}(window));"
                }
            },
            js_vendors: {
                src: [
                    'bower_components/jquery/dist/jquery.js',
                    'bower_components/angular/angular.js',
                    'bower_components/angular-route/angular-route.js',
                    'bower_components/angular-cookies/angular-cookies.js',
                    'bower_components/angular-translate/angular-translate.js',
                    'bower_components/favico.js/favico.js',
                    'bower_components/bootstrap/dist/js/bootstrap.js',
                    'bower_components/angular-slider/slider.js',
                    'bower_components/ng-table/dist/ng-table.js',
                    'bower_components/angular-xeditable/dist/js/xeditable.js'
                ],
                dest: 'public/js/vendor.js'
            },
            css_app: {
                src: [
                    'css/style_theme_1.css',
                    'css/slider.css',
                    'css/table.css',
                    'css/alert.css'
                ],
                dest: 'public/css/app.css'
            },
            css_vendors: {
                src: [
                    'bower_components/bootstrap/dist/css/bootstrap.css',
                    'bower_components/components-font-awesome/css/font-awesome.css',
                    'bower_components/angular-slider/slider.css',
                    'bower_components/ng-table/dist/ng-table.css',
                    'bower_components/angular-xeditable/dist/css/xeditable.css'
                ],
                dest: 'public/css/vendor.css'
            }
        },
        copy: {
            stylesheets: {
                files: [{
                        expand: true,
                        src: [
                            'bower_components/bootstrap/fonts/*',
                            'bower_components/components-font-awesome/fonts/*'
                        ],
                        dest: 'public/fonts/',
                        flatten: true
                }]
            }
        },
        ngAnnotate: {
            options: {
                singleQuotes: true
            },
            all: {
                files: {
                    'public/js/app.js': ['public/js/app.js'],
                    'public/js/vendor.js': ['public/js/vendor.js']
                }
            }
        },
        uglify: {
            options: {
                mangle: true,
                compress: true,
                report: true,
                sourceMap: true
            },
            javascript: {
                files: {
                    'public/js/vendor.js': ['public/js/vendor.js'],
                    'public/js/app.js': ['public/js/app.js']
                }
            }

        },
        cssmin: {
            options: {
                keepSpecialComments : 0
            },
            combine: {
                files: {
                    'public/css/app.css': ['public/css/app.css'],
                    'public/css/vendor.css': ['public/css/vendor.css']
                }
            }
        },
        watch: {
            javascript: {
                files: ['js/**/*.js', 'script.js'],
                tasks: ['concat:js_application']
            },
            css:{
                files: ['css/*.css'],
                tasks: ['concat:css_app']
            }
        }
    });

    grunt.registerTask('default', ['clean', 'concat','copy', 'ngAnnotate', 'uglify', 'cssmin']);
    grunt.registerTask('dev', ['clean', 'concat', 'copy', 'watch']);
};
