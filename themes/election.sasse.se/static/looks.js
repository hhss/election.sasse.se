var looks = require('looks');

looks.less('less/styles.less', 'css/styles.css', {
    'paths': ['components/bootstrap/less'],
    'yuicompress': true
});
