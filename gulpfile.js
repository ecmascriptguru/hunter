let gulp = require('gulp'),
    sass = require('gulp-sass'),
    $ = require('gulp-load-plugins')(),
    browserSync = require('browser-sync').create();


gulp.task('sass', function(){
    return gulp.src(['assets/stylesheets/**/*.scss'])
        .pipe(sass({
            includePaths: ['node_modules']
        })) // Converts Sass to CSS with gulp-sass
        .pipe(gulp.dest('static/css'))
});

gulp.task('fonts', function() {
    return gulp.src([
            'assets/fonts/*.*',
            'node_modules/font-awesome/fonts/fontawesome-webfont.*'
        ])
        .pipe(gulp.dest('static/fonts/'));
});

// Images
gulp.task('images', function () {
    return gulp.src([
            'assets/images/**/*'
        ])
        .pipe($.cache($.imagemin({
            optimizationLevel: 3,
            progressive: true,
            interlaced: true
        })))
        .pipe(gulp.dest('static/img'))
        .pipe($.size());
});

// Clean
gulp.task('clean', function () {
    return gulp.src(['static/css', 'static/fonts', 'static/js'], { read: false }).pipe($.clean());
});

gulp.task('build', ['sass', 'fonts', 'images'])

gulp.task('watch', ['build'], () => {
    gulp.watch(['assets/stylesheets/**/*.scss'], ['sass']); 
    gulp.watch(['assets/fonts/**/*.*'], ['fonts']);
    gulp.watch(['assets/images/**/*.*'], ['images']);
})