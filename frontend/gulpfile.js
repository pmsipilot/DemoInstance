var gulp = require('gulp'),
concat = require('gulp-concat'),
output = './public',
fs = require('fs'),
del = require('del'),
ngAnnotate = require('gulp-ng-annotate');

var config = {
    outputDir: output,
    outputJSDir: output + '/js',
    outputCssDir: output + '/css',
    outputFontsDir: output + '/fonts',

    outputJSAppFile: 'app.js',

    outputJSVendorsFile: 'vendor.js',

    outputVendorsCssFile: 'vendor.css',

    outputFontsDir: output + '/fonts',

    appJsEntry: [
	'script.js',
        'js/service/*.js',
        'js/controller/*.js'
    ],

    vendorsJsEntry: [
        'node_modules/jquery/dist/jquery.js',
        'node_modules/angular/angular.js',
        'node_modules/angular-route/angular-route.js',
        'node_modules/angular-cookies/angular-cookies.js',
        'node_modules/angular-translate/angular-translate.js',
        'node_modules/favico.js/favico.js',
        'node_modules/bootstrap/dist/js/bootstrap.js',
        'node_modules/angular-slider/slider.js',
        'node_modules/ng-table/dist/ng-table.js',
        'node_modules/angular-xeditable/dist/js/xeditable.js'
    ],
    vendorsCssEntry: [
	'node_modules/bootstrap/dist/css/bootstrap.css',
        'node_modules/font-awesome/css/font-awesome.css',
        'node_modules/angular-slider/slider.css',
        'node_modules/ng-table/dist/ng-table.css',
        'node_modules/angular-xeditable/dist/css/xeditable.css'
    ],

    fontsEntry: [
        'node_modules/bootstrap/fonts/*',
        'node_modules/components-font-awesome/fonts/*'
    ],

    annotateEntry: [
	'public/js/app.js',
	'public/js/vendor.js'
    ]
};

gulp.task('build', ['build/js/app', 'build/js/vendor', 'build/css/vendor', 'build/fonts/vendor', 'build/ngAnnotate']);
gulp.task('default', ['clean', 'build']);

//Clean public
gulp.task('clean', function() {
    if (fs.existsSync(config.outputDir)) {
        del.sync(config.outputDir);
    }
});

// Build app
gulp.task('build/js/app', function() {
    gulp.src(config.appJsEntry)
        .pipe(concat(config.outputJSAppFile))
        .pipe(gulp.dest(config.outputJSDir));
});

// Build Vendors
gulp.task('build/js/vendor', function() {
    gulp.src(config.vendorsJsEntry)
        .pipe(concat(config.outputJSVendorsFile))
        .pipe(gulp.dest(config.outputJSDir));
});

// Build Vendors CSS
gulp.task('build/css/vendor', function() {
    gulp.src(config.vendorsCssEntry)
        .pipe(concat(config.outputVendorsCssFile))
        .pipe(gulp.dest(config.outputCssDir));
});

gulp.task('build/fonts/vendor', function () {
    gulp.src(config.fontsEntry)
        .pipe(gulp.dest(config.outputFontsDir));
});

gulp.task('build/ngAnnotate', function () {
    gulp.src(config.annotateEntry)
        .pipe(ngAnnotate())
        .pipe(gulp.dest(config.outputJSDir));
});

